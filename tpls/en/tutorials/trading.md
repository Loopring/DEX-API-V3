# 做市商集成


我们希望通过本教程，可以让您了解到如何通过路印交易所的API来实现自动化交易和做市商程序。在您继续本教程前，请务必先了解如何获取API Key并理解路印对链下请求如何做EdDSA签名。

> 除非有另外说明，本教程中的代码示例均使用Python语言。


## 提交订单

#### 订单格式
您可以通过下面的JSON来表达一个路印的限价单（目前路印不支持市价单）。具体参数细节详见[提交订单](../dex_apis/submitOrder.md)。

```python
newOrder = {
	"exchangeId": 2,
	"orderId": 5,
	"accountId": 1234,
	"tokenSId": 2,
	"tokenBId": 3,
	"amountS": "5000000000000000000",
	"amountB": "15000000",
	"allOrNone": "false",
	"buy": "false",
	"validSince": 1582094327,
	"validUntil": 1587278341,
	"maxFeeBips": 50,
	"label": 211,
	"hash": "14504358714580556901944011952143357684927684879578923674101657902115012783290",
	"signatureRx": "15179969700843231746888635151106024191752286977677731880613780154804077177446",
	"signatureRy": "8103765835373541952843207933665617916816772340145691265012430975846006955894",
	"signatureS" : "4462707474665244243174020779004308974607763640730341744048308145656189589982",
	"clientOrderId": "Test01"
}
```

#### 价格与数量

假设您想在`LRC-USDT`市场上以`$0.03`的价格卖出500个`LRC`，即售出500个`LRC`，买入至少15个`USDT` (500 * 0.03 = 15)。

首先您需要通过`/api/v2/exchange/token`这个API获取LRC和USDT这两个币种在路印交易所的相关配置信息 - 注意：同一个币种，在基于路印协议的两个不同的交易所的配置信息是不相同的。在Loopring.io，LRC和USDT对应的TokenID分别是2和3；它们ERC20合约的`decimals`分别是18和6。其它代币配置信息可以详见[查询交易所支持的通证信息](../dex_apis/getTokens.md)。

通过查询获得的代币信息，可以将订单中的部分数据准备好：

```python
newOrder = {
	'exchangeId': 2,
	'accountId': 1234,
	'tokenSId': 2,  #LRC
	'tokenBId': 3,  #USDT
	'amountS': '500000000000000000000', # 500 * 10**18
	'amountB': '15000000',              #  15 * 10**6
	'allOrNone': 'false',
	'buy': 'false',                     # 卖出
	'validSince': 1582094327,           # 生效时间，比下单时间提前15分钟，见注意事项
	'validUntil': 1587278341,           # 失效时间
	'maxFeeBips': 63,                   # 最大费率，实际费率由服务器计算
	'label': 'hebao::subchannel::0001'
}
```

几点说明：

- `exchangeId`是Loopring.io现在运行的beta1版本的交易所ID，后续路印交易所升级智能合约后，这个`exchangeId`就会更新。beta1对应的`exchangeId`就是2，这是个常量。
-  `accountId`是您注册后获得的账号ID。
- `tokenS`, `amountS`中的*S*代表Sell，代表这两个值和卖出的代币相关； `tokenB`, `amountB`中的*B*代表Buy，代表这两个值和买入的代币相关。路印订单采用的是单向表达，买卖单的数据格式完全一致。
- `amountS`的值是 `500`跟着18个`0`；amountB的值是`15`跟着6个`0`。
- `buy`的值决定订单的完全成交条件。如果`buy`是`'true'`，那么只要买到了15 USDT，该订单就算完全成交，这时候也许订单中的500个LRC并没被全部卖掉。如果`buy`是`'false'`，那么只要卖出了500个LRC，该订单就算完全成交了，可能实际买到的USDT多于15。
- `validSince`和`validUntil`代表该订单的生效时间和过期时间。通过这两个时间戳，您可以不必对每个订单做主动取消的动作。我们强烈建议您在现阶段，将`validSince`设置为比当前时间早15分钟。
- `maxFeeBips`是此订单愿意支付的最大费率，单位是万分之一。如果`maxFeeBips = 10`，代表该订单愿意支付实际买入的tokenB数量的0.1%给交易所。但实际交易所收取的交易手续费可以小于`maxFeeBips`，比如交易所愿意为VIP用户的交易费打折。在实际使用时，我们建议您使用63作为该项的值。如果该值太小，服务器会拒绝撮合您的订单。


#### 订单号

接下来您需要为新订单指定一个`OrderId`。订单`OrderId`是路印交易所一个比较特殊的地方，详见[注意事项](./trader-notes.md)一节关于`OrderId`的说明。您可以通过访问[`/api/v2/orderId`](../dex_apis/getNextOrderId.md)获取下一个有效OrderId。注意`OrderId`由用户出售的代币（tokenS）决定，然后根据返回值更新订单数据结构。



访问`/api/v2/orderid`得到当前币种的`OrderID`，API参数细节参考[获取下一个有效OrderId](../dex_apis/getNextOrderId.md)，建议提前访问API建立并维护一个币种和`OrderID`的对应关系，类似：

```python
token_orderid_mapping = {
    'ETH' : 3,
    'LRC' : 5，
    'DAI' : 2
}
```

订单`OrderID`由用户售出的代币品种，在`LRC-ETH`市场上，如果用户提交一个买单，即售出`ETH`，买入`LRC`，则`OrderID`值为：

```python
order["orderId"] = token_orderid_mapping['ETH']
```

反之如果是卖单，即售出LRC，买入ETH，则OrderID为：

```python
order["orderId"] = token_orderid_mapping['LRC']
```
订单号的限制是基于卖出的token共享的，比如LRC-USDT和ETH-USDT两个市场会共享$$ 2^{20} $$个订单号，用完就不能再下单。因此针对不同的市场，建议注册不同账号做市。

当前路印交易所每一个币种的最大订单`OrderID`为$$ 2^{20} $$，如果当前账号某个币种的`OrderID`超过该值，则下单失败。后续版本的路印交易所将会更新此限制。



对于任何一个卖出币种，同时存活有效的订单数量为$$ 2^{14} $$即16384。您可以想象有16384个槽位，如果两个订单的`OrderID`对16384同余即：
  $$
  OrderA.OrderID\ \%\ 2^{14} \equiv OrderB.OrderID\ \%\ 2^{14}
  $$

那么必须先取消掉先下的那个订单，且保证后下的订单的`OrderID`要大于前一个订单的`OrderID`，否则服务器会拒绝新的订单。普通用户一般不会遇到这个问题。



```python
order.update({"orderId": 2})
```

#### 时间戳

服务器收到订单时会判断订单中的`ValidSince`时间戳，注意不是订单发送的时间，而是订单开始生效的时间，因此推荐订单的`ValidSince`在当前时间上提前15分钟，即：

```python
order["validSince"] = int(time.time() - 900)
```

#### 签名
然后您需要对订单做**Poseidon**哈希计算并对哈希做**EdDSA**签名，再将hash和签名添加到订单JSON中。签名过程详见[注意事项](./trader.md#TraderNotes)签名部分。注意订单签名和普通网络请求的签名算法不同，不同请求的签名请参考对应[`Restful API`请求文档](../restful_api_overview.md)以及[注意事项](./trader.md#TraderNotes)签名部分，算法细节请查询参考文献[3]和[4]。
<span id="OrderSig"></span>
下面是使用Python对订单做签名的示例代码，详情请参考[注意事项](./trader.md#TraderNotes)签名部分关键代码实现一节：

```python
from ethsnarks.poseidon import poseidon_params, poseidon
# 对订单数据签名
PoseidonHashParams = poseidon_params(
	SNARK_SCALAR_FIELD,
	14, 6, 53, b'poseidon', 5,
	security_target=128
)
serialized_order = [
    int(order["exchangeId"]),
    int(order["orderId"]),
    int(order["accountId"]),
    int(order["tokenSId"]),
    int(order["tokenBId"]),
    int(order["amountS"]),
    int(order["amountB"]),
    int(order["allOrNone"]=="true"),
    int(order["validSince"]),
    int(order["validUntil"]),
    int(order["maxFeeBips"]),
    int(order["buy"]=="true"),
    int(order["label"])
]
orderHash = poseidon(serialized_order, PoseidonHashParams)
signedMessage = PoseidonEdDSA.sign(serialized_order, FQ(int(privateKey)))
order.update({
	"hash": str(orderHash),
	"signatureRx": str(signedMessage.sig.R.x),
	"signatureRy": str(signedMessage.sig.R.y),
	"signatureS": str(signedMessage.sig.s),
})
```


- 在访问`api/v2/order`发送订单之前，和其他需要API参数签名不同的是，这里要对订单本身进行签名，签名结果放在订单参数里面，同样地，订单参数也需要序列化再进行`PoseidonHash`运算，这里为了配合`PoseidonHash`，所以序列化成整数数组，请注意这里序列化数组的顺序和服务器必须保持一致，如示例代码所示：

```python
def serialize_api_data(order):
    return [
        int(order["exchangeId"]),
        int(order["orderId"]),
        int(order["accountId"]),
        int(order["tokenSId"]),
        int(order["tokenBId"]),
        int(order["amountS"]),
        int(order["amountB"]),
        int(order["allOrNone"]=="true"),
        int(order["validSince"]),
        int(order["validUntil"]),
        int(order["maxFeeBips"]),
        int(order["buy"]=="true"),
        int(order["label"])
    ]

def sign_order(order, api_secret):
    PoseidonHashParams = poseidon_params(SNARK_SCALAR_FIELD, 14, 6, 53, b'poseidon', 5, security_target=128)
    serialized_order = serialize_api_data(order)
    msgHash = poseidon(serialized_order, PoseidonHashParams)
    signedMessage = PoseidonEdDSA.sign(msgHash, FQ(int(api_secret)))
    order.update({
        "hash": str(msgHash),
        "signatureRx": str(signedMessage.sig.R.x),
        "signatureRy": str(signedMessage.sig.R.y),
        "signatureS": str(signedMessage.sig.s),
    })
```

- 路印交易所使用`EdDSA PoseidonHASH`算法对订单参数签名，`EdDSA PoseidonHASH`算法代码可以参考`ethsnarks`，对订单参数计算`PoseidonHash`的参数如下：

```python
poseidon_params(SNARK_SCALAR_FIELD, 14, 6, 53, b'poseidon', 5, security_target=128)
```

- 订单参数签名和API接口参数签名的区别在于：API接口参数是用`SHA256`计算`HASH`值，再经过`EdDSA`签名，而订单内容是用`PoseidonHASH`计算`HASH`值，然后经过`EdDSA`签名，而`EdDSA`签名算法是相同的。

#### 订单提交

最后您需要通过[`/api/v2/order`](../dex_apis/submitOrder.md)发送订单到服务器。

## 查询订单

您可以通过[`/api/v2/orders`](../dex_apis/getOrderDetail.md)查看订单状态。或者通过订阅WebSocket更新来跟踪订单状态。关于WebSocket订阅部分，请参考[WebSocket介绍](./websocket_overview.md)。


## 取消订单

你可以通过[`/api/v2/orders`](../dex_apis/cancelOrders.html)取消订单。取消订单接口需要签名，和订单数据的签名略有不同，请参考[注意事项](./trader-notes.md)需要签名的API接口一节。


另一种取消订单的方式是通过和交易所的合约交互，改变交易密码和EdDSA秘钥。和中心化交易所不同，改变交易密码后，您的全部订单都会被取消。



## 参考文献及代码库

1. `ethsnarks`代码仓库：https://github.com/HarryR/ethsnarks.git
2. `SHA256 Hash`算法：<https://en.wikipedia.org/wiki/SHA-2>
3. `EdDSA`算法：<https://en.wikipedia.org/wiki/EdDSA>
4. `Poseidon Hash`算法：<https://www.poseidon-hash.info/>


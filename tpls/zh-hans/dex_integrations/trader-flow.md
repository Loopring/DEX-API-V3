## 注册账户

要使用**路印（去中心化）交易所**，您必须先通过向交易所的智能合约发送特殊的以太坊交易来注册帐户。 创建帐户后，您可以通过链上和链外请求与交易所进行交互。

我们建议使用路印交易所的网页界面（[Loopring.io](https://loopring.io)）进行帐户注册。 但是，您也可以使用Etherescan和MyEtherWallet等工具直接与智能合约进行交互。

## 获取API Key

创建好账户之后，您可以使用[Loopring.io](https://loopring.io)的*导出账号*功能导出`API-Key`、EDDSA公私钥`publicKeyX`、` publicKeyY`，和`privateKey`。使用路印交易所的API需要上述信息。

> [!DANGER]
>
> 请妥善保管API Key和EDDSA私钥。如果这些信息不慎泄漏，会导致您资产的损失。在任何情况下，路印交易所和其API均不会向您询问EDDSA私钥。

## 提交订单

- 我们可以通过下面的JSON来表达一个路印的限价订单。具体参数细节详见[提交订单](../dex_apis/submitOrder.md)。

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


- 首先选择合适价格和订单量，填写对应的`tokenID`和`amount`，比如在`LRC-USDT`市场上以`$0.03`的价格卖出500个`LRC`，即售出500个`LRC`，买入15个`USDT`(500*0.03 = 15)，则订单数据如下。需要注意的是订单买卖参数的计数单位为该品种的最小单位，`ETH`,`LRC`以及大部分`ERC20代币`为$$10^{18}$$，而`USDT`则是$$10^{6}$$，用户需要提前访问`/api/v2/exchange/token`得到各个代币的参数，最重要的是`tokenId`和`decimals`，该API详见[查询交易所支持的通证信息](../dex_apis/getTokens.md)。

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
    'maxFeeBips': 50,                   # 最大费率，实际费率由服务器计算
    'label': 'hebao::subchannel::0001'
}
```

- 订单的`maxFeeBips`是此订单的最大费率，实际费率由服务器计算，如果服务器费率大于此上限，则此Order无效，因此填一个服务器上限即可，具体参考[提交订单](../dex_apis/submitOrder.md)里面关于`maxFeeBips`的描述。

- 访问`/api/v2/orderId`获得`OrderId`，详见[获取下一个有效OrderId](../dex_apis/getNextOrderId.md)。查询到当前对应市场对应的`OrderId`，注意`OrderID`由用户出售的代币品种决定，然后根据返回值更新订单数据结构。订单`OrderId`是路印交易所一个比较特殊的不同之处，详见[注意事项](./trader-notes.md)一节关于`OrderId`的说明。

```python
order.update({"orderId": 2,"clientOrderId": "TEST01"})
```

- 对订单做**PoseidonHASH**哈希计算并对哈希做**EDDSA**签名，之后将hash和签名添加到订单JSON中。签名过程详见[注意事项](./trader-notes.md)签名部分，算法细节请查询参考文献[3]和[4]。
<span id="OrderSig"></span>
下面是使用Python对订单做签名的示例：

```python
from ethsnarks.poseidon import poseidon_params, poseidon

# 对订单数据签名
PoseidonHashParams = poseidon_params(
    SNARK_SCALAR_FIELD,
    14, 6, 53, b'poseidon', 5,
    security_target=128
)
msgHash = poseidon(msg_parts, PoseidonHashParams)
signedMessage = PoseidonEdDSA.sign(msgHash, FQ(int(api_secret)))
order.update({
    "hash": str(msgHash),
    "signatureRx": str(signedMessage.sig.R.x),
    "signatureRy": str(signedMessage.sig.R.y),
    "signatureS": str(signedMessage.sig.s),
})
```

- 访问`/api/v2/order`发送订单到服务器，详见[提交订单](../dex_apis/submitOrder.md)，一般来说刚开始主要的错误来自于签名部分，请仔细检查所使用的`API-Secret`以及签名算法流程。

- 访问`/api/v2/orders`查看订单状态，详见[获取订单详情](../dex_apis/getOrderDetail.md)。或者通过订阅Websocket更新来跟踪订单状态，关于WebSocket订阅部分，请参考[Websocket介绍](./websocket_overview.md)。

- 取消订单通过`/api/v2/orders`，参数见[取消订单](../dex_apis/cancelOrders.html)，访问取消订单接口需要签名，和订单数据的签名略有不同，请参考[注意事项](./trader-notes.md)需要签名的API接口一节。

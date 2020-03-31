## Account Registration

To use **Loopring Exchange**, you must register an account first by sending a special Ethereum transaction to the exchange's smart contract. After your account is created, you can interact with the exchange with both on-chain and off-chain requests.

We recommend using Loopring Exchange's web UI, [Loopring.io](https://loopring.io), for account registration. But you can also use tools such as Etherescan, MyEtherWallet, etc., to interact with the smart contract directly.


## Obtain the API key

To use Loopring's APIs, you must obtain your `API-Key`, and your EdDSA public/private key-pair, namely `publicKeyX`, `publicKeyY`, and `privateKey`.

The forementioned information can be exported from your account by using [Loopring.io](https://loopring.io)'s *Export Account* menu.

> [!DANGER]
>
> Please do not disclose your API Key and EdDSA private key. If this information is accidentally leaked, you may suffer loss of your assets. Under no circumstances will Loopring Exchange and its API ask you for your EdDSA private key.

## Submit orders


- You can express a Loopring limit-price order using the following JSON. See [Submit Orders](../dex_apis/submitOrder.md) for details regarding each field。

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

假设您想在`LRC-USDT`市场上以`$0.03`的价格卖出500个`LRC`，即售出500个`LRC`，买入15个`USDT`(500*0.03 = 15)。

首先您需要通过`/api/v2/exchange/token`这个API获取LRC和USDT这两个币种在路印交易所的相关配置信息--注意：同一个币种，在基于路印协议的两个不同的交易所的配置信息是不相同的。在Loopring.io，LRC和USDT对应的TokenID分别是2和3，他们ERC20合约的`decimal`分别是18和6。其它代币配置信息可以详见[查询交易所支持的通证信息](../dex_apis/getTokens.md)。

通过上面的代币信息，就可以将订单准备好了：

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
- `buy`的值决定订单的完全成交条件。如果`buy`是`'true'`，那么只要买到了amountB的tokenB，该订单就算完全成交了，可能实际卖出的tokenS少于amountS。如果`buy`是`'false'`，那么只要卖出了amountS的tokenS，该订单就算完全成交了，可能实际买到的tokenB多于amountB。
- `validSince`和`validUntil`代表该订单的生效时间和过期时间。通过这两个时间戳，您可以不必对每个订单做主动取消的动作。我们强烈建议您在现阶段，将`validSince`设置为比当前时间早15分钟。
- `maxFeeBips`是此订单愿意支付的最大费率，单位是万分之一。如果`maxFeeBips = 10`，代表该订单愿意支付实际买入的tokenB数量的0.1%给交易所。但实际交易所收取的交易手续费可以小于`maxFeeBips`，比如交易所愿意为VIP用户的交易费打折。在实际使用时，我们建议您使用63作为该项的值。如果该值太小，服务器会拒绝撮合您的订单。


接下来您需要为新订单指定一个`OrderId`。您可以通过访问[`/api/v2/orderId`获取下一个有效OrderId](../dex_apis/getNextOrderId.html)。注意`OrderId`由用户出售的代币（tokenS）决定，然后根据返回值更新订单数据结构。订单`OrderId`是路印交易所一个比较特殊的不同之处，详见[注意事项](./trader-notes.html)一节关于`OrderId`的说明。

```python
order.update({"orderId": 2})
```


然后您需要对订单做**Poseidon**哈希计算并对哈希做**EdDSA**签名，再将hash和签名添加到订单JSON中。签名过程详见[注意事项](./trader-notes.html)签名部分，算法细节请查询参考文献[3]和[4]。
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
orderHash = poseidon(msg_parts, PoseidonHashParams)
signedMessage = PoseidonEdDSA.sign(orderHash, FQ(int(api_secret)))
order.update({
    "hash": str(orderHash),
    "signatureRx": str(signedMessage.sig.R.x),
    "signatureRy": str(signedMessage.sig.R.y),
    "signatureS": str(signedMessage.sig.s),
})
```

最后您需要通过[`/api/v2/order`发送订单](../dex_apis/submitOrder.html)到服务器。

## 查询订单

您可以访问[`/api/v2/orders`查看订单状态](../dex_apis/getOrderDetail.html)。或者通过订阅WebSocket更新来跟踪订单状态。关于WebSocket订阅部分，请参考[Websocket介绍](./websocket_overview.md)。

## 取消订单
你可以通过[`/api/v2/orders`取消订单](../dex_apis/cancelOrders.html)。取消订单接口需要签名，和订单数据的签名略有不同，请参考[注意事项](./trader-notes.html)需要签名的API接口一节。

另一种取消订单的方式是通过和交易所的合约交互，改变交易密码和EdDSA秘钥。和中心化交易所不同，改变交易密码后，您的全部订单都会被取消。

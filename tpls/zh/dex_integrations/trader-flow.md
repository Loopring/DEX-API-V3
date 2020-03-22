## 注册账户

- 路印DEX通过发送ETH交易调用智能合约来完成账户的创建，充值，提现等操作（此类请求成为链上请求）

- 对于做市商用户，我们推荐在[路印DEX网站](https://www.loopring.io)完成此类操作，从而省去对接ETH的工作。

## 获取API key

- 创建好账户之后，您可以使用官网的'导出账号'功能导出`API-Key`及`EDDSA`公私钥`publicKeyX`,` publicKeyY`和`privateKey`，路印DEX链下请求需要这些信息。

## 提交订单

- 准备发送订单的参数举例，API参数细节详见[提交订单](../dex_apis/submitOrder.md)。

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


- 首先选择合适价格和交易量，填写对应的`tokenID`和`amount`，比如在`LRC-USDT`市场上以`0.03U`的价格卖出500个`LRC`，则订单数据如下。需要注意的是这里的计数单位参数，如`ETH`,`LRC`以及大部分`ERC20代币`为$$10^{18}$$，而`USDT`则是$$10^{6}$$，用户需要提前访问`/api/v2/exchange/token`得到各个不同的代币的参数，主要是`tokenId`和`decimals`，该API详见[查询交易所支持的通证信息](../dex_apis/getTokens.md)。

  ```python
  order = {
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

- 访问`/api/v2/orderId`获得`OrderId`，详见[获取下一个有效OrderId](../dex_apis/getNextOrderId.md)。查询到当前对应市场对应的`OrderId`，注意`OrderID`由用户出售的代币品种决定，然后根据返回值更新订单数据结构。订单`OrderId`是`LoopringDEX`一个比较特殊的地方，详见[注意事项](./trader-notes.md)一节关于`OrderId`的说明。

  ```python
  order.update({"orderId": 2,
                "clientOrderId": "TEST01"})
  ```

- 对订单签名，签名使用`EDDSA PoseidonHASH`算法，并更新订单数据。签名过程详见[注意事项](./trader-notes.md)签名部分，算法细节请查询参考文献[3]和[4]。
<span id="OrderSig"></span>

  ```python
  from ethsnarks.poseidon import poseidon_params, poseidon

  # 对订单数据签名
  PoseidonHashParams = poseidon_params(SNARK_SCALAR_FIELD, 14, 6, 53, b'poseidon', 5, security_target=128)
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

# API集成--做市交易

## 基本信息

- 本篇描述实现在LoopringDEX上进行做市交易的程序涉及的主要APIs以及对应参数的注意事项
- 代码使用`python`描述

## 交易过程

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


- 选择合适价格和交易量，填写对应的`tokenID`和`amount`，比如在`LRC-USDT`市场上以`0.03U`的价格卖出500个`LRC`，则订单数据如下。需要注意的是这里的计数单位参数，如`ETH`,`LRC`以及大部分`ERC20代币`为$$10^{18}$$，而`USDT`则是$$10^{6}$$，用户需要提前访问`/api/v2/exchange/token`得到各个不同的代币的参数，主要是`tokenId`和`decimals`，该API详见[查询交易所支持的通证信息](../dex_apis/getTokens.md)。

  ```python
  order = {
  	'exchangeId': 2,
  	'accountId': 29,
  	'tokenSId': 2,	#LRC
  	'tokenBId': 3,	#USDT
  	'amountS': '500000000000000000000', # 500 * 10**18
  	'amountB': '15000000',				#  15 * 10**6
  	'allOrNone': 'false',
  	'buy': 'false', 					# 卖出
  	'validSince': 1584508394,			# 生效时间，比下单时间提前15分钟，见注意事项
  	'validUntil': 1587100394,			# 失效时间
  	'maxFeeBips': 50,					# 最大费率，实际费率由服务器计算
  	'label': 'hebao::subchannel::0001'
  }
  ```

- 订单的`maxFeeBips`是此订单的最大费率，实际费率由服务器计算，如果服务器费率大于此上限，则此Order无效，因此填一个服务器上限即可，具体参考[提交订单](../dex_apis/submitOrder.md)里面关于`maxFeeBips`的内容。

- 访问`/api/v2/orderId`，详见[获取下一个有效OrderId](../dex_apis/getNextOrderId.md)。查询到当前对应市场对应的`OrderID`，注意`OrderID`由用户出售的代币品种决定，然后根据返回值更新订单数据结构。订单`OrderID`是`LoopringDEX`一个比较特殊的地方，详见后文注意事项章节关于`OrderID`的说明。

  ```python
  order.update({"orderId": 2,
                "clientOrderId": "TEST01"})
  ```

- 对订单签名，签名使用`EDDSA PoseidonHASH`算法，详见注意事项签名部分，详细算法请查询参考文献[3]和[4]，并更新订单数据：

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

- 访问`/api/v2/order`发送订单到服务器，详见[提交订单](../dex_apis/submitOrder.md)。

- 访问`/api/v2/orders`查看订单状态，详见[获取订单详情](../dex_apis/getOrderDetail.md)。或者通过订阅Websocket更新来跟踪订单状态，关于WebSocket订阅部分，请参考[Websocket介绍](./websocket_overview.md)。

## 注意事项

### 订单生效时间

- 服务器收到订单时会判断订单中的`ValidSince`时间戳，注意不是订单发送的时间，而是订单开始生效的时间，因此推荐订单的`ValidSince`在当前时间上提前15分钟，即：

  ```python
  order.validSince = int(time.time() - 900)
  ```

### 订单OrderID

- 访问`/api/v2/orderid`得到当前币种的`OrderID`，API参数细节参考[获取下一个有效OrderId](../dex_apis/getNextOrderId.md)，建议提前访问API建立并维护一个币种和`OrderID`的对应关系，类似：

  ```python
  token_orderid_mapping = {
      'ETH' : 3,
      'LRC' : 5，
      'DAI' : 2
  }
  ```


- 订单`OrderID`由用户售出的代币品种，在`LRC-ETH`市场上，如果用户提交一个买单，即售出`ETH`，买入`LRC`，则`OrderID`值为：

  ```python
  order.orderId = token_orderid_mapping['ETH']
  ```

  反之如果是卖单，即售出LRC，买入ETH，则OrderID为：

  ```python
  order.orderId = token_orderid_mapping['LRC']
  ```

- 当前`LoopringDEX`每一个币种的最大订单`OrderID`为$$2^{20}​$$，如果当前账户某个币种的`OrderID`超过该值，则下单失败。后续版本的`LoopringDEX`将会更新此限制。
- 同时存活有效的订单数最大为$$2^{14}​$$即16384。
- 如果两个未成交的订单 A和B的OrderID对16384同余，即$$OrderA.OrderID \% 2^{14} = OrderB.OrderID \% 2^{14}​$$，必须取消前面一个，否则后面一个会被服务器拒绝。

### 需要API-KEY的API接口

- API密钥可以从`loopringDEX`网页导出。

- 和个人账户相关的API接口，比如查询订单个数/状态/账户余额时候需要API-KEY，API信息请查询[Restful API 概述](../restful_api_overview.md)。

- API密钥数据放在`http request header`里的`X-API-KEY`中。

  ```python
  def init_request_session(user_api_key):
      session = requests.session()
      session.headers.update({'Accept': 'application/json',
                              'X-API-KEY': user_api_key})
      return session
  ```

### 需要签名的API接口 

- 和账户信息有关的都需要签名，详见[Restful API 概述](../restful_api_overview.md)，这里以[取消订单](../dex_apis/cancelOrders.md)，即`/api/v2/deleteOrders`为例。

- 调用取消订单接口时，除了接口本身所需的参数外，还需传递`signature`即参数签名。

- `LoopringDEX`对API签名使用`EDDSA SHA256`算法，首先将API参数序列化，然后作为` SHA256`的操作对象，得到`SHA256Hash`值，再用`EDDSA`算法对该`SHA256Hash`进行签名，私钥为用户的`API-Secret`，最终的输出有三个整数：Rx/Ry/S，将这三个序列化成字符串并用`,`连接起来即为签名，可参考`sign_api_data`代码示例。

- API-Secret可以从`loopringDEX`网页导出。

- 对API接口的签名使用的`EDDSA`使用`ethsnarks`工程代码，其内部使用`Poseidon HASH`算法，`LoopringDEX`的签名参数如下:

  ```python
  poseidon_params(SNARK_SCALAR_FIELD, 6, 6, 52, b'poseidon', 5, security_target=128)
  ```

- `EDDSA`和`Poseidon Hash`算法细节见参考文献[3]，[4]。

- 可以重载`ethsnarks`的`_SignatureScheme`实现该固定参数的签名类，如下面python代码所示。

- 签名数据放在`http request header`里的`X-API-SIG`中。

  ```python
  session = init_request_session(user_api_key)
  ...
  #初始化API数据 api_request_params
  ...
  #对API数据签名
  x_api_sign = sign_api_data(api_request_params，user_api_secret)
  session.headers.update({'X-API-SIG': x_api_sign})
  ```

- API接口签名代码部分关键函数示例：

  ```python
  #继承ethsnarks.eddsa._SignatureScheme
  class PoseidonEdDSA(_SignatureScheme):
      @classmethod
      def hash_public(cls, *args):
          PoseidonHashParams = poseidon_params(SNARK_SCALAR_FIELD, 6, 6, 52, b'poseidon', 5, security_target=128)
          inputMsg = list(as_scalar(*args))
          return poseidon(inputMsg, PoseidonHashParams)
  
  #对数据签名并返回签名
  def sign_api_data(api_request_params，api_secret):
      data = serialize_api_data(api_request_params)
  	hasher = hashlib.sha256()
  	msgBuf = ujson.dumps(data).encode('utf-8')
      hasher.update(msgBuf)
  	msgHash = int(hasher.hexdigest(), 16) % SNARK_SCALAR_FIELD
  	signed = PoseidonEdDSA.sign(msgHash, FQ(int(api_secret)))
  	signature = ','.join(str(_) for _ in [signed.sig.R.x, signed.sig.R.y, signed.sig.s])
  	return signature
  
  def serialize_api_data(data):
      has_signature = False
      params = []
      for key, value in data.items():
          if key == 'signature':
              has_signature = True
  		else:
              params.append((key, value))
              # sort parameters by key
              params.sort(key=itemgetter(0))
  
      if has_signature:
          params.append(('signature', data['signature']))
  	return params
  ```

### 需要签名的数据类型（订单ORDER）

- 在访问`api/v2/order`发送订单之前，和其他需要API参数签名不同的是，这里要对订单本身进行签名，签名结果放在订单参数里面，同样地，订单参数也需要序列化再进行`PoseidonHash`运算，这里为了配合`PoseidonHash`，所以序列化成整数数组，如下：

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
  
  def sign_order(order, api_secret)
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

- `LoopringDEX`使用`EDDSA PoseidonHASH`算法对订单参数签名，同样的，`EDDSA PoseidonHASH`算法代码可以参考`ethsnarks`，对订单参数计算HASH的`PoseidonHash`的参数如下：

  ```python
  poseidon_params(SNARK_SCALAR_FIELD, 14, 6, 53, b'poseidon', 5, security_target=128)
  ```

- 订单参数签名和API接口参数签名的区别在于：API接口参数是用`SHA256`计算`HASH`值，再经过`EDDSA`签名，而订单内容是用`PoseidonHASH`计算`HASH`值，然后经过`EDDSA`签名，而`EDDSA`签名算法是相同的。

## 参考文献及代码库

1. `ethsnarks`代码仓库: https://github.com/HarryR/ethsnarks.git
2. `SHA256 Hash`算法：<https://csrc.nist.gov/csrc/media/publications/fips/180/2/archive/2002-08-01/documents/fips180-2.pdf>
3. `EDDSA`算法：<https://en.wikipedia.org/wiki/EdDSA>
4. `Poseidon Hash`算法：<https://www.poseidon-hash.info/>


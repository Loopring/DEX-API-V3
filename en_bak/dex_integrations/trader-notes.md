## 注意事项
<span id="TraderNotes"></span>

### 订单生效时间

- 服务器收到订单时会判断订单中的`ValidSince`时间戳，注意不是订单发送的时间，而是订单开始生效的时间，因此推荐订单的`ValidSince`在当前时间上提前15分钟，即：

  ```python
  order["validSince"] = int(time.time() - 900)
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

- 订单`OrderID`由用户售出的通证品种，在`LRC-ETH`市场上，如果用户提交一个买单，即售出`ETH`，买入`LRC`，则`OrderID`值为：

  ```python
  order["orderId"] = token_orderid_mapping['ETH']
  ```

  反之如果是卖单，即售出LRC，买入ETH，则OrderID为：

  ```python
  order["orderId"] = token_orderid_mapping['LRC']
  ```

- 当前`LoopringDEX`每一个币种的最大订单`OrderID`为$$ 2^{20} $$，如果当前账户某个币种的`OrderID`超过该值，则下单失败。后续版本的`LoopringDEX`将会更新此限制。

> [!TIP]
>
> 订单号的限制是基于卖出的token共享的，比如LRC-USDT和ETH-USDT两个市场会共享$$ 2^{20} $$个订单号，用完就不能再下用USDT买入的市场订单了（卖出USDT不受影响）。针对不同市场，建议注册不同账号做市。

<br/>

- 同时存活有效的订单数最大为$$ 2^{14} $$即16384。超出后需要取消一部分订单才能够继续下单。

- 如果两个未成交的订单 A和B的`OrderID`对16384同余，即：
  $$
  OrderA.OrderID\ \%\ 2^{14} \equiv OrderB.OrderID\ \%\ 2^{14}
  $$
  必须取消前面一个，否则后面一个会被服务器拒绝。不过普通用户一般不会遇到这个问题。

### 需要API-KEY的API接口

- API密钥可以从`loopringDEX`网页导出或通过API获取。

- 所有接口（除[查询用户ApiKey](./dex_apis/getApiKey.md)）都需要传入API-KEY，API信息请查询[Restful API 概述](../rest_api_overview.md)。

- API密钥数据放在`http request header`里的`X-API-KEY`中。

  ```python
  def init_request_session(user_api_key):
      session = requests.session()
      session.headers.update({'Accept': 'application/json',
                              'X-API-KEY': user_api_key})
      return session
  ```

### 需要签名的API接口

- 除了需要`API-KEY`外，和账户信息有关的还需要签名，详见[Restful API 概述](../rest_api_overview.md)，这里仅以[取消订单](../dex_apis/cancelOrders.md)为例。

- 调用取消订单接口时，除了接口本身所需的参数外，还需传递`signature`即参数签名。

- `LoopringDEX`对API签名使用`EdDSA SHA256`算法，首先将API参数序列化成型如`[(参数1名, 参数1值), (参数2名, 参数2值), ..., (参数N名, 参数N值)]`的字符串二元组数组，其中参数名按照字典序排序，从而保证服务器验证顺序一致。然后整体转为`JSON`字符串作为` SHA256`的操作对象，得到`SHA256Hash`值，再用`EdDSA`算法对该`SHA256Hash`进行签名，私钥即`privateKey`，最终的签名包含三个整数：`Rx, Ry, S`，将这三个序列化成字符串并用`,`连接起来即为API签名，流程请参考`sign_api_data`代码示例。

- 对API接口的签名使用的`EdDSA`使用`ethsnarks`工程代码，其内部使用`Poseidon HASH`算法，`LoopringDEX`的签名参数如下:

  ```python
  poseidon_params(SNARK_SCALAR_FIELD, 6, 6, 52, b'poseidon', 5, security_target=128)
  ```

- `EdDSA`和`Poseidon Hash`算法细节见参考文献[3]，[4]。

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
  	# sort parameters by key, in alphabet order
      params.sort(key=itemgetter(0))
      if has_signature:
          params.append(('signature', data['signature']))
    return params
  ```

### 需要签名的数据类型（订单ORDER）

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

- `LoopringDEX`使用`EdDSA PoseidonHASH`算法对订单参数签名，`EdDSA PoseidonHASH`算法代码可以参考`ethsnarks`，对订单参数计算`PoseidonHash`的参数如下：

  ```python
  poseidon_params(SNARK_SCALAR_FIELD, 14, 6, 53, b'poseidon', 5, security_target=128)
  ```

- 订单参数签名和API接口参数签名的区别在于：API接口参数是用`SHA256`计算`HASH`值，再经过`EdDSA`签名，而订单内容是用`PoseidonHASH`计算`HASH`值，然后经过`EdDSA`签名，而`EdDSA`签名算法是相同的。

## 参考文献及代码库

1. `ethsnarks`代码仓库：https://github.com/HarryR/ethsnarks.git
2. `SHA256 Hash`算法：<https://en.wikipedia.org/wiki/SHA-2>
3. `EdDSA`算法：<https://en.wikipedia.org/wiki/EdDSA>
4. `Poseidon Hash`算法：<https://www.poseidon-hash.info/>


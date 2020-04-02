# 请求签名

路印中继API涉及到两种不同类别的签名。一种是通用的API签名，用来验证API调用已经被账号拥有者授权；另一种是对API POST到服务端的特定的数据结构做签名，用来向路印协议的电路证明该数据已经被账号拥有者授权。我们分别对这两者做个说明。


## 通用API请求的签名

路印多数API都要求用户对请求做签名。签名要作为HTTP头`X-API-SIG`的值传给中继。签名的过程涉及到4个步骤：

1. 对请求的参数或者payload进行规整，使其转换成一个字符串 `s`；
2. 计算`s`的**SHA-256**哈希值`h`
3. 对`h`用账号的私钥`privateKey`做签名，得到三个值：`Rx`,`Ry`, 和`S`；
4. 将`Rx`,`Ry`, 和`S`通过逗号分隔拼接成最终签名字符串：`${Rx},${Ry},${S}`。

后三个步骤都浅显易懂，但第一步需要做个更详细的说明。


#### URL参数规整
如果您使用的某个API支持URL参数，比如`?a=1&c=3&b=2`，那么您需要将这些URL参数规整成一个JSON对象。规则如下：

1. 将参数的名称和值转换成Key/Value对象数组：`[{"a":"1"},{"c":"3"},{"b":"2"}]`。注意使用双引号，且不要加空格或者换行。
2. 将参数按照Key的字母表升序排列：`[{"a":"1"},{"b":"2"},{"c":"3"}]`。
3. 将这个数组转换成一个字符串`s`。


{% hint style='info' %}
路印目前的API不支URL参数使用`?a=1&a=2&a=3`的形式来把数组`[1,2,3]`作为参数的值。
{% endhint %}

#### Payload规整
如果您使用的API支持payload。假设这个payload JSON对象为：

```json
{
    "y": 2020,
    "x": "foo",
    "z": ["bar1", {"k": 1}]
}
```
1. 首先也需要将这个JSON中第一层的Key/Value转换成Key/Value对象数组：`[{"y":2020},{"x":"foo"},"z":["bar1", {"k": 1}]]`,不要加空格或者换行。如果Value不是字符串而是其它类型也没有关系，不要对Value做任何更改。
2. 将参数按照Key的字母表升序排列：`[{"x":"foo"},{"y":2020},"z":["bar1", {"k": 1}]]`。
3. 将这个数组转换成一个字符串`s`。



#### 综合规整

如果您调用的API即支持URL参数，又支持payload，那么您需要将两个Key/Value对象数组合并后在排序，然后生成一个`s`字符串并对其进行签名。

**TODO: 这个字符串s会自动去掉`"z":["bar1", {"k": 1}]]`中间的空格吗？**


**TODO: 如果URL总有个参数叫`a`, payload JSON里面也有个一样的field，谁会被覆盖？**


## 路印协议链下请求的签名



#### 订单签名

#### 取消订单签名

#### 链下提现签名



---


与以太坊交易使用的ECDSA签名不同，路印协议的链下请求使用EdDSA签名算法（EdDSA对零知识证明更加高效）。

## Poseidon哈希

## EdDSA签名
- 除了需要`API-KEY`外，和账号信息有关的还需要签名，详见[Restful API 概述](../rest_api_overview.md)，这里仅以[取消订单](../dex_apis/cancelOrders.md)为例。

- 调用取消订单接口时，除了接口本身所需的参数外，还需传递`signature`即参数签名。

- 路印交易所对API签名使用`EdDSA SHA256`算法，首先将API参数序列化成型如`[(参数1名, 参数1值), (参数2名, 参数2值), ..., (参数N名, 参数N值)]`的字符串二元组数组，其中参数名按照字典序排序，从而保证服务器验证顺序一致。然后整体转为`JSON`字符串作为` SHA256`的操作对象，得到`SHA256Hash`值，再用`EdDSA`算法对该`SHA256Hash`进行签名，私钥即`privateKey`，最终的签名包含三个整数：`Rx, Ry, S`，将这三个序列化成字符串并用`,`连接起来即为API签名，流程请参考`sign_api_data`代码示例。

- 对API接口的签名使用的`EdDSA`使用`ethsnarks`工程代码，其内部使用`Poseidon HASH`算法，路印交易所的签名参数如下:

```python
poseidon_params(SNARK_SCALAR_FIELD, 6, 6, 52, b'poseidon', 5, security_target=128)
```

- `EdDSA`和`Poseidon Hash`算法细节见参考文献[3]，[4]。

- 可以重载`ethsnarks`的`_SignatureScheme`实现该固定参数的签名类，如下面python代码所示。

- 签名数据放在`http request header`里的`X-API-SIG`中。

```python
apiKey = ...
session = init_request_session(apiKey)
...
#初始化API数据 api_request_params
...
#对API数据签名
sig = sign_api_data(api_request_params，user_api_secret)
session.headers.update({'X-API-SIG': sig})
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
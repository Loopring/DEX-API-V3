# Poseidon哈希与EdDSA签名

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
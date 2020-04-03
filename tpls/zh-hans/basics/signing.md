# 请求签名

路印中继API涉及到两种不同类别的签名。一种是通用的API签名，用来验证API调用已经被账号拥有者授权；另一种是对API POST到服务端的特定的数据结构做签名，用来向路印协议的电路证明该数据已经被账号拥有者授权。我们分别对这两者做个说明。


## 通用API请求的签名

路印多数API都要求用户对请求做签名。签名要作为HTTP头`X-API-SIG`的值传给中继。签名的过程涉及到4个步骤：

1. 对请求的参数或者payload进行规整，使其转换成一个字符串 `s`；
2. 计算`s`的**SHA-256**哈希值`h`
3. 对`h`用账号的私钥`privateKey`做签名，得到三个值：`Rx`,`Ry`, 和`S`（见下面章节）；
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

**TODO（马超）: 这个字符串s会自动去掉`"z":["bar1", {"k": 1}]]`中间的空格吗？**

**TODO（马超）: 如果URL总有个参数叫`a`, payload JSON里面也有个一样的field，谁会被覆盖？**


## 路印协议链下请求的签名

路印协议3.1.1支持“订单”，和“链下提现”两种**链下请求**。由于这两种链下请求都会造成对交易所默克尔树的修改，通过中继API提交这是两种数据时，必须附带特殊的签名。


{% hint style='info' %}
路印协议3.1.1还支持**取消订单**这个链下请求，但会在后续的3.5版本中去掉。因此路印交易所没有计划支持链下取消订单。
{% endhint %}

链下请求签名包括以下步骤：

1. 对请求`r`进行规整，使其变成一个字符串`s`。
2. 计算`s`的**Poseidon**哈希值`h`（见下面章节）。
3. 对`h`用账号的私钥`privateKey`做签名，得到三个值：`Rx`,`Ry`, 和`s`（见下面章节）。
4。将`h`, `Rx`,`Ry`, 和`S`合并到`r`当中。

```json
"hash": ...,
"signatureRx": "16367919966553849834214288740952929086694704883595501207054796240908626703398",
"signatureRy": "5706650945525714138019517276433581394702490352313697178959212750249847059862",
"signatureS": "410675649229327911665390972834008845981102813589085982164606483611508480748"
```

#### 对订单做签名

订单中一些数据项需要按照特定序列化成一个整数数组，对这个数组计算Poseidon哈希，然后对该哈希做EdDSA签名。

{% hint style='info' %}
订单的序列化规则，哈希，签名方式必须严格遵循[路印协议规范](https://github.com/Loopring/protocols/blob/master/packages/loopring_v3/DESIGN.md)。
{% endhint %}

下面我们用Python代码做示范：

```python
def sign_int_array(privateKey, serialized, p):
    PoseidonHashParams = poseidon_params(
        SNARK_SCALAR_FIELD,
        p,
        6,
        53,
        b'poseidon',
        5,
        security_target=128
    )
    
    hash = poseidon(serialized, PoseidonHashParams)
    signedMessage = PoseidonEdDSA.sign(hash, FQ(int(privateKey)))
    return ({
        "hash": str(hash),
        "signatureRx": str(signedMessage.sig.R.x),
        "signatureRy": str(signedMessage.sig.R.y),
        "signatureS": str(signedMessage.sig.s),
    })

def serialize_order(order):
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

def sign_order(privateKey, order):
	serialized = serialize_order(order)
	signed = sign_int_array(serialized, 14 /* 注意这个值 */)
    order.update(signed)
```
{% hint style='info' %}
如果您不使用ethsnarks代码仓库计算poseidon哈希，请一定配置好poseidon的参数，保证其与路印协议使用的参数完全一致。否则验证签名会失败。
{% endhint %}



#### 对链下提现做签名
{% hint style='danger' %}
目前的中继API还不支持客户端提交链下提现请求。不过我们会很快增加这个API。
{% endhint %}

下面链下提现的一个例子：
```json
{
    "exchangeId": 2,
    "accountId":100,
    "tokenId": 0,
    "amount": 1000000000000000000,
    "feeTokenId": "2",
    "amountFee": 20000000000000000000,
    "label": 0,
    "nonce": 10
}
```

用Python对其签名的代码：
```python
def serialize_offchain_withdrawal(withdrawal):
    return [
        int(withdrawal['exchangeId']),
        int(withdrawal['accountId']),
        int(withdrawal['tokenId']),
        int(withdrawal['amount']),
        int(withdrawal['feeTokenId']),
        int(withdrawal['amountFee']),
        int(withdrawal['label']),
        int(withdrawal['nonce'])
    ]

def sign_offchain_withdrawal(privateKey, offchainWithdrawal):
    serialized = serialize_offchain_withdrawal(offchainWithdrawal)
    signed = sign_int_array(serialized, 9 /* 注意这个值 */)
    offchainWithdrawal.update(signed)
```

## 参考资料
您可以通过下列文献和代码仓库了解更多关于Poseidon哈希和EdDSA签名的细节。

1. `ethsnarks`代码仓库：https://github.com/HarryR/ethsnarks.git
2. `SHA256 Hash`算法：<https://en.wikipedia.org/wiki/SHA-2>
3. `EdDSA`算法：<https://en.wikipedia.org/wiki/EdDSA>
4. `Poseidon Hash`算法：<https://www.poseidon-hash.info/>


您也可以参考我们的[示范代码](./examples.md)了解更多应用细节。
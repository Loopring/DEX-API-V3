
# 秘钥管理

使用路印交易所API之前，您需要了解如何获取和更改您账号的EdDSA公秘钥对和API Key。调用API时，API Key需要通过HTTP头传递给路印的中继；EdDSA秘钥用来在客户端对链下请求做数字签名。

## 获取


首先您需要在路印交易所的网页界面（[Loopring.io](https://loopring.io)）注册一个账号。注册好账号之后，您可以使用『导出账号』功能将账号相关的很多信息通过JSON格式导出。这些信息包括EdDSA公秘钥对和API Key。

导出的JSON看起来应该类似于：

```json
{
    "exchangeName": "LoopringDEX: Beta 1",
    "exchangeAddress": "0x944644Ea989Ec64c2Ab9eF341D383cEf586A5777",
    "exchangeId": 2,
    "accountAddress": "0xe9577b420d96adfc97ff1e9e0557f8c73d7247fe",
    "accountId": 12345,
    "apiKey": "qXJpfTKrF0O5jIDPYIu7YkVgLFbvm5uIgPKBmHP2kBpcdKZjgfFKhIlE8evo9lKa",
    "publicKeyX": "20230748339558541226323870947000799026059173889124399831342481595010628000129",
    "publicKeyY": "4980637490279511620100245514492532318691849019959343538108355525575855311214",
    "privateKey": "1242957328515765470505817310060337585626176314364086438653683782645761561015"
}
```

其中的前4项是常量，和路印交易所的版本相关；其它数据项和您的账号相关。其中`publicKeyX`与`publicKeyY`合起来是EdDSA公钥，`privateKey`是EdDSA秘钥。


{% hint style='danger' %}
请您一定妥善保管EdDSA秘钥和API Key。如果这些信息不慎泄漏，会导致您资产的丢失。
在任何情况下，路印交易所和其API均不会向您询问EdDSA私钥。
{% endhint %}


## 更改

您可以通过路印交易所的『更改密码』功能更改您账户的EdDSA公秘钥对。由于涉及到以太坊交易确认和零知识证明，新的EdDSA公秘钥对需要等待至少一个以太坊确认后才会生效。

**TODO: 新key的生效时间需要马超确认！**

API Key则可以通过路印的API接口更改。


#### EdDSA的生成方式
路印协议对EdDSA的生成方式不做任何限制。在路印交易所，每个账号的EdDSA公秘钥对是由这个账号的**以太坊地址**和**交易密码**派生计算出来的。由于地址是公开信息，因此账户交易密码的强度至关重要。


{% hint style='danger' %}
如果您使用路印交易所网站来设置交易密码，您的密码应该足够强大，无需担心被暴力破解；否则您需要特别注意不要使用简单密码。和中心化交易所不同，暴力破解您的EdDSA秘钥可以不必经过路印的中继系统，因为您的EdDSA公钥存储在以太坊上，黑客可以将其读取出来做暴力破解的对比参照。
{% endhint %}


派生算法如下所示：

```python
seed = keccakHash('LOOPRING' + address.toLowerCase() + keccakHash(password))
keyPair = myEdDSAGenerator.generate(seed)
```

其中`keccakHash`返回kecca256运算后的16进制字符串。


#### API Key的生成方式

API Key是在注册账号时有路印中继随机生成的一个全局唯一字符串，与您的账号一对一绑定。

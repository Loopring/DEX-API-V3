
# 管理API Key


## 获取API Key


首先您需要在**路印交易所**的网页界面（[Loopring.io](https://loopring.io)）商注册一个交易所账号。创建好账号之后，您可以使用[Loopring.io](https://loopring.io)的*『导出账号』*功能导出`API-Key`、EdDSA公私钥`publicKeyX`、` publicKeyY`，和`privateKey`。使用路印交易所的API需要上述信息。您到处的信息应该类似于下面的例子：

```json
{
    "exchangeName": "LoopringDEX: Beta 1",
    "exchangeAddress": "0x944644Ea989Ec64c2Ab9eF341D383cEf586A5777",
    "exchangeId": 2,
    "accountAddress": "0xe9577b420d96adfc97ff1e9e0557f8c73d7247fe",
    "accountId": 123456,
    "apiKey": "qXJpfTKrF0O5jIDPYIu7YkVgLFbvm5uIgPKBmHP2kBpcdKZjgfFKhIlE8evo9lKa",
    "publicKeyX": "20230748339558541226323870947000799026059173889124399831342481595010628000129",
    "publicKeyY": "4980637490279511620100245514492532318691849019959343538108355525575855311214",
    "privateKey": "1242957328515765470505753610060337585626176314364086438653683782645761561015"
}
```

{% hint style='danger' %}
请妥善保管API Key和EdDSA私钥。如果这些信息不慎泄漏，会导致您资产的损失。在任何情况下，路印交易所和其API均不会向您询问EdDSA私钥。
{% endhint %}



您可以通过路印交易所的UI（[Loopring.io](https://loopring.io)），在登陆账号后，通过『导出账号』功能获取自己账号的API Key和EdDSA私钥。您也通过[查询用户ApiKey](./dex_apis/getApiKey.md)获取自己账号的API Key。此时您需要对请求做签名，以保证别的用户无法获取您的API key。


## 更改API Key
如果您想更改API Key，可以调用[更新用户ApiKey](./dex_apis/applyApiKey.md)接口，并提供入老的API Key。或者您也可以通过路印交易所的UI（[Loopring.io](https://loopring.io)）手动更新API Key.

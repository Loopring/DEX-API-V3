
# 管理API Key

您可以通过路印交易所的UI（[Loopring.io](https://loopring.io)），在登陆账号后，通过『导出账户』功能获取自己账号的API Key和EdDSA私钥。您也通过[查询用户ApiKey](./dex_apis/getApiKey.md)获取自己账号的API Key。此时您需要对请求做签名，以保证别的用户无法获取您的API key。

如果您想更改API Key，可以调用[更新用户ApiKey](./dex_apis/applyApiKey.md)接口，并提供入老的API Key。或者您也可以通过路印交易所的UI（[Loopring.io](https://loopring.io)）手动更新API Key.



# REST API 概述

本文主要描述路印交易所REST API的共性部分。

{% hint style='info' %}
每个API请求都有流量限制，超额的调用请求会被拒绝（返回429）。如果您长期超额调用API，您的账户就会被列入黑名单，从而无法继续使用API。
{% endhint %}


## HTTP头

所有API都需要指定`X-API-KEY`HTTP头；有一些API还需要指定`X-API-SIG`HTTP头来提供EdDSA签名信息。

需要`X-API-KEY`HTTP头的API：

- 除[查询用户ApiKey](./dex_apis/getApiKey.md)外的所有API。

需要`X-API-SIG`HTTP头的API：

- [查询用户ApiKey](./dex_apis/getApiKey.md)
- [取消订单](./dex_apis/cancelOrder.md)

需要特殊`X-API-SIG`HTTP头签名的请求：

- [提交订单](./dex_apis/submitOrder.md)

## 获取API Key

### 通过路印交易所UI获取

您可以通过路印交易所的UI（[Loopring.io](https://loopring.io)），在登陆账号后，通过『导出账户』功能获取自己账号的API Key和EdDSA私钥。

### 通过API获取

您也通过[查询用户ApiKey](./dex_apis/getApiKey.md)获取自己账号的API Key。此时您需要对请求做签名，以保证别的用户无法获取您的API key。


## 更改API Key

如果您想更改API Key，可以调用[更新用户ApiKey](./dex_apis/applyApiKey.md)接口，并提供入老的API Key。

## 请求签名

### 请求参数是大小写不敏感

如上所述，路印DEX的一部分链下请求需要使用签名，用户在创建账号的同时，会创建一对公私钥用于EdDSA签名。有两类使用此公私钥签名的方式。

一种是电路不感知的签名，主要用于网关进行权限校验：

**[X-API-SIG]**

当用户请求获取API-KEY或取消订单时，需要在header里添加X-API-SIG，生成规则如下：
1. 将请求参数按key字典顺序排序后生成Json String
2. 使用SHA-256计算json字符串的hash
3. 使用创建账户时的EdDSA私钥，对hash签名，将签名结果`Rx,Ry,S`三部分按"`,`"分隔并以上述顺序拼成一个字符串，作为X-API-SIG的值放入请求的header里。签名使用的`EdDSA`参考`ethsnarks`，其内部使用`Poseidon HASH`算法，参数如下：
```py
poseidon_params(SNARK_SCALAR_FIELD, 6, 6, 52, b'poseidon', 5, security_target=128)
```

另外一种是在电路处验签的签名，这种请求利用零知识证明技术保证即使是路印的Relayer也无法更改用户的意图：

** [电路签名](./dex_integrations/trader.md#OrderSig) **

## API返回结果

除了网络错误，所有API都会返回200状态码和代表API结果的JSON数据。JSON返回信息中都包含一个resultInfo字段，用以反馈API调用的通用状态，特别是出错时候的状态码。如果请求正常返回，则还会返回一个data字段，该字段的值也是一个JSON结构，针对不同API代表不同的业务数据，可以参考每个API说明。

{% include "./common.md" %}

# REST API

本部分主要讨论路印DEX Restful API的共性部分。
> [!DANGER]
>
> 
> 每个API请求会有流量限制的说明，超过此流量限制的请求会被拒绝（返回429）。如果调用端长期超过流量限制调用请求，有可能进入黑名单，从而无法调用路印DEX的API。

## HTTP Request Header

API请求要求在Header中传入X-API-KEY 或/和X-API-SIG。请求都需要X-API-KEY才能访问；一些关键请求需要EDDSA签名信息：X-API-SIG。
还有一些请求需要使用特殊的方式来进行EDDSA签名。

需要X-API-KEY的请求：

- 除[查询用户ApiKey](./dex_apis/getApiKey.md)以外的所有请求

需要X-API-SIG的请求：

- [查询用户ApiKey](./dex_apis/getApiKey.md)
- [取消订单](./dex_apis/cancelOrder.md)

需要特殊签名的请求：

- [提交订单](./dex_apis/submitOrder.md)

### 获取API key

**[前端获取]**

用户可以在交易所( https://www.loopring.io )的“导出账户”中看到自己的“apiKey”，并在调用API时，设置到http header的X-API-KEY中。

**[API获取]**

用户注册的时候系统会产生对应的API key，用户通过[查询用户ApiKey](./dex_apis/getApiKey.md)拿到这个key，此时需要对请求签名以保证别的用户无法获取API key。以后每次调用此API都返回同样的key。

如果用户想要更换API key，可以调用[更新用户ApiKey](./dex_apis/applyApiKey.md)接口（请求头需传入老的API key），这样会更换一个新的API key，然后每次调用[查询用户ApiKey](./dex_apis/getApiKey.md)都会返回新的key。

### 请求签名

**请求参数是大小写不敏感的**

如上所述，路印DEX的一部分链下请求需要使用签名，用户在创建账号的同时，会创建一对公私钥用于EDDSA签名。有两类使用此公私钥签名的方式。

一种是电路不感知的签名，主要用于网关进行权限校验：

**[X-API-SIG]**

当用户请求获取API-KEY或取消订单时，需要在header里添加X-API-SIG，生成规则如下：
1. 将请求参数按key字典顺序排序后生成Json String
2. 使用SHA-256计算json字符串的hash
3. 使用创建账户时的EDDSA私钥，对hash签名，将签名结果`Rx,Ry,S`三部分按"`,`"分隔并以上述顺序拼成一个字符串，作为X-API-SIG的值放入请求的header里。签名使用的`EDDSA`参考`ethsnarks`，其内部使用`Poseidon HASH`算法，参数如下：
```py
poseidon_params(SNARK_SCALAR_FIELD, 6, 6, 52, b'poseidon', 5, security_target=128)
```

另外一种是在电路处验签的签名，这种请求利用零知识证明技术保证即使是路印的Relayer也无法更改用户的意图：

** [电路签名](./dex_integrations/trader.md#OrderSig) **

## 返回结果

除了网络错误，所有API都会返回200状态码，以及json信息。

json返回信息中都会包含resultInfo字段，告知本次调用的情况：是否成功；若失败，发生了什么样的错误。

如果请求正常返回，则还会返回data字段（也是json串），该字段针对不同API代表不同的结构，可以参考具体的API说明。

下面是公共信息的细节描述。

{% include "./common.md" %}

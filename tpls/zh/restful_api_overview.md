# Restful API 概述

本部分主要讨论路印DEX Restful API的共性部分。

## Http header

API请求要求在Header中传入X-API-KEY 或/和X-API-SIG。大多数请求都需要X-API-KEY才能访问；一些关键请求需要EDDSA签名信息：X-API-SIG。
还有一些请求需要使用特殊的方式来进行EDDSA签名。下面详细说明。

### 获取API key

**[前端获取]**

用户可以在交易所( https://www.loopring.io )的“导出账户”中看到自己的“apiKey”，并在调用API时，设置到http header的X-API-KEY中。

**[API获取]**

可以使用getApiKey接口获得API key，细节参考接口说明。

还可以使用applyApiKey来更换API key，细节参考接口说明。

需要注意，这两个接口的调用都是需要签名信息的。签名方法会在下面描述。

### 请求签名

如上所述，路印DEX的一部分链下请求需要使用EDDSA进行签名，这其中又有两类签名方式：
TODO(yongfeng): 描述下两种签名方式，一种是电路不感知的，如何签名；一种是电路感知的，给出相关API(我的理解只有submitOrder和cancelOrder两个接口)的链接即可，相关API的描述会有细节。

**[X-API-SIG]**

当用户请求获取API-KEY或取消订单时，需要在header里添加X-API-SIG，生成规则如下：
1. 将请求参数按key字典顺序排序后生成Json String
2. 使用SHA-256计算json字符串的hash
3. 使用创建账户时的EdDSA私钥，对hash签名，将签名结果`"$Rx,$Ry,$S"`三部分按"`,`"分隔并以上述顺序拼成一个字符串，作为X-API-SIG的值放入请求的header里。签名使用的`EDDSA`参考`ethsnarks`，其内部使用`Poseidon HASH`算法，参数如下：
```py
poseidon_params(SNARK_SCALAR_FIELD, 6, 6, 52, b'poseidon', 5, security_target=128)
```

**[电路签名]**

## 返回结果

除了网络错误，所有API都会返回200状态码，以及json信息。

json返回信息中都会包含resultInfo字段，告知本次调用的情况：是否成功；若失败，发生了什么样的错误。

如果请求正常返回，则还会返回data字段（也是json串），该字段针对不同API代表不同的结构，可以参考具体的API说明。

下面是公共信息的细节描述。

{% include "./common.md" %}

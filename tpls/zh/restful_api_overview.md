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

### X-API-SIG

如上所述，路印DEX的一部分链下请求需要使用EDDSA进行签名，这其中又有两类签名方式：
TODO(yongfeng): 描述下两种签名方式，一种是电路不感知的，如何签名；一种是电路感知的，给出相关API(我的理解只有submitOrder和cancelOrder两个接口)的链接即可，相关API的描述会有细节。

## 返回结果

除了网络错误，所有API都会返回200状态码，以及json信息。

json返回信息中都会包含resultInfo字段，告知本次调用的情况：是否成功；若失败，发生了什么样的错误。

如果请求正常返回，则还会返回data字段（也是json串），该字段针对不同API代表不同的结构，可以参考具体的API说明。

下面是公共信息的细节描述。

{% include "./common.md" %}
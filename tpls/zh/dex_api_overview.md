# DEX API 概述

路印DEX API 为Restful API。下面描述的规则适用于所有API。

## Http header

API请求要求在Header中传入X-API-KEY 或/和X-API-SIG。大多数请求都需要X-API-KEY才能访问；一些关键请求需要EDDSA签名信息：X-API-SIG。
还有一些请求需要使用特殊的方式来进行EDDSA签名。下面详细说明。

### 获取API key

用户可以在交易所的“导出账户”中看到自己的“apiKey”，并在调用相关API时，设置到http header的X-API-KEY中。

### X-API-SIG


TODO(yongfeng)

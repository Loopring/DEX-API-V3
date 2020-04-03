

# REST APIs

本文主要描述路印交易所REST API的共性部分。

## 需要API-KEY的API接口

- API密钥可以从`loopringDEX`网页导出或通过API获取。

- 所有接口（除[查询用户ApiKey](./dex_apis/getApiKey.md)）都需要传入API-KEY，API信息请查询[Restful API 概述](../rest_api_overview.md)。

- API密钥数据放在`http request header`里的`X-API-KEY`中。

```python
def init_request_session(user_api_key):
    session = requests.session()
    session.headers.update({'Accept': 'application/json',
                            'X-API-KEY': user_api_key})
    return session
```




## API限流

每个API请求都有流量限制，超额的调用请求会被拒绝（返回429）。如果您长期超额调用API，您的账号就会被列入黑名单，从而无法继续使用API。

## HTTP头

所有API都需要指定`X-API-KEY`HTTP头；有一些API还需要指定`X-API-SIG`HTTP头来提供EdDSA签名信息。

需要`X-API-KEY`HTTP头的API：

- 除[查询用户ApiKey](./dex_apis/getApiKey.md)外的所有API。

需要`X-API-SIG`HTTP头的API：

- [查询用户ApiKey](./dex_apis/getApiKey.md)
- [取消订单](./dex_apis/cancelOrder.md)

需要特殊`X-API-SIG`HTTP头签名的请求：

- [提交订单](./dex_apis/submitOrder.md)

## 请求签名

### 请求参数是大小写不敏感

一种是与电路无关的签名，主要用于网关进行权限校验。生成规则如下：
1. 将请求参数按key字典顺序升序排序后生成JSON字符串，并统一转换为小写。
2. 使用SHA256计算JSON字符串的哈希。
3. 使用创建账号时的EdDSA私钥，对哈希签名。然后将签名结果`Rx,Ry,S`三部分按"`,`"分隔并以该顺序拼成一个字符串。

另一种是与电路有关的签名，详情请见[**电路签名**](./tutorials/trader.md#OrderSig)。

## API返回

除了网络错误，所有API都会返回200状态码和代表API结果的JSON数据。JSON返回信息中都包含一个resultInfo字段，用以反馈API调用的通用状态，特别是出错时候的状态码。如果请求正常返回，则还会返回一个data字段，该字段的值也是一个JSON结构，针对不同API代表不同的业务数据，可以参考每个API说明。

{% include "./common.md" %}

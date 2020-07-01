

# REST API

本文主要描述路印交易所REST API的共性部分。

## 接入URL

```
https://api.loopring.io
```

## 限流

每个API都有流量限制，超额的调用请求会被拒绝（返回429）。如果您长期超额调用，您的账号就会被列入黑名单，从而无法继续使用路印API。

## HTTP头


#### X-API-KEY
除[查询用户ApiKey](./dex_apis/getApiKey.md)外的所有API都需要指定`X-API-KEY`HTTP头，提供用户的ApiKey。

#### X-API-SIG

以下API需要指定`X-API-SIG`HTTP头，提供用户的的EdDSA数字签名：

- [查询用户ApiKey](./dex_apis/getApiKey.md)
- [取消订单](./dex_apis/cancelOrder.md)
- [更新ApiKey](./dex_apis/applyApiKey.md)
- [根据orderHash批量取消订单](./dex_apis/batchCancelOrdersByOrderHash.md)
- [根据clientOrderId批量取消订单](./dex_apis/batchCancelOrdersByClientOrderId.md)
- [提交transfer](./dex_apis/submitTransfer.md)

#### 设置HTTP头
使用Python设置HTTP头的代码如下：

```python
def init_request_session(apiKey, sig):
    session = requests.session()
    session.headers.update({
    	'Accept': 'application/json',
		'X-API-KEY': apiKey,
		'X-API-SIG': sig,
	})
    return session
```

## API返回值

除了网络错误，所有API都会返回200状态码和代表API结果的JSON数据。JSON返回信息中都包含一个`resultInfo`字段，用以反馈API调用的通用状态，特别是出错时候的状态码。如果请求正常返回，则还会返回一个`data`字段，该字段的值也是一个JSON结构，针对不同API代表不同的业务数据，请参考每个API说明。

{% include "./common.md" %}

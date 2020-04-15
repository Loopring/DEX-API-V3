

# REST API

This article describes some common parts for Loopring's REST API.

## Base URL

```
https://api.loopring.io
```

## Rate Limit

Each API has its rate limit settings. The relayer will reject all API invocations beyond this limit, with status code `429`. Stop excessive API invocations to avoid your account from being suspended.

## HTTP Headers


#### X-API-KEY
All API except [querying user ApiKey](./dex_apis/getApiKey.md) need to specify the `X-API-KEY` HTTP header with the user's ApiKey as the value.

#### X-API-SIG

The following API needs to specify the `X-API-SIG` HTTP header to provide an EdDSA signature:

- [Query ApiKey](./dex_apis/getApiKey.md)
- [Cancel order](./dex_apis/cancelOrder.md)
- [Change ApiKey](./dex_apis/applyApiKey.md)

#### Setting HTTP Headers
To set the HTTP headers using Python, use the code below:

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

## Response

Except for network errors, all API will return the `200` HTTP status code and a JSON object representing the actual API result. The JSON  contains a `resultInfo` structure that has a `code` field for application-specific status code, and a `data` JSON object that represents API-specific response.

{% include "./common.md" %}

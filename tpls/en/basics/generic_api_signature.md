#### Algorithm

- Initialize `signatureBase` to an empty string.
- Append the API's  HTTP method to `signatureBase`.
- Append `'＆'` to `signatureBase`.
- Append *percent-encoded* full URL path (without `?` or any query parameters) to `signatureBase`.
- Append `'&'` to `signatureBase`.
- Initialize `parameterString` to an empty string.
- For GET / DELETE requests:
    * Sort query parameters in ascending order lexicographically;
    * Append *percent-encoded* key name to `parameterString`;
    * Append an `'='` to `parameterString`;
    * Append *percent-encoded* value to `parameterString`;
    * Append a `'&'` if there are more key value pairs.
- For POST / PUT requests:
    - Append request body as a string to `parameterString`.
- Append *percent-encoded* `parameterString` to `signatureBase`
- Calculate the **SHA-256** hash of `signatureBase` as `hash`.
- Sign`hash` with the private EdDSA key and get `Rx`, `Ry`, and `S`.
- Concatenate `Rx`,`Ry`, and`S` using `','` as: `${Rx},${Ry},${S}`.

#### HTTP Method and URL

Please make sure you use only the following HTTP methods, in upper case letters.
- GET
- POST
- PUT
- DELETE

Also make sure the HTTPS header is included and is in lower case. For example:

```
https://api3.loopring.io/api/v3/apiKey
```

#### Example

Actually So far only 2 API need this special EDDSA API signing -- **updateApiKey** & **cancel order**, let's see how the signatureBase is contructed.

##### Update user API key
For the above url with the following url query parameters:

```
https://api3.loopring.io/api/v3/apiKey?accountId=10005
```

or

|  Query param   | Value  |
|  ----  | ----  |
| accountId  | 10005 |

`parameterString` shoule be:
```
accountId=10005
```

and `signatureBase` should be:
```
GET&https%3A%2F%2Fapi3.loopring.io%2Fapi%2Fv2%2FapiKey&accountId%3D10005
```

##### Cancel Order

For the above url with the following url query parameters:

```
https://api3.loopring.io/api/v3/order?accountId=10005&clientOrderId=Sample
```

or

|  Query param   | Value  |
|  ----  | ----  |
| accountId  | 10005 |
| clientOrderId  | Sample |

`parameterString` shoule be:
```
accountId=10005&clientOrderId=Sample
```

and `signatureBase` should be:
```
DELETE&https%3A%2F%2Fapi3.loopring.io%2Fapi%2Fv3%2Forder&accountId%3D10005%26clientOrderId%3DSample
```
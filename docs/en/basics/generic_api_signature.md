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
https://api.loopring.io/api/v2/apiKey
```

#### Example
For the above url with the following url query parameters:

```
https://api.loopring.io/api/v2/apiKey?publicKeyX=13375450901292179417154974849571793069
911517354720397125027633242680470075859&publicKeyY=133754509012921794171549748495717930
69911517354720397125027633242680470075859&accountId=1
```

or

|  Query param   | Value  |
|  ----  | ----  |
| publicKeyX  | 13375450901292179417154974849571793069911517354720397125027633242680470075859 |
| publicKeyY  | 13375450901292179417154974849571793069911517354720397125027633242680470075859 |
| accountId  | 1 |

`parameterString` shoule be:
```
accountId=1&publicKeyX=1337545090129217941715497484957179306991151735472039712502763324
2680470075859&publicKeyY=13375450901292179417154974849571793069911517354720397125027633
242680470075859
```

and `signatureBase` should be:
```
GET&https%3A%2F%2Fapi.loopring.io%2Fapi%2Fv2%2FapiKey&accountId%3D1%26publicKeyX%3D1337
5450901292179417154974849571793069911517354720397125027633242680470075859%26publicKeyY%
3D13375450901292179417154974849571793069911517354720397125027633242680470075859
```

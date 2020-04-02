---

## Common info

### URL

**https://api.loopring.io**

### Header

| Field |  Type | Required | Description | Example |
| :---- | :---- | :---- |   :----   |  :--- |
| X-API-KEY | string | N | API Key | "sra1aavfa" |
| X-API-SIG | string | N | Signature | "dkkfinfasdf" |

### Response

| Field |  Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | Y | Result of API invocation | - |

#### ResultInfo
<span id="ResultInfo"></span>

| Field |  Type | Required | Description | Example |
| :---- | :---- | :---- |   :----   |  :--- |
| code | integer | Y | Return code | 0 |
| message | string | Y | Return message.  This is used for debug only. Do not show to users | "SUCCESS" |


### Return code
| Return code | Description |
| :---- | :---- |
| 0 | Success |
| 100000 | Unknown internal error |
| 100001 | Invalid parameter |
| 100002 | Request timeout |
| 100202 | Update fail |
| 100203 | Internal persistence error |
| 100204 | Duplicate request |

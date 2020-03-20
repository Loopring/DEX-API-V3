### Common info
----

#### API host

**https://api.loopring.io**

#### Header

| Field |  Type | Required | Description | Sample |
| ---- | ---- | ---- |   ----   |  --- |
| X-API-KEY | string | N | API Key. Needed by updating api | "sra1aavfa" |
| X-API-SIG | string | N | Signature info. Needed by getapikey and cancelorder api | "dkkfinfasdf" |

#### Response

| Field |  Type | Required | Description | Sample |
| ---- | ---- | ---- | ---- | ---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | Y | Result of api invoking | / |

#### Return code
| Return code | Description |
| ---- | ---- |
| 0 | Success |
| 100000 | Internal unknown error |
| 100001 | Illegality parameter |
| 100002 | Request timeout |
| 100202 | Update fail |
| 100203 | Internal persistence error |
| 100204 | Submit duplicated |

#### 模型

##### ResultInfo
<span id="ResultInfo"></span>

| Field |  Type | Required | Description | Sample |
| ---- | ---- | ---- |   ----   |  --- |
| code | integer | Y | Return code | 0 |
| message | string | Y | Return message.  This is used for debug only. Do not show to users | "SUCCESS" |
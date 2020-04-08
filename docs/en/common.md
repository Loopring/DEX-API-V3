#### Response

| Field |  Type | Required | Description | Example |
| :---- | :---- | :---- | :---- | :---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | Y | Result of API invocation | - |

#### ResultInfo Struct
<span id="ResultInfo"></span>

| Field |  Type | Required | Description | Example |
| :---- | :---- | :---- |   :----   |  :--- |
| code | integer | Y | Status code | 0 |
| message | string | Y | Return message.  This is used for debug only. Do not show to users | "SUCCESS" |


#### Status code
| Status code | Description |
| :---- | :---- |
| 0 | Success |
| 100000 | Unknown internal error |
| 100001 | Invalid parameter |
| 100002 | Request timeout |
| 100202 | Update fail |
| 100203 | Internal persistence error |
| 100204 | Duplicate request |

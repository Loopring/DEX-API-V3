---

## 公共信息

### URL

**https://api.loopring.io**

### HTTP头

| 字段 |  类型 | 必须 | 说明 | 举例 |
| :---- | :---- | :---- |   :----   |  :--- |
| X-API-KEY | string | 否 | API Key | "sra1aavfa" |
| X-API-SIG | string | 否 | 签名信息 | "dkkfinfasdf" |

### 返回值

| 字段 |  类型 | 必须 | 说明 | 举例 |
| :---- | :---- | :---- | :---- | :---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | 是 | 调用结果 | - |

#### ResultInfo
<span id="ResultInfo"></span>

| 字段 |  类型 | 必须 | 说明 | 举例 |
| :---- | :---- | :---- |   :----   |  :--- |
| code | integer | 是 | 返回码 | 0 |
| message | string | 是 | 返回说明。用来帮助调试，不应在前端显示或用于逻辑判断。 | "SUCCESS" |


### 返回码
| 返回码 | 描述 |
| :---- | :---- |
| 0 | 成功 |
| 100000 | 内部未知错误 |
| 100001 | 参数非法 |
| 100002 | 请求超时 |
| 100202 | 更新失败 |
| 100203 | 内部存储错误 |
| 100204 | 重复提交 |

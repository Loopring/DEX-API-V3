### 公共信息
----

#### 访问地址

**http://localhost:9000**

#### 请求头

| 字段 |  类型 | 是否必现 | 说明 | 举例 |
| ---- | ---- | ---- |   ----   |  --- |
| X-API-KEY | string | 否 | API Key. 写操作接口需要 | "sra1aavfa" |
| X-API-SIG | string | 否 | 签名信息. getapikey, cancelorder 接口需要 | "dkkfinfasdf" |

#### 响应

| 字段 |  类型 | 是否必现 | 说明 | 举例 |
| ---- | ---- | ---- | ---- | ---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | 是 | 调用结果 | / |

#### 返回码
| 返回码 | 描述 |
| ---- | ---- |
| 0 | 成功 |
| 100000 | 内部未知错误 |
| 100001 | 参数非法 |

#### 模型

##### ResultInfo
<span id="ResultInfo"></span>

| 字段 |  类型 | 是否必现 | 说明 | 举例 |
| ---- | ---- | ---- |   ----   |  --- |
| code | number | 是 | 返回码 | 0 |
| message | string | 是 | 返回消息.  该返回消息更多用来调试，不要直接在前端显示 | "SUCCESS" |
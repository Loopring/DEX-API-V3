# 获取系统时间

## API 概要
----

### 功能

获取服务端时间戳。返回结果为毫秒级时间戳。

当需要获得尽可能接近服务端时间时可以使用此API。此API还可以用来测试与服务端的连通性。

### HTTP 方法

**GET**

### 访问路径

**/api/v2/timestamp**

## API 描述
----

### 请求参数
无

### 请求示例

``` bash
curl https://api.loopring.io/api/v2/timestamp
```

### 响应字段

| 字段 | 说明 | 类型 | 是否必现 | 备注 |
| ---- | ---- | ---- | ---- | --- |
| timestamp | 时间戳 | number | 否 | 无 |

### 响应示例

``` json
{
    resultInfo: {
        code: 0,
        message: "SUCCESS"
    },
    timestamp: 1582937047249
}
```

### 返回码

无特殊返回码

## 模型
----

无特殊模型

## 公共信息
----

### 访问地址

**https://api.loopring.io**

### 请求头

| 字段 | 说明 | 类型 | 是否必现 | 备注 |
| ---- | ---- | ---- |   ----   |  --- |
| X-API-KEY | API key | string | 否 | 写操作接口需要 |
| X-API-SIG | 签名信息 | string | 否 | getapikey, cancelorder 接口需要 |

### 响应

| 字段 | 说明 | 类型 | 是否必现 | 备注 |
| ---- | ---- | ---- | ---- | ---- |
| resultInfo | 调用结果 | <a href="#ResultInfo">ResultInfo</a> | 是 |  无 |

### 返回码
| 返回码 | 名称 | 描述 |
| ---- | ---- |
| 0 | SUCCESS  | 成功 |
| 10000 | ERR_INTERNAL_UNKNOWN  | 内部未知错误 |
| 10001 | ERR_INVALID_ARGUMENT | 参数非法 |

### 模型

### ResultInfo
<span id="ResultInfo"></span>

| 字段 | 说明 | 类型 | 是否必现 | 备注 |
| ---- | ---- | ---- |   ----   |  --- |
| code | 返回码 | number | 是 | 无 |
| message | 返回消息 | string | 是 | 该返回消息更多用来调试，不要直接在前端显示 |


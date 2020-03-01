# 获取深度信息

## API 概要
----

### 功能

获取某个市场对的深度信息。

### HTTP 方法

**GET**

### 访问路径

**/api/v2/depth**

## API 描述
----

### 请求参数

| 字段 | 说明 | 类型 | 是否必传 | 备注 | 举例 |
| ---- | ---- | ---- | ---- | --- | --- |
| market | 市场对 | string | 是 | 大小写不敏感 | LRC-ETH |
| level | 深度等级 | number | 是 | 越小表示小数位越多(支持的最大等级从/api/v2/exchange/market接口获取) | 1 |
| limit | 返回条数限制 | number | 否 | 无 | 4 |

### 请求示例

``` bash
curl https://api.loopring.io/api/v2/depth?market=LRC-ETH&level=1&limit=3
```

### 响应字段

| 字段 | 说明 | 类型 | 是否必现 | 备注 | 举例 |
| ---- | ---- | ---- | ---- | --- | --- |
| depth | 市场深度信息 | <a href="#Depth">Depth</a> | 否 | 无 | / |

### 响应示例

``` json
{
    resultInfo: {
        code: 0,
        message: "SUCCESS"
    },
    depth: {
        version: 107,
        timestamp: 1582945500183,
        bids: [{
            price: "0.00017",
            size: "8888000120000000000000",
            volume: "1537624020760000000",
            count: 5
        }, {
            price: "0.00008",
            size: "4049080000000000000000",
            volume: "334126528000000000",
            count: 3
        }, {
            price: "0.00005",
            size: "69934100000000000000",
            volume: "3558136900000000",
            count: 2
        }],
        asks: [{
            price: "0.00018",
            size: "36755272099999999983616",
            volume: "6454012343699999995",
            count: 26
        }, {
            price: "0.00019",
            size: "197481100000000000000",
            volume: "36210810700000000",
            count: 6
        }, {
            price: "0.00020",
            size: "1250560499999999991808",
            volume: "241912939200000002",
            count: 4
        }]
    }
}
```

### 返回码

| 返回码 | 名称 | 描述 |
| ---- | ---- |
| 108000 | ERR_DEPTH_UNSUPPORTED_MARKET | 不支持的市场对 |
| 108001 | ERR_DEPTH_UNSUPPORTED_LEVEL | 不支持的深度级别 |

## 模型
----

### Depth
<span id="Depth"></span>

| 字段 | 说明 | 类型 | 是否必现 | 备注 | 举例 |
| ---- | ---- | ---- |   ----   |  --- | --- |
| version | 版本号 | number | 是 | 无 | 107 |
| timestamp | 时间戳 | number | 是 | 无 | 1582945500183 |
| bids | 卖单 | list<<a href="#Slot">Slot</a>> | 是 | 无 | / |
| asks | 卖单 | list<<a href="#Slot">Slot</a>>| 是 | 无 | / |


### Slot
<span id="Slot"></span>

| 字段 | 说明 | 类型 | 是否必现 | 备注 | 举例 |
| ---- | ---- | ---- |   ----   |  --- | --- |
| price | 价格 | string | 是 | 无 | "0.00017" |
| size | 挂单量 | string | 是 | 无 | "8888000120000000000000" |
| volume | 挂单总数量 | string | 是 | 无 | "1537624020760000000" |
| count | 挂单单数 | number| 是 | 无 | 5 |


## 公共信息
----

### 访问地址

**https://api.loopring.io**

### 请求头

| 字段 | 说明 | 类型 | 是否必现 | 备注 | 举例 |
| ---- | ---- | ---- |   ----   |  --- | --- |
| X-API-KEY | API Key | string | 否 | 写操作接口需要 | "sra1aavfa" |
| X-API-SIG | 签名信息 | string | 否 | getapikey, cancelorder 接口需要 | "dkkfinfasdf" |

### 响应

| 字段 | 说明 | 类型 | 是否必现 | 备注 | 举例 |
| ---- | ---- | ---- | ---- | ---- | --- |
| resultInfo | 调用结果 | <a href="#ResultInfo">ResultInfo</a> | 是 |  无 | / |

### 返回码
| 返回码 | 名称 | 描述 |
| ---- | ---- |
| 0 | SUCCESS  | 成功 |
| 100000 | ERR_INTERNAL_UNKNOWN  | 内部未知错误 |
| 100001 | ERR_INVALID_ARGUMENT | 参数非法 |

### 模型

### ResultInfo
<span id="ResultInfo"></span>

| 字段 | 说明 | 类型 | 是否必现 | 备注 | 举例 |
| ---- | ---- | ---- |   ----   |  --- |  --- |
| code | 返回码 | number | 是 | 无 | 0 |
| message | 返回消息 | string | 是 | 该返回消息更多用来调试，不要直接在前端显示 | "SUCCESS" |


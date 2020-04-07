# 订阅CandleStick更新


通过订阅该主题，您可以获得特定交易对CandleStick更新的数据推送。


## 订阅规则

- `topic`需要指定交易对和时间间隔。如果交易对是`LRC-ETH`，时间间隔是1小时，那么`topic`应该拼写为：`candlestick&LRC-ETH&1hr`。
- 订阅该主题不需要提供ApiKey。
- 支持的交易对可以通过api接口[api/v2/exchange/markets](../dex_apis/getMarkets.md)获取。
- 支持的间隔（interval）为1min, 5min, 15min, 30min, 1hr, 2hr, 4hr, 12hr, 1d, 1w

| 间隔  |  说明  |
| :--- | :---- |
| 1min  | 1分钟  |
| 5min  | 5分钟  |
| 15min | 15分钟 |
| 30min | 30分钟 |
|  1hr  | 1小时  |
|  2hr  | 2小时  |
|  4hr  | 4小时  |
| 12hr  | 12小时 |
|  1d   |  1天   |
|  1w   |  1周   |


## 状态码

| 状态码 |                   描述                    |
| :---- | :--------------------------------------- |
| 104106 | `topic`的值或其参数非法|

## 推送示例

```json
{
    "topic": "candlestick&lrc-btc&1hr",
    "ts":1584717910000,
    "data": [
        "1584717910000",  //start
        "5000",  //count
        "3997.3",  //open
        "3998.7",  //close
        "4031.9",  //high
        "3982.5",  //low
        "500000000000000000",  //size
        "2617521141385000000",  //volume
    ]
}
```

## 模型

#### 推送数据结构

| 字段  |             类型              | 必现 |       说明       |           举例            |
| :--- | :--------------------------- | :------ | :-------------- | :----------------------- |
| topic |            string             |    是    | 订阅的主题和条件 | "candlestick&LRC-ETH&1hr" |
|  ts   |            integer            |    时    | 推送时间（毫秒） |       1584717910000       |
| data  | [List\[string]](#candlestick) （CandleStick列表）|    是    | candlestick数据  |             /             |

####<span id= "candlestick">CandleStick结构</span>

| 序号  |  类型   | 必现 |               说明                |         举例          |
| :------ | :----- | :------ | :------------------------------- | :------------------- |
|    1     | integer |    是    |            指开盘时间             |     1584717910000     |
|    2     | integer |    是    |             成交笔数              |         5000          |
|    3     | string  |    是    |             开盘价格              |       "3997.3"        |
|    4     | string  |    是    |             收盘价格              |       "3998.7"        |
|    5     | string  |    是    |              最高价               |       "4031.9"        |
|    6     | string  |    是    |              最低价               |       "3982.5"        |
|    7     | string  |    是    | 为wei为单位的base token的成交数量 | “500000000000000000”  |
|    8     | string  |    是    | 为wei为单位 quote token的成交数量 | "2617521141385000000" |

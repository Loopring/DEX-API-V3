### candlestick 主题

订阅candlestick，获取定时推送的candlestick数据的更新消息推送。订阅该主题不需要传ApiKey信息。

#### 订阅格式

主题&市场&间隔

- 支持的市场可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets)获取

- 支持的间隔（interval）为1min, 5min, 15min, 30min, 1hr, 2hr, 4hr, 12hr, 1d, 1w

| 间隔  |  说明  |
| :---: | :----: |
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

#### 返回错误码

| 返回码 |                   描述                    |
| :----: | :---------------------------------------: |
| 104106 | candlestick主题的订阅条件不合法或者不支持 |

#### 推送示例

```json
{
  "topic": "candlestick&lrc-btc&1hr",
  "ts":1584717910000,
  "data": {
    "1584717910000",						//start
   	"5000",											//count
   	"3997.3",										//open
    "3998.7",										//close
   	"4031.9",										//high
   	"3982.5",										//low
    "500000000000000000",				//size
    "2617521141385000000",			//volume
  }
}
```

#### 模型

##### 推送数据结构

| 字段  |             类型              | 是否必现 |       说明       |           举例            |
| :---: | :---------------------------: | :------: | :--------------: | :-----------------------: |
| topic |            string             |    是    | 订阅的主题和条件 | "candlestick&lrc-btc&1hr" |
|  ts   |            integer            |    时    | 推送时间（毫秒） |       1584717910000       |
| data  | [List\[string]](#candlestick) |    是    | candlestick数据  |             /             |

#####<span id= "candlestick"> CandleStick结构</span>

| 字段编号 |  类型   | 是否必现 |               说明                |         举例          |
| :------: | :-----: | :------: | :-------------------------------: | :-------------------: |
|    1     | integer |    是    |            指开盘时间             |     1584717910000     |
|    2     | integer |    是    |             成交笔数              |         5000          |
|    3     | string  |    是    |             开盘价格              |       "3997.3"        |
|    4     | string  |    是    |             收盘价格              |       "3998.7"        |
|    5     | string  |    是    |              最高价               |       "4031.9"        |
|    6     | string  |    是    |              最低价               |       "3982.5"        |
|    7     | string  |    是    | 为wei为单位的base token的成交数量 | “500000000000000000”  |
|    8     | string  |    是    | 为wei为单位 quote token的成交数量 | "2617521141385000000" |

### 
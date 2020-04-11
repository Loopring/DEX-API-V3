# Candlestick更新

订阅此主题以接收特定交易对Candlestick更新的通知。


## 订阅规则

- 主题名称：`candlestick`
- 订阅该主题是否需要提供ApiKey：否


## 参数列表

| 参数名| 必现 |                描述                 |
| :---- | :---| :--------------------------------- |
| market | 是|交易对（支持的交易对可以通过api接口[api/v2/exchange/markets](../dex_apis/getMarkets.md)获取）| 
| interval | 是|时间间隔|

#### 时间间隔

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
| 104106 | 主题或参数非法|

## 推送示例

```json
{
    "topic": {
        "topic": "candlestick",
        "interval": "2hr"
    },
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

#### 推送消息数据结构

| 字段  |             类型              | 必现 |       说明       |    
| :--- | :--------------------------- | :------ | :-------------- | 
| topic |       JSON        |    是    | 主题和参数 |  
|  ts   |            integer            |    是    | 推送时间（毫秒） |      
| data  | [List\[string]](#candlestick) （`Candlestick`列表）|    是    | cCandlestick数组 |      

####<span id= "candlestick">Candlestick数组</span>

| 序号  |  类型   | 必现 |               说明                |        
| :------ | :----- | :------ | :------------------------------- | 
|    1     | integer |    是    |            指开盘时间             |     
|    2     | integer |    是    |             成交笔数              |         
|    3     | string  |    是    |             开盘价格              |      
|    4     | string  |    是    |             收盘价格              |       
|    5     | string  |    是    |              最高价               |       
|    6     | string  |    是    |              最低价               |      
|    7     | string  |    是    | 为wei为单位的Base Token的成交数量 | 
|    8     | string  |    是    | 为wei为单位 Quote Token的成交数量 | 

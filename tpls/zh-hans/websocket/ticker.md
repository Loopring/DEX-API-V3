# Ticker更新


订阅此主题以接收特定交易对ticker更新的通知。


## 订阅规则

- 主题名称：`ticker`
- 订阅该主题是否需要提供ApiKey：否


## 参数列表

| 参数名| 必现|              描述                 |
| :---- | :--- |:--------------------------------- |
| market | 是 | 交易对（支持的交易对可以通过api接口[api/v2/exchange/markets](../dex_apis/getMarkets.md)获取）|



## 状态码

| 状态码 |                 描述                 |
| :---- | :---------------------------------- |
| 104111 | 主题或参数非法|

## 推送示例

```json
{
    "topic": {
        "topic": "ticker",
        "market": "LRC-ETH"
    },
    "ts": 1584717910000,
    "data": [
        "LRC-ETH",  //market
        "1584717910000",  //timestamp
        "5000000",  //size
        "1000",  //volume
        "0.0002",  //open
        "0.00025",  //high
        "0.0002",  //low
        "0.00025",  //close       
        "5000",  //count    
        "0.00026",  //bid
        "0.00027"  //ask
    ]
}
```

## 模型

#### 推送消息数据结构

|  字段   |          类型           | 必现 |       说明       |    
| :----- | :--------------------- | :------ | :-------------- | 
| topic |       JSON        |    是    | 主题和参数 |  
| ts |         integer         |    是    |     推送时间（毫秒）     |  
|  data   | [List[string]](#ticker) |    是    |     Ticker数组          |

#### <span id="ticker">Ticker数组</span>

| 序号  |  类型   | 必现 |         说明         |    
| :------ | :----- | :------ | :------------------ | 
|    1     | string  |    是    |         交易对         | 
|    2     | integer |    是    |    Ticker生成时间    | 
|    3     | string  |    是    |  Base Token的成交量  |  
|    4     | string  |    是    | Quote Token 的成交量 |    
|    5     | string  |    是    |        开盘价        |  
|    6     | string  |    是    |        最高价        |  
|    7     | string  |    是    |        最低价        | 
|    8     | string  |    是    |      最新成交价      |  
|    9     | integer |    是    |       成交笔数       |    
|    10    | string  |    是    |      买单最高价      |  
|    11    | string  |    是    |      卖单最低价      |   

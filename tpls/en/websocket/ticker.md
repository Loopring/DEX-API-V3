# 订阅Ticker更新

通过订阅该主题，您可以获得特定交易对ticker更新的数据推送。


## 订阅规则

- `topic`需要指定交易对。如果交易对是`LRC-ETH`，那么`topic`应该拼写为：`ticker&LRC-ETH`。
- 订阅该主题不需要提供ApiKey。
- 支持的交易对可以通过api接口[api/v2/exchange/markets](../dex_apis/getMarkets.md)获取。

## 状态码

| 状态码 |                 描述                 |
| :---- | :---------------------------------- |
| 104111 | `topic`的值或其参数非法|

## 推送示例

```json
{
    "topic": "ticker&LRC-ETH",
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

#### 推送数据结构

|  字段   |          类型           | 必现 |       说明       |       举例       |
| :----- | :--------------------- | :------ | :-------------- | :-------------- |
|  topic  |         string          |    是    | 订阅的主题和条件 | "ticker&LRC-ETH" |
| integer |         integer         |    是    |     推送时间     |  1584717910000   |
|  data   | [List[string]](#ticker)  （Ticker）|    是    |     深度信息     |        /         |

#### <span id="ticker">Ticker数据结构</span>

| 序号  |  类型   | 必现 |         说明         |     举例      |
| :------ | :----- | :------ | :------------------ | :----------- |
|    1     | string  |    是    |         交易对         |   "LRC-ETH"   |
|    2     | integer |    是    |    ticker生成时间    | 1584717910000 |
|    3     | string  |    是    |  base token的成交量  |   "5000000"   |
|    4     | string  |    是    | quote token 的成交量 |    "1000"     |
|    5     | string  |    是    |        开盘价        |   "0.0002"    |
|    6     | string  |    是    |        最高价        |   0.00025"    |
|    7     | string  |    是    |        最低价        |   "0.0002"    |
|    8     | string  |    是    |      最新成交价      |   "0.00025"   |
|    9     | integer |    是    |       成交笔数       |     5000      |
|    10    | string  |    是    |      买单最高价      |   "0.00026"   |
|    11    | string  |    是    |      卖单最低价      |   "0.00027"   |

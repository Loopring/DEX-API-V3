### WebSocket 概述

#### 接入URL

[wss://api.loopring.io/v2/ws](wss://api.loopring.io/v2/ws)

#### 心跳消息

当用户连接到光锥中继的WebSocket之后，中继会进行心跳检测，每30s会发送“ping”信息，期待接收客户端的“pong”信息。2分钟未收到回复会自动断开连接。

#### 订阅规则

用户在与光锥中继建立WebSocket连接之后，可以订阅消息。需满足以下规则：

1. 用户可以一次订阅或者取消订阅多个主题，如果订阅的多个主题中有需要ApiKey的，则必须包含ApiKey。
1. 用户可以重复订阅相同的主题，最新的订阅条件会覆盖之前的订阅条件。
1. 用户在一次订阅中，不允许订阅相同的主题
1. 用户在取消订阅需要ApiKey的主题时，必须包含订阅该主题时所使用的ApiKey。

#### 模型

##### 订阅结构

|  字段  |     类型     | 是否必现 |               说明               |                 举例                 |
| :----: | :----------: | :------: | :------------------------------: | :----------------------------------: |
|   op   |    string    |    是    |         订阅或者取消订阅         |                "sub"                 |
| apiKey |    string    |    否    | 订阅要求传ApiKey的主题才是必须的 | “16M2hKHw9b5VuP21YBAJQmCd3VhuNtdDqG” |
|  args  | list<string> |    是    |         订阅的主题及条件         | [ "depth&LRC-ETH&0","trade&LRC-ETH"] |

##### 订阅示例

订阅示例

```json
{
  "op": "sub",
  "args": [
    "candlestick&LRC-BTC&1Hour",
    "depth&LRC-BTC&1",
    "depth10&LRC-BTC&1",
    "trade&LRC-BTC",
    "ticker&LRC-BTC"
  ]
}
```

取消订阅示例

```json
{
  "op": "unSub",
  "args": [
    "candlestick",
    "depth",
    "depth10",
    "trade",
    "ticker"
  ]
}
```

##### 订阅响应结构

|  字段  |     类型     | 是否必现 |               说明               |                 举例                 |
| :----: | :----------: | :------: | :------------------------------: | :----------------------------------: |
|   op   |    string    |    是    |         用户传送来的操作         |                "sub"                 |
| apiKey |    string    |    否    | 订阅要求传ApiKey的主题才是必须的 | “16M2hKHw9b5VuP21YBAJQmCd3VhuNtdDqG” |
|  args  | list<string> |    是    |         订阅的主题及条件         | [ "depth&LRC-ETH&0","trade&LRC-ETH"] |
| result |    [Result](#result)   |    是    |             订阅结果             |                  /                   |

##### 订阅返回示例

订阅成功示例

```json
{
  "op": "sub",
  "apiKey": "",
  "args": [
    "candlestick&LRC-ETH&1hr",
    "depth&LRC-ETH&1",
    "trade&LRC-ETH",
    "ticker&LRC-ETH"
  ],
  "result": {
    "status": "ok"
  }
}
```

订阅条件不合法的失败示例

```json
{
  "op": "sub",
  "apiKey": "",
  "args": [
    "candlestick&LRC-ETH"
  ],
  "result": {
    "status": "failed",
      "error": {
      "code": 104106,
      "message": "receive illegal arg for candlestick:lrc-eth"
    }
  }
}
```

订阅条件无法解析的失败示例

```json
{
  "op": "",
  "apiKey": "",
  "args": [],
  "result": {
    "status": "failed",
    "error": {
      "code": 104115,
      "message": "unexpected msg:xxx"
    }
  }
}
```

#####  <span id="result">Result </span>

|  字段  |      类型       | 是否必现 |         说明         | 举例 |
| :----: | :-------------: | :------: | :------------------: | :--: |
| status |     string      |    是    |     订阅是否成功     | "OK" |
| error  | [Error](#error) |    否    | 订阅失败时的错误信息 |  /   |

##### <span id="error">Error </span>

|  字段   |  类型   | 是否必现 |   说明   |     举例     |
| :-----: | :-----: | :------: | :------: | :----------: |
|  code   | integer |    是    |  错误码  |    107500    |
| message | string  |    是    | 错误信息 | 空的订阅信息 |

#### 公共错误码信息

| **返回码** |                         描述                         |
| :--------: | :--------------------------------------------------: |
|   104100   |                     空的订阅信息                     |
|   104101   | 不支持的操作（光锥中继服务器仅支持sub 和 unsub操作） |
|   104102   |                     不支持的主题                     |
|   104103   |                    重复的订阅主题                    |
|   104104   |                    缺少ApiKey信息                    |
|   104105   |              与之前订阅使用的ApiKey不符              |
|   104112   |                    不合法的ApiKey                    |
|   104113   |               取消订阅未曾订阅过的主题               |
|   104114   |             无法通过APiKey找到对应的用户             |
|   104115   |                  无法识别的订阅消息                  |

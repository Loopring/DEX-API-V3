# WebSocket API

## 接入URL

```
mainnet: wss://ws.api3.loopring.io/v3/ws

testnet(goerli): wss://ws.uat2.loopring.io/v3/ws
```

## 订阅要求
在订阅websocket之前，需要先拿到wsApiKey，然后用该wsApiKey进行连接，步骤如下：
1. 访问REST API"/v3/ws/key"得到返回的`{"key":"fx2xW5hoVFbcaanWS"}`
2. 将`fx2xW5hoVFbcaanWS`拼接到url地址进行websocket连接, 即连接wss://ws.uat3.loopring.io/v3/ws?wsApiKey=fx2xW5hoVFbcaanWS.

## 订阅
客户端可以通过发送JSON数据订阅多个主题：

```JSON
{
  "op": "sub",
  "sequence": 10000,
  "apiKey": ".....",
  "unsubscribeAll": true,
  "topics": [
    {
      "topic": "account"
    },
    {
      "topic": "order",
      "market": "LRC-ETH"
    },
    {
      "topic": "order",
      "market": "LRC-USDT"
    },
    {
      "topic": "orderbook",
      "market": "LRC-ETH",
      "level": 0
    },
    {
      "topic": "orderbook",
      "market": "LRC-USDT",
      "level": 0,
      "count": 20,
      "snapshot": true
    },
    {
      "topic": "ammpool",
      "poolAddress": "0x18920d6E6Fb7EbE057a4DD9260D6D95845c95036",
      "snapshot": true
    }
  ]
}
```


1. 在一次订阅中，如果`topics`中任何一个主题需要ApiKey，那么本次操作就必须包含ApiKey。
1. 在一次订阅中，相同的主题可以出现多次，但同一个主题的相同的配置只可以出现一次。
1. 在一次订阅中，如果有任何参数错误，则全部订阅都会失败。
1. 如果`unsubscribeAll`是`true`，订阅前会先退订之前订阅的所有主题。
1. 订阅时客户端可以指定一个`sequence`代表序列号，后台返回结果也会附带同样的序列号。
1. 最多可以订阅20个主题

## 退订
客户端可以通过发送JSON数据退订多个主题：

```JSON
 {
    "op":"unSub",
    "sequence": 10000,
    "apiKey": ".....",
    "unsubscribeAll": false,
    "topics": [
        {
            "topic": "account",
        },
        {
            "topic": "order",
            "market": "LRC-ETH"
        },
        {
            "topic": "order",
            "market": "LRC-USDT"
        },
        {
            "topic": "orderbook",
            "unsubscribeAll":true
        }
    ]
  },
```


1. 在一次退订中，如果`topics`中任何一个主题需要ApiKey，那么本次操作就必须包含ApiKey。
1. 在一次退订中，相同的主题可以出现多次，但同一个主题的相同的配置只可以出现一次。
1. 在一次退订中，如果有任何参数错误，则全部订阅都会失败。
1. 如果`unsubscribeAll`是`true`，所有主题都会被退订；如果在某个主题内将`unsubscribeAll`设置为`true`，那么该主题的所有配置都会被退订。
1. 退订时客户端可以指定一个`sequence`代表序列号，后台返回结果也会附带同样的序列号。

#### 心跳

WebSocket链接建立后，中继会每30秒会发送“ping”消息给客户端做心跳检测。如果客户端在最近2分钟内都没有任何“pong”消息，中继会断开WebSocket链接。如果客户端的“pong”消息数量超过服务端发送的“ping”消息数量，中继也会断开WebSocket链接。


## 返回值

|  字段  |     类型     | 必现 |               说明               |
| :---- | :---------- | :------ | :------------------------------ |
|   op   |    string    |    是    |         订阅（"sub"）或退订（unSub"）         |
|   sequence   |    integer    |    否    |        操作序列号        |
| topics |   JSON  |    是    |             订阅主题和参数            |
| result |    [Result](#result)   |    是    |             订阅结果             |


####  <span id="result">Result结构</span>

|  字段  |      类型       | 必现 |         说明         |
| :---- | :------------- | :------ | :------------------ |
| status |     string      |    是    |     订阅是否成功     |
| error  | [Error](#error) |    否    | 订阅失败时的错误信息 |

####   <span id="error">Error结构</span>

|  字段   |  类型   | 必现 |   说明   |
| :----- | :----- | :------ | :------ |
|  code   | integer |    是    |  状态码  |
| message | string  |    是    | 错误信息 |

#### 状态码

| **状态码** |                         描述                         |
| :-------- | :-------------------------------------------------- |
|   104100   |                     空的订阅信息                     |
|   104101   | 不支持的操作（路印中继服务器仅支持sub 和 unsub操作） |
|   104102   |                     不支持的主题                     |
|   104103   |                    重复的订阅主题                    |
|   104104   |                    缺少ApiKey信息                    |
|   104105   |              与之前订阅使用的ApiKey不符              |
|   104112   |                    不合法的ApiKey                    |
|   104113   |               退订未曾订阅过的主题               |
|   104114   |             无法通过APiKey找到对应的用户             |
|   104115   |                  无法识别的订阅消息                  |
| 104116 | 订阅的主题超过上限 |

#### 示例

订阅成功示例：

```json
{
  "op": "sub",
  "sequence": 10000,
  "topics": [
    {
      "topic": "orderbook",
      "market": "LRC-ETH",
      "level": 0
    }
  ],
  "result": {
    "status": "ok"
  }
}
```

订阅参数不合法的失败示例：

```json
{
  "op": "sub",
  "sequence": 10000,
  "topics": [
    {
      "topic": "candlestick",
      "market": "LRC-ETH",
      "count": 10
    }
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

订阅参数无法解析的失败示例：

```json
{
    "op": "sub",
    "topics":[],
    "result": {
        "status": "failed",
        "error": {
            "code": 104115,
            "message": "unexpected msg:xxx"
        }
    }
}
```

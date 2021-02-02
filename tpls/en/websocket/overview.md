# WebSocket API

## Base URL

```
mainnet: wss://ws.api3.loopring.io/v3/ws

testnet(goerli): wss://ws.uat3.loopring.io/v3/ws
```

## Before Subscription
Before subscription, user needs to get a connect key, otherwise, websocket connection will be refused. The full connection steps are listed below:
1. Get wsApiKey by access REST path "/v3/ws/key", and you will get response like `{"key":"fx2xW5hoVFbcaanWS"}`
2. Use `fx2xW5hoVFbcaanWS` as a wsApiKey param in ws path, i.e., wss://ws.uat3.loopring.io/v3/ws?wsApiKey=fx2xW5hoVFbcaanWS.

## Subscription
Clients can send JSON to subscribe to multiple topics:

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
    }
  ]
}
```


1. In one subscription request, if at least one topic requires the ApiKey, then the `apiKey` filed is required;
2. In one subscription request, the same topic configuration can only occur once;
3. In one subscription request, if there are any configuration errors, the entire subscription request fails;
4. If `unsubscribeAll` is `true`, all previous subscriptions will be cancelled;
5. If `sequence` is provided, the relayer will use the same sequence number in its response.


## Unsubscription
Clients can send JSON to unsubscribe from multiple topics:

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


1. In one unsubscription request, if at least one topic requires the ApiKey, then the `apiKey` filed is required;
1. In one unsubscription request, the same topic configuration can only occur once;
1. In one unsubscription request, if there are any configuration errors, the entire unsubscription request fails;
1. If the top-level `unsubscribeAll` is `true`, all previous subscriptions will be cancelled; if the per-topic `unsubscribeAll` is `true`, then all subscriptions to that topic will be cancelled;
1. If `sequence` is provided, the relayer will use the same sequence number in its response.
1. Subscribe up to 20 topics in total.

#### Heartbeat

After a WebSocket connection is established, the relay will send a "ping" message to the client for heartbeat detection every 30 seconds. If the client does not reply with a "pong" message within 2 minutes, the relay will disconnect. If the number of "pong" messages exceeds the number of "ping" messages, the relay will also disconnect.


## Response

|  Field  |     Type     | Required |               Note               |
| :---- | :---------- | :------ | :------------------------------ |
|   op   |    string    |    Y    |         "sub" or "unSub"         |
|   sequence   |    integer    |    N    |        A client-side sequence number        |
| topics |   JSON  |    Y    |             Topics and their configurations            |
| result |    [Result](#result)   |    Y    |             Subscription result             |


####  <span id="result">Result</span>

|  Field  |      Type       | Required |         Note         |
| :---- | :------------- | :------ | :------------------ |
| status |     string      |    Y    |     Status code     |
| error  | [Error](#error) |    N    | Error |

####   <span id="error">Error</span>

|  Field   |  Type   | Required |   Note   |
| :----- | :----- | :------ | :------ |
|  code   | integer |    Y    |  Value  |
| message | string  |    Y    | Error message |

#### Status code

| **Value** |                         Note                        |
| :-------- | :-------------------------------------------------- |
|   104100   |                     Topic missing                     |
|   104101   | Invalid op code |
|   104102   |                     Invalid topic                    |
|   104103   |                    Duplicate topic configs                    |
|   104104   |                    Missing ApiKey                    |
|   104105   |              ApiKey mismatched              |
|   104112   |                    Invalid ApiKey                    |
|   104113   |               Subscription not found              |
|   104114   |             Invalid ApiKey (user not found)                |
|   104115   |                  Invalid topic config                |
| 104116 | exceed maximum subscriptions |

#### Examples

A successful subscription：

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

A failed subscription：

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

Another failed subscription：

```json
{
    "op": "sub",
    "topics": [],
    "result": {
        "status": "failed",
        "error": {
            "code": 104115,
            "message": "unexpected msg:xxx"
        }
    }
}
```

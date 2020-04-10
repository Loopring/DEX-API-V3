# Orderbook Notification

Subscribe to this topic to receive notifications about orderbook updates for specific trading pairs.

## Rules

- Topic name: `orderbook`
- ApiKey requred: No


## Parameters

|  Parameter |  Required |             Note                |
| :---- | :------ |:--------------------------------- |
| market | Y | [Trading pair](../dex_apis/getMarkets.md)|
| level | Y | Price aggregation level |
| count | Y | Number of bids/ask price slots, count can not be larger than 50, and only take effect when snapshot is true. |
| snapshot |N | Default to false. If true, the client will receive full notification with up to `count` bid/ask price slots when at least one slot has update. |

## Status code

| Value |                Note                |
| :---- | :--------------------------------- |
| 104107 | Invalid topic or parameters|

## Notification example

```json
{
    "topic": {
        "topic:": "orderbook",
        "market": "LRC-USDT",
        "count": 20,
        "snapshot": true
    },
    "ts": 1584717910000,
    "startVersion": 1212121,
    "endVersion": "1212123",
    "data": {
        "bids": [
            [
                "295.97",  //price
                "456781000000000",  //size
                "3015000000000",  //volume
                "4"  //count
            ]
        ],
        "asks": [
            [
              "298.97",
              "456781000000000000",
              "301500000000000",
              "2"
            ]
        ]
    }
}
```

## Data Model

#### Notification

|     Field     |      Type       | Required |         Note         |
| :---------- | :------------- | :------ | :------------------ |
| topic |       JSON        |    Y    | Topic and parameters |
|      ts      |     integer     |    Y    |       Notification timestamp (milliseconds)       |
| startVersion |     integer     |    Y    | Previous version number |
|  endVersion  |     integer     |    Y    | Updated versionnumber |
|     data     | [OrderBook](#orderbook) |    Y    |       The orderbook       |

####<span id="orderbook">OrderBook</span>

| Field | Type                           | Required | Note     |
| :---- | :------------------------------ | :-------- | :-------- |
| bids | List\[List\[string\]] | Y       | [PriceSlot](#slot) array for bids |
| asks | List\[List\[string\]]| Y       | [PriceSlot](#slot) array for asks  |

#### <span id = "slot">PriceSlot</span>

| Index  | Type   | Required | Note           |
| :------ | :------ | :-------- | :-------------- | :|
|    1     | string | Y       | Price           |
|    2     | string | Y       | Amount (quantity of base token)         |
|    3     | string | Y       | Total (quantity of quote token)    |
|    4     | string | Y       | Number of orders at this price |


Note that amount and total are the curent values, not the delta between the current and the previous values.

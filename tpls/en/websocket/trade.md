# Trade Notification

Subscribe to this topic to receive notifications about bew trades for specific trading pairs.

## Rules

- Topic name: `trade`
- ApiKey requred: No


## Parameters

|  Parameter |   Required |             Note                |
| :---- | :---|:--------------------------------- |
| market |  Y |[Trading pair](../dex_apis/getMarkets.md)|


## Status code

| Value |                Note                |
| :---- | :--------------------------------- |
| 104109 | Invalid topic or parameters|

## Notification example

```json
{
    "topic": {
        "topic": "trade",
        "market": "LRC-ETH"
    },
    "ts": 1584717910000,
    "data": [
        [
            "1584717910000",  //timestamp
            "123456789",  //tradeId
            "buy",  //side
            "500000",  //size 
            "0.0008",  //price
            "100"  //fee
        ]
    ]
}
```

## Data Model

#### Notification

|  Field   |          Type           | Required |       Note       |    
| :----- | :--------------------- | :------ | :-------------- |
| topic |       JSON        |    Y    | Topic and parameters |  
| ts |         integer         |    Y    |     Notification timestamp (milliseconds)     | 
|  data   | [List[List\[string]](#trade)] |    Y    |    Trade array list     |  

#### <span id="trade">Trade</span>

| Index  |  Type   | Required |         Note         |  
| :------ | :----- | :------ | :------------------ | 
|    1     | integer |    Y    |       Trade timestamp       | 
|    2     | integer |    Y    |       Fill sequence number      |   
|    3     | string  |    Y    |  Taker's side (buy or sell)   |    
|    4     | string  |    Y    | Filled amount of base token |  
|    5     | string  |    Y    |       Fill price       |   
|    6     | string  |    Y    |   Fee paid in base token   |    


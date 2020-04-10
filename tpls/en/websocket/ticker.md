# Ticker Notification


Subscribe to this topic to receive notifications about ticker updates for specific trading pairs.

## Rules

- Topic name: `ticker`
- ApiKey requred: No


## Parameters

|  Parameter |  Required |              Note                |
| :---- | :--- |:--------------------------------- |
| market | Y | [Trading pair](../dex_apis/getMarkets.md)|



## Status code

| Value |                 Note                |
| :---- | :---------------------------------- |
| 104111 | Invalid topic or parameters|

## Notification example

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

## Data Model

#### Notification

|  Field   |          Type           | Required |       Note       |    
| :----- | :--------------------- | :------ | :-------------- | 
| topic |       JSON        |    Y    | Topic and parameters |  
| ts |         integer         |    Y    |     Notification timestamp (milliseconds)     |  
|  data   | [List[string]](#ticker) |    Y    |     Ticker array        |

#### <span id="ticker">Ticker</span>

| Index  |  Type   | Required |         Note         |    
| :------ | :----- | :------ | :------------------ | 
|    1     | string  |    Y    |         Trading pair         | 
|    2     | integer |    Y    |    Ticker update timestamp    | 
|    3     | string  |    Y    |  Amount (quantity of base token)  |  
|    4     | string  |    Y    | Total (quantity of quote token) |    
|    5     | string  |    Y    |        Open price        |  
|    6     | string  |    Y    |        Highest price        |  
|    7     | string  |    Y    |        Lowest price        | 
|    8     | string  |    Y    |      Latest price      |  
|    9     | integer |    Y    |       Number of trades       |    
|    10    | string  |    Y    |      Highest bid price      |  
|    11    | string  |    Y    |      Lowest ask price      |   

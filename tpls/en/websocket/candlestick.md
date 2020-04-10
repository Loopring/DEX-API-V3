# Candlestick Notification

Subscribe to this topic to receive notifications about candlestick updates for specific trading pairs.



## Rules

- Topic name: `candlestick`
- ApiKey requred: No


## Parameters

|  Parameter | Required |                Note                |
| :---- | :---| :--------------------------------- |
| market |  Y |[Trading pair](../dex_apis/getMarkets.md)| 
| interval |  Y |Time interval|

#### Time intervals

| Value  |  Note  |
| :--- | :---- |
| 1min  | 1 minute  |
| 5min  | 5 minutes  |
| 15min | 15 minutes |
| 30min | 30 minutes |
|  1hr  | 1 hour  |
|  2hr  | 2 hours  |
|  4hr  | 4 hours |
| 12hr  | 12 hours |
|  1d   |  1 day   |
|  1w   |  1 week   |



## Status code

| Value |                   Note                   |
| :---- | :--------------------------------------- |
| 104106 | Invalid topic or parameters|

## Notification example

```json
{
    "topic": {
        "topic": "candlestick",
        "interval": "2hr"
    },
    "ts":1584717910000,
    "data": [
        "1584717910000",  //open timestamp (ms)
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

## Data Model

#### Notification

| Field  |             Type              | Required |       Note       |    
| :--- | :--------------------------- | :------ | :-------------- | 
| topic |       JSON        |    Y    | Topic and parameters |  
|  ts   |            integer            |    Y    | Notification timestamp (milliseconds) |      
| data  | List\[string]|    Y    | [`Candlestick` array](#candlestick) |      

####<span id= "candlestick">Candlestick</span>

| Index  |  Type   | Required |               Note                |        
| :------ | :----- | :------ | :------------------------------- | 
|    1     | integer |    Y    |            Open timestamp             |     
|    2     | integer |    Y    |             Nubmer of trades              |         
|    3     | string  |    Y    |             Open price              |      
|    4     | string  |    Y    |             Close price              |       
|    5     | string  |    Y    |              Highest price               |       
|    6     | string  |    Y    |              Lowest price               |      
|    7     | string  |    Y    | Traded amount of Base Tokens (in Wei)| 
|    8     | string  |    Y    | Traded amount of quote Tokens (in Wei) | 

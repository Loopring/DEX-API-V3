# Ticker Notification


Subscribe to this topic to receive notifications about ticker updates for specific trading pairs.

## Rules

- Topic name: `ammpool`
- ApiKey requred: No


## Parameters

|  Parameter |  Required |              Note                |
| :---- | :--- |:--------------------------------- |
| poolAddress | Y | [Trading pair](../dex_apis/getAmmPools.md)|



## Status code

| Value |                 Note                |
| :---- | :---------------------------------- |
| 102034 | receive illegal arg for topic ammpool|

## Notification example

```json
{
  "topic" : {
    "topic" : "ammpool",
    "poolAddress" : "0x18920d6E6Fb7EbE057a4DD9260D6D95845c95036",
    "snapshot" : true
  },
  "ts" : 1611267558234,
  "data" : [ [ "11792920485390000000000000", "3998385574130000000000" ], "41277091829000" ]

}
```

## Data Model

#### Notification

|  Field   |          Type           | Required |       Note       |    
| :----- | :--------------------- | :------ | :-------------- | 
| topic |       JSON        |    Y    | Topic and parameters |  
| ts |         integer         |    Y    |     Notification timestamp (milliseconds)     |  
|  data   | [[string, string], string] |    Y    |     Amm snapshot array        |

#### <span id="snapshot">PoolSnapshot</span>

| Index  |  Type   | Required |         Note         |    
| :------ | :----- | :------ | :------------------ | 
|    1     | [string, string]  |    Y    |         Token balance of in pool token pair, i.e. [base token amount, quote token amount]        | 
|    2     | string |    Y    |   Token balance of pool's LP token    | 

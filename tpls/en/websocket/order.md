# Order Notification


Subscribe to this topic to receive notifications about order updates for specific trading pairs.

## Rules

- Topic name: `order`
ApiKey requred: Yes


## Parameters

|  Parameter |   Required |              Note                |
| :---- | :--- | :--------------------------------- |
| market | Y | [Trading pair](../dex_apis/getMarkets.md)|

## Status code

| Value |                Note                |
| :---- | :--------------------------------- |
| 104110 | Invalid topic or parameters|

## Notification example

```json
{
   "topic": {
        "topic": "order",
        "market": "LRC-ETH"
   },
   "ts":1565844328,
   "data": {
        "hash": "11212",
        "clientOrderId": "myOrder",
        "size": "500000000",
        "volume": "210000000",
        "price": "0.000004",
        "filledSize": "30000000",
        "filledVolume": "100000",
        "filledFee": "1000000",
        "status": "processing",
        "createdAt": "1494900087",
        "validSince": "1494900087",
        "validUntil": "1495900087",
        "side": "buy",
        "market": "LRC-ETH"
    }
}
```

## Data Model

#### Notification

| Field  |      Type       | Required |       Note       |     
| :--- | :------------- | :------ | :-------------- | 
| topic |       JSON        |    Y    | Topic and parameters |  
|  ts   |     integer     |    Y    |     Notification timestamp (milliseconds)     |  
| data  | [Order](#order) |    Y    |     The order     |    

#### <span id="order">Order</span>

|     Field      |  Type   | Required |            Note            |    
| :----------- | :----- | :------ | :------------------------ | 
|     hash      | string  |    Y    |          Order hash         |    
| clientOrderId | string  |    Y    |        Client defined order ID        |  
|     size      | string  |    Y    |    Amount (quantity of base token)      | 
|    volume     | string  |    Y    |    Total (quantity of quote token)     | 
|     price     | string  |    Y    |          Order price          |  
|  filledSize   | string  |    Y    | Filled amount of base token  |  
| filledVolume  | string  |    Y    | Filled amount of quote token |   
|   filledFee   | string  |    Y    |      Fees paid      | 
|    status     | string  |    Y    |          Order status         | 
|   createdAt   | integer |    Y    |        Order creation timestamp      | 
|   updateAt    | integer |    Y    |   Order last update timestamp   | 
|     side      | string  |    Y    |           Buy or sell           |    
|    market     | string  |    Y    |            Trading pair           |  

#### Order status

|    Value   |                    Note                    |
| :-------- | :---------------------------------------- |
| processing | Active (aka Open, may be partially filled) |
| processed  |                Fully filled                |
| cancelling |                   Being cancelled                   |
| cancelled  |                 Cancelled                  |
|  expired   |                  Expired                  |
|  waiting   |                Pending active                |

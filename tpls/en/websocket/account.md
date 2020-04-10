# Account Notification

Subscribe to this topic to receive notifications about user balance update.


## Rules

- Topic name: `account`
ApiKey requred: Yes



## Parameters

This topic doesn't support any parameter.


## Notification example

```json
{
    "topic": {
        "topic:": "account"
    },
	"ts":1584717910000,
	"data": {
	    "accountId":1,
	    "totalAmount": "24439253519655",
	    "tokenId": 2,
	    "amountLocked": "0"
	}
}
```

## Data Model

#### Notification

| Field  |        Type         | Required |       Note       |     
| :--- | :----------------- | :------ | :-------------- | 
| topic |       JSON        |    Y    | Topic and parameters |  
|  ts   |       integer       |    Y    |     Notification timestamp (milliseconds)     | 
| data  | [Balance](#balance) |    Y    |     User's new balances   |     

#### <span id= "balance">Balance</span> 

|     Field     |  Type   | Required |    Note    |     
| :---------- | :----- | :------ | :-------- | 
|  accountId   | integer |    Y    |   Account ID   |     
|   tokenId    | integer |    Y    |   Token ID   |     
| totalAmount  | string  |    Y    |  Total token balance  | 
| amountLocked | string  |    Y    | Token balance locked by orders |    


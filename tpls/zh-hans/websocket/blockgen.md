# Block Generation Notification

Subscribe to this topic to receive notifications about Loopring L2 block


## Rules

- Topic name: `blockgen`
ApiKey requred: No



## Parameters

This topic doesn't support any parameter. Subscription & response sample are as below:

Sub:
```json
{
  "op": "sub",
  "sequence": 30006,
  "unsubscribeAll": false,
  "topics": [
    {
      "topic": "blockgen"
    }
  ]
}
```
Response:
```json
{
  "op" : "sub",
  "sequence" : 30006,
  "topics" : [ {
    "topic" : "blockgen"
  } ],
  "result" : {
    "status" : "OK"
  }
}
```

## Notification example

```json
{
    "topic": {
        "topic:": "blockgen"
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
| data  | \[[BlockResp](../dex_apis/getBlock.md)\] |    Y    |     Block generation messages, a list of BlockResp, refer to getBlock API for data format |

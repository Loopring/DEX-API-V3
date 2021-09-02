# Block Generation Notification

Subscribe to this topic to receive notifications about Loopring L2 block


## Rules

- Topic name: `blockgen`
ApiKey requred: No



## Parameters

This topic has an optional flag: `verbose`, which indicates the response has more info about the blocks or just the block id. Once the user gets the block id notification, he can also call getBlock REST API to get the details.

|  Parameter |  Required |              Note                |
| :---- | :--- |:--------------------------------- |
| verbose | N | Default is false, so only block Id returns |


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
    [
      {"blockid": 1},
      {"blockid": 2},
    ]
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

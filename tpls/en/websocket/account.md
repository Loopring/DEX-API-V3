# Account Notification

Subscribe to this topic to receive notifications about user balance update.


## Rules

- Topic name: `account`
ApiKey requred: Yes

## Parameters

This topic has an optional flag: `v3`, which indicates the response is for v3 which has also include NFT info. if the flag is false or absent, the response is just like before.

|  Parameter |  Required |              Note                |
| :---- | :--- |:--------------------------------- |
| accountId | N | not required as apiKey also link to an account |
| v3 | N | If it's a v3 sub which contains NFT info, default is false for compatible with previous sub topic |


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

If v3 is `true`:

| Field  |        Type         | Required |       Note       |
| :--- | :----------------- | :------ | :-------------- |
| topic |       JSON        |    Y    | Topic and parameters |
|  ts   |       integer       |    Y    |     Notification timestamp (milliseconds)     |
| data  | [BalanceV3](#balanceV3) |    Y    |     User's new balances (NFT info included)  |

Otherwise:

| Field  |        Type         | Required |       Note       |
| :--- | :----------------- | :------ | :-------------- |
| topic |       JSON        |    Y    | Topic and parameters |
|  ts   |       integer       |    Y    |     Notification timestamp (milliseconds)     |
| data  | [Balance](#balance) |    Y    |     User's new balances   |

#### <span id= "balanceV3">BalanceV3</span> 

|     Field     |  Type   | Required |    Note    |
| :---------- | :----- | :------ | :-------- |
|  accountId   | integer |    Y    |   Account ID   |
|   tokenId    | integer |    Y    |   Token ID   |
| total  | string  |    Y    |  Total token balance  |
| locked | string  |    Y    | Token balance locked by orders |
| nftId  | string  |    N    |  NFT ID if it's NFT token  |
| nftData | string  |    N    | NFT hash data if it's NFT token |
| tokenAddress  | string  |    N    |  Nft token address if it's NFT token  |

#### <span id= "balance">Balance</span> 

|     Field     |  Type   | Required |    Note    |
| :---------- | :----- | :------ | :-------- |
|  accountId   | integer |    Y    |   Account ID   |
|   tokenId    | integer |    Y    |   Token ID   |
| totalAmount  | string  |    Y    |  Total token balance  |
| amountLocked | string  |    Y    | Token balance locked by orders |

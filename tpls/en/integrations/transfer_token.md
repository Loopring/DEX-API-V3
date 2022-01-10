## Transfer token



### 1 get fee

GET api: api/v3/user/offchainFee

transfer: requestType is 3

`````
header: 
X-API-KEY = bEef7a3Nzk7lgaHm85E0O1JO5ufu0iQ96p3bCmrsZz8TLGG83jTpPDYwcjUC0vlF

request:
https://uat2.loopring.io/api/v3/user/offchainFee?accountId=11329&requestType=3&tokenSymbol=0x0000000000000000000000000000000000000000&amount=2000000000000

response:
{
	"gasPrice": "2194508101",
	"fees": [{
		"token": "ETH",
		"fee": "1920000000000",
		"discount": 1
	}, {
		"token": "LRC",
		"fee": "4770000000000000",
		"discount": 0.8
	}, {
		"token": "USDT",
		"fee": "2190",
		"discount": 0.8
	}, {
		"token": "DAI",
		"fee": "2730000000000000",
		"discount": 1
	}]
}
`````



### 2 get storageID

GET api: api/v3/storageId

`````
header: 
X-API-KEY = bEef7a3Nzk7lgaHm85E0O1JO5ufu0iQ96p3bCmrsZz8TLGG83jTpPDYwcjUC0vlF

request:
https://uat2.loopring.io/api/v3/storageId?accountId=11329&sellTokenId=0

response:
{
	"orderId": 0,
	"offchainId": 1
}
`````



### 3 submit transfer

POST api: api/v3/transfer

storageId: the response in get storageID

maxFee: the response in get fee

payeeId: set to 0 is ok



````
https://uat2.loopring.io/api/v3/transfer

header: 
X-API-KEY = bEef7a3Nzk7lgaHm85E0O1JO5ufu0iQ96p3bCmrsZz8TLGG83jTpPDYwcjUC0vlF
X-API-SIG = 0xf4f902bffcdc2e640efe8f86ef970b65bea4ad1312e8ab33b200852d87a0fd881a584e201b52d768f333eb39b084ccde42dfe110fb683b81319837c6e92fa2691c03

request:
{
	"ecdsaHash": "0xa8023b3765fc5aa05ef578645f9ec45d9208427ff34a57d40257d7c4403fe39c",
	"ecdsaSignature": "0xf4f902bffcdc2e640efe8f86ef970b65bea4ad1312e8ab33b200852d87a0fd881a584e201b52d768f333eb39b084ccde42dfe110fb683b81319837c6e92fa2691c03",
	"eddsaHash": "0x099301b1acb2634f1ea3f15e14ab078a054a1dee69c60b2f60ce7350eccd217b",
	"eddsaSignature": "0x200659c0a16e58e1fe5be034fd7e8f79e819c1464037f7b75c1e58b565e26f021bc97487c02411fbde4b320d06ea270c1b0fdf92e53a503ace5602939e6a786502b3c28766cfdedf7420a698fda48aa9899d5a518b15d3ff912d2a89942ecd07",
	"exchange": "0x2e76EBd1c7c0C8e7c2B875b6d505a260C525d25e",
	"maxFee": {
		"volume": "1920000000000",
		"tokenId": 0
	},
	"memo": "",
	"payeeAddr": "0x8656920c85342d646E5286Cb841F90209272ABec",
	"payeeId": 0,
	"payerAddr": "0x8656920c85342d646E5286Cb841F90209272ABeb",
	"payerId": 11329,
	"storageId": 1,
	"token": {
		"volume": "2000000000000",
		"tokenId": 0
	},
	"validUntil": 1644929199
}

response:
{
	"hash": "0x099301b1acb2634f1ea3f15e14ab078a054a1dee69c60b2f60ce7350eccd217b",
	"status": "processing",
	"isIdempotent": false
}
````





You can also refer to the JS SDK: https://github.com/Loopring/loopring_sdk/blob/master/src/tests/transfer.test.ts#L110


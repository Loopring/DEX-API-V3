## Transfer pay payee updateAccount fee



Payer can pay some token to payee for the first updateAccount fee when transfer, include erc20 transfer and nft transfer.

Set payPayeeUpdateAccount as true in erc20 transfer and nft transfer can pay payee updateAccount fee.



### 1 Check whether can pay payee updateAccount fee

Get the payee account info via [api/v3/account](https://docs-uat.loopring.io/en/dex_apis/getAccount.html), if response is account not found, or nonce is 0 and tags not contains "FirstUpdateAccountPaid", payer can pay the updateAccountFee 



below are some examples that payer can pay the updateAccount fee for payee

### 1.1 Account not found

````
https://uat2.loopring.io//api/v3/account?owner=0x60d2D76ed6E07a9F46EEe7d444257148E08B7bbb

respone:
{"resultInfo":{"code":101002,"message":"account not found"}}
````



### 1.2 Account nonce is 0 and tags not contains FirstUpdateAccountPaid

```
https://uat2.loopring.io//api/v3/account?owner=0x1111111111111111111111111111111111111111

respone:
{
	"accountId": 10500,
	"owner": "0x1111111111111111111111111111111111111111",
	"frozen": false,
	"publicKey": {
		"x": "",
		"y": ""
	},
	"tags": "",
	"nonce": 0,
	"keyNonce": 0,
	"keySeed": ""
}
```





## 2 ERC20 transfer

### 2.1 Get fee

[GET api: api/v3/user/offchainFee](https://docs-uat.loopring.io/en/dex_apis/getBusinessFee2.html)

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



### 2.2 get storageID

[GET api: api/v3/storageId](https://docs-uat.loopring.io/en/dex_apis/getNextStorageId.html)

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



### 2.3 submit transfer

[POST api: api/v3/transfer](https://docs-uat.loopring.io/en/dex_apis/submitTransfer.html)

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
	"ecdsaSignature": "0x09975137d489dcc8616b90b3ba4ea81b8f2eb6d93324255f38f077bee11b568960997054b31ac6b33f4609ebed72fa85808b8928ce6be42aa98d83da938859ad1c03",
	"eddsaSignature": "0x14e9d6ba841634810ef8c893446eae514ef0e7443ec2db9ca6d4347eb82f586c196d9dabb3f72afb2ff1e8580ce35e6674dbcc42ed40cd908846e8aef009b75b0577e7a9c0e107ad3dfa4bd180b720a19be6e56fe64206624a531d16ea909b90",
	"exchange": "0x2e76EBd1c7c0C8e7c2B875b6d505a260C525d25e",
	"hashApproved": "0x1876c9f920fa78a91a56755d845c33964111d6f932767cf71f47efd87ef176a8",
	"maxFee": {
		"volume": "2190",
		"tokenId": 2
	},
	"memo": "",
	"payPayeeUpdateAccount": true,
	"payeeAddr": "0xbb6924b24ba5c6ece81f056cf54e5d720846c188",
	"payeeId": 0,
	"payerAddr": "0x53f879debad6d97371bfd45875a2ec689d6af798",
	"payerId": 11554,
	"storageId": 17,
	"token": {
		"volume": "1000000",
		"tokenId": 2
	},
	"validUntil": 1646747756
}

response:
{
	"hash": "0x099301b1acb2634f1ea3f15e14ab078a054a1dee69c60b2f60ce7350eccd217b",
	"status": "processing",
	"isIdempotent": false
}
````





## 3 NFT transfer

### 3.1 Get fee

[GET api: api/v3/user/nft/offchainFee](https://docs-uat.loopring.io/en/dex_apis/getNftRequestFees.html)

transfer: requestType is 19

`````
header: 
X-API-KEY = bEef7a3Nzk7lgaHm85E0O1JO5ufu0iQ96p3bCmrsZz8TLGG83jTpPDYwcjUC0vlF

request:
https://uat2.loopring.io/api/v3/user/nft/offchainFee?accountId=11329&requestType=19&tokenSymbol=0x0000000000000000000000000000000000000000&amount=2000000000000

response:
{
	"gasPrice": "1500000007",
	"fees": [{
		"token": "ETH",
		"fee": "25100000000000",
		"discount": 1
	}, {
		"token": "LRC",
		"fee": "146800000000000000",
		"discount": 1
	}, {
		"token": "USDT",
		"fee": "105300",
		"discount": 1
	}, {
		"token": "DAI",
		"fee": "105300000000000000",
		"discount": 1
	}]
}
`````



### 3.2 get storageID

[GET api: api/v3/storageId](https://docs-uat.loopring.io/en/dex_apis/getNextStorageId.html)

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



### 3.3 submit nft transfer

[POST api: api/v3/nft/transfer](https://docs-uat.loopring.io/en/dex_apis/submitNftTransfer.html)



````
request:
{
      exchange: '0x2e76EBd1c7c0C8e7c2B875b6d505a260C525d25e',
      fromAccountId: 11120,
      fromAddress: '0x25B51D4c01c974f8f725be5c8ca5ccF5537f3e85',
      toAccountId: 0,
      toAddress: '0x35405E1349658BcA12810d0f879Bf6c5d89B512C',
      token: {
        tokenId: 32773,
        nftData: '0x012b2fe4dd01019bbe456379ca4c0c174064f7fa321d42ef9373cd58dda92fbc',
        amount: '1'
      },
      maxFee: { tokenId: 0, amount: '25100000000000' },
      storageId: 17,
      validUntil: 1667396982,
      payPayeeUpdateAccount: true
}

response:
{
      hash: '0x1df910bc73f2e90d71fdcd8fc1301c70184c62d866cb2e56871db6d16af838f9',
      raw_data: {
        hash: '0x1df910bc73f2e90d71fdcd8fc1301c70184c62d866cb2e56871db6d16af838f9',
        status: 'processing',
        isIdempotent: false
      }
}
````


# Loopring Layer2 OpenAccount

Describe how to setup a new account in loopring layer2.



## 1 Create the AccountId

There are two way:

1 Depoist some token from Layer1

​	you can visit https://loopring.io/#/trade/lite/LRC-ETH to deposit, relayer monitor the deposit event in ethereum, then will open an account for the address

2 send some token to the address in Layer2, relayer would open an account for this address if receives some token



## 2 Get the AccountId

GET API: [/api/v3/account](https://docs-uat.loopring.io/en/dex_apis/getAccount.html)

````
request:
https://uat2.loopring.io/api/v3/account?owner=0x8656920c85342d646E5286Cb841F90209272ABeb

response:
{
	"accountId": 11329,
	"owner": "0x8656920c85342d646E5286Cb841F90209272ABeb",
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
````



## 3 Get updateaccount fee

GET api: [api/v3/user/offchainFee](https://docs-uat.loopring.io/en/dex_apis/getBusinessFee2.html)

requestType: 2 is update account type

```
https://uat2.loopring.io/api/v3/user/offchainFee?accountId=11329&requestType=2&tokenSymbol=0x0000000000000000000000000000000000000000&amount=2000000000000

{
	"gasPrice": "1500000007",
	"fees": [{
		"token": "ETH",
		"fee": "26400000000000",
		"discount": 1
	}, {
		"token": "LRC",
		"fee": "118900000000000000",
		"discount": 0.8
	}, {
		"token": "USDT",
		"fee": "89300",
		"discount": 0.8
	}, {
		"token": "DAI",
		"fee": "111700000000000000",
		"discount": 1
	}]
}
```



## 4 Update Account

POST api:  [/api/v3/account](https://docs-uat.loopring.io/en/dex_apis/submitUpdateAccount.html)

exchange: the exchangeAddress in https://docs-uat.loopring.io/en/dex_apis/getExchangeInfo.html

maxFee: the return of 'Get fee'



`````
header: 
X-API-SIG = 0x05b49f99ac6d8f67d4519dfaf9b545dbc775dcc837441f85ef9aae74c83e5c2d700729cdba1d7a9cc818abb43a598cf1e4eeca547e4e6697ff18c4d2ac111ac21b03

request:
{
	"accountId": 11329,
	"ecdsaSignature": "0x05b49f99ac6d8f67d4519dfaf9b545dbc775dcc837441f85ef9aae74c83e5c2d700729cdba1d7a9cc818abb43a598cf1e4eeca547e4e6697ff18c4d2ac111ac21b03",
	"exchange": "0x2e76EBd1c7c0C8e7c2B875b6d505a260C525d25e",
	"maxFee": {
		"volume": "24000000000000",
		"tokenId": 0
	},
	"nonce": 0,
	"owner": "0x8656920c85342d646E5286Cb841F90209272ABeb",
	"publicKey": {
		"x": "0x20ba7bd404f259c3d49853d6a849425a983c24fc3c01be177f719e84ba776a8c",
		"y": "0x266d7e40dba375c90816287814f20b8e187227a6d05f17d2d329fefac9b782af"
	},
	"validUntil": 1899273791
}

response:
{
	"hash": "0x1d01dd0f4d7846a90235331798f4457829e72d8a4ed8d9393dd29c4859481e7b",
	"status": "processing",
	"isIdempotent": false
}
`````

you can also refer to js sdk:  https://github.com/Loopring/loopring_sdk/blob/master/src/tests/user.test.ts#L219



## 5 Get the apiKey

GET api: [api/v3/apiKey](https://docs-uat.loopring.io/en/dex_apis/getApiKey.html)

X-API-SIG: it's eddsa sig of https://docs-uat.loopring.io/en/basics/signing.html, you can refer to js sdk: https://github.com/Loopring/loopring_sdk/blob/master/src/api/sign/exchange.js#L28



````
header:
X-API-SIG = 0x0564af7928171c2a4c59185b3c869fae42e1e588dac11b5fcbe2d07d4e4bb854093852d8e7bfee8cb318e09d934530b144ea03394a1d4a53e28f261bed2478d605de27aee34f3f68d6e3c637c709f9c338446f04987bd5f94899397fc641e742

request:
https://uat2.loopring.io/api/v3/apiKey?accountId=11329&publicKeyY=0x266d7e40dba375c90816287814f20b8e187227a6d05f17d2d329fefac9b782af&publicKeyX=0x20ba7bd404f259c3d49853d6a849425a983c24fc3c01be177f719e84ba776a8c

response:
{
	"apiKey": "bEef7a3Nzk7lgaHm85E0O1JO5ufu0iQ96p3bCmrsZz8TLGG83jTpPDYwcjUC0vlF"
}
````

Then you can use apiKey and eddsaKey to transfer or submit an order

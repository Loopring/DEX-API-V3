### NFT on Loopring Layer2

### Introducing Counterfactual NFT

Loopring announced NFT support in our latest protocol release (v3.6.2). Since then, our NFT support has got even better: NFT contracts do not need to be deployed on Ethereum before NFT can be minted, transferred, and traded on Loopring. We call this new type of NFT the *Counterfactual NFT*.

#### How is it implemented? 

First, we use `CREATE2` to calculate the counterfactual NFT’s smart contract address that can be deployed on Ethereum later. All we need are:

- A counterfactual NFT factory (`factory` ) that will deploy the actual NFT contract for us when necessary. Deploying a new NFT contract is nothing but creating a new proxy instance that delegates all logic to a concrete counterfactual NFT implementation.
- The NFT contract’s owner address (`owner` ). The owner is also the only minter on Loopring layer2 to mint new NFTs under this contract.

Now the counterfactual NFT’s address can be calculated as follows (code is available in [ our GitHub repo](https://github.com/Loopring/protocols/blob/release_loopring_3.6.3/packages/counterfactual_nft/contracts/NFTFactory.sol)):

```
Create2Upgradeable.computeAddress(               
 keccak256(abi.encodePacked(NFT_CONTRACT_CREATION, owner, baseURI)),
 keccak256(CloneFactory.getByteCode(implementation))
);
```

Loopring only supports our own *NFTFactory* implementation. On Ethereum mainnet, our official *NFTFactory* address is `0xc852aC7aAe4b0f0a0Deb9e8A391ebA2047d80026`(the old one is `0xDB42E6F6cB2A2eFcF4c638cb7A61AdE5beD82609`); on Goerli testnet, the address is `0x25315F9878BA07221db684b7ad3676502E914894`(the old one is `0x40F2C1770E11c5bbA3A26aEeF89616D209705C5D`). Third-party counterfactual NFT factories will be supported shortly.

#### Compute NFT Address API

You can compute counterfactual NFT addresses by interacting with the factory smart contract. We also provide an API for convenience.

**Endpoint**: `/api/v3/nft/info/computeTokenAddress` 
**Parameters**: 

1. *nftFactory*: the official NFT factory address.
2. *nftOwner*: the owner of the NFT contract who can mint on layer1 and layer2.
3. *nftBaseUri*: this is to support another feature in the future, but currently not supported.

An example: [https://uat2.loopring.io/api/v3/nft/info/computeTokenAddress?nftFactory=0x40F2C1770E11c5bbA3A26aEeF89616D209705C5D&nftOwner=0xE20cF871f1646d8651ee9dC95AAB1d93160b3467](https://uat2.loopring.io/api/v3/nft/info/computeTokenAddress?nftFactory=0x40F2C1770E11c5bbA3A26aEeF89616D209705C5D&nftOwner=0xE20cF871f1646d8651ee9dC95AAB1d93160b3467&nftBaseUri) returns:

```
{
  tokenAddress: "0xee354d81778a4c5a08fd9dbeb5cfd01a840a746d"
}
```

#### When to deploy counterfactual NFT contracts?

If all the NFTs under a counterfactual NFT contract ever stay on layer2, the contract will never need to be deployed. But layer1 deployment is necessary for the following transactions to be successful: 

- An NFT is to be withdrawn to layer1.
- The owner wants to mint on layer1.

Deploying counterfactual NFT contracts is permissionless. The idea is someone to perform the first above transactions will have to deploy the contract at his/her own cost. It’s possible to interact with our factory contracts directly to deploy counterfactual NFT contracts. Loopring also provides an API so people can request us to deploy counterfactual NFT contracts on their behalf, but layer2 fees will apply.

#### Deployment API

To check if an NFT contract has been deployed, use [*getCode*](https://uat2.loopring.io/api/v3/delegator/getCode) API as follows:

```
curl 
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"address": "$my_countefactual_nft_address"}' \
  https://uat2.loopring.io/api/v3/delegator/getCode
```

For an NFT contract that has been deployed, it will return something like the following (with non-empty `result`):

```
{
"id":95,
"jsonrpc":"2.0",
"result":"0x363d3d373d3d3d363d732df3ce66d930959afb2ef01486e3dada00a865095af43d82803e903d91602b57fd5bf3"
}
```

Otherwise, the result string will be “0x”. Then you can deploy the contract using this API: /api/v3/nft/deployTokenAddress



### Layer2 NFT Transactions

#### Minting NFTs

(you can refer to js sdk https://github.com/Loopring/loopring_sdk/blob/master/src/tests/mintNFT.test.ts)

You can use the [POST /api/v3/nft/mint](https://docs-uat.loopring.io/en/dex_apis/submitMintNft.html) API to transfer NFTs on layer2. 

##### 1 compute nft tokenAddress 

Params：

​	nftFactory: deployed in ethereum, uat can use 0x40F2C1770E11c5bbA3A26aEeF89616D209705C5D

​	nftOwner: should be the same as minter

​	nftBaseUri: the uri, should be empty now

Api: /api/v3/nft/info/computeTokenAddress

Returns：nft tokenAddress

```
Request:
https://uat2.loopring.io/api/v3/nft/info/computeTokenAddress?nftFactory=0x40F2C1770E11c5bbA3A26aEeF89616D209705C5D&nftOwner=0xE20cF871f1646d8651ee9dC95AAB1d93160b3467&nftBaseUri

Respone:
{"tokenAddress":"0xee354d81778a4c5a08fd9dbeb5cfd01a840a746d"}
```

you can refer to js sdk to compute local: https://github.com/Loopring/loopring_sdk/blob/master/src/tests/nft.test.ts#L188



##### 2 get fee<a name="get_fee"></a>

Api: [/api/v3/user/nft/offchainFee](https://docs-uat.loopring.io/en/dex_apis/getNftRequestFees.html) , fee type: ['9:NFT_MINT', '10:NFT_WITHDRAWAL', '11:NFT_TRANSFER', '13:NFT_DEPLOY']

Returns: fee tokens and amount

```
{
	"gasPrice": "1500000007",
	"fees": [{
			"token": "ETH",
			"fee": "217000000000000",
			"discount": 1
		},
		{
			"token": "LRC",
			"fee": "1537000000000000000",
			"discount": 1
		},
		{
			"token": "USDT",
			"fee": "1013000",
			"discount": 1
		},
		{
			"token": "DAI",
			"fee": "1013000000000000000",
			"discount": 1
		}
	]
}
```



##### 3 mint

````
https://uat2.loopring.io/api/v3/nft/mint

params:
{
      exchange: '0x2e76EBd1c7c0C8e7c2B875b6d505a260C525d25e',
      minterId: 11265,
      minterAddress: '0x466E892Ee9319EA50a19ec1E76CB550ecb196D1A',
      toAccountId: 11265,
      toAddress: '0x466E892Ee9319EA50a19ec1E76CB550ecb196D1A',
      nftType: 0,
      tokenAddress: '0x62d3c4168217083d54850bfcf84943941f6fcc65',
      nftId: '0x0000000000000000000000000000000000000000000000000000000000000152',
      amount: '500',
      validUntil: 1700000000,
      creatorFeeBips: 0,
      storageId: 83,
      maxFee: { tokenId: 0, amount: '666000000000000' },
      forceToMint: false,
      counterFactualNftInfo: {
        nftFactory: '0x40F2C1770E11c5bbA3A26aEeF89616D209705C5D',
        nftOwner: '0x466E892Ee9319EA50a19ec1E76CB550ecb196D1A',
        nftBaseUri: ''
      }
}
    
   
Response:
{
      hash: '0x1c1921a88d799bbda630b25145946b4e11eaf0a7409cc50c7e6c1be27b58776f',
      raw_data: {
        hash: '0x1c1921a88d799bbda630b25145946b4e11eaf0a7409cc50c7e6c1be27b58776f',
        nftTokenId: 32801,
        nftData: '0x032bdcf7fb0b1383ab4eea0f8317640b51f601a9c2697095f7d01f702c2fc07f',
        status: 'processing',
        isIdempotent: false
      },
}
````



To learn more about each parameter, check out our API documents at https://docs.loopring.io (production) or https://doc-uat.loopring.io (UAT).

Note that:

1. `nftType` shall always be `0` which represents ERC1155. Our relayer currently does not support ERC721 mint.

2. `nftId` is an `uint256` value converted from an IPFS hash. In our counterfactual NFT implementation, we expect each NFT to have its very own IPFS directory which contains at least a `metadata.json` file. The IPFS hash is the hash of the NFT’s directory on IPFS. In our example, nftID `82074012285391930765279489314136667830573876033924668146917021887792317657586` corresponds to IPFS hash `QmaYyJx2RTHY7aGLSNX7xEzSYeh8SHU2eLNcVB1XXgzuv9` , so this NFT’s metadata URI is: `*ipfs://QmaYyJx2RTHY7aGLSNX7xEzSYeh8SHU2eLNcVB1XXgzuv9/metadata.json*`*.* Please reference the code in [IPFS.sol](https://github.com/Loopring/protocols/blob/5644b2386d0ce2310ce4d8fd1f060b1289a08ebd/packages/counterfactual_nft/contracts/external/IPFS.sol#L13) to learn more about how NFT IDs are converted into IPFS hashes.

3. `hash` is layer2 hash

4. `nftData` is a layer2 concept and it uniquely represents an NFT on Loopring layer2. 




#### NFT Deploy

Use layer2 token to pay and relayer deploy the NFT tokenAddress to ethereum

Note: need check tokenAddress depolyed or not before deploy

##### 1 getAvailableBroker 

`````
https://uat2.loopring.io/api/v3/getAvailableBroker

respone:
{
	"broker": "0x8737f59Cc3a96B56E94bC743b23108C30FC2624D"
}
`````



##### 2 get deploy fee

Api: /api/v3/user/nft/offchainFee , fee type: ['9:NFT_MINT', '10:NFT_WITHDRAWAL', '11:NFT_TRANSFER', '13:NFT_DEPLOY']

Returns: fee tokens and amount

`````
request:
https://uat2.loopring.io/api/v3/user/nft/offchainFee?accountId=11120&requestType=13&tokenAddress=0x25B51D4c01c974f8f725be5c8ca5ccF5537f3e85

response:
{
	"gasPrice": "2213247487",
	"fees": [{
		"token": "ETH",
		"fee": "221000000000000",
		"discount": 1
	}, {
		"token": "LRC",
		"fee": "688000000000000000",
		"discount": 1
	}, {
		"token": "USDT",
		"fee": "315000",
		"discount": 1
	}, {
		"token": "DAI",
		"fee": "315000000000000000",
		"discount": 1
	}]
}
`````



##### 3 deploy tokenAddress

header need add X-API-SIG, which is eddsa sig of the request sign : https://docs-uat.loopring.io/en/basics/signing.html

the `transfer` is the same as transfer erc20 token

​	transfer.payeeAddr:  the return of getAvailableBroker

​	transfer.payeeId: use 0

​	transfer.maxFee：maxFee.tokenId use the same as token.tokenId

​	transfer.token: choose one of the return of offchainFee 

`````
/api/v3/nft/deployTokenAddress

request:
{
	"nftData": "0x122b75340c47604d61161fc1aa925c319ad5869bdef8e81180d70bc05b4cc01a",
	"tokenAddress": "0x62d3c4168217083d54850bfcf84943941f6fcc65",
	"transfer": {
		"payeeAddr": "0x8737f59Cc3a96B56E94bC743b23108C30FC2624D",
		"payerId": 11265,
		"memo": "",
		"maxFee": {
			"volume": "0",
			"tokenId": 0
		},
		"token": {
			"volume": "221000000000000",
			"tokenId": 0
		},
		"ecdsaSignature": "0x5cf3c3282ccdaa3ba73bf89a819cf58e67e96097cfcafa2e43207364fc4ea1ed73c866d4cebd62dea7470c343f7608ded715c8f5cb5896ca1af87af9bd28f3b31b03",
		"payerAddr": "0x466E892Ee9319EA50a19ec1E76CB550ecb196D1A",
		"eddsaSignature": "0x17851f7029979012bd302f6080f9a54b270c01f9d872eb7a5a01ebcfb090632614f0eaef1597b3cc4c736ba2c6041390cd127354b32149347dd9cba17a0d9cf100db52a928a4abe9370d55af2b37887c34ca6c7f905b69b893c2ef15b3fdb291",
		"validUntil": 1644819840,
		"exchange": "0x2e76EBd1c7c0C8e7c2B875b6d505a260C525d25e",
		"ecdsaHash": "0xf462b42243e1c19a4a6320690fe944565e69b3ecc57d07fdf64c491381c11ae0",
		"eddsaHash": "0x2fe958503353751fef2f5cd602aab714d91f51128599c88d2d4cd3767e75594e",
		"payeeId": 0,
		"storageId": 5
	}
}

response:
{
	"hash": "0x269bd5ba5806e3b155107cd6062082c6c010d8701200aac0a052b287e391da8e",
	"status": "SEND_TX_SUCCESS",
	"isIdempotent": false
}
`````



##### 4 check deploy status

check the hash status in Layer1.
or you can check tokenAddress deployed or not by api/v3/delegator/getCode, can check every 15s until success.

Then you can withdraw after tokenAddress deployed



#### NFT Transfers

(you  can refer to js sdk: https://github.com/Loopring/loopring_sdk/blob/master/src/tests/transferNFT.test.ts)

You can use the [POST /api/v3/nft/transfer](https://docs-uat.loopring.io/en/dex_apis/submitNftTransfer.html) API to transfer NFTs on layer2. Lets see a request example:

`````
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
      maxFee: { tokenId: 0, amount: '2600000000000000' },
      storageId: 17,
      validUntil: 1667396982
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
`````



#### NFT Withdrawal

(you can refer to js sdk https://github.com/Loopring/loopring_sdk/blob/master/src/tests/withdrawNFT.test.ts)

You can use the [POST /api/v3/nft/withdrawal](https://docs-uat.loopring.io/en/dex_apis/submitOffChainNftWithdrawal.html) to withdraw NFTs from layer2 to layer2. Lets see a request example:

`````
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
      maxFee: { tokenId: 0, amount: '2600000000000000' },
      storageId: 17,
      validUntil: 1667396982
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
`````



#### NFT Orders and Trades

\> TODO
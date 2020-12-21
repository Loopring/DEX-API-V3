# Request Signing

The Loopring API involves two different categories of signatures. One is the common **API request signature**, which is used to verify that the API invocations have been authenticated; the other is Loopring Protocol's **off-chain request signature**, which is used by Loopring to verify that off-chain requests have been authenticated. We will explain each of these two categories separately.

## Special API Request Signatures

{% include "./generic_api_signature.md" %}

## Off-chain Request Signatures

Loopring 3.6 supports support lots of off-chain requests: **orders**, **order cancellation**, **swap**, **join AMM pool**, **exit AMM pool** , **transfer** and **off-chain withdrawals**, etc. Since these off-chain requests will result in modifications to the exchange's state Merkel tree, when you submit these types of requests using Loopring's API, sometimes you must provide **EXTRA** special signatures required by the Loopring protocol.

### Overview of signatures and requests

Below is a signature type table for all those requests, each request asks for different signature methods due to different business models.

| Request Type           | eddsaSignature | ecdsaSignature | approvedHash | X-API-SIG |
| -----------            | ----------- | ----------- | -----------   | -----------         |
| submitOrder(AMM swap)  | Y           | N           | N             | N                   |
| cancelOrder            | N           | N           | N             | Special API Request EDDSA Signatures    |
| updateApiKey           | N           | N           | N             | Special API Request EDDSA Signatures    |
| joinAmmPool            | Y           | Disabled    | Y             | N                   |
| exitAmmPool            | Y           | Disabled    | Y             | N                   |
| submitTransfer         | Y           | Disabled    | Y             | EIP712 signature of request structure |
| submitOffchainWithdraw | Y           | Disabled    | Y             | EIP712 signature of request structure |
| updateAccount          | Y           | Y           | Y             | EIP712 signature of request structure |

    * `eddsaSignature`, `ecdsaSignature`, `approvedHash` are located in REST request body.
    * `X-API-SIG` is located in REST request header.
    *`Y` means support.
    *`N` means not support.
    *'Disabled' means no longer support.

We **STRONGLY** suggest using Level-2 EDDSA key to sign every requests, which saves both time & money of both user and Loopring as no Eth mainnet transaction and the corresponding block confirmation. For more details, please refer to [Key Management](./key_mgmt.md).

Below we take signing order and signing transfer/withdrawal as examples, as you will see, the first one order signing needs merely Level-2 EDDSA signature, but the later two need extra EIP712 signature in request header, you can see the difference on the way of submitting the requests.

#### Signing Orders

You need to seralized specific fields of an order into an integer array, then calculate the Poseidon hash of the array, and then sign the hash with your EdDSA private key.


{% hint style='info' %}
The rules for serialization of orders, hashing, and signature methods must strictly follow [Loopring's Specification](https://github.com/Loopring/protocols/blob/master/packages/loopring_v3/DESIGN.md).
{% endhint %}

Below we use Python code as a demo:
```python
class EddsaSignHelper:
    def __init__(self, poseidon_params, private_key):
        self.poseidon_sign_param = poseidon_params
        self.private_key = private_key
        # print(f"self.private_key = {self.private_key}")

    def hash(self, structure_data):
        serialized_data = self.serialize_data(structure_data)
        msgHash = poseidon(serialized_data, self.poseidon_sign_param)
        return msgHash

    def sign(self, structure_data):
        msgHash = self.hash(structure_data)
        signedMessage = PoseidonEdDSA.sign(msgHash, FQ(int(self.private_key, 16)))
        return "0x" + "".join([
                        hex(int(signedMessage.sig.R.x))[2:].zfill(64),
                        hex(int(signedMessage.sig.R.y))[2:].zfill(64),
                        hex(int(signedMessage.sig.s))[2:].zfill(64)
                    ])

class OrderEddsaSignHelper(EddsaSignHelper):
    def __init__(self, private_key):
        super(OrderEddsaSignHelper, self).__init__(
            poseidon_params(SNARK_SCALAR_FIELD, 12, 6, 53, b'poseidon', 5, security_target=128),
            private_key
        )
    
    def serialize_data(self, order):
        return [
            int(order["exchange"], 16),
            int(order["storageId"]),
            int(order["accountId"]),
            int(order["sellToken"]['tokenId']),
            int(order["buyToken"]['tokenId']),
            int(order["sellToken"]['volume']),
            int(order["buyToken"]['volume']),
            int(order["validUntil"]),
            int(order["maxFeeBips"]),
            int(order["fillAmountBOrS"]),
            int(order.get("taker", "0x0"), 16)
        ]
```
{% hint style='info' %}
If you don't use the *ethsnarks* library to calculate Poseidon hash, please pay attention to the values of the Poseidon parameters to ensure that they are entirely consistent with those used by Loopring. Otherwise, signature verification will fail.
{% endhint %}


#### Signing Off-chain Withdrawals

Following structure shows a offchain withdrawal request:
```python
    {
        "exchange": "0x35990C74eB567B3bbEfD2Aa480467b1031b23eD9",
        "accountId": 5,
        "owner": "0x23a51c5f860527f971d0587d130c64536256040d",
        "token": {
            "tokenId": 0,
            "volume": str(1000000000000000000),
        },
        "maxFee" : {
            "tokenId": 0,
            "volume": str(1000000000000000),
        },
        "to": "0xc0ff3f78529ab90f765406f7234ce0f2b1ed69ee",
        "onChainDataHash": "0x" + bytes.hex(onchainDataHash),
        "storageId": 5,
        "validUntil" : 0xfffffff,
        "minGas": 300000,
        "extraData": bytes.hex(extraData)
    }
```

The code for signing it in Python is as follows. Just like the order, the only difference is the request itself, so we just adjust params which calculate the poseidon hash.

```python
class WithdrawalEddsaSignHelper(EddsaSignHelper):
    def __init__(self, private_key):
        super(WithdrawalEddsaSignHelper, self).__init__(
            poseidon_params(SNARK_SCALAR_FIELD, 10, 6, 53, b'poseidon', 5, security_target=128),
            private_key
        )

    def serialize_data(self, withdraw):
        return [
            int(withdraw['exchange'], 16),
            int(withdraw['accountId']),
            int(withdraw['token']['tokenId']),
            int(withdraw['token']['volume']),
            int(withdraw['maxFee']['tokenId']),
            int(withdraw['maxFee']['volume']),
            int(withdraw['onChainDataHash'], 16),
            int(withdraw['validUntil']),
            int(withdraw['storageId']),
        ]
```

#### Signing Internal Transfer

You need to seralized specific fields of an transfer into an integer array, then calculate the Poseidon hash of the array, and then sign the hash with your EdDSA private key.

The following is an example of internal transfers:

```python
    {
        "exchange": "0x35990C74eB567B3bbEfD2Aa480467b1031b23eD9",
        "payerId": 0,
        "payerAddr": "0x611db73454c27e07281d2317aa088f9918321415",
        "payeeId": 0,
        "payeeAddr": "0xc0ff3f78529ab90f765406f7234ce0f2b1ed69ee",
        "token": {
            "tokenId": 0,
            "volume": str(1000000000000000000),
        },
        "maxFee" : {
            "tokenId": 0,
            "volume": str(1000000000000000),
        },
        "storageId": 1,
        "validUntil": 0xfffffff
    }
```

where `storageId` must start from 1 and increment by 2.

The code for signing it in Python is as follows:

```python
class OriginTransferEddsaSignHelper(EddsaSignHelper):
    def __init__(self, private_key):
        super(OriginTransferEddsaSignHelper, self).__init__(
            poseidon_params(SNARK_SCALAR_FIELD, 13, 6, 53, b'poseidon', 5, security_target=128),
            private_key
        )

    def serialize_data(self, originTransfer):
        return [
            int(originTransfer['exchange'], 16),
            int(originTransfer['payerId']),
            int(originTransfer['payeeId']), # payer_toAccountID
            int(originTransfer['token']['tokenId']),
            int(originTransfer['token']['volume']),
            int(originTransfer['maxFee']['tokenId']),
            int(originTransfer['maxFee']['volume']),
            int(originTransfer['payeeAddr'], 16), # payer_to
            0, #int(originTransfer.get('dualAuthKeyX', '0'),16),
            0, #int(originTransfer.get('dualAuthKeyY', '0'),16),
            int(originTransfer['validUntil']),
            int(originTransfer['storageId'])
        ]
```

## Extra ECDSA authentic in header 

{% include "./ecdsa_authentic.md" %}

## References

You can learn more about the Poseidon hash and EdDSA signature through the following literature and github repositories.

1. **ethsnarks**: https://github.com/HarryR/ethsnarks.git
2. **SHA256 Hash**: <https://en.wikipedia.org/wiki/SHA-2>
3. **EdDSA**: <https://en.wikipedia.org/wiki/EdDSA>
4. **Poseidon Hash**: <https://www.poseidon-hash.info/>


You can also refer to our [example code](./examples.md) for more details.

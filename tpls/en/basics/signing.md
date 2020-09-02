# Request Signing

The Loopring API involves two different categories of signatures. One is the common **API request signature**, which is used to verify that the API invocations have been authenticated; the other is Loopring Protocol's **off-chain request signature**, which is used by Loopring to verify that off-chain requests have been authenticated. We will explain each of these two categories separately.

## Common API Request Signatures

{% include "./generic_api_signature.md" %}

## Off-chain Request Signatures

Loopring 3.1.1 supports two types of off-chain requests: **orders** and **off-chain withdrawals**. Since these two off-chain requests will result in modifications to the exchange's state Merkel tree, when you submit these two types of requests using Loopring's API, you must provide special signatures required by the Loopring protocol.

{% hint style='info' %}
Loopring 3.1.1 also supports a third type of off-chain requests: **order cancellation**, but it will be deprecated in the up-coming 3.5 version. Therefore, Loopring Exchange will not support this type of off-chain requests.
{% endhint %}

The off-chain request signature includes the following steps:

1. Regularize the request `r` (JSON) to generate a string` s`.
1. Calculate the **Poseidon** hash of `s` as `h`(see the following section).
1. Sign `h` with the account's EdDSA private key` privateKey` and get three values: `Rx`,` Ry`, and `S` (see the following section).
1. Convert `h`,` Rx`, `Ry`, and` S` into strings and merge them into `r` (please note the name change).

```json
{
    ...,
    "hash": ...,
    "signatureRx": "16367919966553849834214288740952929086694704883595501207054796240908626703398",
    "signatureRy": "5706650945525714138019517276433581394702490352313697178959212750249847059862",
    "signatureS": "410675649229327911665390972834008845981102813589085982164606483611508480748"
}
```

#### Signing Orders

You need to seralized specific fields of an order into an integer array, then calculate the Poseidon hash of the array, and then sign the hash with your EdDSA private key.


{% hint style='info' %}
The rules for serialization of orders, hashing, and signature methods must strictly follow [Loopring's Specification](https://github.com/Loopring/protocols/blob/master/packages/loopring_v3/DESIGN.md).
{% endhint %}

Below we use Python code as a demo:

```python
def sign_int_array(privateKey, serialized, t):
    PoseidonHashParams = poseidon_params(
        SNARK_SCALAR_FIELD,
        t,
        6,
        53,
        b'poseidon',
        5,
        security_target=128
    )
    
    hash = poseidon(serialized, PoseidonHashParams)
    signedMessage = PoseidonEdDSA.sign(hash, FQ(int(privateKey)))
    return ({
        "hash": str(hash),
        "signatureRx": str(signedMessage.sig.R.x),
        "signatureRy": str(signedMessage.sig.R.y),
        "signatureS": str(signedMessage.sig.s),
    })

def serialize_order(order):
    return [
        int(order["exchangeId"]),
        int(order["orderId"]),
        int(order["accountId"]),
        int(order["tokenSId"]),
        int(order["tokenBId"]),
        int(order["amountS"]),
        int(order["amountB"]),
        int(order["allOrNone"]=="true"),
        int(order["validSince"]),
        int(order["validUntil"]),
        int(order["maxFeeBips"]),
        int(order["buy"]=="true"),
        int(order["label"])
    ]

def sign_order(privateKey, order):
	serialized = serialize_order(order)
	signed = sign_int_array(serialized, 14 /* Pay attention to this t value */)
    order.update(signed)
```
{% hint style='info' %}
If you don't use the *ethsnarks* library to calculate Poseidon hash, please pay attention to the values of the Poseidon parameters to ensure that they are entirely consistent with those used by Loopring. Otherwise, signature verification will fail.
{% endhint %}



#### Signing Off-chain Withdrawals
{% hint style='danger' %}
The current Loopring API does not yet support off-chain withdrawal requests. But we will add it soon.
{% endhint %}

The following is an example of off-chain withdrawals:
```json
{
    "exchangeId": 2,
    "accountId":100,
    "tokenId": 0,
    "amount": 1000000000000000000,
    "feeTokenId": "2",
    "amountFee": 20000000000000000000,
    "label": 0,
    "nonce": 10
}
```

where `nonce` must start from 0 and increment by 1.

The code for signing it in Python is as follows:
```python
def serialize_offchain_withdrawal(withdrawal):
    return [
        int(withdrawal['exchangeId']),
        int(withdrawal['accountId']),
        int(withdrawal['tokenId']),
        int(withdrawal['amount']),
        int(withdrawal['feeTokenId']),
        int(withdrawal['amountFee']),
        int(withdrawal['label']),
        int(withdrawal['nonce'])
    ]

def sign_offchain_withdrawal(privateKey, offchainWithdrawal):
    serialized = serialize_offchain_withdrawal(offchainWithdrawal)
    signed = sign_int_array(serialized, 9 /* Pay attention to this t value */)
    offchainWithdrawal.update(signed)
```



#### Signing Internal Transfer

You need to seralized specific fields of an transfer into an integer array, then calculate the Poseidon hash of the array, and then sign the hash with your EdDSA private key.

The following is an example of internal transfers:

```json
{
    "exchangeId": 2,
    "sender":100,
  	"receiver":101,
    "tokenId": 0,
    "amount": 1000000000000000000,
    "feeTokenId": 2,
    "amountFee": 20000000000000000000,
    "label": 0,
    "nonce": 10
}
```

where `nonce` must start from 0 and increment by 1, and internal and transfer share the same  nonce.

The code for signing it in Python is as follows:

```python
def serialize_internal_transfer(transfer):
    return [
        int(transfer['exchangeId']),
        int(transfer['sender']),
        int(transfer['receiver']),
        int(transfer['tokenId']),
        int(transfer['amount']),
        int(transfer['feeTokenId']),
        int(transfer['amountFee']),
        int(transfer['label']),
        int(transfer['nonce'])
    ]

def sign_internal_transfer(privateKey, transfer):
    serialized = serialize_internal_transfer(transfer)
    signed = sign_int_array(serialized, 10 /* 注意这个t值 */)
    transfer.update(signed)
```

In addition to EDSSA signature, you also need to use ECDSA to sign internal transfers. You need to serialize specific fields of an transfer into a Json string, and use sha256 hash algorithm to calculate the hash of the json string. Convert the resutl to hexadecimal string, add a fixed header: "Sign this message to authorize Loopring Pay: ", use personal _sign to sign the combined string.

The code for signing it in Javascript is as follows:

```javascript
function serialize_transfer(transfer) {
  const data = {
    exchangeId: transfer.exchangeId,
    sender: transfer.sender,
    receiver: transfer.receiver,
    token: transfer.tokenId,
    amount: transfer.amount,
    tokenF: transfer.feeTokenId,
    amountF: transfer.amountFee,
    label: transfer.label,
    nonce: transfer.nonce,
    memo:transfer.memo || ""
  };

  return "0x" + sha256(JSON.stringify(data)).toString('hex');
}

function sign_internal_transfer(transfer){
  const transferData = serialize_transfer(transfer);
  const prefix = "Sign this message to authorize Loopring Pay:  ";
  const message = prefix + transferData;
  const sig = personal_sign(privateKey, message);
}
```



## References

You can learn more about the Poseidon hash and EdDSA signature through the following literature and github repositories.

1. **ethsnarks**: https://github.com/HarryR/ethsnarks.git
2. **SHA256 Hash**: <https://en.wikipedia.org/wiki/SHA-2>
3. **EdDSA**: <https://en.wikipedia.org/wiki/EdDSA>
4. **Poseidon Hash**: <https://www.poseidon-hash.info/>


You can also refer to our [example code](./examples.md) for more details.

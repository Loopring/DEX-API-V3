As the above table shows, some requests need extra authentic in request header.

Listed as below:

| Request                | EDDSA       | ECDSA       | Approved Hash | X-API-SIG in header |
| -----------            | ----------- | ----------- | -----------   | -----------         |
| submitTransfer         | Y           | Optional    | Y             | EIP712 signed structure |
| submitOffchainWithdraw | Y           | Optional    | Y             | EIP712 signed structure |
| updateAccount          | Y           | Y           | Y             | EIP712 signed structure |

So, If a user wants to do submitTransfer, submitOffchainWithdraw and updateAccount, in addition to EDSSA signature, you also need to use ECDSA to sign them and put the signature in request header. Loopring 3.6 uses the EIP712 standard, A user need to serialize specific fields of an request, say transfer into a EIP712 compatible structure, and then use standard EIP712 hash algorithm to calculate the hash of the structure, and then, use personal _sign to sign the combined string.

The code for hash & signing it in python is as follows:

```python
def createOriginTransferMessage(req: dict):
    class Transfer(EIP712Struct):
        pass

    setattr(Transfer, 'from', Address())
    Transfer.to           = Address()
    Transfer.tokenID      = Uint(16)
    Transfer.amount       = Uint(96)
    Transfer.feeTokenID   = Uint(16)
    Transfer.maxFee       = Uint(96)
    Transfer.validUntil   = Uint(32)
    Transfer.storageID    = Uint(32)

    transfer = Transfer(**{
        "from"          : req['payerAddr'],
        "to"            : req['payeeAddr'],
        "tokenID"       : req['token']['tokenId'],
        "amount"        : int(req['token']['volume']),
        "feeTokenID"    : req['maxFee']['tokenId'],
        "maxFee"        : int(req['maxFee']['volume']),
        "validUntil"    : req['validUntil'],
        "storageID"     : req['storageId']
    })

    # print(f"transfer type hash = {bytes.hex(transfer.type_hash())}")
    return EIP712.hash_packed(
        EIP712.exchangeDomain.hash_struct(),
        transfer.hash_struct()
    )

message = createUpdateAccountMessage(transfer_request)
v, r, s = sig_utils.ecsign(message, self.ecdsaKey)
```

The EIP712 structure declarations of each requests types can be found in Loopring contract, or just get it from our reference code base. Below are withdrawal request EIP712 structure.
```solidity
    struct Withdrawal
    {
        address owner;
        uint32  accountID;
        uint16  tokenID;
        uint    amount;
        uint16  feeTokenID;
        uint    fee;
        address to;
        bytes32 extraDataHash;
        uint    minGas;
        uint32  validUntil;
        uint32  storageID;
    }
```
So the signature hash code is:
```python
def createOffchainWithdrawalMessage(req: dict):
    class Withdrawal(EIP712Struct):
        owner = Address()
        accountID = Uint(32)
        tokenID = Uint(16)
        amount = Uint(96)
        feeTokenID = Uint(16)
        maxFee = Uint(96)
        to = Address()
        extraData = Bytes()
        minGas = Uint()
        validUntil = Uint(32)
        storageID = Uint(32)

    # "Withdrawal(address owner,uint32 accountID,uint16 tokenID,uint96 amount,uint16 feeTokenID,uint96 maxFee,address to,bytes extraData,uint256 minGas,uint32 validUntil,uint32 storageID)"
    withdrawal = Withdrawal(**{
        "owner"         : req['owner'],
        "accountID"     : req['accountId'],
        "tokenID"       : req['token']['tokenId'],
        "amount"        : int(req['token']['volume']),
        "feeTokenID"    : req['maxFee']['tokenId'],
        "maxFee"        : int(req['maxFee']['volume']),
        "to"            : req['to'],
        "extraData"     : bytes.fromhex(req['extraData']),
        "minGas"        : int(req['minGas']),
        "validUntil"    : req['validUntil'],
        "storageID"     : req['storageId'],
    })

    # print(f"extraData hash = {bytes.hex(Web3.keccak(bytes.fromhex(req['extraData'])))}")
    # print(f"withdrawal type hash = {bytes.hex(withdrawal.type_hash())}")
    return EIP712.hash_packed(
        EIP712.exchangeDomain.hash_struct(),
        withdrawal.hash_struct()
    )

message = createUpdateAccountMessage(withdrawal_request)
v, r, s = sig_utils.ecsign(message, self.ecdsaKey)
```

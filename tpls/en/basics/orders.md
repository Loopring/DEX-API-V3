# Orders


##Uni-Directional Order Model
Unlike the order models of most centralized exchanges, Loopring uses the **Uni-Directional Order Model** (UDOM). UDOM represents buy orders and sell orders uniformly with one single data structure. Let's start with a simplified UDOM model to give you a few examples of Loopring's limit price orders (Loopring doesn't support market price orders).

In the LRC-ETH trading pair, a **sell** order that sells 500 LRC at the price of 0.03ETH/LRC can be expressed as:
```JSON
{   // LRC-ETH: sell 500 LRC at 0.03ETH/LRC
    "sellToken": {
        "token" : "LRC",
        "volume" : 500
    },
    "buyToken": {
        "token" : "ETH",
        "volume" : 15
    }
}
```

a **buy** order that buys 500 LRC at the price of 0.03ETH/LRC can be expressed as:
```JSON
{   // LRC-ETH: buy 500 LRC at 0.03ETH/LRC
    "sellToken": {
        "token" : "ETH",
        "volume" : 15
    },
    "buyToken": {
        "token" : "LRC",
        "volume" : 500
    }
}
```

As you may have noticed, UDOM does not specify trading pairs or prices explicitly.

However, there is a problem with this simplified model: the match-engine doesn't know when an order should be considered as **fully filled**. We need to introduce another parameter called `buy` for this purpose. If `buy == true`, the match-engine shall check the total fill amount of `tokenB` against `amountB` to determine if an order has been fully filled; otherwise, it shall use the total fill amount of `tokenS` against `amountS`. With this new field, the above orders will look like the following: 

```JSON
{   // LRC-ETH: sell 500 LRC at 0.03ETH/LRC
    "sellToken": {
        "token" : "LRC",
        "volume" : 500
    },
    "buyToken": {
        "token" : "ETH",
        "volume" : 15
    }, // = 500 * 0.03, 
    "fillAmountBOrS": false // check sell token's fill amount against ["sellToken"]["volume"]
}
```

```JSON
{   // LRC-ETH: buy 500 LRC at 0.03ETH/LRC
    "sellToken": {
        "token" : "ETH",
        "volume" : 15
    }, // = 500 * 0.03, 
    "buyToken": {
        "token" : "LRC",
        "volume" : 500
    }
    "fillAmountBOrS": true // check buy token's fill amount against ["buyToken"]["volume"]
}
```

Note: If the above sell order is fully filled, the amount of ETH bought may be larger than 15ETH; and if the buy order is fully filled, the ETH paid may be less than 15ETH, which is the impact of the `fillAmountBOrS` parameter on the match engine's behaviors.

What is the effect of reversing the `fillAmountBOrS` value in the two orders above? The sell order for the LRC-ETH trading pair becomes a buy order for the ETH-LRC trading pair, and the buy order for the LRC-ETH trading pair becomes a sell order for the ETH-LRC trading pair. It means one Loopring trading pair, such as LRC-ETH, is equivalent to two trading pairs in many centralized exchanges, i.e.,  LRC-ETH and ETH-LRC.

Besides its elegancy and simplicity, Loopring's UDOM also makes it possible to implement much simpler settlement logic in ZKP circuits.

{% hint %}
So far **AMM swap order** does NOT support `fillAmountBOrS`, so, please set `fillAmountBOrS` to `false` in swap request.
{% endhint %}

## Order object
Loopring's actual order format is a bit more complex. You can use the following JSON to express a limit price order. For details of specific parameters, see [Submit Order](../dex_apis/submitOrder.md).

```JSON
order = {
    // sign part
    "exchange"      : "0x7489DE8c7C1Ee35101196ec650931D7bef9FdAD2",
    "accountId"     : 10004,
    "storageId"     : 0,
    "sellToken": {
        "tokenId": 0, // ETH
        "volume": "15000000000000000000"
    },
    "buyToken" : {
        "tokenId": 1, // LRC
        "volume": "500000000000000000000"
    },
    "validUntil"    : 1700000000,
    "maxFeeBips"    : 50,
    "fillAmountBOrS": true,
    "taker"         : "0000000000000000000000000000000000000000",
    // aux data
    "allOrNone"     : false,
    "clientOrderId" : "SampleOrder",
    "orderType"     : "LIMIT_ORDER", // "AMM", "MAKER_ONLY", "TAKER_ONLY"
    "channelId"     : "channel1::maker1"
    // signature
    "eddsaSignature":"0x1c31e81cdde3c9f92e31ab35733e3403de45325cb5f90832c9d4f8673ec22f501de9e9b97c8d7b475ab12836d87c9c6f2a78a91cd650bc77ec4079ffd966933f10d6a5c133ee270013f1d8596c706f2623d0ba1c3dccbc3f202db606bb00d6bc" // 0x + 192 bytes hex string, i.e., 0x+Rx+Ry+s
}

```

Next, we will further explain some of these data fields for you.

#### Tokens and Amounts
In an actual order,  tokens are not expressed by their names or ERC20 addresses, but by their **token ID**, the index at which the tokens have been registered in the Loopring Exchange's smart contract.  Note that the same ERC20 token may have different IDs on different exchanges built on top of the same Loopring protocol.

In the above example, we assume that the IDs of LRC and ETH are 2 and 0, respectively.
You can query token's information using [Token Information Supported by the Exchange](../dex_apis/getTokens.md).

The amounts of tokens are in their smallest unit as strings. Taking LRC as an example, its `decimals` is 18, so 1.0LRC should be expressed as `" 1000000000000000000 "` (1 followed by 18 0s). Each token's `decimals` is coded in its smart contract; the decimals of ETH is 18.

#### Trading Fee
`maxFeeBips = 50` specifies that the **maximum trading fee** the order is willing to pay to the exchange is 0.5% (the unit of `maxFeeBips` is 0.01%). Loopring charges trading fees in `tokenB` as a percentage of the token bought from a trade. Assuming that the order above has bought `"10000000000000000000"` ETH (10ETH), the actual trading fee **will not exceed 0.05ETH** (`"10000000000000000000"* 0.5%`).

Loopring's relayer offers different trading fee discounts based on the user VIP tiers. The bottom line is that the actual trading fees can never exceed the maximum orders are willing to pay, specified by `maxFeeBips`. 

When you place an order, you must set `maxFeeBips` to be no less than the trading fee rate in the specified trading pair for your account (based on your VIP level). This information can be obtained by querying `/api/v3/user/feeRates`. If you trust Loopring Exchange, you can also set `maxFeeBips` to 63, the maximum value allowed by the Loopring protocol.

#### Timestamps

`validUntil` specifies the order expiration timestamp, both in seconds since epoch.

When the relayer receives an order, it will verify these two timestamps in the order; Loopring's ZKP circuit code will also check these two timestamps during settlement. Due to the delay of zkRollup batch processing, and the possible deviation of the time on Ethereum blockchain and our servers, we strongly recommend that `validSince` be set to the current time,and the window between `validSince` and`validUntil` is no shorter than 1 week; otherwise, your order may be rejected or cancelled by the relayer.

{% hint style='tip' %}
You can take advantage of the `validUntil` timestamp to avoid unnecessary proactive cancellation of orders.
{% endhint %}


#### Fill Status and Storage ID

Loopring 3.6 reserves half of 16384 ($$2 ^ {14} $$) slots for each token to track token amounts changs introduced by **order** and **AMM swap order**, and the other half slots for each token to track the user's offchain requests include **AMM join/exit**, **transfer** and **withdraw** . If an order's storage ID is `N`, then the slot used is `N % 16384`. In other words, if the slot number is `m`, it will be used to track orders with the following IDs:  `m`, `m + 16384`, `m + 16384 * 2`, ... and so on.

Each slot also remembers the ID of the current order being tracked (the initial storage ID is the slot number), and subsequent orders with smaller storage IDs will be rejected. Suppose that slot `1` is tracking order `32769` (` 1 + 16384 * 2`). When the user places orders with ID of `1` or` 16385`, the server will reject these orders and return errors. If you have more than `16384` active orders for a trading pair, you need to cancel some of them to release slots before you can submit new orders.

`Storage ID `is the upgraded `Order ID` of Loopring 3.1, which has big enough capacity, and more usages, See Below table:


| Storage ID            | Ranges                                        | Count     | Usages        |
| ----------------      | -----------------------------------------     | --------- | ------------- |
| Even numbers          | {0, 2, 4,<br>...,<br>4294967292， 4294967294} |2147483648 |transfer<br>withdrawal<br>AMM join<br>AMM exit|
| Odd numbers           | {1, 3, 5,<br>...,<br>4294967293， 4294967295} |2147483648 |order<br>AMM swap order   |


The maximum value of storage ID is `4294967296` ($$2^{32}$$). After reaching this ID limit, you can neither place orders nor transfer/withdraw balance on the corresponding token. For most users, this is not a problem, as 4294967296 is big enough, although it is possible that an ultra high-frequent (>100 TPS for all time) trader or transfer payer meet out of ID error.

It is worth noting that all **sell orders** from the same account in multiple trading pairs with the same base token (such as LRC-ETH and LRC-USDT) share the same 16384 slots. If you do not plan to maintain the allocation of storage IDs and slots between trading pairs on the client-side, you can register multiple accounts, as recommended above.

{% hint style='info' %}
We know the inconvenience caused by the slot design. However, this is a design decision made in the Loopring protocol itself. We hope future technological advances can remove this limitation.
{% endhint %}


#### Other Fields

- `exchangeAddress`: Unlike Looping 3.1, we now use Loopring Exchange's address as a unique numeric ID in the Looping protocol.
- `accountId`: User's account ID.
- `allOrNone`: ` true ` if the order must be fully filled or cancelled. This parameter is not supported yet by our matching engine, so please set it to "false" for now.
- `clientOrderId`: Used to label orders by the client without user awareness. It also has no impact on trading. 
- `channelId`: Used to lable order's channel.

For more details, please refer to [Submit Order](../dex_apis/submitOrder.md).





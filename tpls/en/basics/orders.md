# Orders


##Uni-Directional Order Model
Unlike the order models of most centralized exchanges, Loopring uses the **Uni-Directional Order Model** (UDOM). UDOM represents buy orders and sell orders uniformly with one single data structure. Let's start with a simplified UDOM model to give you a few examples of Loopring's limit price orders (Loopring doesn't support market price orders).

In the LRC-ETH trading pair, a **sell** order that sells 500 LRC at the price of 0.03ETH/LRC can be expressed as:
```JSON
{   // LRC-ETH: sell 500 LRC at 0.03ETH/LRC
    "tokenS": "LRC",
    "tokenB": "ETH",
    "amountS": 500,
    "amountB": 15 // = 500 * 0.03
}
```

{% hint style='info' %}
The letter S stands for *Sell* and letter B stands for *Buy*.
{% endhint %}


a **buy** order that buys 500 LRC at the price of 0.03ETH/LRC can be expressed as:
```JSON
{   // LRC-ETH: buy 500 LRC at 0.03ETH/LRC
    "tokenS": "ETH",
    "tokenB": "LRC",
    "amountS": 15, // = 500 * 0.03
    "amountB": 500 
}
```

As you may have noticed, UDOM does not specify trading pairs or prices explicitly.



However, there is a problem with this simplified model: the match-engine doesn't know when an order should be considered as **fully filled**. We need to introduce another parameter called `buy` for this purpose. If `buy == true`, the match-engine shall check the total fill amount of `tokenB` against `amountB` to determine if an order has been fully filled; otherwise, it shall use the total fill amount of `tokenS` against `amountS`. With this new field, the above orders will look like the following: 

```JSON
{   // LRC-ETH: sell 500 LRC at 0.03ETH/LRC
    "tokenS": "LRC",
    "tokenB": "ETH",
    "amountS": 500,
    "amountB": 15 // = 500 * 0.03, 
    "buy": false  // check tokenS's fill amount against amountS
}
```

```JSON
{   // LRC-ETH: buy 500 LRC at 0.03ETH/LRC
    "tokenS": "ETH",
    "tokenB": "LRC",
    "amountS": 15, // = 500 * 0.03
    "amountB": 500,
    "buy": true // check tokenB's fill amount against amountB
}
```

Note: If the above sell order is fully filled, the amount of ETH bought may be larger than 15ETH; and if the buy order is fully filled, the ETH paid may be less than 15ETH, which is the impact of the `buy` parameter on the match engine's behaviors.


What is the effect of reversing the `buy` value in the two orders above? The sell order for the LRC-ETH trading pair becomes a buy order for the ETH-LRC trading pair, and the buy order for the LRC-ETH trading pair becomes a sell order for the ETH-LRC trading pair. It means one Loopring trading pair, such as LRC-ETH, is equivalent to two trading pairs in many centralized exchanges, i.e.,  LRC-ETH and ETH-LRC.

Besides its elegancy and simplicity, Loopring's UDOM also makes it possible to implement much simpler settlement logic in ZKP circuits.


## Order Structure
Loopring's actual order format is a bit more complex. You can use the following JSON to express a limit price order. For details of specific parameters, see [Submit Order](../dex_apis/submitOrder.md).

```JSON
newOrder = {
    "tokenSId": 2,  // LRC
    "tokenBId": 0,  // ETH
    "amountS": "500000000000000000000",
    "amountB": "15000000000000000000",
    "buy": "false",
    "exchangeId": 2,
    "accountId": 1234,
    "allOrNone": "false", // Must be "false" for now
    "maxFeeBips": 50,
    "label": 211,
    "validSince": 1582094327,
    "validUntil": 1587278341,
    "orderId": 5,
    "hash": "14504358714580556901944011952143357684927684879578923674101657902115012783290",
    "signatureRx": "15179969700843231746888635151106024191752286977677731880613780154804077177446",
    "signatureRy": "8103765835373541952843207933665617916816772340145691265012430975846006955894",
    "signatureS" : "4462707474665244243174020779004308974607763640730341744048308145656189589982",
    "clientOrderId": "Test01",
    "channelId": "channel1::maker1"
}
```

Next, we will further explain some of these data fields for you.

#### Tokens and Amounts
In an actual order,  tokens are not expressed by their names or ERC20 addresses, but by their **token ID**, the index at which the tokens have been registered in the Loopring Exchange's smart contract.  Note that the same ERC20 token may have different IDs on different exchanges built on top of the same Loopring protocol.

In the above example, we assume that the IDs of LRC and ETH are 2 and 0, respectively.
You can query token's information using [Token Information Supported by the Exchange](../dex_apis/getTokens.md).

The amounts of tokens are in their smallest unit as strings. Taking LRC as an example, its `decimals` is 18, so 1.0LRC should be expressed as `" 1000000000000000000 "` (1 followed by 18 0s). Each token's `decimals` is coded in its smart contract; the decimals of ETH is 18.

{% hint style='info' %}
The types of `buy` and` allOrNone` in the order are strings rather than boolean.
{% endhint %}

#### Trading Fee
`maxFeeBips = 50` specifies that the **maximum trading fee** the order is willing to pay to the exchange is 0.5% (the unit of `maxFeeBips` is 0.01%). Loopring charges trading fees in `tokenB` as a percentage of the token bought from a trade. Assuming that the order above has bought `"10000000000000000000"` ETH (10ETH), the actual trading fee **will not exceed 0.05ETH** (`"10000000000000000000"* 0.5%`).

Loopring's relayer offers different trading fee discounts based on the user VIP tiers. The bottom line is that the actual trading fees can never exceed the maximum orders are willing to pay, specified by `maxFeeBips`. 

When you place an order, you must set `maxFeeBips` to be no less than the trading fee rate in the specified trading pair for your account (based on your VIP level). This information can be obtained by querying `/api/v2/user/feeRates`. If you trust Loopring Exchange, you can also set `maxFeeBips` to 63, the maximum value allowed by the Loopring protocol.

#### Timestamps

`validSince` specifies the order's effective timestamp, and`validUntil` specifies the order expiration timestamp, both in seconds since epoch.

When the relayer receives an order, it will verify these two timestamps in the order; Loopring's ZKP circuit code will also check these two timestamps during settlement. Due to the delay of zkRollup batch processing, and the possible deviation of the time on Ethereum blockchain and our servers, we strongly recommend that `validSince` be set to the current time,and the window between `validSince` and`validUntil` is no shorter than 1 week; otherwise, your order may be rejected or cancelled by the relayer.

{% hint style='tip' %}
You can take advantage of the `validUntil` timestamp to avoid unnecessary proactive cancellation of orders.
{% endhint %}


#### Fill Status and Order ID


Loopring 3.1.1 reserves 16384 ($$2 ^ {14} $$) slots for each token to track the aggregated fill amount of each order  that **sells the token**. If an order's ID is `N`, then the slot used is `N % 16384`. In other words, if the slot number is `m`, it will be used to track orders with the following IDs:  `m`, `m + 16384`, `m + 16384 * 2`, ... and so on.

Each slot also remembers the ID of the current order being tracked (the initial order ID is the slot number), and subsequent orders with smaller  IDs will be rejected. Suppose that slot `1` is tracking order `32769` (` 1 + 16384 * 2`). When the user places orders with ID of `1` or` 16385`, the server will reject these orders and return errors. If you have more than `16384` active orders for a trading pair, you need to cancel some of them to release slots before you can submit new orders.


The maximum value of order ID is `1048576` ($$2^{20}$$). After reaching this ID limit, you can no longer place sell orders for the corresponding token. For most users, this is not a big problem; but for trading bots,  we recommend registering multiple accounts to sell different tokens.

{% hint style='info' %}
Loopring 3.5 will remove the limit of the maximum order ID, but still retain the slot design and configuration.
{% endhint %}

It is worth noting that all **sell orders** from the same account in multiple trading pairs with the same base token (such as LRC-ETH and LRC-USDT) share the same 16384 slots. If you do not plan to maintain the allocation of order IDs and slots between trading pairs on the client-side, you can register multiple accounts, as recommended above.

{% hint style='info' %}
We know the inconvenience caused by the slot design. However, this is a design decision made in the Loopring protocol itself. We hope future technological advances can remove this limitation.
{% endhint %}


#### Other Fields

- `exchangeId`: Loopring Exchange's unique numeric ID in the Looping protocol, currently has value `2` and is constant. This ID will change once we upgrade to a new protocol version.
- `accountId`: User's account ID.
- `allOrNone`: `" true "` if the order must be fully filled or canceled. This parameter is not supported yet by our matching engine, so please set it to "false" for now.
- `label`: Used to label orders at the protocol layer but has no impact on trading. Because users will sign this field as part of the order, so it's more trustworthy for different parties to use, for example, to calculate profit-sharing.
- `clientOrderId`: Used to label orders by the client without user awareness. It also has no impact on trading. 
- `channelId`: Used to lable order's channel.

For more details, please refer to [Submit Order](../dex_apis/submitOrder.md).





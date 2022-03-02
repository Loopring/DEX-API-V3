# ChangeLogs

## 2021.09.01:
  1. Align websocket and V3 balance response data structure.
     1. ERC20 balance data no change.
     2. Websocket account topic subscription data changed:
        1. The topic changes to {"topic": "account", "accountId": "10005", "v3": true}, and 2 response fields changed:
            ```
            totalAmount -> total
            amountLocked -> locked
            ```
          to align with the V3 REST query balance API response.
        "v3" flag in subscription is optional and back compatible with previous subscription message.
  2. Refine block generation websocket notification, add `verbose` flag to get detail info.
  3. Add `hashes` filter to L2 tx queries.
  4. getStorageId logic changed, a new flag `maxNext` to back compatible with previous behavior.

## 2021.09.20:
  1. Make /api/v3/user/transfers a general transfer query by hash without accountId.

## 2021.11.29:
  1. Fix typo

## 2022.03.02:
  1. Add NFT related
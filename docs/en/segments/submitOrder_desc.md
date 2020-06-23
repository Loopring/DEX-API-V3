Please follow the following steps to submit an order:

1. Get the next orderId through `/api/v2/orderId`. If you maintain order IDs on the client side, you can skip this step.
1. Choose reasonable values for `validSince` and` validUntil`. We recommend that `validSince` is set to the current system time, and `validUntil` is set to be at least one month later than the current time.
1. Choose a reasonable `MaxFeeBips`. We recommend setting this value to `63`.
1. Use`clientOrderId` and/or `channelId` for better client-side tracking.
1. Sign the order.
1. Submit the order and receive the order's hash.

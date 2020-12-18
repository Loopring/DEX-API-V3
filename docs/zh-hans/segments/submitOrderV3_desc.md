
您需要以下步骤来下单：

1. 通过`/api/v2/orderId`获取正确的`orderId`。如果您在客户端维护订单ID，可以跳过该步骤。
1. 选择合理的`validSince`和`validUntil`值。我们推荐的参数是`validSince`设置为当前系统时间，`validUntil`设置成比当前时间晚至少一个月。
1. 选择合理的`MaxFeeBips`。我们建议这个值设置为`63`。
1. 如果您想更好地追踪订单，请选择使用`clientOrderId`和（或）`channelId`。
1. 对订单进行签名。
1. 提交订单, 确认返回的结果包含订单哈希和订单最新的状态。

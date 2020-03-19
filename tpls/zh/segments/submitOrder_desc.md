提交订单接口, 要正确提交Loopring订单,需要以下步骤:  
- 通过/api/v2/orderId获取正确的orderId
- 选择合理有效时间(validSince和validUntil, 最佳方案是validSince大于当前时间, validUntil是当前时间很久之后, 比如一年)
- 选择合理的MaxFeeBips, 这个字段限制了交易所对用户收费的上限
- 如果做市商想使用自己的唯一ID来标示订单, 请使用clientOrderId
- 如果订单是有渠道来源的, 请使用channelId
- 对订单进行签名
- 提交订单, 确认返回的结果包含订单Hash

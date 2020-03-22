## DEX
去中心化交易所。

## ZKP
零知识证明。

## Relayer
路印DEX的后台系统，负责订单操作，交易撮合，零知识证明生成等。

## 链上请求
发送ETH交易调用路印DEX合约的请求。

## 链下请求
直接发送给relayer的请求。

## Base token
指一个交易对的交易对象，即写在靠前部分的Token。 LRC-ETH市场对，LRC 即为该市场对的Base Token。

## Quote token
指一个交易对的定价Token，即写在靠后部分的Token。 LRC-ETH市场对，ETH 即为该市场对的Quote Token。

## Size
指订单的base Token数量。对于 2000 LRC 买 1 EHT的订单，2000 即为size

## Volume
指订单的quote Token 数量。对于 2000 LRC 买 1 EHT的订单，1 即为volume

## EDDSA
用户用于下单签名的算法，区别ETH公私钥对。路印交易所的链上请求需要用户使用ETH的私钥签名，而一些链下请求（下单，取消订单）则使用EDDSA产生的私钥来对交易进行签名。

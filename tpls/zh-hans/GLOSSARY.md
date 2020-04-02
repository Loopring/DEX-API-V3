# 术语

### DEX
Decenralized EXchange的简称，即去中心化交易所。**路印交易所**是搭建在以太坊公有链上的去中心化交易所。

### Zero Knowledge Proofs (ZKP)
零知识证明。

### Relayer
中继，即路印交易所的后台系统，负责订单操作，交易撮合，零知识证明生成等。

### 链上请求
通过交易，在以太坊上发送给路印交易所智能合约的请求。

### 链下请求
通过路印中继的API，绕过以太坊区块链，直接发送给路印交易所的请求。

### Base token
指一个交易对的交易对象，即写在靠前部分的Token。 LRC-ETH市场对，LRC 即为该市场对的Base Token。

### Quote token
指一个交易对的定价Token，即写在靠后部分的Token。 LRC-ETH市场对，ETH 即为该市场对的Quote Token。

### Size
指订单的base Token数量。对于 2000 LRC 买 1 EHT的订单，size为2000。

### Volume
指订单的quote Token 数量。对于 2000 LRC 买 1 EHT的订单，Volume为1。

### EdDSA
用于对链下请求做签名的算法。路印交易所的链上请求需要用户使用以太坊地址对应的ECDSA私钥签名，而链下请求则需要使用交易账号的EdDSA私钥来签名。

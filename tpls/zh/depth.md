### depth 主题

订阅深度的主题，获取定时推送的深度信；订阅该主题不需要apiKey；在没有数据更新时，不进行数据推送。

#### 订阅规则

主题&市场&归并等级

- 支持的市场以及市场对应支持的归并等级，可以通过api接口[https://api.loopring.io/api/v2/exchange/markets](https://api.loopring.io/api/v2/exchange/markets) 获取

#### 返回错误码

| 返回码 |                描述                 |
| :----: | :---------------------------------: |
| 104107 | depth主题的订阅条件不合法或者不支持 |

#### 推送示例

```json
{
  "topic": "depth&LRC-ETH&1",
  "ts": 1584717910000,
  "startVersion": 1212121,
  "endVersion": "1212123",
  "data": {
    bids: [
      [
        "295.97",								//price
        "456781000000000",			//size
        "3015000000000",				//volume
        "4"											//count
      ]
    ],
    asks: [
      
    ]
  }
}
```

#### 模型

##### 推送数据结构

|     字段     |      类型       | 是否必现 |         说明         |       举例        |
| :----------: | :-------------: | :------: | :------------------: | :---------------: |
|    topic     |     string      |    是    |   订阅的主题和条件   | "depth&LRC-ETH&1" |
|      ts      |     integer     |    是    |       推送时间       |   1584717910000   |
| startVersion |     integer     |    是    | 该次推送的起始版本号 |      1212121      |
|  endVersion  |     integer     |    是    | 该次推送的终结版本号 |      1212123      |
|     data     | [Depth](#depth) |    是    |       深度信息       |         /         |

#####<span id="depth">  Depth数据结构</span>

| 字段 | 类型                           | 是否必现 | 说明     | 举例 |
| ---- | ------------------------------ | -------- | -------- | ---- |
| bids | [List\[List\[string\]]](#slot) | 是       | 买单深度 | /    |
| asks | [List\[List\[string\]]](#slot) | 是       | 卖单深度 | /    |

#### <span id = "slot">深度条目</span>

每一条深度数据

| 字段编号 | 类型   | 是否必现 | 说明           | 举例       |
| :------: | ------ | -------- | -------------- | ---------- |
|    1     | string | 是       | 价格           | "0.002"    |
|    2     | string | 是       | 挂单量         | "21000"    |
|    3     | string | 是       | 挂单总量       | "33220000" |
|    4     | string | 是       | 聚合的订单数目 | "4"        |

#### 如何构建本地的Orderbook

1. 订阅 depth主题

2. 开始缓存收到的更新。同一个价位，后收到的更新覆盖前面的。

3. 访问接口 https://api.loopring.io/api/v1/depth 获得一个全量的深度快照。

4. 3中获取的快照如果version大约本地version（endVersion），则直接覆盖，如果小于本地version，则相同的价格不覆盖，不同的价格则覆盖。

5. 将深度快照中的内容更新到本地orderbook副本中，并从websocket接收到的第一个startVersion <=本地 version+1 且 endVersion >= 本地version 的event开始继续更新本地副本。

6. 每一个新推送的startVersion应该恰好等于上一个event的endVersion+1，否则可能出现了丢包，请从step3重新进行初始化

7. 每一个推送中的挂单量代表这个价格目前的挂单量绝对值，而不是相对变化。

8. 如果某个价格对应的挂单量为0，表示该价位的挂单已经撤单或者被吃，应该移除这个价位。
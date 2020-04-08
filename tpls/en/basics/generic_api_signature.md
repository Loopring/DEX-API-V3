#### 签名生成算法（伪代码）

- 初始化空字符串`signatureBase`
- 将请求方法字符串追加到`signatureBase`
- 将“＆”字符附加到`signatureBase`
- 将`percent-encoded`的请求路径（不是查询字符串）追加到`signatureBase`
- 将“＆”字符附加到`signatureBase`
- 初始化空字符串`parameterString`
- 对于GET / DELETE 数据
    * 将请求里的参数按键的字典顺序排序，得到排过序后的键/值对
    * 将`percent-encoded`的键附加到`parameterString`
    * 将“=”字符附加到`parameterString`
    * 将`percent-encoded`的值附加到`parameterString`
    * 如果有更多的键/值对，请在`parameterString`后面附加“＆”字符
- 对于POST / PUT 数据
    - 将发送请求的body json字符串附加到`parameterString`
- 将`percent-encoded`的`parameterString`附加到`signatureBase`
- 计算`signatureBase`的**SHA-256**哈希值`hash`
- 对`hash`用账号的私钥`privateKey`做签名，得到三个值：`Rx`,`Ry`, 和`S`
- 将`Rx`,`Ry`, 和`S`通过逗号分隔拼接成最终签名字符串：`${Rx},${Ry},${S}`

#### 获取请求方法和URL

要生成签名，请先确定HTTP method和请求的base URL。loopring.io REST API使用四种请求方法：

- GET
- POST
- PUT
- DELETE

> Http method
```
GET
```

base URL是请求指向的URL，减去任何查询字符串或哈希参数。 请始终对loopring.io API使用"https://"协议。
> Base URL:
```
https://api.loopring.io/api/v2/apiKey
```

#### 获取请求参数
接下来，从query string中获取请求参数(用于GET和POST请求)和body(POST、PUT)。

在HTTP请求中，参数是url编码的，但是您应该收集原始值。在上面的原始HTTP请求中，参数如下:

|  参数名   | 参数值  |
|  ----  | ----  |
| publicKeyX  | 13375450901292179417154974849571793069911517354720397125027633242680470075859 |
| publicKeyY  | 13375450901292179417154974849571793069911517354720397125027633242680470075859 |
| accountId  | 1 |

这些值需要进行编码和拼接:

- 按键按字典顺序对参数列表进行排序
- 对于每个键/值对:
    - `percent-encoded`参数名并将其附加到输出字符串中
    - 将' = '字符附加到输出字符串
    - `percent-encoded`参数值并将其附加到输出字符串中
    - 如果还剩下更多的键/值对，则将'&'字符附加到输出字符串中

> Parameter string:
```
accountId=1&publicKeyX=13375450901292179417154974849571793069911517354720397125027633242680470075859&publicKeyY=13375450901292179417154974849571793069911517354720397125027633242680470075859
```

#### 生成 `signature base string`
`signature base string`是我们按照以下顺序将之前生成的三个字符串连接起来的结果:HTTP method、`percent-encoded`的`base URL`和`percent-encoded`的`parameter string`，在相邻组件之间用'&'字符连接。

> Signature base string:
```
GET&https%3A%2F%2Fapi.loopring.io%2Fapi%2Fv2%2FapiKey&accountId%3D1%26publicKeyX%3D13375450901292179417154974849571793069911517354720397125027633242680470075859%26publicKeyY%3D13375450901292179417154974849571793069911517354720397125027633242680470075859
```
请注意，每一部分都应该是经过`percent-encoded`的，因此在生成的签名基字符串中应该正好有两个'&'字符。


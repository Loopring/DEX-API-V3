#### 签名生成算法

- 初始化空字符串`signatureBase`；
- 将API请求的HTTP方法字符串追加到`signatureBase`；
- 将“＆”字符附加到`signatureBase`；
- 将*百分号编码后（percent-encoded）*后的完整URL路径（不包括“?”和查询参数）追加到`signatureBase`；
- 将“＆”字符附加到`signatureBase`；
- 初始化空字符串`parameterString`；
- 对于GET / DELETE 请求：
    * 将请求里的参数按键的字典顺序升序排序，得到排过序后的键/值对；
    * 将*百分号编码后*后的键附加到`parameterString`；
    * 将“=”字符附加到`parameterString`；
    * 将*百分号编码后*后的值附加到`parameterString`；
    * 如果有更多的键/值对，请在`parameterString`后面附加“＆”字符，并重复上述操作；
- 对于POST / PUT 请求；
    - 将发送请求的Body JSON字符串附加到`parameterString`；
- 将*百分号编码后*后的`parameterString`附加到`signatureBase`；
- 计算`signatureBase`的**SHA-256**哈希值`hash`；
- 对`hash`用账号的私钥`privateKey`做签名，得到三个值：`Rx`,`Ry`, 和`S`；
- 将`Rx`,`Ry`, 和`S`通过逗号分隔拼接成最终签名字符串：`${Rx},${Ry},${S}`。

#### HTTP Method and URL

请使用大写的HTTP方法：
- GET
- POST
- PUT
- DELETE

URL中请一定包含HTTPS协议头，确保协议头和接入URL全部小写，比如：

```
https://api.loopring.io/api/v2/apiKey
```

#### 示例
假设上面的URL包含下列Query参数：

```
https://api.loopring.io/api/v2/apiKey?publicKeyX=13375450901292179417154974849571793069
911517354720397125027633242680470075859&publicKeyY=133754509012921794171549748495717930
69911517354720397125027633242680470075859&accountId=1
```

即：

|  参数名   | 参数值  |
|  ----  | ----  |
| publicKeyX  | 13375450901292179417154974849571793069911517354720397125027633242680470075859 |
| publicKeyY  | 13375450901292179417154974849571793069911517354720397125027633242680470075859 |
| accountId  | 1 |

那么，`parameterString`应该为：
```
accountId=1&publicKeyX=1337545090129217941715497484957179306991151735472039712502763324
2680470075859&publicKeyY=13375450901292179417154974849571793069911517354720397125027633
242680470075859
```

`signatureBase`应该为：
```
GET&https%3A%2F%2Fapi.loopring.io%2Fapi%2Fv2%2FapiKey&accountId%3D1%26publicKeyX%3D1337
5450901292179417154974849571793069911517354720397125027633242680470075859%26publicKeyY%
3D13375450901292179417154974849571793069911517354720397125027633242680470075859
```

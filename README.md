# DEX-API
Loopring 文档。

## 准备
### 安装 node.js
https://nodejs.org/en/
### 安装 gitbook

```
npm install gitbook-cli -g
gitbook fetch
```

### gitbook 手册
https://chrisniael.gitbooks.io/gitbook-documentation/content/
https://docs.gitbook.com/

## 本地写文档
如果是第一次使用，需要运行下面命令：

```
./xdoc.py refresh build
cd generated
gitbook install
gitbook serve
```

之后访问下面的链接即可看到文档：
http://localhost:4000/

以后在编写完文档后，只需要运行 ./xdoc.py build 命令即可:
```
./xdoc.py build
```
页面会自动刷新。

如果gitbook server挂了，重新运行即可：
```
gitbook serve
```
gitbook install 命令用来安装插件，一般来说运行一次即可。除非你配置了新的插件。

** 确保你的gitbook命令运行在 generated 目录下。 **

## 发布文档
执行：

```
./publish.sh
git add .
git commit -m "YOUR_COMMENT"
git push origin master
```

文档会发布到下面的页面：
https://loopring.github.io/DEX-API/

# DEX-API
The API of Loopring DEX

## Preparation
### Install node.js
https://nodejs.org/en/
### Install gitbook

```
npm install gitbook-cli -g
gitbook fetch
```

### Learn gitbook
https://chrisniael.gitbooks.io/gitbook-documentation/content/
https://docs.gitbook.com/

## Write doc locally
First run:

```
./xdoc.py
cd generated
gitbook install # run this command only after modifying plugins
gitbook serve
```

Then visit:
http://localhost:4000/

After that, you could only run cmd ./xdoc.py while you edit the file:
```
./xdoc.py
```
And your page will be refreshed automatically.

And if you shut down gitbook serve, just restart it with command:
```
gitbook serve
```
You just need install plugins only once.

** Make sure gitbook related commands running in generated folder. **

## Publish doc
Run:

```
./build.sh
git add .
git commit -m "YOUR_COMMENT"
git push origin master
```

Then visit:
https://loopring.github.io/DEX-API/


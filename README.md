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
gitbook install # run this command only after modifying plugins
gitbook serve
```

Then visit:
http://localhost:4000/

## Publish doc
Run:

```
gitbook install # run this command only after modifying plugins
./build.sh
git add .
git commit -m "YOUR_COMMENT"
git push origin master
```

Then visit:
https://loopring.github.io/DEX-API/


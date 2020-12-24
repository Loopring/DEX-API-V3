rm api\?hl\=en*
wget $dev/api\?hl\=en 
cp api\?hl\=en meta/swagger_en.json 
cp api\?hl\=en meta/swagger_zh-hans.json
python  ./xdoc.py build

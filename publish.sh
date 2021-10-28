#!/bin/sh
#
# Copyright 2020 Loopring Org. All Rights Reserved.
# Author: chao@loopring.org (Ma Chao)

time=$(date "+%Y%m%d-%H%M%S")

cd generated && \
    rm -rf $(ls | grep -v "node_modules") && \
    cd .. && \
    python3 ./xdoc.py build && \
    cd generated && \
    gitbook build . docs && \
    cd .. && rm -rf ./docs && \
    cp -rf generated/docs . && \
    python3 ./xdoc.py windup && \
    git add . && git commit -m "publish ${time}" && git push origin v3-draft

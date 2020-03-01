#!/bin/sh
#
# Copyright 2020 Loopring Org. All Rights Reserved.
# Author: chao@loopring.org (Ma Chao)

./xdoc.py && cd generated && gitbook build . docs && cd .. && cp -rf generated/docs .

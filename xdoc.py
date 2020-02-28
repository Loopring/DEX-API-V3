#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2020 Loopring Org. All Rights Reserved.

__author__ = 'chao@loopring.org (Ma Chao)'

import os

from jinja2 import Environment, FileSystemLoader

path = '{}/tpl/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)

tpl = env.get_template('zh_cn/summary.tpl')
print(tpl.render(seq=['hoss', 'chao']))


def generateStructs():

def main():
    print('ok')

if __name__ == '__main__':
    main()

#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright 2020 Loopring Org. All Rights Reserved.

__author__ = 'chao@loopring.org (Ma Chao)'

import logging
import os
import subprocess

from functools import partial
from jinja2 import Environment, FileSystemLoader


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

LOGGER = logging.getLogger(__name__)

def run_command_with_return_info(cmd):
    try:
        return (True, subprocess.check_output([cmd], shell = True))
    except:
        LOGGER.error('Command %s failed.'%(cmd))
        return (False, None)

PURGE_DIR = '.generated'
OUTPUT_DIR = 'generated'
PURGE_IGNORE = ['swp', 'py', 'generated', '.generated', '.git', 'docs', '_book',
                'README.md', '.gitignore', 'build.sh']
OUTPUT_IGNORE = ['_book', 'docs', 'node_modules']


def sync_out():
    if not os.path.exists(OUTPUT_DIR):
        run_command_with_return_info('mkdir %s'%(OUTPUT_DIR))
    forward_sync(PURGE_DIR, OUTPUT_DIR, ['.'])
    nodes = get_first_layer_nodes(OUTPUT_DIR, OUTPUT_IGNORE)
    backward_sync(OUTPUT_DIR, PURGE_DIR, nodes)

def is_wanted(node, blackList):
    for ignore in blackList:
        if node.endswith(ignore):
            return False
    return True


def get_first_layer_nodes(root, black):
    nodes = filter(partial(is_wanted, blackList = black),
                   os.listdir(root))
    return nodes


def render_file(filename):
    # TODO(hoss):
    return (False, None)

def forward_sync(sourceDir, targetDir, nodes):
    for node in nodes:
        fullSourcePath = os.path.join(sourceDir, node)
        fullTargetPath = os.path.join(targetDir, node)
        if os.path.isfile(fullSourcePath):
            run_command_with_return_info('cp %s %s'%(fullSourcePath,
                                                     fullTargetPath))
        else:
            if (not node == '.'):
                if not os.path.exists(fullTargetPath):
                    run_command_with_return_info('mkdir %s'%(fullTargetPath))
            forward_sync(fullSourcePath, fullTargetPath,
                         os.listdir(fullSourcePath))

def backward_sync(sourceDir, targetDir, nodes):
    for node in nodes:
        fullSourcePath = os.path.join(sourceDir, node)
        fullTargetPath = os.path.join(targetDir, node)
        if not os.path.exists(fullTargetPath):
            run_command_with_return_info('rm -rf %s'%(fullSourcePath))
        else:
            if os.path.isdir(fullSourcePath):
                backward_sync(
                    fullSourcePath, fullTargetPath, os.listdir(fullSourcePath))

def recursive_generate(sourceDir, targetDir, nodes):
    for node in nodes:
        fullSourcePath = os.path.join(sourceDir, node)
        fullTargetPath = os.path.join(targetDir, node)
        if os.path.isfile(fullSourcePath):
            (res, content) = render_file(fullSourcePath)
            if (not res):
                run_command_with_return_info(
                    'cp %s %s'%(fullSourcePath, fullTargetPath))
            else:
                pass  # TODO(hoss):
        else:
            run_command_with_return_info('mkdir %s'%(fullTargetPath))
            recursive_generate(fullSourcePath, fullTargetPath,
                              os.listdir(fullSourcePath))

def purge_and_generate():
    run_command_with_return_info('rm -rf %s'%(PURGE_DIR))
    run_command_with_return_info('mkdir %s'%(PURGE_DIR))
    recursive_generate('.', PURGE_DIR, get_first_layer_nodes('.', PURGE_IGNORE))


def generate_structs():
    LOGGER.info('Creating gitbook files...')
    purge_and_generate()
    LOGGER.info('Syncing gitbook files...')
    sync_out()

def main():
    generate_structs()

if __name__ == '__main__':
    main()
    # print('kaka')
# path = '{}/tpl/'.format(os.path.dirname(__file__))
# loader = FileSystemLoader(path)
# env = Environment(loader=loader)

# tpl = env.get_template('zh_cn/summary.tpl')
# print(tpl.render(seq=['hoss', 'chao']))

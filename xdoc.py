#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright 2020 Loopring Org. All Rights Reserved.

__author__ = 'chao@loopring.org (Ma Chao)'

import http.client
import json
import logging
import os
import re
import subprocess

from functools import partial
from jinja2 import Environment, FileSystemLoader


logging.basicConfig(level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

LOGGER = logging.getLogger(__name__)

PURGE_DIR = '.generated'
OUTPUT_DIR = 'generated'
PURGE_IGNORE = ['swp', 'py', 'generated', '.generated', '.git', 'docs', '_book',
                'README.md', '.gitignore', 'build.sh', 'meta', 'tpl', 'i18n']
OUTPUT_IGNORE = ['_book', 'docs', 'node_modules']

SWAGGER_JSON_BASE = 'api.loopring.io'
# TODO(hoss): Change this to http://api.loopring.io/api after released.
SWAGGER_JSON_PATH = '/swagger.json'

VARS = None


def run_command_with_return_info(cmd):
    try:
        return (True, subprocess.check_output([cmd], shell = True))
    except:
        LOGGER.error('Command %s failed.'%(cmd))
        return (False, None)

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


def copy_static_files():
    run_command_with_return_info('cp ./.bookignore %s'%(PURGE_DIR))
    run_command_with_return_info('cp ./LANGS.md %s'%(PURGE_DIR))
    run_command_with_return_info('cp ./book.json %s'%(PURGE_DIR))

def parse_model(name, modelInfo):
    model = {}
    model['type'] = modelInfo['type']
    required = []
    properties = []
    if (modelInfo.get('required') is not None):
        required = modelInfo['required']
    if (modelInfo.get('properties') is not None):
        propjson = modelInfo['properties']
        for prop in propjson.keys():
            property_ = {}
            property_['name'] = prop
            if prop in required:
                property_['required'] = True
            else:
                property_['required'] = False

            if (propjson[prop].get('$ref') is not None):
                property_['ref'] = propjson[prop]['$ref']
            else:
                property_['type'] = propjson[prop]['type']
                if (property_['type'] == 'array'):
                    property_['itemType'] = propjson[prop]['items']['$ref']
                else:
                    if (propjson[prop].get('example') is not None):
                        property_['example'] = propjson[prop]['example']
                    if (propjson[prop].get('description') is not None):
                        property_['description'] = propjson[prop]['description']
            properties.append(property_)
    model['properties'] = properties
    return model

def parse_api(path, apiInfo):
    api = {}
    api['path'] = path
    api['method'] = list(apiInfo.keys())[0]
    rawInfo = list(apiInfo.values())[0]
    api['operationId'] = rawInfo['operationId']
    api['description'] = rawInfo['description']
    api['summary'] = rawInfo['summary']
    return api

def load_api_desc(lang):
    # TODO(hoss): Change this function
    inf = open('./meta/swagger.json')
    swagger = json.loads(inf.read())
    inf.close()
    # Uncomment this when everythis is done
    # conn = http.client.HTTPSConnection(SWAGGER_JSON_BASE)
    # conn.request("GET", SWAGGER_JSON_PATH + '?hl=%s'%(lang))
    # swagger = json.loads(conn.getresponse().read())

    apis = {}

    paths = swagger['paths']

    for path in paths.keys():
        if path in VARS['enable_apis']:
            apis[path] = parse_api(path, paths[path])

    VARS['apis'] = apis

    models = {}
    definitions = swagger['definitions']

    for model in definitions.keys():
        models[model] = parse_model(model, definitions[model])

    VARS['models'] = models

def load_message(lang):
    inf = open('./i18n/messages.%s'%(lang))
    l = json.loads(inf.read())
    inf.close()
    VARS['l'] = l

def load_info_with_lang(lang):
    load_message(lang)
    load_api_desc(lang)

def generate_api_doc(path, filename):
    # TODO(hoss): TBD
    print('kakakaka')
    return os.path.join(path, filename) + '.md'

def func_replace(matched):
    value = matched.group('func')
    return eval(value)

def render_exec_func(content):
    return re.sub('<(?P<func>.+)>', func_replace, content)

def render_with_lang(lang):
    load_info_with_lang(lang)

    path = '{}/tpls/'.format(os.path.dirname(__file__))
    loader = FileSystemLoader(path)
    env = Environment(loader=loader)

    summaryTpl = env.get_template('SUMMARY.tpl')
    summary = summaryTpl.render(l = VARS['l'], apis = VARS['apis'].values())
    rendered = render_exec_func(summary)
    print(rendered)



    # TODO(hoss): TBD

def generate_structs():
    run_command_with_return_info('rm -rf %s'%(PURGE_DIR))
    run_command_with_return_info('mkdir %s'%(PURGE_DIR))
    # recursive_generate('.', PURGE_DIR, get_first_layer_nodes('.', PURGE_IGNORE))
    copy_static_files()
    for lang in VARS['langs']:
        render_with_lang(lang)

def load_info():
    global VARS
    inf = open('./meta/vars.json')
    VARS = json.loads(inf.read())
    inf.close()

def main():
    LOGGER.info('Loading info...')
    load_info()
    LOGGER.info('Creating gitbook files...')
    generate_structs()
    # LOGGER.info('Syncing gitbook files...')
    # sync_out()

if __name__ == '__main__':
    main()

#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
#
# Copyright 2020 Loopring Org. All Rights Reserved.

__author__ = 'chao@loopring.org (Ma Chao)'

import argparse
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
PURGE_IGNORE = ['swp', 'tpl']
OUTPUT_IGNORE = ['_book', 'docs', 'node_modules']

SWAGGER_JSON_PATH = '/api'

VARS = {}

path = '{}/tpls/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
ENV = Environment(loader=loader)


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
            run_command_with_return_info(
                'cp %s %s'%(fullSourcePath, fullTargetPath))
        else:
            if not os.path.exists(fullTargetPath):
                run_command_with_return_info('mkdir %s'%(fullTargetPath))
            recursive_generate(fullSourcePath, fullTargetPath,
                              os.listdir(fullSourcePath))


def copy_static_files():
    run_command_with_return_info('cp ./.bookignore %s'%(PURGE_DIR))
    run_command_with_return_info('cp ./LANGS.md %s'%(PURGE_DIR))
    run_command_with_return_info('cp ./book.json %s'%(PURGE_DIR))

def set_field(f, t, field):
    if (f.get(field) is not None):
        t[field] = f[field]

def parse_model(name, modelInfo):
    model = {}
    model['type'] = modelInfo['type']
    model['description'] = modelInfo.get('description', '')
    required = modelInfo.get('required', [])
    properties = []
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
                property_['$ref'] = propjson[prop]['$ref']
            else:
                property_['type'] = propjson[prop]['type']
                set_field(propjson[prop], property_, 'description')
                set_field(propjson[prop], property_, 'example')
                if (property_['type'] == 'array'):
                    set_field(propjson[prop]['items'], property_, '$ref')
                    if (propjson[prop]['items'].get('type') is not None):
                        property_['itemType'] = propjson[prop]['items']['type']

            properties.append(property_)
    model['properties'] = properties
    return model

def parse_params(parameters):
    params = []
    for parameter in parameters:
        p = {}
        set_field(parameter, p, 'name')
        set_field(parameter, p, 'description')
        set_field(parameter, p, 'required')
        set_field(parameter, p, 'type')
        set_field(parameter, p, 'x-example')
        if (parameter.get('schema') is not None):
            set_field(parameter['schema'], p, '$ref')
        params.append(p)
    return params

def parse_responses(responses):
    errorCodes = responses.keys()
    resps = {}
    codes = []
    for error in errorCodes:
        if (error == '0' or error == '200'):
            ret = {}
            set_field(responses[error], ret, 'description')
            if (responses[error].get('schema') is not None):
                set_field(responses[error]['schema'], ret, '$ref')
            resps['ret'] = ret
        else:
            r = {}
            r['ec'] = error
            set_field(responses[error], r, 'description')
            codes.append(r)
    resps['codes'] = codes
    return resps

def parse_api(path, apiInfo):
    api = {}
    api['path'] = path
    api['method'] = list(apiInfo.keys())[0].upper()
    rawInfo = list(apiInfo.values())[0]
    api['operationId'] = rawInfo['operationId']
    api['description'] = rawInfo['description']
    api['summary'] = rawInfo['summary']
    api['params'] = parse_params(rawInfo['parameters'])
    api['responses'] = parse_responses(rawInfo['responses'])
    return api

def load_api_desc(lang):

    inf = open('./meta/swagger_%s.json'%(lang))
    swagger = json.loads(inf.read())
    inf.close()

    apis = {}

    paths = swagger['paths']

    for path in paths.keys():
        if path in VARS['v']['enable_apis']:
            apis[path] = parse_api(path, paths[path])

    # LOGGER.info(apis)

    VARS['apis'] = apis

    models = {}
    definitions = swagger['definitions']

    for model in definitions.keys():
        models[model] = parse_model(model, definitions[model])

    # LOGGER.info(models)

    VARS['models'] = models

def load_message(lang):
    inf = open('./i18n/messages.%s'%(lang))
    l = json.loads(inf.read())
    inf.close()
    VARS['l'] = l

def load_info_with_lang(lang):
    load_message(lang)
    load_api_desc(lang)

def generate_api_doc(name, path, filename):
    apiTpl = ENV.get_template('api_doc.tpl')
    apidoc = apiTpl.render(l = VARS['l'], api = VARS['apis'][name])

    output_file(apidoc, os.path.join(
        './', PURGE_DIR, VARS['currentLang'], path, filename))

    return os.path.join(path, filename)

def func_replace(matched):
    value = matched.group('func')
    return eval(value)

def render_exec_func(content):
    return re.sub('<#(?P<func>.+)#>', func_replace, content)

def output_file(content, fullpath):
    dirpath = os.path.dirname(os.path.realpath(fullpath))
    if not os.path.exists(dirpath):
        run_command_with_return_info('mkdir -p %s'%(dirpath))

    outf = open(fullpath, 'w')
    outf.write(content)
    outf.close()

def render_with_lang(lang):
    VARS['currentLang'] = lang
    load_info_with_lang(lang)

    summaryTpl = ENV.get_template('SUMMARY.tpl')
    summary = summaryTpl.render(l = VARS['l'], apis = VARS['apis'].values())
    rSummary = render_exec_func(summary)

    output_file(rSummary, os.path.join('./', PURGE_DIR, lang, 'SUMMARY.md'))

    commonTpl = ENV.get_template('common.tpl')
    common = commonTpl.render(l = VARS['l'], v = VARS['v'])

    output_file(common, os.path.join('./', PURGE_DIR, lang, 'common.md'))

def generate_structs():
    run_command_with_return_info('rm -rf %s'%(PURGE_DIR))
    run_command_with_return_info('mkdir %s'%(PURGE_DIR))
    copy_static_files()
    for lang in VARS['v']['langs']:
        render_with_lang(lang)

    recursive_generate(
        './tpls', PURGE_DIR, get_first_layer_nodes('./tpls', PURGE_IGNORE))

def load_info():
    global VARS
    inf = open('./meta/vars.json')
    VARS['v'] = json.loads(inf.read())
    inf.close()

def build_doc():
    LOGGER.info('Loading info...')
    load_info()
    LOGGER.info('Creating gitbook files...')
    generate_structs()
    LOGGER.info('Syncing gitbook files...')
    sync_out()

def fetch_and_save_swagger_json(lang):
    conn = None

    if VARS['v']['hosturl'].startswith('https://'):
        host = VARS['v']['hosturl'].replace('https://', '')
        conn = http.client.HTTPSConnection(host)
    else:
        host = VARS['v']['hosturl'].replace('http://', '')
        conn = http.client.HTTPConnection(host)

    LOGGER.info('Fetching swagger.json with lang %s...'%(lang))
    conn.request("GET", SWAGGER_JSON_PATH + '?hl=%s'%(lang))
    swagger = json.dumps(json.loads(conn.getresponse().read()))

    LOGGER.info('Writing swagger.json with lang %s...'%(lang))
    output_file(swagger, './meta/swagger_%s.json'%(lang))

def refresh_swagger():
    LOGGER.info('Loading info...')
    load_info()
    for lang in VARS['v']['langs']:
        fetch_and_save_swagger_json(lang)

def main():
    """Main for xdoc"""

    parser = argparse.ArgumentParser(description = 'This tool is used for' +
                                     ' generating API docs (gitbook hosted).',
                                     fromfile_prefix_chars = '@')
    parser.add_argument('command', type = str, default = 'build',
                        choices = ['build', 'refresh'])

    args = parser.parse_args()

    if args.command == 'build':
        build_doc()
    elif args.command == 'refresh':
        refresh_swagger()
    else:
        build_doc()

if __name__ == '__main__':
    main()

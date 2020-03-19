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

INDENT = 4
SEG_SIZE = 20


def get_request_parames(params, method):
    if method == 'GET':
        return params
    elif method == 'POST':
        modelName = params[0]['$ref']
        return VARS['models'][modelName]['properties']
    else:
        return params

def get_response_fields(response):
    modelName = response['$ref']
    return VARS['models'][modelName]['properties']

def create_html_type(field):
    # if (field.get('type') is None or field['type'] == 'object'):
    if (field.get('type') is None):
        if (field.get('$ref') is not None):
            cleanRef = field['$ref']
            return '<a href="#%s">%s</a>'%(cleanRef, cleanRef)
        else:
            return '/'
    else:
        if (field['type'] == 'array'):
            cleanRef = ''
            if (field.get('$ref') is not None):
                cleanRef = field['$ref']
                return 'list< <a href="#%s">%s</a> >'%(cleanRef, cleanRef)
            else:
                return 'list< %s >'%(field['itemType'])
        elif (field.get('$ref') is not None):
            cleanRef = field['$ref']
            return '<a href="#%s">%s</a>'%(cleanRef, cleanRef)
        else:
            return field['type']

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

def set_field(f, t, field, tField = None, segSize = SEG_SIZE,
              showMsgIfMiss = False, message = None):
    if (f.get(field) is not None):
        if (tField is None):
            tField = field
        t[tField] = f[field]
        if (field == '$ref'):
            t[tField] = t[tField].replace('#/definitions/', '')
        elif (field == 'example' or field == 'x-example' or field == 'description'):
            if isinstance(t[tField], bool):
                t[tField] = str(t[tField]).lower()
            elif (t[tField] == 0):
                t[tField] = '0'
            if (isinstance(t[tField], str)):
                t[tField] = modify_str(t[tField], segSize)
        return
    if (showMsgIfMiss):
        if message is None:
            LOGGER.error('%s has no %s'%(f, field))
        else:
            LOGGER.error(message)

# This function is used to seg long word
# for better shown in markdown table cell.
def seg_str(word, segSize):
    length = len(word)
    if (length < segSize):
        return word
    segs = []
    i = 0
    while (i < length):
        segs.append(word[i : i + segSize])
        i += segSize
    return '<br/>'.join(segs)

def modify_str(content, segSize):
    words = content.split(' ')
    return ' '.join([seg_str(word, segSize) for word in words])

def parse_model(name, modelInfo):
    model = {}
    model['name'] = name
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

            set_field(propjson[prop], property_, '$ref')
            set_field(propjson[prop], property_, 'type',
                showMsgIfMiss = (property_.get('$ref') is None),
                message = 'Must set $ref or type for %s of %s'%(prop, name))
            set_field(propjson[prop], property_, 'description')
            set_field(propjson[prop], property_, 'example',
                showMsgIfMiss = (property_.get('type') is not None
                                 and property_['type'] != 'array'
                                 and property_['type'] != 'object'),
                message = '%s of %s has no example'%(prop, name))
            if (property_.get('type') is not None and
                property_['type'] == 'array'):
                set_field(propjson[prop]['items'], property_, '$ref')
                if (propjson[prop]['items'].get('type') is not None):
                    property_['itemType'] = propjson[prop]['items']['type']
                    if (property_.get('example') is None):
                        LOGGER.error('%s of %s has no example.'%(prop, name))
                if (property_.get('$ref') is None
                    and property_.get('itemType') is None):
                    LOGGER.error('%s of %s miss $ref or itemType'%(prop, name))

            properties.append(property_)
    model['properties'] = properties
    return model

def parse_params(parameters):
    params = []
    refs = []
    for parameter in parameters:
        p = {}
        set_field(parameter, p, 'name', showMsgIfMiss = True)
        set_field(parameter, p, 'description', showMsgIfMiss = True)
        set_field(parameter, p, 'required', showMsgIfMiss = True)
        set_field(parameter, p, 'type', showMsgIfMiss = True)
        set_field(parameter, p, 'x-example', 'example', showMsgIfMiss = True)
        if (parameter.get('schema') is not None):
            set_field(parameter['schema'], p, '$ref', showMsgIfMiss = True)
            refs.append(p['$ref'])
        params.append(p)
    return (params, refs)

def parse_responses(responses):
    errorCodes = responses.keys()
    resps = {}
    codes = []
    refs = []
    for error in errorCodes:
        if (error == '0' or error == '200'):
            ret = {}
            set_field(responses[error], ret, 'description',
                      showMsgIfMiss = True)
            if (responses[error].get('schema') is not None):
                set_field(responses[error]['schema'], ret, '$ref',
                          showMsgIfMiss = True)
                refs.append(ret['$ref'])
            resps['ret'] = ret
        else:
            r = {}
            r['ec'] = error
            set_field(responses[error], r, 'description', segSize = 100,
                      showMsgIfMiss = True)
            codes.append(r)
    resps['codes'] = codes
    return (resps, refs)

def parse_api(path, apiInfo):
    api = {}
    api['path'] = path
    api['method'] = list(apiInfo.keys())[0].upper()
    rawInfo = list(apiInfo.values())[0]
    api['operationId'] = rawInfo['operationId']
    set_field(rawInfo, api, 'description')
    set_field(rawInfo, api, 'summary', showMsgIfMiss = True,
              message = 'API %s has no summary'%(path))
    # api['summary'] = rawInfo['summary']
    (api['params'], reqRefs) = parse_params(rawInfo['parameters'])
    (api['responses'], resRefs) = parse_responses(rawInfo['responses'])
    api['refs'] = reqRefs + resRefs
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

def prop_to_json(prop, spaceNum):
    valStr = ''
    if (prop.get('type') is None):
        valStr = model_to_json(
            prop['$ref'],
            spaceNum).lstrip()
    else:
        if (prop['type'] == 'string'):
            valStr = '"%s"'%(prop.get('example', ''))
        else:
            if (prop.get('example') is not None):
                valStr = prop['example']
            elif (prop['type'] == 'object'):
                valStr = model_to_json(
                    prop['$ref'],
                    spaceNum).lstrip()
            elif (prop['type'] == 'array'):
                valStr = '[\n'
                if (prop.get('$ref') is not None):
                    valStr += model_to_json(
                        prop['$ref'],
                        spaceNum + INDENT) + '\n'
                else:
                    valStr += ' ' * (spaceNum + INDENT) + prop['itemType'] + '\n'
                valStr += ' ' * spaceNum + ']'
            else:
                valStr = prop['type']
    return ' ' * spaceNum + '"%s"'%(prop['name']) + ' : ' + str(valStr)

def model_to_json(modelName, spaceNum = 0):
    model = VARS['models'][modelName]
    ret = ' ' * spaceNum + '{\n'
    ret += prop_to_json(model['properties'][0], spaceNum + INDENT)
    for prop in model['properties'][1:]:
        ret += ',\n'
        ret += prop_to_json(prop, spaceNum + INDENT)
    ret += '\n' + ' ' * spaceNum + '}'
    return ret

def create_response_example(api):
    return model_to_json(api['responses']['ret']['$ref'])

def create_request_example(api):
    ret = 'curl %s%s'%(VARS['v']['hosturl'], api['path'])
    param = ''
    if (api['method'] == 'GET'):
        for p in api['params']:
            param += p['name'] + '=' + str(p['example']) + '&'
        if (param == ''):
            return ret
        else:
            return ret + '?' + param[0: -1]
    elif (api['method'] == 'POST'):
        payload = model_to_json(
            api['params'][0]['$ref'])
        if (payload == ''):
            return ret
        else:
            return ret + ' -X POST -H "Content-Type:application/json" -d \\\n\'%s\''%(payload)

def expend_models(modelName):
    modelNames = []
    for prop in VARS['models'][modelName]['properties']:
        if prop.get('$ref') is not None:
            name = prop.get('$ref')
            modelNames.append(name)
            modelNames += expend_models(name)
    return modelNames


def get_ref_models(api):
    modelNames = []
    for ref in api['refs']:
        m = VARS['models'][ref]
        for prop in m['properties']:
            if prop.get('$ref') is not None:
                name = prop.get('$ref')
                modelNames.append(name)
                modelNames += expend_models(name)
    ret = [VARS['models'][x] for x in modelNames if x != 'ResultInfo' ]
    return ret

def get_description(api):
    if (api.get('description') is not None and api['description'] != ''):
        return api['description']
    descFilePath = os.path.join('./tpls', VARS['currentLang'], 'segments',
        api['operationId'] + '_desc.md')
    if os.path.exists(descFilePath):
        return '{% include "../segments/' + api['operationId'] + '_desc.md" %}'
    else:
        LOGGER.error('API %s has no description.'%(api['operationId']))
        return '/'


def generate_api_doc(name, path, filename):
    apiTpl = ENV.get_template('api_doc.tpl')
    apidoc = apiTpl.render(
        l = VARS['l'],
        api = VARS['apis'][name],
        c_type = create_html_type,
        c_request_example = create_request_example,
        g_response_fields = get_response_fields,
        g_request_params = get_request_parames,
        c_response_example = create_response_example,
        g_ref_models = get_ref_models,
        g_desc = get_description)

    output_file(apidoc, os.path.join(
        './', PURGE_DIR, VARS['currentLang'], path, filename + '.md'))

    return os.path.join(path, filename + '.md')

def func_replace(matched):
    value = matched.group('func')
    return eval(value)

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
    summary = summaryTpl.render(
        l = VARS['l'],
        apis = VARS['apis'].values(),
        g_api_doc = generate_api_doc)

    output_file(summary, os.path.join('./', PURGE_DIR, lang, 'SUMMARY.md'))

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
    parser.add_argument('command', type = str, nargs = '+', default = 'build',
                        choices = ['build', 'refresh'])

    args = parser.parse_args()

    if 'refresh' in args.command:
        refresh_swagger()
    if 'build' in args.command:
        build_doc()

if __name__ == '__main__':
    main()

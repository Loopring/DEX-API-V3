[//]: # ({{ l.comment.claim }})

## {{api.summary}}
{% set tps = g_tps(api) %}
{{l.apidoc.throttle}}: {{tps.count}} {{l.apidoc.every}}
{%- if tps.interval == 1 %}
{{l.apidoc.second}}
{%- else %}
{{tps.interval}} {{l.apidoc.seconds}}
{% endif %}

### {{ l.apidoc.overview }}
----

#### {{ l.apidoc.method }}

**{{ api.method }}**

#### {{ l.apidoc.path }}

**{{ api.path }}**

#### {{ l.apidoc.function }}

{{ g_desc(api) }}


### {{ l.apidoc.desc }}
----

#### {{ l.apidoc.header }}

{% set headers = g_request_headers(api.operationId) %}
{% if headers|length == 0 %}
{{l.apidoc.none}}
{% else %}
| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :---- | :---- | :---- |   :----   |  :--- |
{%- for header in headers %}
{%- if header == 'X-API-KEY' %}
| X-API-KEY | string | {{ l.apidoc.yes }} | {{ l.apidoc.keydesc }} | "HlkcGxbqBeaF76j4rvPaOasyfPwnkQ<br/>6B6DQ6THZWbvrAGxzEdulXQvOKLrRW<br/>ZLnN" |
{%- endif -%}
{%- if header == 'X-EDDSA-SIG' %}
| X-API-SIG | string | {{ l.apidoc.yes }} | {{ l.apidoc.eddsa_header_sigdesc }} | "0xeb14773e8a07d19bc4fe56e36d041dcb<br>0026bf21e05c7652f7e92160deaf5ea9<br>c4fe56e34773e86d041dcbeb1a07d19b<br>002652f7e92160deaf5e6bf21e05c7a9<br>002652f7e92160deaf5e6bf21e05c7a9<br>eb14773e8a07d19bc4fe56e36d041dcb" |
{%- endif -%}
{%- if header == 'X-ECDSA-SIG' %}
| X-API-SIG | string | {{ l.apidoc.yes }} | {{ l.apidoc.ecdsa_header_sigdesc }} | "0xccf0a141fce2dc5cbbd4f802c52220e9<br>e2ce260e86704d6258603eb346eefe2d<br>4a450005c362b223b28402d087f7065e<br>a5eee0314531adf6a580fce64c25dca81c02" |
{%- endif -%}
{% endfor %}
{% endif %}

#### {{ l.apidoc.reqparam }}

{% set fields = g_request_params(api.params, api.method) %}
{% if fields|length > 0 %}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :---- | :---- | :---- | :---- | :--- |
{%- for field in fields %}
| {{field.name}} | {{c_type(field)}} |
{%- if field.required -%}
{{l.apidoc.yes}}
{%- else -%}
{{l.apidoc.no}}
{%- endif -%}
| {{field.description}}
{%- if field.default -%}
<br/>{{l.apidoc.default}} : {{ field.default }}
{%- endif -%}
{%- if field.enum -%}
<br/>{{l.apidoc.allow}} : {{ field.enum }}
{%- endif -%}
| {{ g_example(field['example']) }} |
{%- endfor %}
{% else %}
{{l.apidoc.none}}
{% endif %}

#### {{ l.apidoc.reqexpl }}

{% raw %}
{% codetabs name="HTTP", type="http" -%}
{% endraw %}
{{c_request_http_example(api)}}
{% raw %}
{%- language name="CURL", type="bash" -%}
{% endraw %}
{{c_request_curl_example(api)}}
{% raw %}
{%- endcodetabs %}
{% endraw %}

#### {{ l.apidoc.resfield }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :---- | :---- | :---- | :---- | :--- |
{%- for field in g_response_fields(api.responses.ret) %}
| {{field.name}} | {{c_type(field)}} |
{%- if field.required -%}
{{l.apidoc.yes}}
{%- else -%}
{{l.apidoc.no}}
{%- endif -%}
| {{field.description}}
{%- if field.default -%}
<br/>{{l.apidoc.default}} : {{ field.default }}
{%- endif -%}
{%- if field.enum -%}
<br/>{{l.apidoc.allow}} : {{ field.enum }}
{%- endif -%}
| {{ g_example(field['example']) }} |
{%- endfor %}

#### {{ l.apidoc.resexpl }}

``` json
{{c_response_example(api)}}
```

#### {{ l.apidoc.retcode }}

| {{ l.apidoc.value }} | {{ l.apidoc.codedesc }} |
| :---- | :---- |
{%- for code in api.responses.codes %}
|{{code.ec}}|{{code.description}}|
{%- endfor %}

{% set models = g_ref_models(api) %}
{% if models|length > 0 %}
### {{ l.apidoc.model }}
----

{% for model in models %}
#### {{model.name}}
<span id="{{model.name}}"></span>
{%- if model.description != '' -%}
{{model.description}}
{%- endif %}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :---- | :---- | :---- | :---- | :--- |
{%- for field in model.properties %}
| {{field.name}} | {{c_type(field)}} |
{%- if field.required -%}
{{l.apidoc.yes}}
{%- else -%}
{{l.apidoc.no}}
{%- endif -%}
| {{field.description}}
{%- if field.default -%}
<br/>{{l.apidoc.default}} : {{ field.default }}
{%- endif -%}
{%- if field.enum -%}
<br/>{{l.apidoc.allow}} : {{ field.enum }}
{%- endif -%}
| {{ g_example(field['example']) }} |
{%- endfor %}

{% endfor %}
{% endif %}

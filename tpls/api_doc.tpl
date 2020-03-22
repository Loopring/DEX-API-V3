[//]: # ({{ l.comment.claim }})

## {{api.summary}}

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
| :----: | :----: | :----: |   :----:   |  :---: |
{%- for header in headers %}
{%- if header == 'X-API-KEY' %}
| X-API-KEY | string | {{ l.apidoc.yes }} | {{ l.apidoc.keydesc }} | "sra1aavfa" |
{%- endif -%}
{%- if header == 'X-API-SIG' %}
| X-API-SIG | string | {{ l.apidoc.yes }} | {{ l.apidoc.sigdesc }} | "dkkfinfasdf" |
{%- endif -%}
{% endfor %}
{% endif %}

#### {{ l.apidoc.reqparam }}

{% set fields = g_request_params(api.params, api.method) %}
{% if fields|length > 0 %}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :----: | :----: | :----: | :----: | :---: |
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
| :----: | :----: | :----: | :----: | :---: |
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

| {{ l.apidoc.retcode }} | {{ l.apidoc.codedesc }} |
| :----: | :----: |
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
| :----: | :----: | :----: | :----: | :---: |
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

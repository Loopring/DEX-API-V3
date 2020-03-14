[//]: # ({{ l.comment.claim }})

## {{api.summary}}

### {{ l.apidoc.overview }}
----

#### {{ l.apidoc.function }}

{{ api.description }}

#### {{ l.apidoc.method }}

**{{ api.method }}**

#### {{ l.apidoc.path }}

**{{ api.path }}**

### {{ l.apidoc.desc }}
----

#### {{ l.apidoc.reqparam }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- | ---- | --- |
{%- for field in g_request_params(api.params, api.method) %}
| {{field.name}} | {{c_type(field)}} |
{%- if field.required -%}
{{l.apidoc.yes}}
{%- else -%}
{{l.apidoc.no}}
{%- endif -%}
| {{field.description}} |
{%- if field['example'] -%}
{{field['example']}} |
{%- else -%}
/ |
{%- endif -%}
{%- endfor %}

#### {{ l.apidoc.reqexpl }}

``` bash
{{c_request_example(api)}}
```

#### {{ l.apidoc.resfield }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- | ---- | --- |
{%- for field in g_response_fields(api.responses.ret) %}
| {{field.name}} | {{c_type(field)}} |
{%- if field.required -%}
{{l.apidoc.yes}}
{%- else -%}
{{l.apidoc.no}}
{%- endif -%}
| {{field.description}} |
{%- if field['example'] -%}
{{field['example']}} |
{%- else -%}
/ |
{%- endif -%}
{%- endfor %}

#### {{ l.apidoc.resexpl }}

``` json
{{c_response_example(api)}}
```

#### {{ l.apidoc.retcode }}

| {{ l.apidoc.retcode }} | {{ l.apidoc.codedesc }} |
| ---- | ---- |

TBD

### {{ l.apidoc.model }}
----

TBD

{% raw %}
{% include "../common.md" %}
{% endraw %}

{{api.method}} {{api.pathWithParams}} HTTP/1.1
Host: {{api.hosturl}}
Connection: keep-alive
Accept: */*
Accept-Encoding: gzip, deflate, br
Accept-Language: zh,en;q=0.9
{%- for header in api.headers  %}
{{header.key}}: {{header.value}}
{%- endfor %}
{% if api.method == 'POST' %}
{{ api.payload }}
{%- endif -%}

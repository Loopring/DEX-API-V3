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
{% for param in api.params %}
| | | | | |
TBD
{% endfor %}

#### {{ l.apidoc.reqexpl }}

TBD

#### {{ l.apidoc.resfield }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- | ---- | --- |

TBD

#### {{ l.apidoc.resexpl }}

TBD

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

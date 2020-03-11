## {{ l.apidoc.common }}
----

### {{ l.apidoc.urlhost }}

**https://api.loopring.io**

### {{ l.apidoc.header }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- |   ----   |  --- |
| X-API-KEY | string | {{ l.apidoc.no }} | {{ l.apidoc.keydesc }} | "sra1aavfa" |
| X-API-SIG | string | {{ l.apidoc.no }} | {{ l.apidoc.sigdesc }} | "dkkfinfasdf" |

### {{ l.apidoc.resp }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- | ---- | ---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | {{ l.apidoc.yes }} | {{ l.apidoc.resdesc }} | / |

### {{ l.apidoc.retcode }}
| {{ l.apidoc.retcode }} | {{ l.apidoc.codedesc }} |
| ---- | ---- |
| 0 | {{ l.apidoc.code0 }} |
| 100000 | {{ l.apidoc.code1000000 }} |
| 100001 | {{ l.apidoc.code1000001 }} |

### 模型

### ResultInfo
<span id="ResultInfo"></span>

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- |   ----   |  --- |
| code | number | {{ l.apidoc.yes }} | {{ l.apidoc.retcode }} | 0 |
| message | string | {{ l.apidoc.yes }} | {{ l.apidoc.retmsg }} | "SUCCESS" |

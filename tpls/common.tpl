### {{ l.apidoc.common }}
----

#### {{ l.apidoc.hosturl }}

**{{ v.hosturl }}**

#### {{ l.apidoc.header }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- |   ----   |  --- |
| X-API-KEY | string | {{ l.apidoc.no }} | {{ l.apidoc.keydesc }} | "sra1aavfa" |
| X-API-SIG | string | {{ l.apidoc.no }} | {{ l.apidoc.sigdesc }} | "dkkfinfasdf" |

#### {{ l.apidoc.resp }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- | ---- | ---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | {{ l.apidoc.yes }} | {{ l.apidoc.resdesc }} | / |

#### {{ l.apidoc.retcode }}
| {{ l.apidoc.retcode }} | {{ l.apidoc.codedesc }} |
| ---- | ---- |
| 0 | {{ l.apidoc.code0 }} |
| 100000 | {{ l.apidoc.code1000000 }} |
| 100001 | {{ l.apidoc.code1000001 }} |
| 100002 | {{ l.apidoc.code1000002 }} |
| 100202 | {{ l.apidoc.code1000202 }} |
| 100203 | {{ l.apidoc.code1000203 }} |
| 100204 | {{ l.apidoc.code1000204 }} |

#### 模型

##### ResultInfo
<span id="ResultInfo"></span>

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| ---- | ---- | ---- |   ----   |  --- |
| code | integer | {{ l.apidoc.yes }} | {{ l.apidoc.retcode }} | 0 |
| message | string | {{ l.apidoc.yes }} | {{ l.apidoc.retmsg }} | "SUCCESS" |

---

## {{ l.apidoc.common }}

### {{ l.apidoc.hosturl }}

**{{ v.hosturl }}**

### {{ l.apidoc.header }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :---- | :---- | :---- |   :----   |  :--- |
| X-API-KEY | string | {{ l.apidoc.no }} | {{ l.apidoc.keydesc }} | "HlkcGxbqBeaF76j4rvPaOasyfPwnkQ<br/>6B6DQ6THZWbvrAGxzEdulXQvOKLrRW<br/>ZLnN" |
| X-API-SIG | string | {{ l.apidoc.no }} | {{ l.apidoc.sigdesc }} | "138345244293157165270722452892<br/>010987433674489288289416943333<br/>00773464291931668,192524381644<br/>249809013234960675797674572982<br/>626096331826549685003177960107<br/>94338,129650216991857917204601<br/>962488677667247381368354153200<br/>8712357317204831986826" |

### {{ l.apidoc.resp }}

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :---- | :---- | :---- | :---- | :---- |
| resultInfo | <a href="#ResultInfo">ResultInfo</a> | {{ l.apidoc.yes }} | {{ l.apidoc.resdesc }} | - |

#### ResultInfo
<span id="ResultInfo"></span>

| {{ l.apidoc.field }} |  {{ l.apidoc.ftype }} | {{ l.apidoc.frequire }} | {{ l.apidoc.fdesc }} | {{ l.apidoc.fsample }} |
| :---- | :---- | :---- |   :----   |  :--- |
| code | integer | {{ l.apidoc.yes }} | {{ l.apidoc.retcode }} | 0 |
| message | string | {{ l.apidoc.yes }} | {{ l.apidoc.retmsg }} | "SUCCESS" |


### {{ l.apidoc.retcode }}
| {{ l.apidoc.retcode }} | {{ l.apidoc.codedesc }} |
| :---- | :---- |
| 0 | {{ l.apidoc.code0 }} |
| 100000 | {{ l.apidoc.code1000000 }} |
| 100001 | {{ l.apidoc.code1000001 }} |
| 100002 | {{ l.apidoc.code1000002 }} |
| 100202 | {{ l.apidoc.code1000202 }} |
| 100203 | {{ l.apidoc.code1000203 }} |
| 100204 | {{ l.apidoc.code1000204 }} |


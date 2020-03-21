# Summary

## {{ l.summary.chapter1.title }}

* [{{ l.summary.chapter1.session1 }}](README.md)
* [{{ l.summary.chapter1.session2 }}](GLOSSORY.md)

## {{ l.summary.chapter2.title }}

* [{{ l.summary.chapter2.session1.title }}](dex_integration_overview.md)
    {** [{{ l.summary.chapter2.session1.sub1.title }}]()*}
        {** [{{ l.summary.chapter2.session1.sub1.subsub1 }}](dex_integrations/register.md)*}
        {** [{{ l.summary.chapter2.session1.sub1.subsub2 }}](dex_integrations/deposit.md)*}
    * [{{ l.summary.chapter2.session1.sub2 }}]()
* [{{ l.summary.chapter2.session2.title }}](dex_api_overview.md)
    * [{{ l.summary.chapter2.session2.sub1 }}](restful_api_overview.md)
        {% for api in apis %}
        * [{{ api.summary }}]({{g_api_doc(api.operationId, "dex_apis", api.operationId)}})
        {% endfor %}
    * [{{ l.summary.chapter2.session2.sub2 }}](websocket/overview.md)
        * [{{l.websocket.depth}}](websocket/depth.md)
        * [{{l.websocket.depth10}}](websocket/depth10.md)
        * [{{l.websocket.trade}}](websocket/trade.md)
        * [{{l.websocket.ticker}}](websocket/ticker.md)
        * [{{l.websocket.candleStick}}](websocket/candleStick.md)
        * [{{l.websocket.account}}](websocket/account.md)
        * [{{l.websocket.order}}](websocket/order.md)
{*## {{ l.summary.chapter3.title }}*}

{** [{{ l.summary.chapter3.session1 }}](wallet_integration_overview.md)*}
{** [{{ l.summary.chapter3.session2 }}](wallet_api_overview.md)*}

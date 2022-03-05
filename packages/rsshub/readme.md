# RssHub 路由格式化工具:

- RssHub 路由格式化工具
- 方便快速批量生成订阅路由
- RssHub 有固定的路由前缀规则, 但是从各种第三方服务获取的 URL 是另一种格式.
- 提供一个脚本工具, 批量格式化转换成符合 RssHub 路由规则的 URL

## 支持的订阅类型:

- telegram channel
  - 
- YouTube channel
    - https://docs.rsshub.app/social-media.html#youtube-pin-dao
    - 路由: /youtube/channel/:id/:disableEmbed?
- twitter:
    - https://docs.rsshub.app/social-media.html#twitter
    - 路由: /twitter/user/:id/:routeParams?
- v2ex:
    - https://docs.rsshub.app/bbs.html#v2ex
- wechat:
    - https://docs.rsshub.app/new-media.html#wei-xin

> 订阅服务: 提供微信公众号 RSS 订阅服务

- https://weixin.sogou.com/
- https://feeddd.org/feeds
    - 搜索微信公众号
- https://search.careerengine.us/
- https://github.com/fritx/awesome-wechat

> 18+

- 1024:
    - https://docs.rsshub.app/multimedia.html#cao-liu-she-qu
- https://docs.rsshub.app/multimedia.html#s-hentai

```ruby


https://rsshub.app/cool18/bbs6
https://rsshub.app/ehentai/tag/language:chinese/1


```

## reference:

- https://pro.autojs.org/
- https://hamibot.com/marketplace/vLSBc


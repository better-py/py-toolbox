# discord 工具:

> 说明:

- ✅消息归档助手: discord 群 channel 归档后, 把channel 内的历史消息, 转发到 目标 thread 下.

> 文档: 

- ✅https://github.com/hhstore/blog/issues/388

## 准备工作:

> 创建 bot:

- https://imyq.co/discord-bot-dev/

> 把本 bot 添加到目标群:

- 此处 bot 要求了最高权限, 只是为了偷懒, 代码里没有脏东西.(后续再逐步改为正常权限)
- bot 邀请链接:
    - https://discord.com/api/oauth2/authorize?client_id=1018558452529909791&permissions=8&scope=bot

## 使用方式:

- 运行:

```ruby
# way1:
cd toolbox/
task discord:run

# way2:
cd packages/discord-cli/
task run

```

## reference:

> libs:

- https://github.com/Rapptz/discord.py
    - https://discordpy.readthedocs.io/en/latest/
    - https://discordpy.readthedocs.io/en/latest/quickstart.html
    - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html
    - https://discordpy.readthedocs.io/en/latest/interactions/api.html

> discord api:

- https://discord.com/developers/docs/intro
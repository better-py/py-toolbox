import os
from collections.abc import Sequence
from typing import Any, List
import click
import discord
from discord import File
from discord.ext import commands


class DisMateBot(commands.Bot):
    """
    :ref: https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html

    """

    async def on_ready(self):
        """成功启动, 会打印如下信息, 否则失败

        :return:
        """
        print('Discord Bot<DisMate> Logged in as:')
        print(self.user.name)
        print(self.user.id)
        print('------')

        #
        # setup cmds:
        #
        await self.setup_cmds()

    async def on_error(self, event_method: str, /, *args: Any, **kwargs: Any) -> None:
        await self.on_error(event_method, *args, **kwargs)
        print(f"on error: {event_method}")

    ##########################################################################################

    async def setup_cmds(self):
        """注册所有 bot 命令: 所有新增 CMD, 都需要在此函数内添加子函数.
        (discord.py 这个包模块设计有点蠢, 不影响使用)

        :return:
        """

        @self.command()
        async def echo(ctx):
            """测试: 输出你好

            :param ctx:
            :return:
            """
            print('greet here!')
            await ctx.send(":smiley: :wave: Hello, there!")

        @self.command()
        async def hello(ctx):
            """测试: 输出你好

            :param ctx:
            :return:
            """
            print('greet here!')
            await ctx.send(":smiley: :wave: Hello, there!")

        @self.command()
        async def add(ctx, a: int, b: int):
            """计算器 - 加法: [输入示例: $add 22 33]

            :param ctx:
            :param a:
            :param b:
            :return:
            """
            await ctx.send(a + b)

        @self.command()
        async def multiply(ctx, a: int, b: int):
            """计算器 - 乘法: [输入示例: $multiply 22 33]

            :param ctx:
            :param a:
            :param b:
            :return:
            """
            await ctx.send(a * b)

        @self.command()
        async def cat(ctx):
            """发送一个 gif 图片

            :param ctx:
            :return:
            """
            await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

        @self.command()
        async def all_channels(ctx):
            """查询所有频道 [输入示例: $all_channels]

            :输入示例: $all_channels
            :param ctx:
            :return:
            """
            embed = discord.Embed(title="all channels", description="group channels:", color=0xeee657)

            result = self.get_all_channels()

            i = 0
            for item in result:
                v = f"guid={item.guild}, name={item.name}, id={item.id}, category_id={item.category_id}"

                print(f"chan: {v}")
                embed.add_field(name="chan: ", value=v)

                if i % 30 == 0:
                    # 每30个, 发送一条消息
                    await ctx.send(embed=embed)
                    embed.clear_fields()

                i += 1

        @self.command()
        async def all_groups(ctx):
            """查询全部群信息. [输入示例: $all_groups]

            :输入示例: $all_groups
            :param ctx:
            :return:
            """
            embed = discord.Embed(title="all guilds:", description="group guilds:", color=0xeee657)

            async for item in self.fetch_guilds():
                v = f"id={item.id}, name={item.name}, {item.owner_id}"
                print(f"group: {v}")

                embed.add_field(name="group: ", value=v)
                await ctx.send(embed=embed)
                embed.clear_fields()

        @self.command()
        async def group(ctx, group_id: int):
            """查询指定群的元信息: 包括 chan 列表 和 thread 列表.[输入示例: $group 996337248964456469]

            :输入示例: $group 996337248964456469
            :param ctx:
            :param group_id:
            :return:
            """
            embed = discord.Embed(title=f"group: {group_id}", description="metadata:", color=0xeee657)

            result = self.get_guild(group_id)
            print(f"group info: {result.channels}")

            embed.add_field(name="meta", value=result)

            for chan in result.channels:
                embed.add_field(name=f"chan {chan.id}", value=f"{chan.name}, {chan.category_id}")
            for thr in result.threads:
                embed.add_field(name=f"thread {thr.id}", value=f"{thr.name}, {thr.parent}")
            await ctx.send(embed=embed)

        @self.command()
        async def channel(ctx, channel_id: int):
            """获取单个频道信息.(命令别名) [输入示例: $chan 877037968701939753]

            :输入示例: $chan 877037968701939753
            :param ctx:
            :param channel_id:
            :return:
            """
            await channel_by_id(ctx, channel_id)

        @self.command()
        async def channel_by_id(ctx, channel_id: int):
            """获取单个频道信息. [输入示例: $channel_by_id 877037968701939753]

            :输入示例: $channel_by_id 877037968701939753
            :param ctx:
            :param channel_id:
            :return:
            """
            embed = discord.Embed(title=f"channel: {channel_id}", description="metadata", color=0xeee657)

            chan = self.get_channel(channel_id)

            # print:
            v = f"name: {chan.id}, {chan.name}, {chan.category_id}, {chan.guild}, {chan.threads}"
            print(f"channel info: {v}")

            embed.add_field(name="name", value=chan.name)
            embed.add_field(name="id", value=chan.id)
            embed.add_field(name="category id", value=chan.category_id)
            embed.add_field(name="guild", value=chan.guild)
            embed.add_field(name="threads", value=chan.threads)

            for tr in chan.threads:
                embed.add_field(name=f"thread: {tr.name}", value=f"id={tr.id}")

            await ctx.send(embed=embed)

        @self.command()
        async def migrate(ctx, from_chan_id: int, to_chan_id: int, to_thread_id: int):
            """频道历史消息迁移, [从 A channel 迁移到 B channel 下的 C thread 中].

            :示例: $migrate 996337249404862547 996337249404862548 1018957028795875389
            :param ctx:
            :param from_chan_id:
            :param to_chan_id:
            :param to_thread_id:
            :return:
            """
            await migrate_channel_to_thread(ctx, from_chan_id, to_chan_id, to_thread_id)

        @self.command()
        async def migrate_channel_to_thread(ctx, from_chan_id: int, to_chan_id: int, to_thread_id: int):
            """频道历史消息迁移, [从 A channel 迁移到 B channel 下的 C thread 中].

            :示例: $migrate 996337249404862547 996337249404862548 1018957028795875389
            :param ctx:
            :param from_chan_id:
            :param to_chan_id:
            :param to_thread_id:
            :return:
            """
            embed = discord.Embed(
                title=f"migrate: {from_chan_id} ",
                description=f"migrate chan messages to thread {to_thread_id}",
                color=0xeee657,
            )

            from_chan = self.get_channel(from_chan_id)
            to_chan = self.get_channel(to_chan_id)
            to_thread = to_chan.get_thread(to_thread_id)

            print(f"from channel: {from_chan}, to channel: {to_chan}, to thread: {to_thread}")

            # todo x: 关键参数(最后一条消息的 ID), 用于迭代结束判断 # 潜在风险, 如果最后一条消息被删除了, 会出现问题
            last_id = from_chan.last_message_id
            if not last_id:
                print(f"invalid channel, {from_chan.last_message_id}, {from_chan.last_message}")
                return

            print(f"chan {from_chan}, last message ={last_id}")

            limit = 100
            after_at = None
            msg_id = None
            count = 0
            while True:
                # todo x: fix 动态获取最新值
                # last_id = from_chan.last_message_id

                # 迭代:
                async for msg in from_chan.history(limit=limit, oldest_first=True, after=after_at):
                    print(
                        f"message content: {msg.content}, {msg.created_at}, {msg.edited_at}, {msg.id}, {msg.embeds}, {msg.type}")

                    # 图片消息:
                    if msg.attachments:
                        embed = discord.Embed(
                            title=f"Migrate From: {from_chan.name} ",
                            color=0xeee657,
                        )
                        embed.add_field(name="Author", value=msg.author)
                        embed.add_field(name="CreatedAt", value=f"{msg.created_at.date()}")
                        files = []
                        for item in msg.attachments:
                            embed.add_field(name="Attachment", value=item.url, inline=False)

                            # 图片文件
                            # with os.open(f'{item.id}', mode='wb') as f:
                            #     f.write(await item.read(use_cached=True))
                            #     files.append(f)

                        #
                        # TODO X: 执行消息迁移动作, 嵌入图片文件
                        #
                        await to_thread.send(embed=embed)
                        # await to_thread.send(files=[await item.to_file(use_cached=True) for item in msg.attachments])
                        # await to_thread.send(files=files)

                    # 纯文本消息:
                    elif msg.content:
                        embed = discord.Embed(
                            title=f"Migrate From: {from_chan.name} ",
                            color=0xeee657,
                        )
                        embed.add_field(name="Author", value=msg.author)
                        embed.add_field(name="CreatedAt", value=f"{msg.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                        embed.add_field(name="Content", value=msg.content, inline=False)

                        #
                        # TODO X: 执行消息迁移动作
                        #
                        await to_thread.send(embed=embed)
                    else:
                        break

                    # 更新下次迭代的时间戳
                    after_at = msg.created_at
                    msg_id = msg.id
                    count += 1

                # 更新下次迭代的时间戳
                after_at = after_at
                print(f"chan messages iter: count={count}, after at={after_at}, current msg id:{msg_id}")

                # todo x: 潜在 bug, 确保最新的消息, 不被删除(每次执行 migrate, 都发一条新消息)
                if msg_id == last_id:
                    break

            embed.add_field(name="count", value=count)
            await ctx.send(embed=embed)

        @self.command()
        async def info(ctx):
            """输出 bot 信息. [输入示例: $info]

            :param ctx:
            :return:
            """
            embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)

            # give info about you here
            embed.add_field(name="Author", value="<YOUR-USERNAME>")

            # Shows the number of servers the bot is member of.
            embed.add_field(name="Server count", value=f"{len(self.guilds)}")

            # give users a link to invite thsi bot to their server
            embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")

            await ctx.send(embed=embed)

        # self.remove_command('help')

        @self.command()
        async def help2(ctx):
            """自定义帮助菜单. [输入示例: $help2] 与 内置 $help 区别

            :param ctx:
            :return:
            """
            embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:",
                                  color=0xeee657)

            embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
            embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
            embed.add_field(name="$greet", value="Gives a nice greet message", inline=False)
            embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
            embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
            embed.add_field(name="$help", value="Gives this message", inline=False)

            await ctx.send(embed=embed)


################################################################################################


@click.command()
@click.option("--token", default="", help="discord token")
@click.option("--http_proxy", default=None, help="discord http proxy")
def main(token: str, http_proxy: str) -> None:
    print(f"discord config >> token: {token}, http proxy: {http_proxy}")

    intents = discord.Intents.all()
    intents.members = True

    # export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
    bot = DisMateBot(
        command_prefix='$',
        intents=intents,
        proxy=http_proxy or "http://127.0.0.1:7890",
    )

    # run:
    bot.run(token)


if __name__ == '__main__':
    """
    示例: discord 群内, 输入, $greet

    """
    main()

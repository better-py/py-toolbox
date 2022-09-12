from typing import Any
import click
import discord
from discord.ext import commands


class DisMateBot(commands.Bot):
    """
    :ref: https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html

    """

    async def on_ready(self):
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
        print(f"on error: ${event_method}")

    ##########################################################################################

    async def setup_cmds(self):
        """注册所有 bot 命令:

        :return:
        """

        @self.command()
        async def echo(ctx):
            print('greet here!')
            await ctx.send(":smiley: :wave: Hello, there!")

        @self.command()
        async def hello(ctx):
            print('greet here!')
            await ctx.send(":smiley: :wave: Hello, there!")

        @self.command()
        async def add(ctx, a: int, b: int):
            await ctx.send(a + b)

        @self.command()
        async def multiply(ctx, a: int, b: int):
            await ctx.send(a * b)

        @self.command()
        async def cat(ctx):
            await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

        @self.command()
        async def all_channels(ctx):
            """cmd = $all_channels
                查询所有频道

            :param ctx:
            :return:
            """
            embed = discord.Embed(title="all channels", description="group channels:", color=0xeee657)

            result = self.get_all_channels()

            i = 0
            for item in result:
                v = f"guid=${item.guild}, name=${item.name}, id=${item.id}, category_id=${item.category_id}"

                print(f"channel: ${v}")
                embed.add_field(name="channel: ", value=v)

                if i % 30 == 0:
                    # 每30个, 发送一条消息
                    await ctx.send(embed=embed)
                    embed.clear_fields()

                i += 1

        @self.command()
        async def all_groups(ctx):
            """查询全部群信息
            :输入示例: $all_groups

            :param ctx:
            :return:
            """
            embed = discord.Embed(title="all guilds:", description="group guilds:", color=0xeee657)

            async for item in self.fetch_guilds():
                v = f"id=${item.id}, name=${item.name}, ${item.owner_id}"
                print(f"group: ${v}")

                embed.add_field(name="group: ", value=v)
                await ctx.send(embed=embed)
                embed.clear_fields()

        @self.command()
        async def channel(ctx, channel_id: int):
            """获取单个频道信息.(命令别名)
            :输入示例: $channel 877037968701939753

            :param ctx:
            :param channel_id:
            :return:
            """
            await channel_by_id(ctx, channel_id)

        @self.command()
        async def channel_by_id(ctx, channel_id: int):
            """获取单个频道信息.
            :输入示例: $channel_by_id 877037968701939753

            :param ctx:
            :param channel_id:
            :return:
            """
            embed = discord.Embed(title=f"channel: ${channel_id}", description="metadata", color=0xeee657)

            channel = self.get_channel(channel_id)

            # print:
            v = f"name:${channel.id}, ${channel.name}, ${channel.category_id}, ${channel.guild}, ${channel.threads}"
            print(f"channel info: ${v}")

            embed.add_field(name="name", value=channel.name)
            embed.add_field(name="id", value=channel.id)
            embed.add_field(name="category id", value=channel.category_id)
            embed.add_field(name="guild", value=channel.guild)
            embed.add_field(name="threads", value=channel.threads)

            for tr in channel.threads:
                embed.add_field(name=f"thread: ${tr.name}", value=f"id=${tr.id}")

            await ctx.send(embed=embed)

        @self.command()
        async def info(ctx):
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
    print(f"discord config >> token: ${token}, http proxy: ${http_proxy}")

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

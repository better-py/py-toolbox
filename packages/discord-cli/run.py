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
        async def add(ctx, a: int, b: int):
            await ctx.send(a + b)

        @self.command()
        async def multiply(ctx, a: int, b: int):
            await ctx.send(a * b)

        @self.command()
        async def cat(ctx):
            await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

        @self.command()
        async def query_channels(ctx):
            result = self.get_all_channels()
            print('channels: ', result)

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

        self.remove_command('help')

        @self.command()
        async def help(ctx):
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

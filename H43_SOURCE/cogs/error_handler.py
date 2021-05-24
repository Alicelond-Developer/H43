from discord.ext import commands
import asyncio


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        usual_errors = (commands.CommandNotFound, commands.UserInputError, commands.DisabledCommand,
                        commands.CheckFailure, commands.NoPrivateMessage, asyncio.TimeoutError)

        error = getattr(error, 'original', error)

        if isinstance(error, usual_errors):
            return

        if isinstance(error, commands.CommandOnCooldown):

            try:
                await ctx.message.delete()
            except Exception:
                pass

            if self.client.cooldown_bypass:
                return await ctx.reinvoke()
            else:
                cooldown = error.retry_after
                msg = f'''クールダウン中にコマンドを実行しようとしました。再度 {cooldown:.2f}秒後に実行してください。
                                ```{ctx.message.content}```'''
                return await ctx.author.send(msg)

        raise error


def setup(client):
    client.add_cog(ErrorHandler(client))

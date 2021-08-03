from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='!')
token = os.environ['DISCORD_BOT_TOKEN']



@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)




@bot.command()
async def おはよう(ctx):
    await ctx.send('ぐっどもーにんぐべあー')


class ReleCog(commands.Cog):
    def __init__(self,bot):
        self.bot = bot # command.Botインスタンスを代入

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,payload):
        if payload.member.bot: #Botアカウントは無視
            return


        if payload.channel_id != 872259629437030430: #特定のチャンネル以外でリアクション
            return

        if payload.emoji.name ==":bear:": #特定の絵文字
            await payload.member.add_roles(
                payload.menmber.guild.get_role(871738081437450321) #ロールID
            )


    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        if guild is None or member is None: #鯖やメンバー情報が読めなかった場合
            return

        if member.bot: #botは無視
            return

        if payload.channel_id !=872259629437030430:
            return

        if payload.emoji.name ==":bear:":
            await payload.member.remove_roles(
                payload.member.guild.get_role(871738081437450321)
            )





bot.run(token)

import discord
from discord import message
from discord import colour
from discord.ext import commands
import os
import traceback


intents = discord.Intents.all()  # すべての権限を追加
bot = commands.Bot(command_prefix="!", intents=intents)
token = 'ODcxNjgxMzAzNDE2ODE1NjQ3.YQe2eQ.Chse9ldXUoOkWDSBPVHjKQJkK1Q'
MemberIdList = []
ID_CHANNEL_WELCOME = 872259629437030430 # 入室用チャンネルのID(int)
ID_ROLE_WELCOME = 871738081437450321 # 付けたい役職のID(int)
EMOJI_WELCOME = '🐻' # 対応する絵文字


@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="じゃんたま",type=1))



@bot.command()
async def おはよう(ctx):
    await ctx.send('ぐっどもーにんぐべあー')



@bot.command()
async def メンバー初期化(ctx):
    guild = ctx.guild
    for user in guild.members:
        if not user.bot:
            MemberIdList.append(user.id)
            text = f'{user.name} '
            await bot.get_channel(ID_CHANNEL_WELCOME).send(text)



# 役職を付与する非同期関数を定義
async def grant_role(payload):
    # 絵文字が異なる場合は処理を打ち切る
    if payload.emoji.name != EMOJI_WELCOME: 
        return

    # チャンネルが異なる場合は処理を打ち切る
    if payload.channel_id != ID_CHANNEL_WELCOME:
        return

    # Member オブジェクトと Role オブジェクトを取得して役職を付与
    member = payload.member
    guild = bot.get_guild(payload.guild_id)
    role = guild.get_role(ID_ROLE_WELCOME)
    await member.add_roles(role)
    return member

# リアクション追加時に実行されるイベントハンドラを定義
@bot.event
async def on_raw_reaction_add(payload):
    # 役職を付与する非同期関数を実行して Optional[Member] オブジェクトを取得
    member = await grant_role(payload)
    if member is not None: # 役職を付与したメンバーがいる時
        text = f'{member.mention} ようこそ！'
        await bot.get_channel(ID_CHANNEL_WELCOME).send(text)

@bot.event
async def on_message(message):
    """同時凸募集(!rect@数字)"""
    if message.content.startswith("!rect"):
        mcount = int(message.content[6:len(message.content)])
        text = "同時凸あと{}人募集中\n"
        revmsg = text.format(mcount)
        #friend_list 押した人のList
        friend_list = []
        msg = await message.channel.send(revmsg)

        #投票の欄
        await msg.add_reaction('↩️')
        await msg.add_reaction('✋')

        #リアクションをチェックする
        while len(friend_list) < int(message.content[6:len(message.content)]):
            target_reaction = await bot.wait_for('reaction_add')
            #発言したユーザが同一でない場合　真
            if target_reaction.user != msg.author:
                #====================================================
                #押された絵文字が既存のものの場合 >> 左　del
                if target_reaction.reaction.emoji == '↩️':
                    #==================================================
                    #◀のリアクションに追加があったら反応 friend_listにuser.nameがあった場合　真
                    if target_reaction.user.name in friend_list:
                        friend_list.remove(target_reaction.user.name)
                        mcount += 1
                        #リストから名前削除
                        await bot.edit_message(msg, text.format(mcount)+'\n'.join(friend_list))

                            #メッセージ書き換え
                    else:
                        pass

                #==============================================================
                #押された絵文字が既存のものの場合　>> 右　add
                elif target_reaction.reaction.emoji == '✋':
                    if target_reaction.user.name in friend_list:
                        pass

                    else:
                        friend_list.append(target_reaction.user.name)
                        #リストに名前追加
                        mcount = mcount - 1
                        await bot.edit_message(msg, text.format(mcount) +'\n'.join(friend_list))


                elif target_reaction.reaction.emoji == '✖':
                        await bot.edit_message(msg, '募集終了\n'+ '\n'.join(friend_list))
                        await bot.unpin_message(msg)
                        break
                await bot.remove_reaction(msg, target_reaction.reaction.emoji, target_reaction.user)
                #ユーザーがつけたリアクションを消す※権限によってはエラー
                #==============================================================
        else:
            await bot.edit_message(msg, '募集終了\n'+ '\n'.join(friend_list))



        

bot.run(token)
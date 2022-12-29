from worldskills import *
import discord
from discord.ext import commands
import aiocron
from datetime import datetime
import re

# enviroment
game = discord.Game('기능')
bot = commands.Bot(command_prefix='!', status=discord.Status.online, activity=game)
TOKEN = 'BOT TOKEN'

# common job field
def get_new_comment():
    session = login()
    latest_data = get_latest_data(session=session)
    chanaged_data = get_changed_data(latest_data=latest_data)
    
    if len(chanaged_data):
        embed = discord.Embed(title='과제 질의', description="새로운 과제 질의가 있습니다!", color=0xAAFFFF)
        for i in chanaged_data:
            if i[3] > 0:
                embed.add_field(name=i[0], value=f'{i[3]}개의 댓글이 추가되었습니다. (현재: {i[2]}개)\nurl: {i[1]}')
            else:
                embed.add_field(name=i[0], value=f'{-i[3]}개의 댓글이 삭제되었습니다. (현재: {i[2]}개)\nurl: {i[1]}')
        embed.set_thumbnail(url='https://www.korea.kr/goNewsRes/attaches/editor/2019.01/27/20190127224207298_MVBHMYGV.jpg')
        embed.set_footer(text="클라우드컴퓨팅 김건희 ❤")

        return embed
    else:
        return None

def user_profile(username, occupation, picture, msg):
    embed = discord.Embed(title=username, description=occupation, color=0xD000FF)
    
    file = discord.File(f'./discord_bot_image/{picture}', filename='image.jpg')
    embed.set_thumbnail(url="attachment://image.jpg")
    embed.add_field(name='특징', value=msg)

    return embed, file

def get_lunch_menu():
    neis_request_url = 'https://open.neis.go.kr/hub/mealServiceDietInfo'
    neis_params = {'KEY':'efe286d0d8b74405934d74218b333f89', 'Type':'json', 'pIndex':1, 'pSize':5, 'ATPT_OFCDC_SC_CODE':'B10', 'SD_SCHUL_CODE':'7010537','MLSV_YMD':f'{datetime.now().strftime("%Y%m%d")}'}
    res = requests.get(neis_request_url, params=neis_params)
    tmp_menu = res.json()["mealServiceDietInfo"][1]['row'][0]["DDISH_NM"].split('<br/>')

    lunch_menu = list()

    for i in tmp_menu:
        lunch_menu.append(re.sub(r"[^가-힣]", "", i))

    return lunch_menu

def lunch_embed(lunch_menu):
    embed = discord.Embed(title='오늘의 급식', description=f'{datetime.now().strftime("%Y년 %m월 %d일")}', color=0xE0FFFF)
    file = discord.File(f'./discord_bot_image/lunch.jpg', filename='image.jpg')
    embed.set_thumbnail(url="attachment://image.jpg")
    
    msg = ''

    for i in lunch_menu:
        msg += f'{i}\n'

    embed.add_field(name='중식', value=msg)

    return embed, file

# cron jobs field
@aiocron.crontab('*/5 * * * *')
async def cron1():
    message_channel = bot.get_channel(992377021441257536)
    
    embed = get_new_comment()

    if embed:
        await message_channel.send(embed=embed)
    else:
        return

@aiocron.crontab('0 22 * * 1-5')
async def cron2():
    await bot.change_presence(status=discord.Status.idle)

@aiocron.crontab('0 8 * * 1-5')
async def cron3():
    await bot.change_presence(status=discord.Status.online)

@aiocron.crontab('0 7 * * 1-5')
async def cron4():
    channel = bot.get_channel(994438966193434694)
    lunch_menu = get_lunch_menu()
    embed, file = lunch_embed(lunch_menu)

    await channel.send(embed=embed, file=file)

# command jobs field
# lunch
@bot.command(aliases=['점심', '중식'])
async def 급식(ctx):
    lunch_menu = get_lunch_menu()
    embed, file = lunch_embed(lunch_menu)

    await ctx.send(embed=embed, file=file)

# user


# worldskils
@bot.command()
async def 댓글(ctx):
    embed = get_new_comment()

    if embed:
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title='과제 질의', description="새로운 과제 질의가 없습니다.", color=0xAAFFFF)
        embed.set_thumbnail(url='https://post-phinf.pstatic.net/MjAyMTA4MzFfMTA3/MDAxNjMwMzg3MDcyNDM2.yfDkLDMEOqY97UnjAsKWEGuCJaxGkq9tyJyTUAE6pq0g.mlalmRbED4rb7wsvPebtBK-H_JuwvsnKs0oyXHkI5Osg.PNG/3.png?type=w1200')
        await ctx.channel.send(embed=embed)

# admin
'''
def check_admin(ctx):
    admin_id = 585468570285375488
    if admin_id == ctx.author.id():
        return True
    else:
        return False
'''
'''
@bot.command()
async def 봇_온라인(ctx):
    try:
        if check_admin:
            await bot.change_presence(status=discord.Status.online)
            await ctx.send('봇 온라인 전환 시도')
            #logging('[COMMON]', f'{ctx.author.name}({ctx.author.id}) 봇_온라인 성공')
        else:
            await ctx.send('권한 에러')
            #logging('[SECURE]', f'{ctx.author.name}({ctx.author.id}) 봇_온라인 실패(권한 에러)')
            return
    except:
        await ctx.send('worldskills! 봇을 온라인으로 전환하던중 에러가 발생했습니다.')
        #logging('[ERROR]', f'{ctx.author.name}({ctx.author.id}) 봇_온라인 실패(내부 에러)')
'''
'''
@bot.command()
async def 봇_자리비움(ctx):
    try:
        if check_admin:
            await bot.change_presence(status=discord.Status.idle)
            await ctx.send('봇 자리비움 전환 시도중')
            #logging('[COMMON]', f'{ctx.author.name}({ctx.author.id}) 봇_자리비움 성공')
        else:
            await ctx.send('권한 에러')
            #logging('[SECURE]', f'{ctx.author.name}({ctx.author.id}) 봇_자리비움 실패(권한 에러)')
            return
    except:
        await ctx.send('worldskills! 봇을 자리비움으로 전환하던중 에러가 발생했습니다.')
        #logging('[ERROR]', f'{ctx.author.name}({ctx.author.id}) 봇_자리비움 실패(내부 에러)')
'''
'''
@bot.command()
async def 봇_종료(ctx):
    try:
        if check_admin:
            await ctx.send('worldskills! 봇을 종료합니다.')
            #logging('[COMMON]', f'{ctx.author.name}({ctx.author.id}) 봇_종료 성공')
            sys.exit()
        else:
            await ctx.send('권한 에러')
            #logging('[SECURE]', f'{ctx.author.name}({ctx.author.id}) 봇_종료 실패(권한 에러)')
            return
    except:
        await ctx.send('worldskills! 봇을 종료하던중 오류가 발생했습니다.')
        #logging('[ERROR]', f'{ctx.author.name}({ctx.author.id}) 봇_종료 실패(내부 에러)')
'''
'''
async def logging(type, msg):
    message_channel = bot.get_channel(992810899540824105)
    await message_channel.send(type, msg)
'''

# bot start
bot.run(TOKEN)
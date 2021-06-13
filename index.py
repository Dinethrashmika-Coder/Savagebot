import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
from discord.ext.commands import bot
from discord.member import Member
import aiohttp
import asyncio
import re
import sys
import traceback
from datetime import datetime
from typing import Union
from discord.ext.commands.core import has_guild_permissions
import time
from PIL import Image, ImageFilter
from io import BytesIO





client = commands.Bot(command_prefix='S!')

status = cycle('In the Savage Server Of Dineth Rashmika')

@tasks.loop(seconds=5)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))



@client.event
async def on_ready():
  change_status.start()
  print('The Bot is online')


@client.command()
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount)



@client.command(aliases=['8ball', 'test'])
async def  _8ball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')          

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name='Members')
    await member.add_roles(role)

@client.command()
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    icon_url = member.avatar_url

    avatarEmbed = discord.Embed(
        title=f"{member.name}\'s Avatar", color=0xFFA500)

    avatarEmbed.set_image(url=f"{icon_url}")

    avatarEmbed.timestamp = ctx.message.created_at

    await ctx.send(embed=avatarEmbed)


client.remove_command('help')

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author

    embed = discord.Embed(

        colour = discord.Colour.orange()
    )

    embed.set_author(name='help')
    embed.add_field(name='S!ping', value='Returns Pong!', inline=False)

    await author.send(embed=embed)




@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
 await member.kick(reason=reason)

 if not Member:  # if not member isnt mentioned
    await ctx.send("User isnt mentioned")

    await member.kick(reason=reason)
        
    embed = discord.Embed(
        title=f"{ctx.author.name}  kicked:  {member.name}", color=0xea7938)
    embed.add_field(name="Reason", value=reason)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_image(
        url='https://media.giphy.com/media/xTcnTjeH5rtf6bdlwA/giphy.gif')
    embed.set_footer(text="Savage Bot")
    embed.add_field(name="Bot?", value=member.bot)

    await ctx.send(embed=embed)   

@client.command()
async def ban(ctx, user: discord.User):
    guild = ctx.guild
    mbed = discord.Embed(
        title='Booh Yah!',
        description=f"{user} has successfully been banned."
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed=mbed)
        await guild.ban(user=user)


@client.command()
async def unban(ctx, user: discord.User):
    guild = ctx.guild
    mbed = discord.Embed(
        title='Booh Yah!',
        description=f"{user} has successfully been unbanned."
    )
    if ctx.author.guild_permissions.ban_members:
        await ctx.send(embed=mbed)
        await guild.unban(user=user)


@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(
        title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")


@client.command(description="Unmutes a specified user.")
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await member.send(f" you have unmutedd from: - {ctx.guild.name}")
    embed = discord.Embed(
        title="unmute", description=f" unmuted-{member.mention}", colour=discord.Colour.light_gray())
    await ctx.send(embed=embed)


@client.command
@commands.has_permissions(kick_members=True)
async def tempmute(ctx, member: discord.Member, time: Union[int, str] = 0, reason=None):
    if not member or time == 0:
        return
    elif reason == None:
        reason = 'No reason'
    try:
        if time_list[2] == "s":
            time_in_s = int(time_list[1])
        if time_list[2] == "min":
            time_in_s = int(time_list[1]) * 60
        if time_list[2] == "h":
            time_in_s = int(time_list[1]) * 60 * 60
        if time_list[2] == "d":
            time_in_s = int(time_list[1]) * 60 * 60 * 60
    except:
        time_in_s = 0

    tempmuteembed = discord.Embed(colour=discord.Colour.from_rgb(0, 255, 0))
    tempmuteembed.set_author(icon_url=member.avatar_url,
                             name=f'{member} has been tempmuted!')
    tempmuteembed.set_footer(
        text=f"{ctx.guild.name}  •  {datetime.strftime(datetime.now(), '%d.%m.%Y at %I:%M %p')}")
    tempmuteembed.add_field(name=f'ID:', value=f'{member.id}', inline=False)
    tempmuteembed.add_field(name='Reason:', value=f"{reason}")
    tempmuteembed.add_field(name='Duration:', value=f"{time}")
    tempmuteembed.add_field(
        name=f'By:', value=f'{ctx.author.name}#{ctx.author.discriminator}', inline=False)
    await ctx.send(embed=tempmuteembed)

    guild = ctx.guild
    for role in guild.roles:
        if role.name == 'Muted':
            await member.add_roles(role)
            await ctx.send(embed=tempmuteembed)
            await asyncio.sleep(time_in_s)
            await member.remove_roles(role)
            return



@client.command()
async def ping(ctx):
    before = time.monotonic()
    message = await ctx.send("Pong!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")



    
@client.command(pass_context=True)
async def meme(ctx):
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children']
                            [random.randint(0, 25)]['data']['url'])
            await ctx.send(embed=embed)


@client.command()
async def rip(ctx,member:discord.Member=None):
    if not member:
        member = ctx.author

    rip = Image.open('rip.jpg')

    asset = member.avatar_url_as(size=128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)
    
    pfp = pfp.resize((370,370))

    rip.paste(pfp, (207,237))
     
    rip.save('prip.jpg')

    await ctx.send(file = discord.File('prip.jpg'))







client.run('ODQ5Mjk3NDI1MjA1MTY2MTg3.YLZH3Q.Fowg5V9iybn4E6lS1mPjx4YU68M')
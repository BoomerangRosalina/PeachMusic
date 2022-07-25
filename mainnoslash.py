import discord
import random
from discord.ext import commands
import asyncio
import sys

client = commands.Bot(command_prefix = 'p;')
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="p;help"))
    print("Peach Music is Ready")

@client.command()
async def help(ctx):
    embed = discord.Embed(title="Cat Peach Music Commands", description="Here are the commands for Cat Peach Music", color=(16743167))
    embed.add_field(name = "BOT COMMANDS", value = "p;help - This message\np;ping - Checks the Latency of the Bot\np;info - Some Information about the bot\np;invite - Links to invite the bot and to their support server\np;say - Makes the Bot say stuff", inline=False)
    embed.add_field(name = "MUSIC COMMANDS", value = "p;connect - Summons the Bot into the VC\np;disconnect - Disconnects the Bot from VC\np;songids - Get a list of song IDs for p;play\np;play - Plays a Nintendo Song from a Song ID", inline=False)
    embed.add_field(name = "VC MODERATION", value = "p;vcmmute - Server mutes a member from speaking in VC.\np;vcmunmute - Removes the Server mute and allows them to speak\np;forcedisccnnect - Force disconnects the bot from VC\np;vcallmute - Server Mute everyone in the VC you are in\np;vcallunmute - Server Unmutes everyone in your current VC", inline=False)
    embed.add_field(name = "OTHER", value = "p;serverinfo - Show basic stats about your server\np;userinfo - Show basic info about yourself or another user\np;devcmds - Bot Developer only commands list", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def ping(ctx):
    await ctx.send(f'My Latency is: {round(client.latency * 1000)}ms')

@client.command()
async def info(ctx):
    embed=discord.Embed(title="Peach Music Information", description=f"Peach Music\nPrefix: p;\nServers I am in: {len(client.guilds)}\nMembers I serve for: {len(client.users)}\n\n\n**BOT STAFF**\nMy Creators: Boomerang Mario#5018 (872608213076426763)\nCo-owner: AMarioLover#3304 (839289231305605120)\nWebsite Manager: Cat Rosalina#8088 (882011182125416518)", color=16743167)
    embed.set_footer(text="DISCLAIMER: This Bot is Not Affilirated with Nintendo")
    await ctx.send(embed=embed)

@client.command()
async def invite(ctx):
    embed = discord.Embed(title="Invite Links", description="Invite the Bot: https://discord.com/api/oauth2/authorize?client_id=873436797634494556&permissions=0&scope=bot\n\nSupport Server: https://discord.gg/cbqDfn8jvd\n\nPrivacy Policy: https://boomerangrosalina.glitch.me/peachmusicprivacy.html\n\nOur Website: https://boomerangrosalina.glitch.me/peachmusic.html", color=(16743167))
    await ctx.send(embed=embed)

@client.command()
async def say(ctx, *, question: commands.clean_content):
    await ctx.send(f'{question}')
    await ctx.message.delete()

@say.error
async def say_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("What do you want me to say?")
    else:
        raise error





@client.command()
async def songids(ctx):
    embed = discord.Embed(title="Peach Music Song IDs", description="These are the song codes to play music with Cat Peach Music. Use p;play <songid> to play a song. (example: p;play superbellhill", color=(16743167))
    embed.add_field(name = "FULL SONGS", value = "ashley - Ashleys Song\nashleyjp - Ashleys Song in Japan\nkirbyssb - Gournment Race Super Smash Bros\nbowserjrappears - Bowser Jr Appears - Mario Party 10 OST\nfromanewworld - From a New World\nsuperbellhillms - Super Bell Hill (M&S At the Rio Games 2016 RMX)\nsuperbellhill - Super Bell Hill\nkirbykss - Kirby Super Star\nlondonloopfinallap - MKT - London Loop Final Lap\np;play mlbisgrandfinale = Grand Finale - Mario and Luigi Bowsers Inside Story", inline=False)
    embed.add_field(name = "Jingles", value = "worldclear - SM3DW Clear Jingle\nvictoryparade - SM3DW Boss Clear Victory Parade", inline=False)
    embed.add_field(name = "REMIXES", value = "kirby8bit - Gournment Race 8bit\nkirbyksss\nkirbymetal - Gournment Race Metal Cover\np;play kirbysymphonicmetal = Gournment Race Intense Symphonic Metal Cover\nsuperbellhill16bit - Super Bell Hill 16bit", inline=False)
    embed.add_field(name = "EXTRA SOUNDS", value = "marioburned - Mario Burning", inline=False)
    embed.add_field(name = "BONUS", value = "potcmpc - Pirates of the Caribbean - Mario Paint Composer\npotcmpcrock - Pirates of the Caribbean - Mario Paint Composer ROCK\nastronomiasm64 - Astronomia SM64 RMX", inline=False)
    embed.add_field(name = "MORE SONGS", value = "See more music codes here: https://boomerangrosalina.glitch.me/peachmusicids.html", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def connect(ctx):
    if(ctx.author.voice is None):
        await ctx.send("Whoops. It appears you are not in a VC. Please join a VC and try this command again")
    await ctx.author.voice.channel.connect()
    await ctx.send("Successfully Connected to the VC.")

@client.command(aliases=["leave", "stop"])
async def disconnect(ctx):
    if(ctx.author.voice is None):
        await ctx.send("You need to be in a VC to disconnect me from the Voice Channel")
        return
    server = ctx.message.guild.voice_client
    await server.disconnect()
    await ctx.send("Successfully disconnected from the VC")

@client.command()
async def play(ctx, *, songid):
    if(ctx.author.voice is None):
        await ctx.send("Whoops. It appears you are not in a VC. Please join a VC and try this command again")
        return
    if ctx.guild.voice_client in  client.voice_clients:
        guild = ctx.guild
        voice_client: discord.VoiceClient = discord.utils.get(client.voice_clients, guild=guild)
        audio_source = discord.FFmpegPCMAudio(f'{songid}.mp3')
        if not voice_client.is_playing():
            voice_client.play(audio_source, after=None)
            await ctx.send(f"<a:DiscordMusic:899453467771432990> The Song ID: {songid} IS NOW PLAYING <a:PeachDance:899456657497657405>")
    else:
        await ctx.send("I am not inside your VC. To make me join your VC, use p;connect")

@play.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to provide a song ID which can be found in p;songcodes\n\np;play <songcode>", color=(16743167))
        await ctx.send(embed=embed)






@client.command(aliases=["forceleave", "forcestop"])
@commands.has_permissions(administrator=True)
async def forcedisconnect(ctx):
    server = ctx.message.guild.voice_client
    await server.disconnect()
    await ctx.send("Successfully disconnected from the VC")

@forcedisconnect.error
async def forcedisconnect_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``Administrator`` Permission to use this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(administrator=True)
async def vcallmute(ctx):
    try:
        if(ctx.author.voice is None):
            await ctx.send("Please join the VC you wish to server mute everyone in")
            return
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=True)
        await ctx.send("I have successfully muted everyone in your VC that I am able to Server Mute")
    except:
        await ctx.send("SOMETHING WENT WRONG WHEN TRYING TO USE THIS COMMAND\n\nPossible Problems:\n- I dont have permission to do this. REQUIRED PERMISSION: MUTE_MEMBERS (VC PERMISSION)\n- There is a channel override issue with the VC you are trying to make me mute everyone in")

@vcallmute.error
async def vcallmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``Administrator`` Permission to use this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(administrator=True)
async def vcallunmute(ctx):
    try:
        if(ctx.author.voice is None):
            await ctx.send("Please join the VC you wish to server unmute everyone in")
            return
        vc = ctx.author.voice.channel
        for member in vc.members:
            await member.edit(mute=False)
        await ctx.send("I have successfully unmuted everyone in your VC that I am able to Server Unmute")
    except:
        await ctx.send("SOMETHING WENT WRONG WHEN TRYING TO USE THIS COMMAND\n\nPossible Problems:\n- I dont have permission to do this. REQUIRED PERMISSION: MUTE_MEMBERS (VC PERMISSION)\n- There is a channel override issue with the VC you are trying to make me unmute everyone in")

@vcallunmute.error
async def vcallunmute_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``Administrator`` Permission to use this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(administrator=True)
async def vcmmute(ctx, member: discord.User, *, reason=None):
    try:
        if member == ctx.message.author:
            await ctx.channel.send("Why would you mute yourself? That sounds stupid")
            return
        if member == client.user:
            await ctx.send("What have I done to deserve this?")
            return
        if reason == None:
            reason = "No Reason provided by Mod"
            
        await member.edit(mute=True)
        await ctx.send("Successfully Server Muted that user")
        try:
            embed = discord.Embed(title="VC SERVER MUTED", description=f"You have been VC server muted in: {ctx.guild.name}. This means you can not speak in Voice channels within this server\nReason: {reason}\nResponsible Moderator: {ctx.author.display_name}", color=(16755968))
            await member.send(embed=embed)
        except:
            await ctx.send("The user had DMs off or has blocked me. Therefor, I cant DM them the case details")
        return
    except:
        await ctx.send("Failed to Server mute that user in VC. I may not have the MUTE_MEMBERS permission. Check the Permissions of me and try again.")
        return

@vcmmute.error
async def vcmmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to mention a user on which you wish to Server mute them from speaking in VCs\np;vcmembermute @MemberMention reason", color=(16743167))
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``Administrator`` Permission to use this command.")
    else:
        raise error

@client.command()
@commands.has_permissions(administrator=True)
async def vcmunmute(ctx, member: discord.User):
    try:
        await member.edit(mute=False)
        await ctx.send("Successfully Server UnMuted that user")
        return
    except:
        await ctx.send("Failed to Server unmute that user in VC. I may not have the MUTE_MEMBERS permission. Check the Permissions of me and try again.")
        return

@vcmunmute.error
async def vcmunmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title="AN ERROR HAS OCCURED", description="You need to mention a user on which you wish to Server unmute them from speaking in VCs\np;vcmemberunmute @MemberMention", color=(16743167))
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You need to have the ``Administrator`` Permission to use this command.")
    else:
        raise error






format = "%a, %d %b %Y | %H:%M:%S %ZGMT"

@client.command(aliases=["si", "serverstats"])
async def serverinfo(ctx):
    embed = discord.Embed(title="SERVER INFORMATION", description=f"Guild Name: {ctx.guild.name}\nMember Count: {ctx.guild.member_count}\nGuild ID: {ctx.guild.id}\nServer Region: {ctx.guild.region}\nVerification Level: {ctx.guild.verification_level}\nServer Creation Date: {ctx.guild.created_at.strftime(format)}", color=(16743167))
    embed.add_field(name = "SPECIAL", value = f"Features: {', '.join(f'**{x}**' for x in ctx.guild.features)} \nSplash: {ctx.guild.splash}")

    text_channels = len(ctx.guild.text_channels)
    voice_channels = len(ctx.guild.voice_channels)
    categories = len(ctx.guild.categories)
    channels = text_channels + voice_channels
    embed.add_field(name = "Channel Count", value = f"Channels: **{channels}**\nText Channels; **{text_channels}**\nVoice Channels; **{voice_channels}**\nCategories; **{categories}**", inline=False)
    embed.add_field(name = "Boosters", value = f"BOOST COUNT: Server Boost Count: {ctx.guild.premium_subscription_count}", inline=False)
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.set_footer(text="Cat Peach Music")
    await ctx.send(embed=embed)

@client.command(aliases=["ui"])
async def userinfo(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(title="USER INFORMATION/STATS", description=f"USERNAME: {user.name}\nUSER ID: {user.id}\nDISCRIMINATOR TAG: {user.discriminator}\nRegistered At: {user.created_at.strftime(date_format)}\n\nJoined Server AT: {user.joined_at.strftime(date_format)}", color=(16743167))
    embed.set_footer(text="Cat Peach Music")
    embed.set_thumbnail(url=user.avatar_url)
    await ctx.send(embed=embed)






botstaff = [872608213076426763, 839289231305605120]

@client.command()
async def devcmd(ctx):
    embed = discord.Embed(title="Developer/Bot Staff Commands", description="Hello my bot staff. Here is some Developer commands.", color=(16711680))
    embed.add_field(name = "STATUS COMMANDS", value = "p;resetstatus - Reset the Bot status\np;listenstatus - Gives the bot a listening status", inline=False)
    embed.add_field(name = "UTILITY", value = "p;restart - Restarts the Bot", inline=False)
    await ctx.send(embed=embed)

def restart_program():
    python = sys.executable
    os.execl(python, python, * sys.argv)

@client.command()
async def restart(ctx):
    if ctx.author.id in botstaff:
        await ctx.send("Restarting... Allow up to 5 seconds")
        restart_program()
    else:
        await ctx.send("This command can only be used by the Bot staff")
        return

@client.command()
async def resetstatus(ctx):
    if ctx.author.id in botstaff:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="p;help"))
        await ctx.send("My Status is Successfully Changed")
    else:
        await ctx.send("This command can only be used by the Bot staff")
        return

@client.command()
async def listenstatus(ctx, *, question):
    if ctx.author.id in botstaff:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{question}"))
        await ctx.send("My Status is Successfully Changed")
    else:
        await ctx.send("This command can only be used by the Bot staff")
        return




client.run("INSERTBOTTOKENHERE")

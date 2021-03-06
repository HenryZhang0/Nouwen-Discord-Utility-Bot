import os
import discord
from discord.utils import get
import requests
import json
import time
import random
from shutil import copyfile
#from replit import db
import keep_alive
from cheese import Chess
import cv2
from datetime import datetime, date, timedelta
import pickle
from player import Player
import urllib
from PIL import Image
import asyncio
from io import BytesIO
import io
#GLOBAL VARIABLES
client = discord.Client()
image_types = ["png", "jpeg", "gif", "jpg"]
prev_time = [datetime.now()]
board = Chess()
responding = [True]
players = dict()
channel= -1

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    return(quote)
def load_board(load):
    board.load_board(load)
def reset_board():
    board.reset()
def combine_picture(back,front):
    img1 = cv2.imread(back)
    x,y,z = img1.shape
    img2 = cv2.imread(front)
    try:
        img2 = cv2.resize(img2, (y, x))
    except:
        print('image combine failed')
    dst = cv2.addWeighted(img1,0.5,img2,0.5,0)
    cv2.imwrite('combined.png',dst)
    print('images combined')
def check_checkmate():
    out = ''
    if board.checkmate():
        out= "Checkmate! \n"
        if board.fen().split(' ')[1]=='b':
            out+='<:bk:843596932014276641> White wins!<:wk:843596932324261898>'
        else:
            out+='<:bk:843596932014276641> Black Wins! <:bk:843596932014276641>'
    return out
attachments = []
async def draw_board(chan,author,msg='',reaction=''):
    pfp = author.avatar_url
    turn = check_checkmate()
    if not turn:
        if board.fen().split(' ')[1]=='b':
            turn += "<:br:843596932017946685> Black's turn <:br:843596932017946685>"
        else:
            turn += "<:wr:843596931791847535> White's turn <:wr:843596931791847535>"
   # out=await chan.send(msg+'\n'+turn+'\n'+(board.emote()))
    embed=discord.Embed(title=msg, description='Example command "=f3b4"', color=0x0a4ff0)
    embed.set_author(name=str(author), icon_url=pfp)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/527318923763253268/843930270365253642/2560px-Flag_of_Israel.png")
    embed.add_field(name=turn, value=board.emote(), inline=True)
    embed.set_footer(text="Click emoji to undo move")
    out = await chan.send(embed=embed)
    if reaction:
        await out.add_reaction(reaction)
async def send(msg):
    global channel
    await channel.send(msg)





def loadPlayers():
    global players
    players = pickle.load(open("players.pickle","rb"))
    print('loaded', players)

#Initial
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Just wiped out TomatoCow")
    await client.change_presence(status=discord.Status.online, activity=game)
    loadPlayers()

async def send_person_picture(channel,name):
    name = name[:-1]
    dir = random.choice(os.listdir("people/"+name+"/"))
    await channel.send(file=discord.File("people/"+name+"/"+dir))

async def change_server_pic(message):
    attachment = attachments[-1]
    filetype = '.'+attachment.content_type[attachment.content_type.index('/')+1:]
    filename = "pfp"+filetype
    print("recieved",attachment.filename)
    await attachment.save("pfp/pfp"+filetype)
    f = open("pfp/name.txt", "w")
    f.write(filename)
    f.close()
    name = open("pfp/name.txt", "r")
    dir = 'pfp/'+str(name.read())
    print(dir)

    server1 = client.get_guild(352311125242806272)
    with open(dir, 'rb') as f:
        icon = f.read()
    await server1.edit(icon=icon)
    
    print('> changed server image ')
    await message.add_reaction('<:egor:677925462919479313>')
    await message.add_reaction('<:nacc:713563538899075102>')
    await message.channel.send('Server icon updated', delete_after=5.0)

async def change_bot_pic(message):
    attachment = attachments[-1]
    filetype = '.'+attachment.content_type[attachment.content_type.index('/')+1:]
    filename = "pfp"+filetype
    print("recieved",attachment.filename)
    await attachment.save("pfp/pfp"+filetype)
    f = open("pfp/name.txt", "w")
    f.write(filename)
    f.close()
    name = open("pfp/name.txt", "r")
    dir = 'pfp/'+str(name.read())
    print(dir)
    fp = open(dir, 'rb')
    pfp = fp.read()
    await client.user.edit(avatar=pfp)
    
    await message.add_reaction('<:nacc:713563538899075102>')
    print('> changed image ')
    await message.channel.send('Profile picture updated', delete_after=5.0)


async def changestat(user, stat, modify):
    id = str(user.id)
    
    stats = readstat(user)
    
    stats[stat] = str(int(stats[stat])+modify)

    f = open('players/'+id+'.txt', 'w')
    f.write('\n'.join(stats))
    f.close()
    print('file written')

    print(str(user),stats)
    

async def add_coin(user, amount):
    print('Coin Found')
    await changestat(user, 0,amount)

async def change_nickname(user):
    health = players[user.id].hp
    if health==0:
        await user.add_roles(discord.utils.get(user.guild.roles, name='DEAD'))
    else:
        await user.remove_roles(discord.utils.get(user.guild.roles, name='DEAD'))
    await user.edit(nick=str(user)[0:-5]+' ' + '???'*int(players[user.id].hp))

def sort():
    s = list(p[1] for p in players.items())
    s.sort(key = lambda x:x.coins, reverse=True)
    return s
def update_players():
    pickle_out = open("players.pickle","wb")
    pickle.dump(players, pickle_out)
    pickle_out.close()

def new_player(user):
    global players
    print(players)
    players[user.id] = Player(str(user)[0:-5])
    update_players()

nacc = ["https://imgur.com/LmVrSzq.png","https://imgur.com/Y45KmiG.png","https://i.imgur.com/ikVtGVr.png","https://i.imgur.com/g4At6o0.png","https://i.imgur.com/SXP52CD.png","https://i.imgur.com/ZEY0Dcj.png","https://i.imgur.com/3tMTw27.png","https://i.imgur.com/Efwzpny.png","https://i.imgur.com/Z6QnGkG.gif"]  
egor = ['https://i.imgur.com/RMsfREO.jpg', 'https://i.imgur.com/GpoW5WP.jpg', 'https://i.imgur.com/jTheKpy.png', 'https://i.imgur.com/7p9cwk9.jpg', 'https://i.imgur.com/uM6SC5X.png', 'https://i.imgur.com/r7ecfg0.jpg', 'https://i.imgur.com/EPc8pce.png', 'https://i.imgur.com/oVODwOD.jpg', 'https://i.imgur.com/mYGS9cT.jpg', 'https://i.imgur.com/dVyWXzT.jpg', 'https://i.imgur.com/sgAWJRn.jpg', 'https://i.imgur.com/RAyE0ag.jpg', 'https://i.imgur.com/ksMdtMS.jpg']
jew = -1
activejew = [False]
@client.event
async def on_message(message):
    global channel
    global players
    global jew
    msg = message.content
    channel = message.channel
    user = message.author
    if message.author == client.user:
        return

    if msg.startswith('!newplayer') and message.channel.permissions_for(message.author).administrator:
        if msg=='!newplayer':
            new_player(user)
            await change_nickname(user)
        else:
            person = message.mentions[0]
            new_player(person)
            await change_nickname(person)
        print(players)
        update_players()
    if msg.startswith('!deleteplayer'):
        if message.channel.permissions_for(message.author).administrator:
            #person = message.mentions[0]
            players.popitem()
            update_players()

    if msg.startswith('!transfer'):
        person = message.mentions[0]
        coins = players[user.id].coins
        transfer = int(msg.split()[2])
        if str(user) == str(person):
            await message.reply('Do you want to get taxed?')
        elif int(coins)<transfer:
            await message.reply('you got no money bro')
        else:
            await message.reply('????    `'+ str(person)[0:-5] + ' recieved '+str(int(transfer*0.77))+' coins`')
            players[person.id].coins += int(transfer*0.77)
            players[user.id].coins +=transfer*-1
        update_players()

    if msg.startswith('!attack'):
        person = message.mentions[0]
        coins = players[user.id].coins
        if str(user) == str(person):
            await message.reply('No self harming in this server')
            players[user.id].poop()
        elif int(players[person.id].hp)==0:
            await message.reply('You\'re beating a dead horse')
        elif int(coins)>=10:
            await message.reply('<a:cooldoge:852924340353761361><:ikillu:706222776880595007>')
            players[user.id].coins -= 10
            x = players[user.id].attack(players[person.id])
            await send(x)
            await change_nickname(person)
        else:
            await message.reply('You don\'t have enough money. (Costs 10)')
        update_players()

    if msg.startswith('!heal') and not msg == '!health':
        person = user
        if not msg=='!heal':
            person = message.mentions[0]
        coins = players[user.id].coins
        if coins<15:
            await message.reply('You don\'t have enough money. (Costs 15)')
        elif int(players[person.id].getHp())==3:
            await message.reply('Already max health')
        elif str(user) == str(person):
            players[user.id].heal()
            players[user.id].coins -= 15
            await change_nickname(person)
            await message.reply('<a:potion:853439638005612575>    `'+ str(person)[0:-5] + ' gained a life`')
        elif int(coins)>=15:
            await message.reply('<a:potion:853439638005612575>    `'+ str(person)[0:-5] + ' gained a life`')
            players[person.id].heal()
            players[user.id].coins -= 15
            await change_nickname(person)
        else:
            await message.reply('error')
        update_players()

    if msg=='!sort':
        print(sort())
        print(user.name)
    if msg == '!health' or msg=='!hp':
        output = ''
        for p in players.items():
            p = p[1]
            output += '`'+str(p) + ': '+ str(p.getHp()) + '`\n'
        await channel.send("__**HEALTH BOARD**__ <a:hyperheart:853755189889728513>\n" + output)
    if msg == '!money' or msg=='!coins':
        output = ''
        s = list(p[1] for p in players.items())
        s.sort(key = lambda x:x.coins, reverse=True)
        for p in s:
            output += '`'+str(p) + ': '+ str(p.coins) + '`\n'
        await channel.send("__**MONEY BOARD**__ <a:bitcoin:853374907563901008>\n" + output)
    if msg == '!coin':
        if message.channel.permissions_for(message.author).administrator:
            await message.add_reaction('<a:bitcoin:853374907563901008>')

    if msg=='!jewchance':
        await channel.send('one in ' + str(40+30*list(map(str,sort())).index(str(user.name))))

    if msg == '!jew' or (str(user.name) in list(map(str,sort())) and (random.randint(0,50+20*list(map(str,sort())).index(str(user.name)))==1)):
        stole = random.randint(5,30)
        embed = discord.Embed(title='A random Jew appeared!', description = '???? ???? ???? ????',color = discord.Colour.blue())
        #embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/527318923763253268/843930270365253642/2560px-Flag_of_Israel.png")
        embed.set_image(url = 'https://www.stephenhicks.org/wp-content/uploads/2021/03/Jew_stereotype.jpg')
        embed.add_field(name='He stole %s coins from you' % stole, value = 'Fight The Resourceful Jew before he runs away!', inline=True)
        embed.set_footer(text='"Oy vey I take some your money"')
        players[user.id].coins -=stole
        if players[user.id].coins<0:
            players[user.id].coins=0

        jew = await message.reply(embed=embed)
        await jew.add_reaction('<:minecraftsword:853785342154768405>')
        activejew[0] = True
        await asyncio.sleep(5)
        if activejew[0]: #IF RUNS AWAY
            await message.clear_reactions()
            emb =discord.Embed(title="The jew ran away with your shekels")   
            emb.set_thumbnail(url="https://cdn.discordapp.com/attachments/527318923763253268/843930270365253642/2560px-Flag_of_Israel.png")
            emb.set_image(url = 'https://i.imgur.com/c9VfUlh.png')
            emb.add_field(name='He stole %s coins from you' % stole, value = 'The Resourceful Jew ran away!', inline=True)
            emb.set_footer(text='"Control the money, control the world HEHEHEE!"')
            await jew.clear_reactions()     
            #await channel.send(embed=emb)
            activejew[0]=False
            await jew.edit(embed = emb)

    if datetime.now().second %8 == 0 and random.randint(2,4)%2==0 and len(msg)>5 :
        print(time.time())
        await message.add_reaction('<a:bitcoin:853374907563901008>')
    if(len(msg)>8 and random.randint(1,170)==2):
        await message.add_reaction('<a:bytecoin:853448824856248371>')


    if msg.startswith('!stats'):
        stats = []
        name = ''
        names = ['> Coins\t','> Health\t','**Shield**','> Block %\t','> Block +\t', '**Weapon**', '> Attack %\t', '> Attack +\t','**Equipment**']
        output = ''
        if msg=='!stats':
            target = user
            name = str(user)
        else:
            target = message.mentions[0]
            name = str(target)[0:-5] 
        o = players[target.id]
        stats = [o.coins,o.hp,o.shield,o.shield.chance,o.shield.plus,o.weapon,o.weapon.chance, o.weapon.plus,''.join(o.arsenal)]
        for i,j in enumerate(stats):
            output += names[i] +" "+ str(j) + '\n'
        await message.reply('**__'+name+'__**\n'+output)














#UTIL
    if msg=='!shutdown':
        if message.channel.permissions_for(message.author).administrator:
            print('shutdown')
            update_players()
            exit()
    if msg.startswith("!responding"):
        value = msg.split("!responding ",1)[1]
        if value.lower() == "true":
            responding[0] = True
            await message.channel.send("Responses turned on")
        else:
            responding[0] = False
            await message.channel.send("Responses turned off") 
    if msg.startswith("!echo"):
        print(msg)
        await message.channel.send(msg[5:])
    if msg.lower()=='ping!':
        print("Pinged")
        await message.channel.send("Pong")
#Trigger Responses
    if responding[0]: 
        if message.content.startswith('inspireme'):
            quote = get_quote()
            await channel.send(quote)
        if msg=='!movie':
            embed = discord.Embed(title='Joker 2019')
            embed.set_image(url="https://cdn.discordapp.com/attachments/655798594397536291/660941408915554324/Joker_2019.webm")
            await message.channel.send(embed=embed)
        if msg=='howtall?':
            await channel.send("https://cdn.discordapp.com/attachments/529783388295528470/844291219580387338/unknown.png")
        if msg == 'egor!':
            await channel.send(random.choice(egor))
        if msg == 'nacc!':
            await channel.send(random.choice(nacc))
#NOTES
    if msg.startswith("!log"):
        print(message.author)
        print(msg)
        if len(msg[:-5])>150:
            await message.channel.send("Tree's can only grow 150m tall so naturally, logs are 150 characters in length")
        else:
            f = open("story.txt", "a")
            f.write("**"+str(message.author)[:-5] + "** - "+msg[5:]+"\n")
            f.close()
            await message.channel.send("Logged: "+msg[5:])
    if msg=='!notes':
        name = open("story.txt", "r")
        dir = "__**Benum's Book**__\n"+str(name.read())
        print(dir)
        await message.channel.send(dir)
        name.close()
#CHESS
    if msg=='chess!':
        await draw_board(channel,message.author)
    if msg=='chessfen!':
        await message.channel.send((board.fen()))
    if msg.startswith('loadgame!'):
        load_board(msg.split("loadgame! ",1)[1])
        await draw_board(channel,message.author,"Loaded board!")

    if msg=='resetchess!':
        board.reset()
        await draw_board(channel,message.author,"Game Reset!")

    if msg.startswith("-"):
        if(board.move(msg[1:])):   
            await draw_board(channel,message.author,"Moved "+msg[1:],'???')
        else:
            await channel.send("Illegal move <:pepega:709439143775830118>")
    
    if msg.startswith("="):
        if(board.move(msg[1:])):
            await draw_board(channel,message.author,"\nBot: "+board.engine_move(),"????")
        else:
            await message.channel.send("Illegal move <:pepega:709439143775830118>")

#PICTURE MANIPULATION
    if msg in ['shirify','beckyfy','egorfy','jamesfy','henryfy','sankeethfy','peterfy','naccfy']:
        #DOWNLOAD
        attachment = attachments[-1]
        filetype = '.'+attachment.content_type[attachment.content_type.index('/')+1:]
        filename = "pfp"+filetype
        print("recieved",attachment.filename)
        await attachment.save("pfp/pfp"+filetype)
        f = open("pfp/name.txt", "w")
        f.write(filename)
        f.close()
        name = open("pfp/name.txt", "r")
        dir = 'pfp/'+str(name.read())
        print(dir)
        combine_picture(dir,'people/'+msg[:-2]+'/'+msg[:-2]+'.png')
        await message.channel.send(file=discord.File("combined.png"))
#Updaters
    if msg.endswith("!!"):
        await message.guild.edit(name=(msg[:-2])[0:100])
        print("Changed server name to", msg[:-2])

    if msg=='changepic':
        #await change_bot_pic(message) 
        await change_server_pic(message)  
    for attach in message.attachments:
        if any(attach.filename.lower().endswith(image) for image in image_types):
            attachments.append(attach)
            tim = datetime.now()
            print(tim - prev_time[-1])
            cooldown = (tim - prev_time[-1])>timedelta(minutes=1)     
            if cooldown:
                prev_time.append(tim)
                try:
                    #await change_bot_pic(message)
                    await change_server_pic(message)
                except:
                    print("attempted to change pic FAILED")
                    await message.channel.send('bruh you change avatar too fast. Try again later uwu')
            else:
                print("Under 10 minutes cooldown")  
#Posts
    if msg.startswith("!announcement"): 
        print("announcement request")   
        await message.add_reaction('<:upvote:852978943015649310>')
        await message.add_reaction('a<:yes:852920705909260298>')
        await message.add_reaction('a<:no:852920706257256550>')



@client.event
async def on_reaction_add(reaction, user):
    global jew
    global players
    global channel
    emoji = reaction.emoji
    channel = reaction.message.channel
    if user.bot:
        return
    if(str(emoji)=='<:minecraftsword:853785342154768405>'):
        print(jew)
        #await jew.edit(content='The jew ran away with your sheckles', embed=None)
        activejew[0] = False
        emb = discord.Embed(title="Fighting Jew in Dreidel Battle!")

        emb.set_thumbnail(url="https://i.imgur.com/RWrDK3P.png")
        emb.set_image(url = 'https://media1.tenor.com/images/bdfad2a084b3bdadaf0612af140163be/tenor.gif?itemid=13014274')
        emb.add_field(name='SHIN - ??', value = 'Put another coin in the pot', inline=True)
        emb.set_footer(text='Spin the Dreidel!')
        await jew.clear_reactions()     
        #await channel.send(embed=emb)
        activejew[0]=False
        #await jew.edit(embed = emb)
        await channel.send(embed=emb)
        await reaction.message.clear_reactions()

    if(str(emoji)=='<a:bytecoin:853448824856248371>'):
        await reaction.message.clear_reactions()
        print('bytecoin')
        players[user.id].add_coin(8)
        await channel.send('<a:bytecoin:853448824856248371> '+str(user)[0:-5]+' found a ***BYTECOIN!!!*** (8 Coins)   Total Coins: '+ str(players[user.id].coins), delete_after=10)
        update_players()
    if(str(emoji)=='<a:bitcoin:853374907563901008>'):
        await reaction.message.clear_reactions()
        print('coin')
        players[user.id].add_coin(1)
        await channel.send(str(user)[0:-5]+' found a coin!! Total Coins: '+ str(players[user.id].coins), delete_after=5.0)
        update_players()
    if(emoji=='????'):
        board.undo()
        board.undo()
        await reaction.message.delete()
        await draw_board(channel,'Move Returned')
    if(emoji=='???'):
        board.undo()
        await reaction.message.delete()
        await draw_board(channel,'Move Retracted')
    if(str(emoji)=='<:ibs:761582130966691856>'):
        await channel.send('https://cdn.discordapp.com/attachments/843523078931218462/844026855451131944/emoji.png')
    if(str(emoji)=='<:egor:677925462919479313>'):
        print('egorpic')
        server1 = client.get_guild(352311125242806272)
        url = (random.choice(egor))  
        urllib.request.urlretrieve(url, 'icon'+url[-4:])
        dir = 'icon'+url[-4:]
        with open(dir, 'rb') as f:
            icon = f.read()
        await server1.edit(icon=icon)
        await channel.send('Changed Icon to Egor', delete_after = 5.0)
    if(str(emoji)=='<:nacc:713563538899075102>'):
        print('naccpic')
        server1 = client.get_guild(352311125242806272)
        #dir = "people/nacc/"+random.choice(os.listdir("people/nacc/"))
        url = (random.choice(nacc))  
        urllib.request.urlretrieve(url, 'icon'+url[-4:])
        #await channel.send(file=discord.File('icon'+url.split('/')[-1]))
        dir = 'icon'+url[-4:]
        with open(dir, 'rb') as f:
            icon = f.read()
        await server1.edit(icon=icon)
        await channel.send('Changed Icon to Nacc', delete_after = 5.0)

    if(str(emoji)=='<:downvote:853013163258413076>'):
            count = max(list(r.count for r in reaction.message.reactions))

            if count>=4:
                await client.get_channel(775432587492589578).send(str(reaction.message.author)+': '+str(reaction.message.content))
                if(reaction.message.attachments):
                    await client.get_channel(775432587492589578).send(str(reaction.message.attachments[0].url))
                print('user message deleted')
                await reaction.message.delete()
                await reaction.message.channel.send(str(reaction.message.author.mention)+'\'s message has been deleted due to much hate')
                
            print("Number of downvotes:", count)

    if(str(emoji)=='<:upvote:852978943015649310>'):
        if reaction.message.content.startswith('!announcement '):
            count = reaction.message.reactions[0].count
            if count>=5:
                print('Announcement Posted')
                await reaction.message.reply(str(reaction.message.author.mention)+' announcement posted due to overpowering votes')
                await reaction.message.clear_reactions()
                await client.get_channel(720671666333810699).send(str(reaction.message.content)[14:]+'\n\n*`'+'By '+str(reaction.message.author)+'`*')
                await reaction.message.add_reaction('<a:verified:837524558604009492>')
            print("Number of upvotes:", reaction.message.reactions[0].count)

    if(str(emoji)=='<a:yes:852920705909260298>'):
        if reaction.message.channel.permissions_for(user).administrator:
            print('Announcement Posted')
            await reaction.message.reply(str(reaction.message.author.mention)+' announcement approved by admin')
            await reaction.message.clear_reactions()
            await client.get_channel(720671666333810699).send(str(reaction.message.content)[14:]+'\n\n*`'+'By '+str(reaction.message.author)+'`*')
            await reaction.message.add_reaction('<a:verified:837524558604009492>')

    if(str(emoji)=='<a:no:852920706257256550>'):
        if reaction.message.channel.permissions_for(user).administrator:
            print('Rejected Announcement')
            await reaction.message.reply(str(reaction.message.author.mention)+' announcement rejected by admin')
            await reaction.message.clear_reactions()
            await reaction.message.add_reaction('<:stonksnt:852914352428023808>')
    print(str(user), reaction.emoji, reaction.message.channel.permissions_for(user).administrator)











#RUN
keep_alive.keep_alive()
token = open("token.txt", "r").read()
client.run(token)
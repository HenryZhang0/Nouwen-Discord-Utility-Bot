import os
import discord
import requests
import json
import random
#from replit import db
import keep_alive
from cheese import Chess
import cv2
from datetime import datetime, date, timedelta


#GLOBAL VARIABLES
client = discord.Client()

image_types = ["png", "jpeg", "gif", "jpg"]
triggers = {
    "bruh": "i was like bruh",
    "CS": "you mean geomatics?"
}
anytriggers = {
    'poo','peen'
}
prev_time = [datetime.now()]
board = Chess()

responding = [True]

db = {"trigger":["cow","frank"]}

#HELPER FUNCTIONS

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q']
    return(quote)

def update_triggers(msg):
    if "trigger" in db.keys():
        trigger = db["trigger"]
        trigger.append(msg)
        db["trigger"] = trigger
    else:
        db["trigger"] = [msg]

def delete_trigger(index):
    trigger = db["trigger"]
    if len(trigger) > index:
        del trigger[index]
        db["trigger"] = trigger
        

def load_board(load):
    board.load_board(load)
def reset_board():
    board.reset()

def combine_picture(back,front):
    img1 = cv2.imread(back)
    x,y,z = img1.shape
    img2 = cv2.imread(front)
    #print(x,y,z)
    try:
        img2 = cv2.resize(img2, (y, x))
    except:
        print('image combine failed')
    #print(img2.shape)
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
    

#Initial
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    game = discord.Game("Just wiped out TomatoCow")
    await client.change_presence(status=discord.Status.online, activity=game)

async def send_person_picture(channel,name):
    name = name[:-1]
    dir = random.choice(os.listdir("people/"+name+"/"))
    await channel.send(file=discord.File("people/"+name+"/"+dir))

async def changepic(message):
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
    for guild in client.guilds:
        print(guild.id) 
    server1 = client.get_guild(352311125242806272)
    with open(dir, 'rb') as f:
        icon = f.read()
    await server1.edit(icon=icon)
    fp = open(dir, 'rb')
    pfp = fp.read()
    await client.user.edit(avatar=pfp)
    
    print('> changed image ')
    await message.channel.send('Server picture updated')

@client.event
async def on_message(message):
    msg = message.content
    channel = message.channel


#UTIL
    if message.author == client.user:
        return
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

#    if msg.startswith("+"):
#        try:
#            x = eval(msg[1:])
#            await channel.send(x)
#        except:
#            await channel.send("Unable to read equation")


#Trigger Responses

    if responding[0]: 
        if message.content.startswith(tuple(triggers.keys())):
            await channel.send(triggers.get(message.content))  
        elif message.content.startswith('inspireme'):
            quote = get_quote()
            await channel.send(quote)
        elif any(word in message.content for word in anytriggers):
            await channel.send('booga')
        elif msg.lower() in ['egor!','sankeeth!','nacc!']:
            await send_person_picture(channel, msg.lower())
        #sankeeth reaction
        if msg.lower() in list(db["trigger"]):
            await message.add_reaction('<:ibs:761582130966691856>')
        if msg.startswith("!listtriggers"):
            await channel.send(list(db["trigger"]))
        if message.content.startswith("!newtrigger"):
            trig = msg.split("!newtrigger ",1)[1]
            update_triggers(trig)
            await channel.send("New word added")
        if message.content.startswith("!deletetrigger"):
            trigger = []
            if "trigger" in db.keys():
                index = int(msg.split("!deletetrigger",1)[1])
                delete_trigger(index)
                trigger = db["trigger"]
            await channel.send(trigger)
        if msg=='!movie':
            embed = discord.Embed(title='Joker 2019')
            embed.set_image(url="https://cdn.discordapp.com/attachments/655798594397536291/660941408915554324/Joker_2019.webm")
            await message.channel.send(embed=embed)
        if msg=='howtall?':
            await channel.send("https://cdn.discordapp.com/attachments/529783388295528470/844291219580387338/unknown.png")




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
            await draw_board(channel,message.author,"Moved "+msg[1:],'◀')
        else:
            await channel.send("Illegal move <:pepega:709439143775830118>")
    
    if msg.startswith("="):
        if(board.move(msg[1:])):
            await draw_board(channel,message.author,"\nBot: "+board.engine_move(),"🔄")
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
        
    if msg=='changepic':
        await changepic(message)
        
    
#Profile Picture Updater
    for attach in message.attachments:
        if any(attach.filename.lower().endswith(image) for image in image_types):
            attachments.append(attach)
            
            tim = datetime.now()
            print(tim - prev_time[-1])
            cooldown = (tim - prev_time[-1])>timedelta(minutes=10)
                
            if cooldown:
                prev_time.append(tim)
                #DOWNLOAD
                attachment = attachments[-1]
                filetype = '.'+attachment.content_type[attachment.content_type.index('/')+1:]
                filename = "pfp"+filetype
                print("recieved",attachment.filename)
                await attachment.save("pfp/pfp"+filetype)
                f = open("pfp/name.txt", "w")
                f.write(filename)
                f.close()
                try:
                    name = open("pfp/name.txt", "r")
                    dir = 'pfp/'+str(name.read())
                    print(dir)
                    with open(dir, 'rb') as f:
                        icon = f.read()
                    await client.edit_server(message.server, icon=icon)
                    #fp = open(dir, 'rb')
                    #pfp = fp.read()
                    #await client.user.edit(avatar=pfp)
                    print('> changed image ')
                    await message.channel.send('Server picture updated')
                except:
                    print("attempted to change pic FAILED")
                    #await message.channel.send('bruh you change avatar too fast. Try again later uwu')
            else:
                print("Under 10 minutes cooldown")
        
@client.event
async def on_reaction_add(reaction, user):
    emoji = reaction.emoji
    channel = reaction.message.channel
    if user.bot:
        return
    if(emoji=='🔄'):
        board.undo()
        board.undo()
        await reaction.message.delete()
        await draw_board(channel,'Move Returned')
    if(emoji=='◀'):
        board.undo()
        await reaction.message.delete()
        await draw_board(channel,'Move Retracted')
    if(str(emoji)=='<:ibs:761582130966691856>'):
        await channel.send('https://cdn.discordapp.com/attachments/843523078931218462/844026855451131944/emoji.png')
    print(str(user), reaction.emoji)



#RUN
keep_alive.keep_alive()
client.run("token")
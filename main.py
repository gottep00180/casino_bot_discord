#invite link : https://discord.com/api/oauth2/authorize?client_id=935524944748634172&permissions=8&scope=bot
import discord
from discord.utils import get
from discord.ext import commands
import random
import requests
import mysql.connector
# import mysql.connector

# wrapper / decorator 
bot = commands.Bot(command_prefix='john!',help_command=None)

@bot.event
async def on_ready():
    print("ALREADY login to bot")
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "casino"
)
@bot.command()
async def balance(ctx):
   if ctx.channel.name == "random" or ctx.channel.name == "🎲𝐁𝐈𝐋𝐋𝐈𝐎𝐍𝐀𝐈𝐑𝐄-𝐂𝐀𝐒𝐈𝐍𝐎":
        player_id = str(ctx.author.id)
        print(player_id)
        player_name = str(ctx.author)
        mycursor = mydb.cursor()
        sql = "SELECT * FROM profile WHERE userid = %s"
        val = (player_id, )
        mycursor.execute(sql,val)
        result = mycursor.fetchone()
        if type(result) == type(None):
            await ctx.channel.send("<@"+player_id+"> คุณยังไม่ได้มีโปรไฟล์ในฐานข้อมูล รอสักครู่เรากำลังสร้างให้คุณ")
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'create_profile','userid': player_id,'player_name': player_name}
            x = requests.post(url, data = myobj)
            player_points = 500
            print("create profile for"+player_name+"success")
            await ctx.channel.send("<@"+player_id+"> คุณมีโปรไฟล์ในฐานข้อมูลแล้ว")
        if type(result) != type(None):
            player_points = result[2]
        await ctx.channel.send("<@"+player_id+">คุณมีเงินในบัญชีเหลือ : "+str(player_points)+"\nเลขบัญชีของคุณคือ"+player_id+"")
@bot.command()
async def casino(ctx, ra_points):
    if ctx.channel.name == "random" or ctx.channel.name == "🎲𝐁𝐈𝐋𝐋𝐈𝐎𝐍𝐀𝐈𝐑𝐄-𝐂𝐀𝐒𝐈𝐍𝐎":

        precentage = random.randint(1, 1000)
        player_id = str(ctx.author.id)
        print(player_id)
        player_name = str(ctx.author)
        mycursor = mydb.cursor()
        sql = "SELECT * FROM profile WHERE userid = %s"
        val = (player_id, )
        mycursor.execute(sql,val)
        result = mycursor.fetchone()
        if type(result) == type(None):
            await ctx.channel.send("<@"+player_id+"> คุณยังไม่ได้มีโปรไฟล์ในฐานข้อมูล รอสักครู่เรากำลังสร้างให้คุณ")
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'create_profile','userid': player_id,'player_name': player_name}
            x = requests.post(url, data = myobj)
            player_points = 500
            print("create profile for"+player_name+"success")
            await ctx.channel.send("<@"+player_id+"> คุณมีโปรไฟล์ในฐานข้อมูลแล้ว")
        if type(result) != type(None):
            player_points = result[2]
        # print(str(player_name)+"percentage is"+str(precentage))
        ra_points = float(ra_points)
        if ra_points < 10:
            await ctx.channel.send("ในการสุ่มแต่ละครั้งยอดเงินจะต้องไม่ต่ำกว่า 10 points")
        if player_points >= ra_points and ra_points >= 10:
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'submoney', 'userid': player_id, 'money': ra_points }
            x = requests.post(url, data = myobj)
            if ra_points < 10000:
                tax = "0%"
            if ra_points >= 10000 and ra_points < 100000:
                ra_points = (25/100) * ra_points
                tax = "25%"
            if ra_points >= 100000 and ra_points < 1000000:
                ra_points = (50/100) * ra_points
                tax = "50%"
            if ra_points >= 1000000 :
                ra_points = (70/100) * ra_points
                tax = "75%"


            if precentage >= 998: # 0.2% rate
                multiple = ra_points * 100
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 100 เท่า \nคุณเสียภาษี"+tax)
            if precentage < 998 and precentage >= 978: # 2 % rate
                multiple = ra_points * 10
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 10 เท่า\nคุณเสียภาษี"+tax)
            if precentage < 978 and precentage >= 948: # 3 % rate
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 5 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 5
            if precentage < 948 and precentage >= 748: #  20% rate
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 1 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 1
            if precentage < 748 and precentage >= 248: #  50% rate
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 0.5 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 0.5
            if precentage < 248 and precentage >= 0: # 28% rate
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 0.2 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 0.2


            # if precentage >= 990: # 0.2% rate
            #     multiple = ra_points * 100
            #     await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 100 เท่า \nคุณเสียภาษี"+tax)
            # if precentage < 990 and precentage >= 940: # 2 % rate
            #     multiple = ra_points * 10
            #     await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 10 เท่า\nคุณเสียภาษี"+tax)
            # if precentage < 940 and precentage >= 880: # 3 % rate
            #     await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 5 เท่า\nคุณเสียภาษี"+tax)
            #     multiple = ra_points * 5
            # if precentage < 880 and precentage >= 580: #  20% rate
            #     await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 1 เท่า\nคุณเสียภาษี"+tax)
            #     multiple = ra_points * 1
            # if precentage < 580 and precentage >= 180: #  50% rate
            #     await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 0.5 เท่า\nคุณเสียภาษี"+tax)
            #     multiple = ra_points * 0.5
            # if precentage < 180 and precentage >= 0: # 28% rate
            #     await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 0.2 เท่า\nคุณเสียภาษี"+tax)
            #     multiple = ra_points * 0.2

                
            url = 'http://localhost/python-api/index.php'
            myobj = { 'action': 'addmoney', 'userid': player_id, 'money': multiple }
            x = requests.post(url, data = myobj)
            print(player_name+" สุ่มด้วยจำนวนเงิน"+str(ra_points)+" ได้กลับไป "+str(multiple)+" points")
        if player_points < ra_points:
            await ctx.channel.send("คุณมีเงินไม่เพียงพอต่อการเล่นครับ")
@bot.command()
async def pay(ctx, amount ,target_id):
    #chck user profile
    amount = int(amount)
    target_id = str(target_id)
    player_id = str(ctx.author.id)
    player_name = str(ctx.author)
    mycursor = mydb.cursor()
    sql = "SELECT * FROM profile WHERE userid = %s"
    val = (player_id, )
    mycursor.execute(sql,val)
    result = mycursor.fetchone()
    if type(result) == type(None):
        await ctx.channel.send("<@"+player_id+"> คุณยังไม่ได้มีโปรไฟล์ในฐานข้อมูล รอสักครู่เรากำลังสร้างให้คุณ")
        url = 'http://localhost/python-api/index.php'
        myobj = {'action': 'create_profile','userid': player_id,'player_name': player_name}
        x = requests.post(url, data = myobj)
        player_points = 500
        print("create profile for"+player_name+"success")
        await ctx.channel.send("<@"+player_id+"> คุณมีโปรไฟล์ในฐานข้อมูลแล้ว")
    if type(result) != type(None):
        player_points = result[2]
    #check target profile
    mycursor = mydb.cursor()
    sql = "SELECT * FROM profile WHERE userid = %s"
    val = (target_id, )
    mycursor.execute(sql,val)
    result = mycursor.fetchone()
    if type(result) == type(None):
        await ctx.channel.send("<@"+player_id+"> ไม่พบบัญชีปลายทาง กรุณาตรวจสอบหมายเลขบัญชีอีกครั้ง")
    if type(result) != type(None):
        if player_points >= amount:
            #give money to target
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'addmoney','userid': target_id ,'money': amount}
            x = requests.post(url, data = myobj)
            # mycursor = mydb.cursor()
            # sql = "UPDATE profile SET points = points + %s WHERE userid = %s"
            # val = (amount, target_id)
            # print(str(player_name) + " pay " + str(target_id) + " total "+str(amount)+" points")
            # mycursor.execute(sql, val)
            # mydb.commit()
            #remove money from player
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'submoney','userid': player_id ,'money': amount}
            x = requests.post(url, data = myobj)
            print(str(player_name)+" โอนเงินให้"+str(target_id)+" จำนวน "+str(amount)+" points")
            await ctx.channel.send("<@"+player_id+"> โอนให้บัญชี "+str(target_id)+"เงินเรียบร้อย")
                    
                    
    
bot.run("Token Token Token")

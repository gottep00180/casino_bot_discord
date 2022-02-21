# CREDIT : JohnDoeDev
# github : https://github.com/gottep00180/casino_bot_discord/
# ไม่มีลิขสิทธิ์ใดๆ จะดัดแปลงเพื่อนำไปขายก็ได้ 

#import module ต่างๆเพื่อนำมาใช้งาน
import discord
from discord.utils import get
from discord.ext import commands
import random
import requests
import json
bot = commands.Bot(command_prefix='john!',help_command=None)

@bot.event
async def on_ready():
    #หาก login bot สำเร็จ จะแสดงข้อความ
    print("ALREADY login to bot")
@bot.command()
#function เช็คเงินในบัญชี ผู้เล่น
async def balance(ctx):
   #เช็คห้องที่ผู้เล่นส่งข้อความ
   if ctx.channel.name == "random" or ctx.channel.name == "🎲𝐁𝐈𝐋𝐋𝐈𝐎𝐍𝐀𝐈𝐑𝐄-𝐂𝐀𝐒𝐈𝐍𝐎":
        #กำหนดตัวแปรเกียวกับข้อมูลผู้เล่น
        player_id = str(ctx.author.id) #discord id ของ player
        player_name = str(ctx.author)  #ชื่อ dicsord ของ player 
        #ทำการใช้ api เช็คข้อมูล player
        url = 'http://localhost/python-api/index.php'
        myobj = {'action': 'userdata','player_id': player_id,'player_name': player_name}
        x = requests.post(url, data = myobj)
        #ใช้ json โหลดค่าสถานะต่างๆ
        res = json.loads(x.text)
        #เช็คว่าเจอข้อมูล player หรือไม่
        if res['found']  == "No":
            #หากไม่เจอข้อมูล player
            await ctx.channel.send("<@"+player_id+"> คุณยังไม่ได้มีโปรไฟล์ในฐานข้อมูล รอสักครู่เรากำลังสร้างให้คุณ")
            #ใช้ api สร้างโปรไฟล์ให้ player
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'create_profile','userid': player_id,'player_name': player_name}
            x = requests.post(url, data = myobj)
            print(x.text)
            #กำหนดเงินเริ่มต้นของ player ( 500 )
            player_points = 500
            print("create profile for"+player_name+"success")
            #สิ้นสดการสร้างโปรไฟล์
            await ctx.channel.send("<@"+player_id+"> คุณมีโปรไฟล์ในฐานข้อมูลแล้ว")
        if res['found']  == "Yes":
            #หากเจอข้อมูล player
            player_points =  int(res['money']) #กำหนดตัวแปรเงิน ของ player เป็นชนิด integer (ตัวเลข หากไม่ format จะเกิด Error) 
        await ctx.channel.send("<@"+player_id+">คุณมีเงินในบัญชีเหลือ : "+str(player_points)+"\nเลขบัญชีของคุณคือ"+player_id+"")
@bot.command()
#function สุ่มเงิน
#รับค่า ra_points คือ จำนวนเงินที่ผู้เล่นจะใช้สุ่ม
async def casino(ctx, ra_points): 
    if ctx.channel.name == "random" or ctx.channel.name == "🎲𝐁𝐈𝐋𝐋𝐈𝐎𝐍𝐀𝐈𝐑𝐄-𝐂𝐀𝐒𝐈𝐍𝐎":
        #code  หลังจากนี้จำเป็นต้องใช้ความรู้ทางคณิตศาสตร์ในเรื่อง การแปลงจำนวนเป็น %,หลักความน่าจะเป็น
        #กำหนดค่าที่ใช้สำหรับสุ่ม 
        precentage = random.randint(1, 1000)
        #กำหนดตัวแปรข้อมูลของ player
        player_id = str(ctx.author.id)
        player_name = str(ctx.author)
        #ใช้ api เช็คข้อมูลของ player 
        url = 'http://localhost/python-api/index.php'
        myobj = {'action': 'userdata','player_id': player_id,'player_name': player_name}
        x = requests.post(url, data = myobj)
        res = json.loads(x.text)
        #ไม่ขอทำการอธิบายตรงนี้ซ้ำนะครับ
        if res['found']  == "No":
            await ctx.channel.send("<@"+player_id+"> คุณยังไม่ได้มีโปรไฟล์ในฐานข้อมูล รอสักครู่เรากำลังสร้างให้คุณ")
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'create_profile','userid': player_id,'player_name': player_name}
            x = requests.post(url, data = myobj)
            print(x.text)
            player_points = 500
            print("create profile for"+player_name+"success")
            await ctx.channel.send("<@"+player_id+"> คุณมีโปรไฟล์ในฐานข้อมูลแล้ว")
        if res['found'] == "Yes":
            player_points =  int(res['money'])
        #format ชนิดข้อมูลเป็น integer  
        ra_points = int(ra_points)
        #หากใช้เงินสุ่มต่ำกว่า 10 points
        #หากไม่ต้องการมีขั้นต่ำในการสุ่ม ลบโค้ดสองบรรทัดนี้ออกได้เลย
        #หมายเหตุ : หากไม่มีขั้นต่ำในการสุ่ม เราแนะนำให้เปลี่ยนชนิดข้อมูลจาก int เป็น float
        if ra_points < 10:
            await ctx.channel.send("ในการสุ่มแต่ละครั้งยอดเงินจะต้องไม่ต่ำกว่า 10 points")
        #เช็คจำนวนเงิน ผู้เล่นว่ามีเพียงพอต่อการเล่นหรือไม่ และ จำนวนเงินผ่านขั้นต่ำหรือไม่
        if player_points >= ra_points and ra_points >= 10:
            #ใช้ api ลดเงินจากบัญชีผู้เล่น
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'submoney', 'player_id': player_id, 'money': ra_points }
            x = requests.post(url, data = myobj)
            print(x.text)
            #การเก็บภาษี หากไม่ต้องการลบทิ้งได้เลย
            #หมายเหตุ : หากลบภาษีออกโปรดระวังในเรื่องปัญหาเงินเฟ้อ
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

            #ตรงนี้จะเป็นเรทการตรวจสอบว่า player สุ่มเงินได้ระดับไหน
            #ตรงนี้จะใช้ค่า % ในการคำนวณหากไม่เข้าใจไม่แนะนำให้เปลี่ยนแปลงโค้ด
            #หมายเหตุ : หากเปลี่ยนแปลงเรทโปรดระวังในเรื่องปัญหาเงินเฟ้อ
            if precentage >= 998: # 0.2% rate x 100 money
                #ตัวแปร multiple คือตัวแปรสำหรับ เงินที่ผู้เล่นจะได้กลับไป
                multiple = ra_points * 100
                #ส่งข้อความบอกผู้เล่นว่าได้เงินเพิ่มกี่เท่า
                #หากต้องการบอกเป็นเงินที่ผู้เล่นได้กลับไป ก็สามารถ ใช้ตัวแปร multiple มาแสดงได้
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 100 เท่า \nคุณเสียภาษี"+tax)
            if precentage < 998 and precentage >= 978: # 2 % rate x10 money
                multiple = ra_points * 10
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 10 เท่า\nคุณเสียภาษี"+tax)
            if precentage < 978 and precentage >= 948: # 3 % rate x 5 money
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 5 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 5
            if precentage < 948 and precentage >= 748: #  20% rate x 1 money
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 1 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 1
            if precentage < 748 and precentage >= 248: #  50% rate x 0.5 money
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 0.5 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 0.5
            if precentage < 248 and precentage >= 0: # 28% rate x 0.2 money
                await ctx.channel.send("WOW!! <@"+player_id+"> ได้รับเงิน 0.2 เท่า\nคุณเสียภาษี"+tax)
                multiple = ra_points * 0.2


            #ใช้ api เพิ่มเงินเข้าบัญชีผู้เล่น     
            url = 'http://localhost/python-api/index.php'
            myobj = { 'action': 'addmoney', 'userid': player_id, 'money': multiple }
            x = requests.post(url, data = myobj)
            print(x.text)
            #print ออกทาง console สำหรับท่านใดที่ต้องการเก็บ log
            print(player_name+" สุ่มด้วยจำนวนเงิน"+str(ra_points)+" ได้กลับไป "+str(multiple)+" points")
        if player_points < ra_points:
            #หากผู้เล่นมีเงินไม่เพียงพอต่อการเล่น
            await ctx.channel.send("<@"+player_id+">คุณมีเงินไม่เพียงพอต่อการเล่นครับ")
@bot.command()
#function การโอนเงิน
#รับค่า amount คือ เงินที่ต้องการโอนให้ผู้เล่นคนอื่น
#รับค่า target_id หรือ บัญชีที่ผู้เล่นจะโอนเงินให้
async def pay(ctx, amount ,target_id):
    #ทำการ format ข้อมูล amount เป็น integer
    amount = int(amount)
    target_id = str(target_id)
    #ตัวแปรข้อมูล player
    player_id = str(ctx.author.id)
    player_name = str(ctx.author)
    #เช็คข้อมูล player
    url = 'http://localhost/python-api/index.php'
    myobj = {'action': 'userdata','player_id': player_id,'player_name': player_name}
    x = requests.post(url, data = myobj)
    res = json.loads(x.text)
    if res['found']  == "No":
        await ctx.channel.send("<@"+player_id+"> คุณยังไม่ได้มีโปรไฟล์ในฐานข้อมูล รอสักครู่เรากำลังสร้างให้คุณ")
        url = 'http://localhost/python-api/index.php'
        myobj = {'action': 'create_profile','userid': player_id,'player_name': player_name}
        x = requests.post(url, data = myobj)
        print(x.text)
        player_points = 500
        print("create profile for"+player_name+"success")
        await ctx.channel.send("<@"+player_id+"> คุณมีโปรไฟล์ในฐานข้อมูลแล้ว")
    if res['found'] == "Yes":
        player_points =  int(res['money'])
    #เช็คข้อมูล บัญชีปลายทาง
    url = 'http://localhost/python-api/index.php'
    myobj = {'action': 'userdata','player_id': player_id}
    x = requests.post(url, data = myobj)
    res = json.loads(x.text)
    #เช็คว่ามีบัญชีปลายทางหรือไม่
    if res['found'] == "No":
        #หากไม่มี
        await ctx.channel.send("<@"+player_id+"> ไม่พบบัญชีปลายทาง กรุณาตรวจสอบหมายเลขบัญชีอีกครั้ง")
    if res['found'] == "Yes":
        #หากพบบัญชีปลายทาง
        #เช็คเงินผู้เล่นว่ามีมากพอต่อการโอนหรือไม่
        if player_points >= amount:
            #เพิ่มเงินเข้าบัญชีปลายทาง
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'addmoney','userid': target_id ,'money': amount}
            x = requests.post(url, data = myobj)
            print(x.text)
            #หักเงินจากบัญชีคนโอน
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'submoney', 'player_id': player_id, 'money': amount }
            x = requests.post(url, data = myobj)
            print(x.text)
            #print ออกทาง console
            print(str(player_name)+" โอนเงินให้"+str(target_id)+" จำนวน "+str(amount)+" points")
            #ส่งข้อความบอก player
            await ctx.channel.send("<@"+player_id+"> โอนให้บัญชี "+str(target_id)+"เงินเรียบร้อย")
@bot.command()
#function ซื้อยศ 
#รับค่า rank คือ ชื่อยศที่ player ต้องการซื้อ
async def buy(ctx, rank):
    #formatตัวแปร rank เป็น string
    rank = str(rank)
    #เช็คช่องข้อความที่ผู้เล่นส่ง
    if ctx.channel.name == "random":
        #ตัวแปรข้อมูลของ player
        player_id = str(ctx.author.id)
        player_name = str(ctx.author)
        #ยศที่ player มี
        user = ctx.author.roles
        #เช็คข้อมูลของ player
        url = 'http://localhost/python-api/index.php'
        myobj = {'action': 'userdata','player_id': player_id,'player_name': player_name}
        x = requests.post(url, data = myobj)
        res = json.loads(x.text)
        if res['found']  == "No":
            await ctx.channel.send("<@"+player_id+"> คุณยังไม่ได้มีโปรไฟล์ในฐานข้อมูล รอสักครู่เรากำลังสร้างให้คุณ")
            url = 'http://localhost/python-api/index.php'
            myobj = {'action': 'create_profile','userid': player_id,'player_name': player_name}
            x = requests.post(url, data = myobj)
            print(x.text)
            player_points = 500
            print("create profile for"+player_name+"success")
            await ctx.channel.send("<@"+player_id+"> คุณมีโปรไฟล์ในฐานข้อมูลแล้ว")
        if res['found']  == "Yes":
            player_points =  int(res['money'])
        #เช็คว่าผู้เล่นต้องการซื้่อ ยศ newbie หรือไม่
        if rank == "newbie":
            #หากผู้เล่นมีเงินไม่พอต่อการซื้อยศ (3,000 points)
            if player_points < 3000:
                await ctx.channel.send("<@"+player_id+"> คุณมีเงินไม่เพียงพอ ในการซื้อยศครั้งนี้")
            #หากต้องการซื้อยศ newbie
            if player_points >= 3000:
                #ผู้เล่นมีเงินพอต่อการซื้อ (ราคา 3,000 points)
                #ตัวแปรเข้าถึง discord ที่ผู้เล่นใช้บอท
                guild = ctx.author.guild
                #การเข้าถึงยศ
                role = discord.utils.get(guild.roles, name="〖🎲〗 นักพนันสมัครเล่น") # Gets the role
                #เช็คผู้เ่ลนมียศนี้แล้วหรือยัง
                if role in user:
                    await ctx.channel.send("<@"+player_id+"> คุณเป็น 〖🎲〗 นักพนันสมัครเล่น อยู่แล้ว")
                else:
                    #หากยังไม่มี
                    if role is None: # เช็คให้แน่ใจว่า ยศนี้มีอยู่แล้วบนดิสคอร์ดนั้นๆ
                        #หากยังไม่มียศ
                        await ctx.channel.send("<@"+player_id+"> ยศนี้ไม่มีอยุ่บนดิสคอร์ดนี้ โปรดติดต่อแอดมิน")
                    if role is not None:
                        #หากมียศนี้แล้ว
                        #role คือตัวแปรยศที่จะำทการให้ 
                        role = discord.utils.find(lambda r: r.name == '〖🎲〗 นักพนันสมัครเล่น', ctx.message.guild.roles)
                        #ใช้ api หักเงินจากบัญชีผู้เล่น
                        url = 'http://localhost/python-api/index.php'
                        myobj = {'action': 'submoney', 'player_id': player_id, 'money': amount }
                        x = requests.post(url, data = myobj)
                        print(x.text)
                        #ให้ยศกับ player 
                        #ตรงนี้บอทจะต้องมียศที่สูงกว่ายศที่จะให้มิฉะนั้นบอทจะไม่สามารถให้ยศแก่ผู้เล่นได้
                        await ctx.author.add_roles(role)
                        #ส่งข้อความบอก player
                        await ctx.channel.send("<@"+player_id+"> สั่งซื้อสำเร็จ ยินดีต้อนรับ 〖🎲〗 นักพนันสมัครเล่น คนใหม่")
            
                    
                    
    
bot.run("Your bot token here")

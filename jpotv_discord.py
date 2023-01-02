import datetime
from time import sleep

import cv2
import discord
import m3u8
import yaml
import os
from discord.ext import tasks
from selenium import webdriver

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

with open(f'{os.environ["JPOTV"]}/cred/path.yaml', encoding="UTF-8") as f:
    cred = yaml.load(f, Loader=yaml.FullLoader)

## function line
## channel search
def find_channel():
    channel_ch_list = []
    channel_spt_list = []
    channel_ch_list_1 = []
    channel_spt_list_1 = []

    # channel 1 ~ 20
    for i in range(1, 20):
        if len(str(i)) == 1:
            ch = "0" + str(i)
        else:
            ch = str(i)

        url_ch = cred["CH_PATH"]
        url_ch = url_ch + cred["KEYPAIR"]
        try:
            playlist = m3u8.load(url_ch)
            channel_ch_list.append(url_ch)
        except:
            pass

        url_spt = cred["SPT_PATH"]
        url_spt = url_spt + cred["KEYPAIR"]
        try:
            playlist = m3u8.load(url_spt)
            channel_spt_list.append(url_spt)
        except:
            pass

    # channel 20~40
    for i in range(20, 40):
        if len(str(i)) == 1:
            ch = "0" + str(i)
        else:
            ch = str(i)

        url_ch = cred["CH_PATH"]
        url_ch = url_ch + cred["KEYPAIR"]
        try:
            playlist = m3u8.load(url_ch)
            channel_ch_list_1.append(url_ch)
        except:
            pass

        url_spt = cred["SPT_PATH"]
        url_spt = url_spt + cred["KEYPAIR"]
        try:
            playlist = m3u8.load(url_spt)
            channel_spt_list_1.append(url_spt)
        except:
            pass

    res_list = (
        channel_spt_list + channel_ch_list + channel_spt_list_1 + channel_ch_list_1
    )
    return res_list

## new search
def find_channel_new():
    link_1 = cred["link_1"]
    link_2 = cred["link_2"]
    link_3 = cred["link_3"]

    res_list = [link_1, link_2, link_3]
    return res_list

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    cronjob.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

    if message.content.startswith("채널"):
        channel = message.channel
        await message.channel.send(f"{channel.id}")

    # channel search
    if message.content == "ㅈ포티비":
        await message.channel.send(f"현재 살아있는 ㅈ포티비 링크")

        #res_list = find_channel()
        res_list = find_channel_new()

        counter = 1
        for i in res_list:
            driver = webdriver.Safari()
            driver.get(i)
            sleep(5)
            img_name = i[41:46] + ".png"
            driver.get_screenshot_as_file(f"result/{img_name}")
            # img compare
            image = cv2.imread(f"result/{img_name}", cv2.IMREAD_GRAYSCALE)
            image_size = 0

            for line in image:
                for j in line:
                    image_size += line[j]

            if abs(image_size / cred["BLACK_FILE_SIZE"]) > 1.05 or abs(image_size / cred["BLACK_FILE_SIZE"]) < 0.95:
                await message.channel.send(f"탐색중 총{len(res_list)} 중 {counter}번째")
                img_file = discord.File(f"result/{img_name}")
                await message.channel.send(i, file=img_file)

            driver.close()

            counter += 1
        await message.channel.send(f"탐색 완료")


@tasks.loop(minutes=1)
async def cronjob():
    print("funcg")
    ch = client.get_channel(cred["JPOTV_CHANNEL_ID"])
    now = datetime.datetime.now().minute
    if now in (10, 25, 40, 55):
    #if now:
        await ch.send(f"{now}분 채널 탐색 시작")
        #res_list = find_channel()
        res_list = find_channel_new()
        print(res_list)
        counter = 1
        for i in res_list:
            driver = webdriver.Safari()
            driver.get(i)
            sleep(5)
            img_name = i[41:46] + ".png"
            driver.get_screenshot_as_file(f"result/{img_name}")
            # img compare
            image = cv2.imread(f"result/{img_name}", cv2.IMREAD_GRAYSCALE)
            image_size = 0

            for line in image:
                for j in line:
                    image_size += line[j]

            #if abs(image_size / BLACK_FILE_SIE) > 1.05 or abs(image_size / BLACK_FILE_SIE) < 0.95:
            if image_size :
                await ch.send(f"탐색중 총{len(res_list)} 중 {counter}번째")
                img_file = discord.File(f"result/{img_name}")
                await ch.send(i, file=img_file)

            driver.close()

            counter += 1
    else:
        pass


token = cred["DISCORD"]
client.run(token)

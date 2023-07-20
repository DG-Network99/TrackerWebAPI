import os
import asyncio
from pyrogram import Client, filters
#from pyrogram import *
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, User, ChatJoinRequest
from sql import add_user, query_msg, full_userbase, add_channel, full_channelbase, channel_query_msg, add_product, full_productbase
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from pyromod import listen
import Keep_Alive



WAIT_MSG = """"<b>Processing ...</b>"""
REPLY_ERROR = """<code>Use this command as a replay to any telegram message with out any spaces.</code>"""

Bot = Client(
    "my bot",
    bot_token="",
    api_id=int(""),
    api_hash=""

)

ADMINS = []
ADMINS.append(1459159818)  # username
ADMINS.append(5398449311)  # sk
ADMINS.append(947720397)  # gpp
ADMINS.append(1192254405)  # panthor
ADMINS.append(1378380156)  # dina

def get_channel_id():
    users = full_channelbase()
    channel_id = []
    for i in users:
        channel_id.append(i.id)
    return channel_id

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(client: Bot, message: Message):
    bot = await client.get_me()
    print(client)
    user = message.from_user
    print(user)
    try:
        await add_user(user.id, user.username)

    except Exception as e:
        print(e)    


    button = [[
        InlineKeyboardButton("UPDATES", url="https://t.me/TechzenBots"),
        InlineKeyboardButton("SUPPORT", url="https://t.me/TechzenBots")
    ], [InlineKeyboardButton("SUBSCRIBE", url=f"https://t.me/TechzenBots")]]

    await message.reply_text(
        text=
        f"**Hello {message.from_user.mention}\n\nI am Amazon Purchase Suggestor AI Bot under construction**",
        reply_markup=InlineKeyboardMarkup(button),
        disable_web_page_preview=True)

@Bot.on_message(filters.private & filters.command(["suggest"]))
async def suggest(client: Bot, message: Message):
    # asking = await client.ask(message.chat.id, "enter: ")
    # get_response = await client.listen(message.chat.id, timeout=300, filters=filters.user(message.from_user.id) & filters.text)
    # print(get_response)

    get_response = await message.chat.ask('Provide the Product you want to purchase')
    # print(answer)
    
    filtered_product_list = await amazon_scrapper(get_response.text)

    # result = map(lambda a : str(a) + "/n", filtered_product_list)
    # res = list(result)
    products_foratted_string = ""
    index = 1
    for i in filtered_product_list[:8]:
        products_foratted_string  = products_foratted_string + i + '\n\n'
        index+=1
        

    print(products_foratted_string)
    if products_foratted_string:
        await get_response.reply(f'<b>Your Product list: </b>\n\n{products_foratted_string} \nTry Again /suggest', quote=False) 
    else:
        await get_response.reply(f'<b>Something went wrong. Please check your spelling.\nTry Again /suggest </b>', quote=False)     
 
@Bot.on_message(filters.private & filters.command(["p"]))
async def add_products(client: Bot, message: Message):
    product = await message.chat.ask('Enter the product name')
    print(product.text)
    await add_user(message.from_user.id, message.from_user.username)
    user = message.from_user
    print(user)
    try:
        response = await add_product(message.from_user.id, product.text)
        print(response)
    
    except Exception as e:
        print("problem in add product", e)

    await product.reply("Product Added")

@Bot.on_message(filters.private & filters.command(["list"]))
async def list_product(client: Bot, message: Message):
    products = await full_productbase(message.from_user.id)

    products_list = []

    for product in products:
        print(product.product_name)
        products_list.append(product.product_name)
    
    web_format = f'https://interested-reducing-bug-pdt.trycloudflare.com/{message.from_user.id}'
    # msg = await client.send_message(chat_id=message.chat.id, text= products_list)
    msg = await client.send_message(chat_id=message.chat.id, text= web_format) 



Keep_Alive.keep_alive()
print("Bot Started")
Bot.run()

import os, time, requests
import g4f, random
from pyrogram import filters
from Celestia import Celestia
from pyrogram.enums import ChatAction, ParseMode
from Celestia.modules.chatbot import cele_text



                



@Celestia.on_message(filters.command(["deep"], prefixes=["+", ".", "/", "-", "?", "$", "#", "&"]))
async def chat(celestia, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "**ʜᴇʟʟᴏ sɪʀ**\n**ᴇxᴀᴍᴘʟᴇ:-** Please provide text after the .deep command"
            )
        else:
            a = message.text.split(' ', 1)[1]
            data = {
                'text': a,  
            }

            headers = {
                'api-key': 'c8e3d7fc-1f7e-455b-8019-5c1b7f21047a',
            }

            r = requests.post("https://api.deepai.org/api/text-generator", data=data, headers=headers)
            response = r.json()

            if 'output' in response:
                answer_text = response['output']
                await message.reply_text(f"{answer_text}")
            else:
                await message.reply_text("Failed to generate text. Please try again later.")

    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e}")




@Celestia.on_message(filters.command(["bing"],  prefixes=["+", ".", "/", "-", "?", "$","#","&"]))
async def bing_ai(celestia :Celestia, message):
    
    try:
        if len(message.command) < 2:
            await message.reply_text(
            "**ʜᴇʟʟᴏ sɪʀ**\n**ᴇxᴀᴍᴘʟᴇ:-**`.bing How to set girlfriend ?`")
        else:
            query = message.text.split(' ', 1)[1]
            response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": query}],  
            provider=g4f.Provider.Bing
            )
            await message.reply_text(f"{response}")     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")        


@Celestia.on_message(filters.command(["chatbase"],  prefixes=["+", ".", "/", "-", "?", "$","#","&"]))
async def chatbase_ai(celestia :Celestia, message):
    
    try:
        if len(message.command) < 2:
            await message.reply_text(
            "**ʜᴇʟʟᴏ sɪʀ**\n**ᴇxᴀᴍᴘʟᴇ:-**`.ChatBase How to set girlfriend ?`")
        else:
            query = message.text.split(' ', 1)[1]
            response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": query}],  
            provider=g4f.Provider.ChatBase
            )
            await message.reply_text(f"{response}")     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")        



@Celestia.on_message(filters.command(["ssistant", "ssis"],  prefixes=["a","A"]))
async def chatbase_ai(celestia :Celestia, message):
    
    try:
        if len(message.command) < 2:
            await message.reply_text(random.choice(cele_text))
            
        else:
            query = message.text.split(' ', 1)[1]
            response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": query}],  
            provider=g4f.Provider.Llama2
            )
            await message.reply_text(f"{response}")     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")        




@Celestia.on_message(filters.command(["gpt"],  prefixes=["+", ".", "/", "-", "?", "$","#","&"]))
async def gpt_ai(celestia :Celestia, message):
    
    try:
        if len(message.command) < 2:
            await message.reply_text(
            "**ʜᴇʟʟᴏ sɪʀ**\n**ᴇxᴀᴍᴘʟᴇ:-**`.gpt How to set girlfriend ?`")
        else:
            query = message.text.split(' ', 1)[1]
            response = await g4f.ChatCompletion.create_async(
            model=g4f.models.default,
            messages=[{"role": "user", "content": query}],  
            provider=g4f.Provider.ChatgptAi
            )
            await message.reply_text(f"{response}")     
    except Exception as e:
        await message.reply_text(f"**ᴇʀʀᴏʀ**: {e} ")        




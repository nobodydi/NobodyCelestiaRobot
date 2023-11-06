import pydub
from Celestia import Celestia
from pyrogram import filters



@Celestia.on_message(filters.command("bass") & filters.reply)
async def download_and_enhance_audio(client, message):
    try:
        reply_message = message.reply_to_message

        if reply_message.audio:
            celu = await message.reply("processing")
            audio = await reply_message.download()
            audio_segment = pydub.AudioSegment.from_file(audio)
            await celu.edit("now adding bass and uploading...")
            
            enhanced_audio = audio_segment + 10           
            enhanced_audio.export("enhanced_audio.ogg", format="ogg")
            await celu.delete()
            await message.reply_audio("enhanced_audio.ogg")
        else:
            await message.reply("The replied message is not an audio.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")





@Celestia.on_message(filters.command("loudly") & filters.reply)
async def download_and_enhance_audio(client, message):
    try:
        reply_message = message.reply_to_message

        if reply_message.audio:
            celu = await message.reply("processing")
            audio = await reply_message.download()
            audio_segment = pydub.AudioSegment.from_file(audio)
            await celu.edit("now adding loude audio and uploading...")
        
            louder_audio = audio_segment + 10
            
            louder_audio.export("louder_audio.ogg", format="ogg")
            await celu.delete()
            await message.reply_audio("louder_audio.ogg")
        else:
            await message.reply("The replied message is not an audio.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")





@Celestia.on_message(filters.command("mono") & filters.reply)
async def split_stereo_and_send_audio(client, message):
    try:
        reply_message = message.reply_to_message

        if reply_message.audio:
            a = pydub.AudioSegment.from_file(await reply_message.download())
            b = a.split_to_mono()
            mono_audio = b[0]
            mono_audio.export("celestia.wav", format="wav")
            await message.reply_audio("celestia.wav")
        else:
            await message.reply("The replied message is not an audio.")
    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")



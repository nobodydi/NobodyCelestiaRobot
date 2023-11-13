import random
from Celestia import Celestia
from pyrogram import filters
from pyrogram.types import CallbackQuery InlineKeyboardMarkup, InlineKeyboardButton
from Celestia.modules.Games.games import users_collection


character_data = {
    "vivi": {"image": "", "name": "Vivi", "level": 1},
    "shikamaru": {"image": "", "name": "Shikamaru", "level": 1},
    "sado": {"image": "", "name": "Sado", "level": 1}
    }


@Celestia.on_message(filters.command("character"))
async def character_creation(client, message):
    user_id = message.from_user.id
    

    keyboard = InlineKeyboardMarkup(
        [[
                InlineKeyboardButton("", callback_data=f"vivi_"),
                InlineKeyboardButton("", callback_data=f"shikamaru_")
        ][
                InlineKeyboardButton("", callback_data=f"sado_")
        ]]
    )

    await message.reply_photo(
        photo="https://telegra.ph/file/55e27bacddf487d920a1a.jpg",
        caption="Choose your character:",
        reply_markup=keyboard
    )



@Celestia.on_callback_query(filters.regex(r'^choose_(Soda|Vivi|Shikamaru)$'))
async def choose_character_callback(client, query):
    user_id = query.from_user.id
    character_name = query.data.split('_')[1]

    users_data = {
        "name": character_name,
        "health": 100,
        "rank": "Novice Traveler",
        "partner": None,
        "experience": "[▰▱▱▱▱]1%",
        "level": 1,  
        "location": None,
        "battle_win": 0,
        "total_win": 0,
        "player_id": user_id
    }

    users_collection.insert_one({user_id: users_data})
    await query.edit_message_text(f"You have chosen {character_name}! You can now use the /fight command.")

@Celestia.on_message(filters.command("profile"))
async def profile_command(client, message):
    user_id = message.from_user.id

    user_data = users_collection.find_one({user_id})

    if not user_data:
        await message.reply("You haven't created a character yet. Use the /character command to create one.")
        return

    character_data = user_data
    user_profile = f"""
┏━━━━━━━━━━━━━━━━━
┣ Umm Player profile 
┗━━━━━━━━━━━━━━━━━
┏━⦿
┣⬢ Name : {character_data['name']}
┣⬢ Health : {character_data['health']}
┣⬢ Celeus : 0
┣⬢ Player ID : {character_data['player_id']}
┗━━━━━━━━━⦿

┏━⦿
┣ Exp : {character_data['experience']}
┣ Level : {character_data['level']}
┣ Rank : {character_data['rank']}
┣ Location : {character_data['location']}
┣ Battles Win : {character_data['battle_win']}
┣ Total Battles : {character_data['total_win']}
┗━━━━━━━━━⦿
"""

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Family", callback_data="family_profile"),
         InlineKeyboardButton("Shop", callback_data="open_shop")]
    ])

    await message.reply_photo(
        photo="https://telegra.ph/file/55e27bacddf487d920a1a.jpg",
        caption=user_profile,
        reply_markup=reply_markup
    )




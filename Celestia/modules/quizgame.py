from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo, re, random
from config import MONGO_URL, OWNER_ID
from Celestia import Celestia


client = pymongo.MongoClient(MONGO_URL)
db = client["quiz_games_db"]
questions_collection = db["questions"]
winners_collection = db["winners"]





def create_quiz_keyboard_regex(question):
    options = question["options"]
    buttons = [InlineKeyboardButton(f"Option {i+1}", callback_data=f"option_{i+1}") for i in range(4)]
    keyboard = InlineKeyboardMarkup([buttons])
    return keyboard



def get_top_10_winners():
    top_winners = winners_collection.aggregate([
        {"$group": {"_id": "$user_id", "username": {"$first": "$username"}, "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    return [winner["username"] for winner in top_winners]









@Celestia.on_message(filters.command("addquiz") & filters.user(OWNER_ID))
async def add_quiz(_, message):
    if len(message.text) < 11:
        return await message.reply("**Please provide the quiz details in the format:**\n\n /addquiz quiz_url+question+option1+option2+option3+option4+correct_answer")
    if not message.text.split(maxsplit=1)[1]:
        return await message.reply("**Please provide the quiz details in the format:**\n\n /addquiz quiz_url+question+option1+option2+option3+option4+correct_answer")
    quiz_details = message.text.split(maxsplit=1)[1]
    data = quiz_details.split("+")
    if not data[0].startswith("https"):
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ǫᴜɪᴢ ʟɪɴᴋ.**")
    if not data[1]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ǫᴜɪᴢ ǫᴜᴇsᴛɪᴏɴ.**")
    if not data[2]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴏᴘᴛɪᴏɴ1.**")
    if not data[3]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴏᴘᴛɪᴏɴ2.**")
    if not data[4]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴏᴘᴛɪᴏɴ3.**")
    if not data[5]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴏᴘᴛɪᴏɴ4.**")
    if not data[6]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ correct answere.**")
    
  
    quiz_url, question, option1, option2, option3, option4, correct_answer = data
    quiz_data = {
        "quiz_url": quiz_url,
        "question": question,
        "options": [option1, option2, option3, option4],
        "correct_answer": correct_answer
    }
    
    questions_collection.insert_one(quiz_data)
    await message.reply("Quiz added successfully!")






@Celestia.on_message(filters.group, group=11)
async def quiz_watcher(_, message):
    chat_id = message.chat.id

    if not message.from_user:
        return

    chat_document = questions_collection.find_one({"_id": chat_id})

    if not chat_document:
        return

    if "message_count" not in chat_document:
        questions_collection.update_one({"_id": chat_id}, {"$set": {"message_count": 0}})
        chat_document["message_count"] = 0

    questions_collection.update_one({"_id": chat_id}, {"$inc": {"message_count": 1})
    message_count = chat_document["message_count"]

    if message_count == 10:
        quiz_question = random.choice(chat_document["quiz_questions"])
        question_text = quiz_question["question"]
        options = quiz_question["options"]

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(option, callback_data=f"answer_{option}")]
            for option in options
        ])

        await _.send_photo(
            chat_id,
            photo=quiz_question["photo"],
            caption=question_text,
            reply_markup=keyboard
        )

        questions_collection.update_one({"_id": chat_id}, {"$set": {"quiz_message_id": message.message_id}})


@Celestia.on_callback_query()
async def check_answer(client, callback_query):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username
    selected_option = callback_query.data

    if callback_query.message.reply_to_message and "quiz_message_id" in callback_query.message.reply_to_message.reply_markup.inline_keyboard[0][0].callback_data:
        correct_answer = callback_query.message.reply_to_message.reply_markup.inline_keyboard[0][0].callback_data.split("_")[-1]
        if selected_option == correct_answer:
            winners_collection.insert_one({"user_id": user_id, "username": username, "question_id": callback_query.message.reply_to_message.message_id})
            await callback_query.answer("Correct answer! You are a winner.")
        else:
            await callback_query.answer("Wrong answer. Try again next time.")



@Celestia.on_message(filters.command("ranks"))
async def display_top_10_winners(client, message):
    top_winners = get_top_10_winners()
    if top_winners:
        winners_text = "\n".join([f"{i+1}. {username}" for i, username in enumerate(top_winners)])
        await message.reply(f"Top 10 Winners:\n{winners_text}")
    else:
        await message.reply("No winners yet!")









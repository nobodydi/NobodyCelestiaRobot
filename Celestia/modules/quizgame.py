import asyncio
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pymongo, re, random
from config import MONGO_URL, OWNER_ID
from Celestia import Celestia


client = pymongo.MongoClient(MONGO_URL)
db = client["quiz_games_db"]
questions_collection = db["questions"]
winners_collection = db["winners"]


DICT = {}




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
    if not data[2:5]:
        return await message.reply("**sᴡᴇᴇᴛʜᴇᴀʀᴛ ɪ ᴛʜɪɴᴋ ʏᴏᴜ ғᴏʀɢᴇᴛ ᴏᴘᴛɪᴏɴs.**")
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



# =================> wacther <=================== #



@Celestia.on_message(filters.group, group=11)
async def _watcher(client, message):
    chat_id = message.chat.id
    if not message.from_user:
        return

    if chat_id not in DICT:
        DICT[chat_id] = {'count': 0, 'running_count': 0, 'quiz_url': None, 'question': None, 'options': None, 'correct_answer': None}
    
    DICT[chat_id]['count'] += 1

    if DICT[chat_id]['count'] == 10:
        result = questions_collection.find()
        quizes = list(result)
        data = random.choice(quizes)
        photo = data["quiz_url"]
        question = data["question"]
        options = data["options"]
        correct = data["correct_answer"]
        try:
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(option, callback_data=f"answer_{option}")]
                for option in options
            ])

            await client.send_photo(
                chat_id,
                photo=photo,
                caption=f"Question: {question}",
                reply_markup=keyboard
            )
            DICT[chat_id]["quiz_url"] = photo
            DICT[chat_id]["question"] = question
            DICT[chat_id]["options"] = options
            DICT[chat_id]["correct_answer"] = correct
        except errors.FloodWait as e:
            await asyncio.sleep(e.x)
    
    if DICT[chat_id].get('correct_answer'):
        DICT[chat_id]['running_count'] += 1
        if DICT[chat_id]['running_count'] == 30:
            try:
                correct_answer = DICT[chat_id]['correct_answer']
                await client.send_message(chat_id, f"**correct answer is **: {correct_answer}\n**Make sure to remember it next time.**")
                DICT.pop(chat_id)
            except errors.FloodWait as e:
                await asyncio.sleep(e.x)




@Celestia.on_callback_query(filters.regex(r'^answer_\w+'))
async def callback_answer(client, query):
    chat_id = callback_query.message.chat.id
    if DICT.get(chat_id) and not DICT[chat_id]["correct_answer"]:
        DICT[chat_id]["correct_answer"] = True
        correct_answer = DICT[chat_id]['correct_answer']
        user_answer = query.data.replace('answer_',')  
        if user_answer == correct_answer:
            await query.message.edit_text(f"**Your answer is correct!**")
        
            user_scores_collection.update_one(
                {"chat_id": chat_id},
                {"$inc": {"correct_answers": 1}},
                upsert=True
            )
        else:
            await query.message.edit_text(f"**Your answer is wrong. The correct answer is {correct_answer}.**")





@Celestia.on_message(filters.command("ranks") & filters.group)
async def show_ranks(client, message):
    top_players = user_scores_collection.find({"correct_answers": {"$gt": 0}}).sort("correct_answers", -1).limit(10)
    if top_players.count() == 0:
        await message.reply("No users have answered correctly yet. Be the first one!")
        return

    response = "Top 10 Players:\n"
    for i, player in enumerate(top_players, start=1):
        response += f"{i}. {player['chat_id']} - {player['correct_answers']} correct answers\n"
    await message.reply(response)






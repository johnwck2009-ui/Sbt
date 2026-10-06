import os
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

QUESTIONS = [
    {
        "question": "តើប្រទេសណាឈ្នះ FIFA World Cup ច្រើនជាងគេ?",
        "options": ["ប្រេស៊ីល", "អាហ្សង់ទីន", "អាល្លឺម៉ង់", "បារាំង"],
        "answer": 0,
    },
    {
        "question": "តើកីឡាបាល់បោះត្រូវបានបង្កើតឡើងក្នុងឆ្នាំណា?",
        "options": ["1891", "1901", "1911", "1921"],
        "answer": 0,
    },
    {
        "question": "តើក្រុមមួយក្នុងកីឡាបាល់ទាត់មានកីឡាករប៉ុន្មាននាក់នៅលើទីលាន?",
        "options": ["9", "10", "11", "12"],
        "answer": 2,
    },
    {
        "question": "តើការប្រកួត Grand Slam វាយកូនបាល់មានប៉ុន្មាន?",
        "options": ["2", "3", "4", "5"],
        "answer": 2,
    },
    {
        "question": "តើកីឡាអូឡាំពិកសម័យទំនើបចាប់ផ្តើមនៅឆ្នាំណា?",
        "options": ["1886", "1896", "1906", "1916"],
        "answer": 1,
    },
    {
        "question": "តើការលេងកីឡាវាយកូនហ្គោលមួយជុំស្តង់ដារមានប៉ុន្មានរន្ធ?",
        "options": ["9", "12", "18", "24"],
        "answer": 2,
    },
    {
        "question": "តើកីឡាគ្រីឃីតមួយក្រុមមានកីឡាករប៉ុន្មាននាក់?",
        "options": ["9", "10", "11", "12"],
        "answer": 2,
    },
    {
        "question": "តើ Wimbledon ចាប់ផ្តើមនៅឆ្នាំណា?",
        "options": ["1877", "1887", "1897", "1907"],
        "answer": 0,
    },
    {
        "question": "តើចម្ងាយម៉ារ៉ាតុងផ្លូវការគឺប៉ុន្មាន?",
        "options": ["40.195 គីឡូម៉ែត្រ", "41.195 គីឡូម៉ែត្រ", "42.195 គីឡូម៉ែត្រ", "43.195 គីឡូម៉ែត្រ"],
        "answer": 2,
    },
    {
        "question": "តើកីឡាបាល់ទះដំបូងត្រូវបានហៅថាអ្វី?",
        "options": ["Mintonette", "Netball", "Volleyball", "Handball"],
        "answer": 0,
    },
    {
        "question": "តើ Formula 1 World Championship លើកដំបូងធ្វើឡើងនៅឆ្នាំណា?",
        "options": ["1940", "1950", "1960", "1970"],
        "answer": 1,
    },
    {
        "question": "តើកីឡាណាមួយប្រើពាក្យ «love» សម្រាប់ពិន្ទុសូន្យ?",
        "options": ["វាយកូនបាល់", "បាល់ទាត់", "បាល់បោះ", "ហ្គោល"],
        "answer": 0,
    },
    {
        "question": "តើកីឡាអូឡាំពិកសម័យទំនើបលើកដំបូងធ្វើឡើងនៅទីក្រុងណា?",
        "options": ["ប៉ារីស", "ឡុងដ៍", "អាថែន", "រ៉ូម"],
        "answer": 2,
    },
    {
        "question": "តើការប្រកួតបាល់ទាត់ស្តង់ដារមានប៉ុន្មានតង់?",
        "options": ["1", "2", "3", "4"],
        "answer": 1,
    },
    {
        "question": "តើប្រទេសណាជាម្ចាស់ផ្ទះ FIFA World Cup លើកដំបូង?",
        "options": ["ប្រេស៊ីល", "អ៊ុយរូហ្គាយ", "អ៊ីតាលី", "បារាំង"],
        "answer": 1,
    },
    {
        "question": "តើកីឡាបាល់បោះដំបូងប្រើអ្វីជាគោលដៅ?",
        "options": ["ប្រអប់ឈើ", "កន្ត្រកផ្លែប៉េស", "សំណាញ់ដែក", "ធុងទឹក"],
        "answer": 1,
    },
]

def quiz_keyboard(question_id):
    options = QUESTIONS[question_id]["options"]
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(options[0], callback_data=f"answer:{question_id}:0")],
        [InlineKeyboardButton(options[1], callback_data=f"answer:{question_id}:1")],
        [InlineKeyboardButton(options[2], callback_data=f"answer:{question_id}:2")],
        [InlineKeyboardButton(options[3], callback_data=f"answer:{question_id}:3")],
        [InlineKeyboardButton("សំណួរបន្ទាប់", callback_data="next")],
    ])

def question_message(question_id):
    return f"សំណួរកីឡា\n\n{QUESTIONS[question_id]['question']}"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_id = random.randrange(len(QUESTIONS))
    context.user_data["question_id"] = question_id
    await update.message.reply_text(
        f"SB Sports Quiz\n\n{question_message(question_id)}",
        reply_markup=quiz_keyboard(question_id),
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "next":
        question_id = random.randrange(len(QUESTIONS))
        context.user_data["question_id"] = question_id
        await query.edit_message_text(
            question_message(question_id),
            reply_markup=quiz_keyboard(question_id),
        )
        return

    _, question_id_text, answer_text = query.data.split(":")
    question_id = int(question_id_text)
    selected = int(answer_text)
    question = QUESTIONS[question_id]

    if selected == question["answer"]:
        result = "ត្រឹមត្រូវ!"
    else:
        correct = question["options"][question["answer"]]
        result = f"មិនត្រឹមត្រូវ។ ចម្លើយត្រឹមត្រូវគឺ {correct}។"

    await query.edit_message_text(
        f"{result}\n\n{question['question']}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("សំណួរបន្ទាប់", callback_data="next")]
        ]),
    )

def main():
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(quiz, pattern=r"^(answer:\d+:\d+|next)$"))
    app.run_polling()

if __name__ == "__main__":
    main()

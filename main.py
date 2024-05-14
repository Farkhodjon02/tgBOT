import telebot

TOKEN = ''

bot = telebot.TeleBot(TOKEN)

questions = [
    {
        "question": "The conversion time of a flash ADC:",
        "options": ["a) is proportional with number of bits on output, N",
                    "b) is not stable(oscillates +-1 bit) for constant input signals)",
                    "c) Depends of the level of the input signal ",
                    "d) Is independent of the number of bits on output,N"],
        "correct_option": "d) Is independent of the number of bits on output,N",
        "proof": "Correct option: d) Is independent of the number of bits on output,N, Learning details from book"
    },
    {
        "question": "A 1% increase of all the resistance of a flash type analog-to-digital converter determines:",
        "options": ["a) 1% higher current consumption of the resistor chain that generates all the voltage references",
                    "b) A 1% longer conversion time",
                    "c) No change of the conversion time",
                    "d) A 1% increase of all reference voltages"],
        "correct_option": "c) No change of the conversion time",
        "proof": "Correct option: No change of the conversion time, Learning details from book"
    },
    {
        "question": "The outputs of two identical open-drain logic gates are connected together. When both gates output a zero logic level (0 V), the voltage of the output node, Vout will stabilize to:",
        "options": ["a) Dependent on the capacitive load connected to ground (GND).",
                    "b) Dependent on the capacitive load connected to supply (VDD).",
                    "c) Vol<=Vout<=Voh",
                    "d) 0V<=Vout<=Vol"],
        "correct_option": "d) 0V<=Vout<=Vol",
        "proof": "Correct option: 0V<=Vout<=Vol, Learning details from book"
    },
    {
        "question": "The integration interval of a dual-slope integration ADC:",
        "options": ["a) can be set to a value higher than 100 PLC(Power Line Cycle)but without an effective noise rejection",
                    "b) cannot be set to a value lower than 1PLC(Power Line Cycle)",
                    "c) can be set to a value lower than 1PLC(Power Line Cycle) but without an effective noise rejection ",
                    "d) cannot be set to a value higher than 1PLC( Power Line Cycle)."],
        "correct_option": "c) can be set to a value lower than 1PLC(Power Line Cycle) but without an effective noise rejection",
        "proof": "Correct option: can be set to a value lower than 1PLC( Power Line Cycle) but without an effective noise rejection, Learning details from book"
    },
    {
        "question": "This is a sample question.",
        "options": ["a) Option A",
                    "b) Option B",
                    "c) Option C",
                    "d) Option D"],
        "correct_option": "a) Option A",
        "proof": "Correct option: a) Option A, Learning details from book"
    },
]

user_data = {}

def generate_keyboard(options):
    keyboard = telebot.types.InlineKeyboardMarkup()
    for idx, option in enumerate(options):
        keyboard.row(telebot.types.InlineKeyboardButton(option, callback_data=str(idx)))
    return keyboard

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to the Quiz Bot! Press /start_quiz to begin.")

@bot.message_handler(commands=['start_quiz'])
def start_quiz(message):
    chat_id = message.chat.id
    user_data[chat_id] = {"current_question": 0, "correct_count": 0}
    send_question(chat_id)

def send_question(chat_id):
    current_question = user_data[chat_id]["current_question"]
    if current_question < len(questions):
        question_data = questions[current_question]
        question = question_data["question"]
        options = question_data["options"]
        user_data[chat_id]["correct_option"] = question_data["correct_option"]
        bot.send_message(chat_id, question, reply_markup=generate_keyboard(options))
    else:
        end_quiz(chat_id)

def end_quiz(chat_id):
    correct_count = user_data[chat_id]["correct_count"]
    bot.send_message(chat_id, f"The quiz has ended. You answered {correct_count} out of {len(questions)} questions correctly.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    chat_id = call.message.chat.id
    current_question = user_data[chat_id]["current_question"]
    correct_option = user_data[chat_id]["correct_option"]
    selected_option_index = int(call.data)  # Convert callback data to integer

    print("Current question:", current_question)
    print("Total questions:", len(questions))

    if current_question < len(questions):
        print("Options for current question:", questions[current_question]["options"])

    if current_question < len(questions) and questions[current_question]["options"][selected_option_index] == correct_option:
        user_data[chat_id]["correct_count"] += 1
        bot.answer_callback_query(call.id, "Correct answer! 🎉")
        bot.send_message(chat_id, "Your answer is correct!")
    else:
        bot.answer_callback_query(call.id, "Incorrect answer. 😔")
        bot.send_message(chat_id, "Your answer is wrong.")
    user_data[chat_id]["current_question"] += 1
    send_proof(chat_id)

def send_proof(chat_id):
    current_question = user_data[chat_id]["current_question"] - 1
    proof = questions[current_question]["proof"]
    bot.send_message(chat_id, f"Proof: {proof}")
    send_question(chat_id)

# Bot polling
bot.polling()

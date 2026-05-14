import os
from dotenv import load_dotenv

load_dotenv()  # загружает .env

###### КОНСТАНТЫ ИЗ .ENV ######
SR_LOGIN = os.getenv('sr_login')  # Ваш демо-ключ
SR_PASS = os.getenv('sr_pass')
DB_HOST = os.getenv('db_host')
DB_PORT = os.getenv('db_port')
DB_SCHEMA = os.getenv('db_schema')
DB_DATABASE = os.getenv('db_database')

LOG = os.getenv('login')
PASS = os.getenv('password')

BOT_TOKEN=os.getenv('bot_token')
BOT_NAME=os.getenv('bot_name')

###### ТЕКСТЫ ######
HELP_TEXT = """
/add_client Имя Телефон
...
"""

###### VPT ТЕКСТЫ ######
CLIENT_ID = 'Выбери клента'
MOOD_TXT = "Как ты себя сегодня чувствуешь?\n\nВыспался ли ты и какое у тебя общее состояние?"
TRAINING_HISTORY = "Есть ли у тебя опыт тренировок в зале?\n\nКак долго занимался, с тренером или сам, и почему решил начать сейчас?"
HEALTH_COMPLAINTS = "Есть ли сейчас жалобы на здоровье или дискомфорт? Что беспокоило за последние две недели?"
FITNESS_GOALS = "Что ты хочешь изменить в себе?\n\nЗачем тебе тренировки и какой результат нужен в цифрах?"
EXPECTED_LIFE_CHANGES = "Если через 3 месяца ты достигнешь цели, какие изменения произойдут в жизни?\n\nУкажи до 5 вариантов."
GOAL_DETAILS = "Добавь детали, которые помогут точнее понять твою цель и лучше спланировать тренировки."
TRAINING_FREQUENCY = "Как часто ты планируешь тренироваться?"
PRODUCT_ID = "Какой пакет или блок занятий ты приобрёл?"
NEXT_SESSION_DATE = "Когда у тебя следующее занятие?"
PAYMENT_DATE = "На какую дату назначена оплата?"


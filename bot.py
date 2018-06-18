from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import random
import os
from googletrans import Translator
from flaskext.mysql import MySQL

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_HOST'] = os.environ.get('localhost')
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_USER'] = os.environ.get('root')
app.config['MYSQL_DATABASE_PASSWORD'] = os.environ.get('')
app.config['MYSQL_DATABASE_DB'] = os.environ.get('db_junebot')
mysql.init_app(app)


CHANNEL_ACCESS_TOKEN = os.environ.get('7YR60AJ855Zu1Etxsc7aCdFqhip1o8yAKj7PzLe90ClE9Po0fz5o81BeghtpCki4+zFZ7FrYjjbrFvQw84+Axi+P1zWPnxSCTl/lF5gVTDaDqdC5IHk30qnjo7GQ1hHKizexgGNpBPn/Fwz3slJqkQdB04t89/1O/w1cDnyilFU=')
CHANNEL_SECRET = os.environ.get('c3aa02ca5442a7640d2c577f936da0d4')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route('/')
def hello():
    return 'Hello World!'

@app.route('/webhook', methods=['POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as Text
    body = request.get_data(as_text=True)
    app.logger.info('Request body: '+body)

    # handler webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    conn = mysql.connect()
    c = conn.cursor()

    q = event.message.text.strip(' ')
    print('q=:'+q+':')
    foo = ['เรียกผมเหรอครับ', 'วาจังดายย', 'อะไรวะ', 'เรียกอยู่ได้', 'ถาหาขาไพ่?', 'Zzzz', 'ครับครับ', 'ย๊างหมอ']
    randAns = random.choice(foo)
    # print(randAns)
    line_bot_api.reply_message(
         event.reply_token,
         TextSendMessage(text=randAns))

    c.close()
    conn.close()

if __name__ == '__main__':
    app.run()

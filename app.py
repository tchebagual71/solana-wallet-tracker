from flask import Flask, request
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from telegram import Bot
from telegram.utils.request import Request
from PIL import Image
from io import BytesIO
import re
import logging
from datetime import datetime
import requests
import os

# Your config values
MONGODB_URI = 'mongodb+srv://test:test@cluster0.ehtddne.mongodb.net'
BOT_TOKEN = '6502984988:AAEE65Mor8XNvxhb3irkxtR8WqDHcbdinL8'
HELIUS_KEY = '9e17b24d-b88d-41e2-86e1-0bb6bf5b8095'
HELIUS_WEBHOOK_URL = 'https://walletwatchr-cacf9141608c.herokuapp.com/wallet'
HELIUS_WEBHOOK_ID = '5d8cadd0-ce36-4cb9-8cbc-6dc3d21705f'

client = MongoClient(MONGODB_URI, server_api=ServerApi('1'))
db = client.sol_wallets
wallets_collection = db.wallets

# Set up logging
logging.basicConfig(
    filename='wallet.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Telegram Bot Functions
def send_message_to_user(bot_token, user_id, message):
    request = Request(con_pool_size=8)
    bot = Bot(bot_token, request=request)
    bot.send_message(chat_id=user_id, text=message, parse_mode="Markdown", disable_web_page_preview=True)

def send_image_to_user(bot_token, user_id, message, image_url):
    request = Request(con_pool_size=8)
    bot = Bot(bot_token, request=request)
    image_bytes = get_image(image_url)
    bot.send_photo(chat_id=user_id, photo=image_bytes, caption=message, parse_mode="Markdown")

# Image Handling Functions
def get_image(url):
    response = requests.get(url).content
    image = Image.open(BytesIO(response))
    image = image.convert('RGB')
    max_size = (800, 800)
    image.thumbnail(max_size, Image.ANTIALIAS)
    image_bytes = BytesIO()
    image.save(image_bytes, 'JPEG', quality=85)
    image_bytes.seek(0)
    return image_bytes

def get_compressed_image(asset_id):
    url = f'https://rpc.helius.xyz/?api-key={HELIUS_KEY}'
    r_data = {"jsonrpc": "2.0", "id": "my-id", "method": "getAsset", "params": [asset_id]}
    response = requests.post(url, json=r_data)
    result = response.json()['result']['content']['json_uri']
    image_response = requests.get(url=result)
    return image_response.json()['image']

# Main Functions
def format_wallet_address(match_obj):
    wallet_address = match_obj.group(0)
    return wallet_address[:4] + "..." + wallet_address[-4:]

def check_image(data):
    token_mint = ''
    for token in data[0]['tokenTransfers']:
        if 'NonFungible' in token['tokenStandard']:
            token_mint = token['mint']
    if len(token_mint) > 0:
        url = f"https://api.helius.xyz/v0/token-metadata?api-key={HELIUS_KEY}"
        r_data = {"mintAccounts": [token_mint], "includeOffChain": True, "disableCache": False}
        response = requests.post(url, json=r_data)
        metadata = response.json()[0]['offChainMetadata']
        if 'metadata' in metadata and 'image' in metadata['metadata']:
            return metadata['metadata']['image']
    return ''

def create_message(data):
    accounts, messages, found_users = process_transaction_data(data)
    notify_users(accounts, messages, found_users)
    logging.info('ok event')
    return 'OK'

# Flask Setup
app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, this is the root page of the Solana Wallet Tracker!', 200

@app.route('/wallet', methods=['POST'])
def handle_webhook():
    data = request.json
    return create_message(data)

# Bot Initialization
if __name__ == '__main__':
    send_message_to_user(BOT_TOKEN, "YOUR_TELEGRAM_USER_ID", "Wallet Watchr is now online!")
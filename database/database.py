#Don't remove This Line From Here. Tg: @im_piro | @PiroHackz



import time
from datetime import datetime, timedelta
import pymongo
import os
from config import DB_URI, DB_NAME, VERIFY_EXPIRE
from bot import Bot
from datetime import datetime


current_time = datetime.now()
time_left = expiration_time - current_time
days_left = time_left.days
expiration_time = current_time + timedelta(days=time_limit_days)
expiration_timestamp = expiration_time.strftime("%Y-%m-%d %H:%M:%S")

dbclient = pymongo.MongoClient(DB_URI)
database = dbclient[DB_NAME]


user_data = database['users']
collection = database['premium-users']

default_verify = {
    'is_verified': False,
    'verified_time': VERIFY_EXPIRE,
    'verify_token': "",
    'link': ""
}

def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': 0,
            'verify_token': "",
            'link': ""
        }
    }


async def present_user(user_id : int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    user_data.insert_one(user)
    return

async def db_verify_status(user_id):
    user = user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def update_verify_status(user_id, verify_token="", is_verified=False, verified_time=0, link=""):
    current = await db_verify_status(user_id)
    current['verify_token'] = verify_token
    current['is_verified'] = is_verified
    current['verified_time'] = int(verified_time)  # Ensure it's an integer
    current['link'] = link
    await db_update_verify_status(user_id, current)

async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])
    return user_ids

async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

async def add_premium(user_id, time_limit_months):
    expiration_date = datetime.now() + timedelta(days=time_limit_months * 30)
    premium_data = {
        "user_id": user_id,
        "expiration_timestamp": expiration_date.strftime("%Y-%m-%d %H:%M:%S"),
    }
    collection.insert_one(premium_data)
    dbclient.close()

async def remove_premium(user_id):
    result = collection.delete_one({"user_id": user_id})
    dbclient.close()

async def remove_expired_users():
    current_time = datetime.now()
    expired_users = collection.find({
        "expiration_timestamp": {"$lte": current_time.strftime("%Y-%m-%d %H:%M:%S")}
    })
    
    for expired_user in expired_users:
        user_id = expired_user["user_id"]
        collection.delete_one({"user_id": user_id})

    dbclient.close()


async def list_premium_users():
    premium_users = collection.find({})
    
    premium_user_list = []

    for user in premium_users:
        user_id = user["user_id"]
        user_info = await Bot.get_users(user_id)  # Note: added 'await' here
        username = user_info.username if user_info.username else user_info.first_name
        expiration_timestamp = user["expiration_timestamp"]
        expiration_time = datetime.strptime(expiration_timestamp, "%Y-%m-%d %H:%M:%S")
        current_time = datetime.now()
        time_left = expiration_time - current_time
        days_left = time_left.days
        premium_user_list.append(f"{user_id} - {username} - Days Left: {days_left}")

    return premium_user_list

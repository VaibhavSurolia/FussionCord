#This will store the store data in the database

from functions.dbconnect import *
from datetime import datetime
from functions.encryption import *

collection = "messages"

async def store_message(sender, channel_id, message):
    dict = {
        "sender": sender,
        "channel_id": channel_id,
        "message": message,
        "time": datetime.now()
        }
    await send_data(collection, dict)
    return True

async def get_messages(message_id):
    data = await find_data(collection, {"id": id})
    return data

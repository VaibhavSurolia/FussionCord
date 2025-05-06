#This file will interact with the database and return the data

from bson.objectid import ObjectId
import asyncio
import json
from pymongo import MongoClient

with open('config.json', 'r') as f:
    config = json.load(f)

client = MongoClient("mongodb://localhost:27017/lonely")

db = client.lonely

async def send_data(collection, data):
    collection = db[collection]
    send_data = collection.insert_one(data)

async def find_data(collection, data):
    collection = db[collection]
    results = collection.find_one(data)
    return results

async def delete_data(collection, data):
    collection = db[collection]
    deleted = collection.delete_one(data)

async def update_data(collection, dict, new_data):
    collection = db[collection]
    updated = collection.update_one(dict, {"$set": new_data})

async def remove_data(collection, dict, new_data):
    collection = db[collection]
    updated = collection.update_one(dict, {"$unset": new_data})
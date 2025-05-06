#Just some important functions for the program for handling user related data

import json
import os
import asyncio
from pydantic import BaseModel
from functions.dbconnect import *
from functions.encryption import *

collection = "user"


class Item(BaseModel):
    name: str

async def user_create(email, password, name, surname, birthdate, phone_number = None, city = None, country = None):
    data = await user_check(email)
    if data is True:
        return False
    token = await encrypt(email, password)
    dict = {
        "token": token,
        "user_info": {
            "email": email,
            "name": name,
            "surname": surname,
            "birthdate": birthdate,
            "phone_number": phone_number,
            "city": city,
            "country": country
        },
        "orders": {
            "cart": {
                "id": []
            },
            "orders": {
                "id": []
            }
        },
        "others":{
            "wishlist": {
                "id": []
            },
            "recently_viewed": {
                "id": [],
                "category": []
            }
        }
    }     
    
    data = await send_data(collection, dict)
    return data


async def user_check(email):
    data = await find_data(collection, {
        "user_info.email": email
    })
    if data is None:
        return False
    else:
        return True

async def user_delete(email, password):
    data = await user_check(email)
    if data is False:
        return("Email not registered")
    await delete_data(collection, {
        "user_info.email": email
    })

async def user_get(token):
    data = await decrypt(token)
    data = data.split(':')
    email = data[0]
    password = data[1]
    data = await find_data(collection, {
        "user_info.email": email,
        "user_info.password": password
    })
    if data is None:
        return False
    else:
        return data

async def user_update(email, name = None, surname = None, birthdate = None, phone_number = None, address = None, city = None, country = None):
    data = await user_check(email)
    if data is True:
        return False
    dict = [email, name, surname, birthdate, phone_number, address, city, country]
    for key, value in dict.items():
        if value is None:
            del dict[key]
    update_data(collection, {"email": email}, dict)
    return True

#print(asyncio.run(user_delete("me@lonelyguyy.me", "i wonder...")))

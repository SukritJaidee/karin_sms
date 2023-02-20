# coding=utf8
import json
import requests
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER
from Crypto.Cipher import AES
import codecs
import calendar
import time
from helper.initial_f import *
from helper.eresort_f import *

def pad(m):
    return m+chr(16-len(m)%16)*(16-len(m)%16)

def gen_password(openapi, device_id, ACCESS_KEY, phone_number):
  response = openapi.post(f"/v1.0/devices/{device_id}/door-lock/password-ticket")
  # print(response)
  ticket_key = response["result"]["ticket_key"]
  ticket_id = response["result"]["ticket_id"]
  key = ACCESS_KEY

  # decrypt ticket_key with ACCESS_KEY
  decipher = AES.new(key, AES.MODE_ECB)
  real_key_decrypt = decipher.decrypt(codecs.decode(ticket_key, 'hex_codec'))
  real_key_str = real_key_decrypt.decode('UTF-8')
  real_key = real_key_str[:16]

  # encrypt password with decrypt key
  real_key = bytes(real_key, "UTF-8")
  cipher = AES.new(real_key, AES.MODE_ECB)
  password = phone_number[:-3] # 7 digit
  msg = cipher.encrypt(pad(password))
  password_hex = msg.hex()

  current_GMT = time.gmtime()
  ts = calendar.timegm(current_GMT)

  body = {
      "password": password_hex,
      "password_type": "ticket",
      "ticket_id": ticket_id,
      "effective_time": ts,
      "invalid_time": ts + 10*360*24*7, # 5m #5คือวัน,24คือชั่วโมงม10*60เพื่อแปลงจากวิเป็นนาที
      "name":phone_number+"_9"
  }
  response = openapi.post(f"/v1.0/devices/{device_id}/door-lock/temp-password", body)
  return response

# df = latest_eresort()
# room_name = df['room_number'].iloc[2]
# ACCESS_ID = home_data[room_name]['ACCESS_ID']
# ACCESS_KEY = home_data[room_name]['ACCESS_KEY']
# API_ENDPOINT = home_data[room_name]['API_ENDPOINT']
# device_id = home_data[room_name]['device_id']
# openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
# openapi.connect()
# phone_number = df['phone_number'].iloc[2]
# res = gen_password(openapi, device_id, ACCESS_KEY, phone_number)
# print(res)
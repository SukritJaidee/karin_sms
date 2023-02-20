# coding=utf8
#@title 2.Send sms
import pytz
import pandas as pd
from twilio.rest import Client
from datetime import datetime, timedelta, date, tzinfo
from helper.eresort_f import *

def send_mess(phone_number):
  account_sid = 'AC4a2d278f6d854b30b77c6961569423e0'
  auth_token = 'a2b592faabf4300b1f12fbeac73ef19b'
  client = Client(account_sid, auth_token)
  message = client.messages.create(
                                messaging_service_sid='MGd217ed5113f22d5ac84ff11250571752',
                                body='ท่านได้ทำการ check-in เรียบร้อยแล้ว \n\nรหัส OTP สำหรับเปิดบ้านของท่าน คือ'+'\n\n'+str(phone_number[:-3])+ '#'+' \n\nรหัสนี้จะสามารถใช้ได้ตั้งแต่วันที่ Check-in จนถึงเวลา 12.00 น. ของวันที่ Check-out'+ '\n\n**รหัส OTP จะเปลี่ยนทุกครั้งเมื่อ Check-out** ',
                                to='+66'+phone_number[1:]
                            )
  # print(message.sid)
  return message.sid

def send_mess_out(phone_number, text):
      account_sid = 'AC4a2d278f6d854b30b77c6961569423e0'
      auth_token = 'a2b592faabf4300b1f12fbeac73ef19b'
      client = Client(account_sid, auth_token)
      message = client.messages.create(
          messaging_service_sid='MGd217ed5113f22d5ac84ff11250571752',
          # body='ขอบคุณสำหรับการเข้าพักบ้านครินทร์  \n\nท่านสามารถตรวจสอบการใช้พลังงานสะอาดจากการเข้าพักครั้งนี้ได้ ที่นี่ \n\nติดตามข่าวสารพลังงานได้ที่ \nhttps://energysolutions.egat.co.th \n\nขอบคุณค่ะ',
          body= 'ขอบคุณสำหรับการเข้าพักบ้านครินทร์  \n\nท่านสามารถตรวจสอบการใช้พลังงานสะอาดจากการเข้าพักครั้งนี้ได้ ที่นี่ '+text+'\n\nติดตามข่าวสารพลังงานได้ที่ \nhttps://energysolutions.egat.co.th \n\nขอบคุณค่ะ',
          to='+66'+phone_number[1:]
          )
      # print(message.sid)
      return message.sid

#@title 5.Update SMS
def update_sms(df):
    df1 = pd.DataFrame({"sent":["", "", "", "", ""]})
    for i in range(len(df1)):
        format_date = "%Y-%m-%d %H:%M:%S"
        dnow = pd.to_datetime(datetime.now(pytz.timezone('Asia/Bangkok')))
        dnow1 = dnow.strftime(format_date)
        dnow1 = pd.to_datetime(dnow1)
        # print(f"now datetime {dnow1}")
        try:
            dresort = df['datetime'].iloc[i]
            dresort = str(int(dresort[:4]) - 543) + dresort[4:]
            dresort = pd.to_datetime(dresort)
            # print(f"resort datetime {dresort}")
            delta =  dnow1 - dresort
            min = (delta.total_seconds())/60
            # print(f"min {min}")
            if (min > 0) and (df['room_status'].iloc[i]=="1"):
                df1['sent'][i] = "1"
            elif (min > 0) and (df['room_status'].iloc[i]==""):
                df1['sent'][i] = "0"
            else:
                df1['sent'][i] = ""
        except Exception as e:
          pass
          # print(e)
    return df1

# df = latest_eresort()
# df1 =  update_sms(df)
# print(df1)

# text = random.choice(ran_url)
# phone_number = "0811454333"
# send_mess(phone_number)
# # output = send_mess(phone_number)
# output = send_mess_out(phone_number, text)
# print(output)
#@title 1.E-resort function

# https://findev.egat.co.th (ระบบ DEV)
# https://findev.egat.co.th/eresort (ระบบ DEV)
# https://finapp.egat.co.th (ระบบ production)
import json
import requests
import pandas as pd

def e_resort():
  url = "https://finnet................" # DEV Internet
  # url = "https://finnet................" #Production Internet

  # url = "https://finapi................" #Production Intranet
  # url = "https://finapi................" #DEV Intranet

  payload, headers={}, {'X-API-Key': '..................................'} ## Dev keys
  # payload, headers = {}, {'X-API-Key': ''..................................'}'} ## Production keys
  response = requests.request("GET", url, headers=headers, data=payload)
  # print(response)
  data = json.loads(response.text)
  # print(data)
  return data

def latest_eresort():
  r_numbers, r_status_list, datetime_list, regis_date_list, ph_number_list = [],  [],  [],  [],  []
  ph_number_c_list, last_update_list = [], []
  data = e_resort()
  for i in range(len(data)):
      r_number = data[i]['room_number']
      r_status = data[i]['room_status']
      datetime = data[i]['datetime']
      register_date = data[i]['register_date']
      ph_number = data[i]['phone_number']
      ph_number_count = data[i]['phone_number_count']
      last_update = data[i]['last_update']

      # print(f"room_number:{r_number}, room_status:{r_status}, datetime:{datetime}, register_date:{register_date}, phone_number:{ph_number}, phone_number_count:{ph_number_count}, last_update:{last_update}")
      r_numbers.append(r_number); r_status_list.append(r_status); datetime_list.append(datetime); regis_date_list.append(register_date);
      ph_number_list.append(ph_number); ph_number_c_list.append(ph_number_count); last_update_list.append(last_update);

  df = pd.DataFrame({'room_number':r_numbers, 'room_status':r_status_list, 'datetime':datetime_list, 'register_date':regis_date_list, 'phone_number':ph_number_list, 'phone_number_count':ph_number_c_list, 'last_update':last_update_list})
  df.sort_values(by=['last_update'], inplace=True)
  # print(display(df))
  df = df.drop_duplicates(['room_number'], keep='last')
  df.sort_values(by=['room_number'], inplace=True)
  # print(display(df))
  df['room_number'].replace({"1":'karin236', "2":'karin237', "3":'karin238', "4":'karin239', "5":'karin240'}, inplace=True)
  return df

# df = latest_eresort()
# print(df)

# data = e_resort()
# print(data)

import random
from helper.eresort_f import *
from helper.sendsms_f import *
from helper.initial_f import *
from helper.delete_f import *
from helper.gendoorlock_f import *
from tuya_connector import TuyaOpenAPI, TUYA_LOGGER

df = latest_eresort()
# df2 = pd.DataFrame({"prev_ph_nc":["1", "1", "1", "1", "1"]})
df2 = pd.DataFrame({})
df2['prev_ph_nc'] = df['phone_number_count']
df2.reset_index(drop=True, inplace=True)
df1 = update_sms(df)
df1.reset_index(drop=True, inplace=True)
# print(df2)

while (True):
    df = latest_eresort()
    df.reset_index(drop=True, inplace=True)
    res = pd.concat([df, df1], axis=1)
    # print(res)
    for k in range(len(df)):
        room_name = df['room_number'].iloc[k]

        ## check-in และ sms ต้องถูกส่ง
        # print(f"## {room_name} ##")
        if (df['room_status'].iloc[k] == "1") and (df1['sent'].iloc[k] == ""):
            ACCESS_ID = home_data[room_name]['ACCESS_ID']
            ACCESS_KEY = home_data[room_name]['ACCESS_KEY']
            API_ENDPOINT = home_data[room_name]['API_ENDPOINT']
            device_id = home_data[room_name]['device_id']
            openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
            openapi.connect()
            try:
                phone_number = df['phone_number'].iloc[k]
                res = gen_password(openapi, device_id, ACCESS_KEY, phone_number)
                send_sme = send_mess(phone_number)
                df1['sent'][k] = "1"
                print(f"            room: {room_name} check-in SMS: {df1['sent'].iloc[k]}")
            except Exception as e:
                print(f"            room: {room_name}, error: {e}")

        ## check-out และ sms ต้องถูกส่ง
        elif (df['room_status'].iloc[k] == "0") and (df1['sent'].iloc[k] == "1"):
            ACCESS_ID = home_data[room_name]['ACCESS_ID']
            ACCESS_KEY = home_data[room_name]['ACCESS_KEY']
            API_ENDPOINT = home_data[room_name]['API_ENDPOINT']
            device_id = home_data[room_name]['device_id']
            openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
            openapi.connect()
            try:
                res =delete_pass(openapi, device_id)
                phone_number = df['phone_number'].iloc[k]
                print('            phone number:', phone_number)
                send_out = send_mess_out(phone_number, random.choice(ran_url))
                df1['sent'][k] = ""
                print(f"            room: {room_name} check-out SMS: {df1['sent'].iloc[k]}")
            except Exception as e:
                print(f"room: {room_name}, error: {e}")
        else:
            pass
        try:
            # print(df['phone_number_count'])
            # print(df2)
            if (int(df['phone_number_count'].iloc[k]) > int(df2['prev_ph_nc'].iloc[k]) and (df['room_status'].iloc[k] == "1")):
                # print('af', df['phone_number_count'])
                # print('af', df2)
                df2['prev_ph_nc'] = df['phone_number_count']
                print("Change phone number")
                ACCESS_ID = home_data[room_name]['ACCESS_ID']
                ACCESS_KEY = home_data[room_name]['ACCESS_KEY']
                API_ENDPOINT = home_data[room_name]['API_ENDPOINT']
                device_id = home_data[room_name]['device_id']
                openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
                openapi.connect()
                try:
                    phone_number = df['phone_number'].iloc[k]
                    res = gen_password(openapi, device_id, ACCESS_KEY, phone_number)
                    send_sme = send_mess(phone_number)
                    # df1['sent'][k] = "1"
                    print(f"            room: {room_name} check-in SMS: {df1['sent'].iloc[k]}")
                except Exception as e:
                    print(f"            room: {room_name}, error: {e}")
            else:
                pass
        except Exception as e:
            print(e)

    time.sleep(5)

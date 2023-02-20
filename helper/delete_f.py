#@title 3.Delete password

def delete_pass(openapi, device_id):
  # response = openapi.post(f"/v1.0/devices/{device_id}/door-lock/issue-password")
  response = openapi.get(f"/v1.0/devices/{device_id}/door-lock/temp-passwords?valid=true")
  print(f"response from openapi.get {response}")
  for i in range(len(response['result'])):
    password_id = response['result'][i]['id']
    # Delete a temporary password
    response = openapi.delete(f"/v1.0/devices/{device_id}/door-lock/temp-passwords/{password_id}")
    print(f"response from openapi.delete {response}")
    return True

# ACCESS_ID= "tgvqcqtfemjgku3v34wh"
# ACCESS_KEY="d619ea2d449d4792b9fc2d810b06d1ee"
# API_ENDPOINT =  "https://openapi.tuyaus.com"
# device_id = "eb67cededa28c02b3frk7l"
# openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
# openapi.connect()

# response1 = openapi.get(f"/v1.0/devices/{device_id}/door-lock/temp-passwords?valid=true")
# for i in range(len(response1['result'])):
#   password_id = response1['result'][i]['id']
#   response = openapi.delete(f"/v1.0/devices/{device_id}/door-lock/temp-passwords/{password_id}")
#   print(f"response from openapi.delete {response}")
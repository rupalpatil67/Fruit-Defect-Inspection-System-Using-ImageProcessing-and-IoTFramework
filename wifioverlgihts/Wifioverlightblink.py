import requests

ESP8266_IP = "192.168.29.236" # replace with the IP address of your ESP8266
URL = "http://" + ESP8266_IP + "/message" # the URL of the ESP8266 endpoint that receives the message

message = "fresh" # the message to send

params = {"message": message} # create a dictionary with the message parameter
response = requests.get(URL, params=params) # send a GET request to the ESP8266 with the message parameter

if response.status_code == 200: # if the response status code is 200 (OK)
    print("Message sent successfully")
else:
    print("Error sending message")

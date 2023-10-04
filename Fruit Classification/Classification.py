import os
import io
import requests
from PIL import Image
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
import re
import tensorflow as tf
import numpy as np
from PIL import Image
import cv2

def serial1(input1):
    ###
    import serial
    print((input1))
    ser = serial.Serial('COM3', 9600)  # Initialize the serial connection
    if input1 == "fresh":
        ser.write(b'fresh\r\n')  # Send the "AT" command to the module
        ser.readline().decode('utf-8')  # Read the response from the module
    # print(response)
    if input1 == "rotten":
        ser.write(b'rotten\r\n')  # Send the "AT" command to the module
        ser.readline().decode('utf-8')
    ser.close()  # Close the serial connection

    ####
    #
    # import requests
    # ESP8266_IP = "192.168.29.236"  # replace with the IP address of your ESP8266
    # URL = "http://" + ESP8266_IP + "/message"  # the URL of the ESP8266 endpoint that receives the message
    #   # the message to send
    #
    # params = {"message": input1}  # create a dictionary with the message parameter
    # response = requests.get(URL, params=params)  # send a GET request to the ESP8266 with the message parameter
    #
    # if response.status_code == 200:  # if the response status code is 200 (OK)
    #     print("Message sent successfully")
    # else:
    #     import serial
    #     print((input1))
    #     ser = serial.Serial('COM3', 9600)  # Initialize the serial connection
    #     if input1 == "fresh":
    #         ser.write(b'fresh\r\n')  # Send the "AT" command to the module
    #         ser.readline().decode('utf-8')  # Read the response from the module
    #     # print(response)
    #     if input1 == "rotten":
    #         ser.write(b'rotten\r\n')  # Send the "AT" command to the module
    #         ser.readline().decode('utf-8')
    #     ser.close()
    #


drive_link = 'https://drive.google.com/drive/u/0/folders/1GAVPkUuzz8IsNYcNHWGQ7DM8CbK4SkS8' # replace your drive link
clientfile="client_secret_1010923104017-m7d4q3kq3p97fopmc0liuflsqdfa45s4.apps.googleusercontent.com.json" #replace your JSon File

folder_id = re.findall('/folders/(.*)', drive_link)[0]
mime_type = 'image/jpeg' #or 'image/png'   or 'image/jpg'
size = (299, 299)
scopes = ['https://www.googleapis.com/auth/drive.readonly']
flow = InstalledAppFlow.from_client_secrets_file(clientfile, scopes=scopes)


creds_path = 'creds.json'
if os.path.exists(creds_path):
    creds = Credentials.from_authorized_user_file(creds_path, scopes)
else:
    creds = flow.run_local_server(port=0)
    with open(creds_path, 'w') as f:
        f.write(creds.to_json())

if datetime.now() + timedelta(minutes=5) > creds.expiry:
    creds.refresh(Request())

from googleapiclient.discovery import build
service = build('drive', 'v3', credentials=creds)

# folder all imges
results = service.files().list(q=f"'{folder_id}' in parents and mimeType='{mime_type}'", fields="nextPageToken, files(id, name)").execute()
items = results.get('files', [])

#folder last 1 min edited

# now = datetime.utcnow()
# one_minute_ago = (datetime.utcnow() - timedelta(minutes=35)).isoformat() + 'Z'
#
# # Fetch the list of files in the folder modified in the last 1 minute
# results = service.files().list(q=f"'{folder_id}' in parents and mimeType='{mime_type}' and modifiedTime > '{one_minute_ago}'", fields="nextPageToken, files(id, name, modifiedTime)").execute()
# items = results.get('files', [])



arr=[]
counter=0
if not items:
    print('No images found.')
else:
    for item in items:
        file_id = item['id']
        file_name = item['name']
        url = f"https://drive.google.com/uc?id={file_id}"
        img_bytes = io.BytesIO(requests.get(url).content)
        img = Image.open(img_bytes)
        img = img.resize(size)
        print(file_name)

        ############

        import requests
        import cv2
        import numpy as np

        # Fetch the image from the internet
        response = requests.get(url)
        img_array = np.array(bytearray(response.content), dtype=np.uint8)
        # Load the image into OpenCV
        imge = cv2.imdecode(img_array, -1)
        # Convert the image to grayscale


        height, width = imge.shape[:2]
        # Define the desired size of the output image
        new_size = (int(width / 2), int(height / 2))
        # Resize the image using cv2.resize()
        resized_img = cv2.resize(imge, new_size)


        gray_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        # Invert the grayscale image
        neg_img = 255 - gray_img
        # Convert the negative image back to color (optional)
        color_neg_img = cv2.cvtColor(neg_img, cv2.COLOR_GRAY2BGR)
        # Save the resulting image
        #cv2.imwrite('negative_image.jpg', color_neg_img)
        cv2.imshow('Negative Image', color_neg_img)
        cv2.waitKey(0)

        # b_and_w_image = cv2.cvtColor(resized_img, cv2.COLOR_BGR2GRAY)
        # inverted_image = 255 - b_and_w_image
        # blurred = cv2.GaussianBlur(inverted_image, (21, 21), 0)
        # inverted_blurred = 255 - blurred
        # pencil_sketch = cv2.divide(b_and_w_image, inverted_blurred, scale=256.0)
        # cv2.imshow("Sketch Image", pencil_sketch)
        # cv2.waitKey(0)
        # cv2.imshow("Inverrted Image", inverted_image)
        # cv2.waitKey(0)
        # cv2.imshow("blur Image", inverted_blurred)
        # cv2.waitKey(0)
        cv2.imshow("orignal img", resized_img)
        cv2.waitKey(0)

        cv2.destroyAllWindows()




        ##classification
        model = tf.keras.applications.InceptionV3(weights='imagenet')
        img_array = np.array(img) / 255.0
        img_array = img_array.reshape((1, 299, 299, 3))
        prediction = model.predict(img_array)

        if prediction[0][0] > prediction[0][1]:
            print("fresh")
            arr.append("fresh")
            #serial1("fresh")
        else:
            print("rotten")
            arr.append("rotten")
            #serial1("rotten")
        counter+=1
        if counter == 3:break
print(arr)
if (arr.count("fresh")) > (arr.count("rotten")):
    #print("lopp fresh")
    serial1("fresh")
elif (arr.count("rotten")) > (arr.count("fresh")):
    #print("loop rotten")
    serial1("rotten")








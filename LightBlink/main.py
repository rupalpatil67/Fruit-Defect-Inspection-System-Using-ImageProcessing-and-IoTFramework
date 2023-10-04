import serial

ser = serial.Serial('COM3', 9600) # Initialize the serial connection
print(("Enter fresh or rotten\n"))
input1=input()
if input1=="fresh":
    ser.write(b'fresh\r\n') # Send the "AT" command to the module
    ser.readline().decode('utf-8') # Read the response from the module
#print(response)
if input1=="rotten":
    ser.write(b'rotten\r\n')  # Send the "AT" command to the module
    ser.readline().decode('utf-8')
ser.close() # Close the serial connection

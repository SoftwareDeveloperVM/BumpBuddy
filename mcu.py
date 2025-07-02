# Import network modules to allow the RPI Pico to connect to Wifi
import network
import time


# Replace with Wifi credentials
SSID = '#WIFI'
PASSWORD = '#PWD'




# Function to connect to Wifi
def connect_wifi():
   wlan = network.WLAN(network.STA_IF)
   wlan.active(True)


   # If not connected to Wifi already,
   if not wlan.isconnected():
       print(f"Connecting to network")
       wlan.connect(SSID, PASSWORD)


       timeout = 10
       start_time = time.time()
       while not wlan.isconnected():
           if time.time() - start_time > timeout:
               print("Failed to connect.")
               return None
           time.sleep(1)


   # Connected to Wifi Message
   print('Connected to WiFi')
   print('IP Address:', wlan.ifconfig()[0])
   return wlan




# Call the function
connect_wifi()

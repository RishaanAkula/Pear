
import os
from pathlib import Path
import requests
import tkinter as tk
from PIL import Image, ImageTk
from io import BytesIO


def load_env_file():
  env_path = Path(__file__).with_name(".env")
  if not env_path.exists():
    return
  for line in env_path.read_text().splitlines():
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
      continue
    key, value = line.split("=", 1)
    os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env_file()
google_api_key = os.getenv("GOOGLE_API_KEY")
api_key = os.getenv("DISTANCE_API_KEY")


def main():
  global password
  destination = destination_entry.get()
  home = home_entry.get()
  url = f'https://api.distancematrix.ai/maps/api/distancematrix/json?origins={home}&destinations={destination}&key={api_key}'
  response = requests.get(url)
  distance = response.json()['rows'][0]['elements'][0]['distance']['text']
  duration = response.json()['rows'][0]['elements'][0]['duration']['text']
  password = "d872258c216b817fb79e5d07d9934231"
  weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={destination}&units=imperial&APPID={password}")
  temp = weather.json()['main']['temp']
  result_Label.config(text=f"The distance between {home} and {destination} is {distance} and it takes {duration} \n to get from {home} to {destination}; also, the temperature in {destination} is {temp} degrees")
  get_image()

  

def get_image():
  home = home_entry.get()
  destination = destination_entry.get()
  weather = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={destination}&units=imperial&APPID={password}")
  icon = weather.json()["weather"][0]["icon"]
  global img, image_Label
  icon_url = f"https://openweathermap.org/img/wn/{icon}@2x.png"
  response = requests.get(icon_url)
  image = Image.open(BytesIO(response.content))
  img = ImageTk.PhotoImage(image)
  image_Label.config(image=img)
  image_Label.pack(side = "bottom", fill = "both", expand = "yes")




pear = tk.Tk()
pear.title("Pear")
tk.Label(pear, text = "Enter your destination").pack()
destination_entry = tk.Entry(pear)
destination_entry.pack()
tk.Label(pear, text = "Enter your location").pack()
home_entry = tk.Entry(pear)
home_entry.pack()
tk.Button(pear, text="Get Location", command=main).pack()
image_Label = tk.Label(pear)
image_Label.pack_forget()
result_Label = tk.Label(pear, text="Result")
result_Label.pack()
pear.mainloop()




main()





from datetime import datetime
from dotenv import load_dotenv
import os
import re
import requests
from tkinter import *
from tkinter import messagebox


load_dotenv()
WORDLE_KEY = os.getenv("wordle_key")
WEATHER_KEY = os.getenv("weather_key")

#Constants
MINIMUM_LENGTH = 5
REQUIRED_SUM = 25

# Set up and run Tkinter GUI and start gameplay
def main():
  global window
  window = Tk()
  window.title("Super Secure Passwords")
  window.geometry("400x400")
  window.resizable(False, False)
  window.config(padx=20, pady=20)

  # Make columns expand evenly
  window.columnconfigure(0, weight=1)
  window.columnconfigure(1, weight=2)
  window.columnconfigure(2, weight=1)

  # Canvas with image
  canvas = Canvas(window, width=200, height=200, highlightthickness=0)
  img = PhotoImage(file="lock.png")
  canvas.create_image(100, 100, image=img)
  canvas.grid(row=0, column=0, columnspan=3, pady=(0, 20))

  # Label
  label = Label(window, text="Password:", font=('Helvetica', 14))
  label.grid(row=1, column=0, sticky="e", padx=(0, 10), pady=5)

  # Entry
  global password_entry
  password_entry = Entry(window, width=25, font=('Helvetica', 14))
  password_entry.focus()
  password_entry.grid(row=1, column=1, columnspan=2, sticky="w", pady=5)

  # Submit Button
  button = Button(window, text="Submit", font=('Helvetica', 12), padx=10, pady=5, command=check_input)
  button.grid(row=2, column=0, columnspan=3, pady=20)

  window.mainloop()

# Structure of the game logic
def check_input():
  value = password_entry.get()
  checks = [
    (check_len, "Password must contain at least 5 characters"),
    (check_mix_case, "Password must contain a mix of upper and lowercase characters."),
    (check_num, "Password must contain at least one number."),
    (check_special, "Password must include a special character."),
    (check_total, f"Password must add up to {REQUIRED_SUM}."),
    (weather_check, "Password must include the current weather in Auckland, New Zealand."),
    (check_wordle, "Password must contain the lastest Wordle solution."),
    (check_day, "Password must include the day today in Spanish."),
  ]

  # progressively check each requirement, if one fails then go back to the beginning
  for check, error_message in checks:
    if not check(value):
      messagebox.showerror(title="Invalid Password", message=error_message)
      return


  # If all checks pass, begin the "special ending"
  emoj = '(◕‿◕✿)'
  window.clipboard_append(emoj)

  character = pep(value)
  if character:
    window.clipboard_clear()
    global idx
    idx = value.index(emoj)
    messagebox.showerror(
      title="Action needed",
      message="Your password has reached the limit for a carbon-neutral password. "
              "Please shorten it or include a carbon offset."
    )
    password_entry.after(2000, ice)


# check password is sufficiently long
def check_len(s):
  return len(s) > MINIMUM_LENGTH

# check for a mix of upper/lower case
def check_mix_case(s):
  up = False
  low = False
  for i in range(len(s)):
    if s[i].isupper() == True:
      up = True
    if s[i].islower() == True:
      low = True
  return up and low

#check for numbers in password
def check_num(s):
  nums = [a for a in s if a.isdigit()]
  return len(nums) > 0

# check numbers sum to desired total
def check_total(s):
  nums = [int(a) for a in s if a.isdigit()]
  return sum(nums) == REQUIRED_SUM

# check for special character
def check_special(s):
  characters = [
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', ':',
    '?', '.', ','
  ]
  chars = [a for a in s if a in characters]
  return len(chars) > 0

# get current weather in Auckland and get possible accepted variants
def get_weather():
  params = {
    'access_key': WEATHER_KEY,
    'query': 'Auckland'
  }
  api_result = requests.get('http://api.weatherstack.com/current', params)
  response = api_result.json()
  weather = response['current']['weather_descriptions'][0]
  print(weather)
  sun = ["Sunny", "Fine", "Clear"]
  cloud = ["Cloud", "Overcast"]
  rain = ["Rain", "Shower", "Drizzle"]
  other = ["Snow", "Hail", "Storm"]
  types = [sun, cloud, rain, other]
  for i in range(4):
    category = types[i]
    for h in range(len(category)):
      if category[h].lower() in weather.lower():
        genre = types[i]
  return genre

#check for weather in password
def weather_check(s):
  weather = get_weather()
  found = False
  for k in range(len(weather)):
    if weather[k].lower() in s.lower():
      found = True
  return found

# check for today's wordle in password
def check_wordle(s):
  #wordle = get_wordle()

  # placeholder answer
  wordle = 'chirp'
  return wordle.lower() in s.lower()

#get latest wordle solution
def get_wordle():
  url = "https://wordle-api3.p.rapidapi.com/getwordtomorrow"
  headers = {
    "x-rapidapi-key": WORDLE_KEY,
    "x-rapidapi-host": "wordle-api3.p.rapidapi.com"
  }
  response = requests.get(url, headers=headers)
  data =response.json()
  todays = data['word']
  return todays

# get the day in spanish and check for it (accented or not) in password
def check_day(s):
  days = [
    'lunes', 'martes', 'miercoles', 'jueves', 'viernes', 'sabado', 'domingo'
  ]
  dt = datetime.now()
  day = dt.weekday()
  day = days[day]
  if day == 'miercoles' and re.search(".*mi[eé]rcoles.*", s.lower()):
    return True
  elif day == 'sabado' and re.search(".*s[aá]bado.*", s.lower()):
    return True
  elif day in s.lower():
    return True
  else:
    return False

# Prompt and check for character in password
def pep(s):
  if '(◕‿◕✿)' not in s:
    message = 'This is your password security manager, Pip. \n (◕‿◕✿) \nPlease paste  him into your password to keep him safe.'
    messagebox.showerror(title="Invalid Password", message=message)
    return False
  else:
    return True

# start timed sequence of replacing password characters with snowmen
def ice():
  password_entry.after(3000, delete)

# delete certain characters in string and replace them with snowman
def delete():
  password_entry.delete(0)
  password_entry.insert(0, "☃")
  password_entry.delete(10)
  password_entry.insert(10, "☃")
  password_entry.delete(END)
  password_entry.insert(END, "☃")
  password_entry.after(2000, snowman)


def snowman():
  password_entry.delete(idx, idx + 6)
  password_entry.insert(idx, "☃☃☃☃☃☃")
  messagebox.showwarning(
    title="Account Suspended!",
    message="Pip has frozen. Please close the application and try again later.")

if __name__ == "__main__":
  main()

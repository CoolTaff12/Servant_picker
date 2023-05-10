import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
# ----------------
import numpy as np
from random import *
# ----------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
# ----------------
# vlc name is python-vlc if you want to install it
import vlc
# In this case libvlc.dll will not be found. Make sure to install the 64bit-version
# ----------------

# Runs in Python 3.8.
# Package               version
# certifi               2022.12.7
# setuptools            60.2.0
# pip                   23.0.1
#                       21.3.1
# Pillow                9.4.0
# idna                  3.4
# charset-normalizer    3.1.0
# requests              2.28.2
# urllib3               1.26.15
# numpy                 1.21.6
# wheel                 0.37.1
# python-vlc (vlc)      30.0.18122

# Create form root
root = tk.Tk()
root.title("Servant Picker")
root.geometry("850x350")
colorCode = "#0276B4"
root.configure(background=colorCode)

# Create Canvas
canvas1 = tk.Canvas(root, width=850, height=350, name="myCanvas")

canvas1.pack(fill="both", expand=True)

# Add image file
bg = Image.open("7waUcXA3cy8EK6Ct.png").resize((850, 350), Image.LANCZOS)
bg = ImageTk.PhotoImage(bg)

# Display image
canvas1.create_image(0, 0, image=bg,
                     anchor="nw")

# Add Text
# canvas1.create_text(200, 250, text="Welcome")

# Exclude these servants: 150 152 153 169 241 334
exclude_these = [84, 150, 152, 153, 169, 241]
latest_Servant_number = 308 + 2
previous_servant = []

driver = webdriver.Chrome()
# driver.maximize_window()
driver.get("https://tiermaker.com/create/fgo-servant-tier-list-sorted-by-servant-id-1548189?ref=button")

def SPECIAL_SERVANT_TEAM(arguments):
    team = {
        1 : np.array([52, 38, 273, 2, 0, 0]),
        2 : np.array([59, 203, 104, 2, 0, 0])
    }
    return team.get(arguments, np.array([0, 0, 0, 0, 0]))


def SPECIAL_SUMMON_MUSIC(arguments):
    file = {
        1: "mPw6ecM33QzSi48Y.mp3",
        2: "burunyaa.wav"
    }
    x = vlc.MediaPlayer('SFX/'+str(file.get(arguments)))
    x.play()
    print("Runover" + str(arguments))


def SUMMON(servant_number, is_special):

    if is_special and servant_number == 0:
            confirmed_servant_data = Image.open("ryoma.png").resize((138, 150), Image.LANCZOS)
    else:
        wait = WebDriverWait(driver, 1)
        summoning_circle = wait.until(
            ec.visibility_of_element_located((By.XPATH,
                                              '//*[@id="create-image-carousel"]/div[' + str(servant_number) + ']')))
        # Get image from div
        summoning_servant = str(summoning_circle.get_attribute("style")).split('"')
        addressing_servant_url = "https://tiermaker.com" + summoning_servant[1]
        servants_response = requests.get(addressing_servant_url)
        confirmed_servant_data = servants_response.content

        # Adds the image and resizes it
        confirmed_servant_data = Image.open(BytesIO(confirmed_servant_data)).resize((138, 150), Image.LANCZOS)

    servant = ImageTk.PhotoImage(confirmed_servant_data)

    return (servant)


def SUMMONING_CIRCLE():
    global new_servants
    global special_summon
    throne_of_heroes = np.array([choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                               choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                               choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                               choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                               choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                               choice(list(set(range(2, latest_Servant_number)) - set(exclude_these)))])

    new_servants = []
    special_summon = bool(randint(1, 6) == 3)
    if special_summon:
        random_twice = randint(1, 2)
        throne_of_heroes = SPECIAL_SERVANT_TEAM(random_twice)
        SPECIAL_SUMMON_MUSIC(random_twice)

    for servant_order, servant_nr in enumerate(throne_of_heroes):
        new_servants.append(SUMMON(servant_nr, special_summon))
        canvas1.itemconfigure(previous_servant[servant_order], image=new_servants[servant_order])


# Randomize 6 servants numbers in throne_of_heroes
throne_of_heroes = np.array([choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these)))])

servant_team = []
for servant_order, servant_nr in enumerate(throne_of_heroes):
    servant_team.append(SUMMON(servant_nr, False))
    previous_servant.append(canvas1.create_image(15 + (138 * servant_order), 90, anchor="nw",
                                                 image=servant_team[servant_order]))


btn = tk.Button(root, anchor="s", text="Re-summon", command=lambda: SUMMONING_CIRCLE(), background="#0095E5",
                activebackground="#00A6FF", border=0)

btn_canvas = canvas1.create_window(425, 30, anchor="s", window=btn)


def ON_CLOSING():
    print("Goodbye")
    driver.close()
    root.destroy()


driver.minimize_window()

root.protocol("WM_DELETE_WINDOW", ON_CLOSING)
root.mainloop()

exit()
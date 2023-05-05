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
canvas1 = tk.Canvas(root, width=850, height=350)

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


def first_run():
    print("Start here!")


# Randomize 6 servants numbers in throneOfHeroes
throneOfHeroes = np.array([choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these))),
                           choice(list(set(range(2, latest_Servant_number)) - set(exclude_these)))])

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://tiermaker.com/create/fgo-servant-tier-list-sorted-by-servant-id-1548189?ref=button")


def reveal_servant(servant_array, first_time):
    # Create panel with added values and chang their size

    for servant in servant_array:
        if first_time:
            print(type(servant))
            panel = tk.Label(root, width=138, height=150, image=servant, background=colorCode, name=str(servant) + "0")
            panel.pack(side="left", fill="both", expand=0)

        else:
            # Get name from widget
            new_test_image = Image.open("CHAR!.png").resize((138, 150), Image.LANCZOS)
            new_test_image = ImageTk.PhotoImage(new_test_image)
            print(type(new_test_image))
            # use this code for real
            # root.nametowidget('.pyimage20').config(image=new_Test_image).pack()
            # use this for jokes
            evading_fire = '.pyimage' + str(randint(2, 7)) + '0'
            # first_image = root.children["pyimage10"]
            # print(first_image)
            random_chance = randint(1, 4)
            if random_chance == 3:
                mp3_url = "mPw6ecM33QzSi48Y.mp3"
                x = vlc.MediaPlayer(mp3_url)
                x.play()
                # Force select a team
                getter_beam = '.pyimage' + str(randint(2, 7)) + '0'
                getter_image = Image.open("ryoma.png").resize((138, 150), Image.LANCZOS)
                getter_image = ImageTk.PhotoImage(getter_image)
                root.nametowidget(getter_beam).config(image=getter_image)

            print(evading_fire)
            root.nametowidget(evading_fire).config(image=new_test_image)
            root.pack(side="left", fill="both", expand=0)
            # check out this website
            # https://stackoverflow.com/questions/38229857/how-to-avoid-attributeerror-tkinter-tkapp-object-has-no-attribute-passcheck

    # check_var1 = tk.IntVar()
    # c1 = tk.Checkbutton(root, text="1", variable=check_var1, onvalue=1, offvalue=0,
    #  height=5, width=20, background=colorCode)
    # c1.pack()


def summoning(first_time):

    slots = 1
    servant_array = []

    # Pick random servant
    for servant_Nr in throneOfHeroes:

        # Gets image from the web
        # wait for the Full Time Employees to be visible
        wait = WebDriverWait(driver, 1)
        summoning_circle = wait.until(
            ec.visibility_of_element_located((By.XPATH,
                                              '//*[@id="create-image-carousel"]/div[' + str(servant_Nr) + ']')))
        # Get image from div
        summoning_servant = str(summoning_circle.get_attribute("style")).split('"')
        addressing_servant_url = "https://tiermaker.com" + summoning_servant[1]
        servants_response = requests.get(addressing_servant_url)
        confirmed_servant_data = servants_response.content

        # Adds the image and resizes it
        confirmed_servant_data = Image.open(BytesIO(confirmed_servant_data)).resize((138, 150), Image.LANCZOS)
        servant = ImageTk.PhotoImage(confirmed_servant_data)

        if slots == 6:
            servant_array.append(servant)
            reveal_servant(servant_array, first_time)

            break
        else:
            servant_array.append(servant)
            print(servant_Nr)

        slots = slots + 1


# Reset function
def update_summon():
    summoning(False)


# Adding and displaying a reset button
btn = tk.Button(root, anchor="s", text="Re-summon", command=update_summon, background="#0095E5",
                activebackground="#00A6FF", border=0)

btn_canvas = canvas1.create_window(425, 30, anchor="s", window=btn)


def quote(wingu):
    print(wingu)


def on_closing():
    quote("Goodbye")
    driver.close()
    root.destroy()

# btn.pack()

summoning(True)

# Driver doesn't even need to me closed, just minimized
driver.minimize_window()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()

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
# numpy                 1.24.2
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
latest_Servant_number = 313 + 2
servant_team = []
previous_servant = []
previous_servants_check = []
check_boxes = []
new_servants = []
special_summon = False
reset_checks = False

driver = webdriver.Chrome()
driver.get("https://tiermaker.com/create/fgo-servant-tier-list-sorted-by-servant-id-1548189?ref=button")


def ON_CLOSING():
    print("Goodbye")
    driver.close()
    root.destroy()


def SET_ALL(value):
    [psc.set(value) for psc in previous_servants_check]


def DISABLE_OR_ENABLE_ALL(function_mode):
    if function_mode:
        [canvas1.itemconfigure(psc, state='normal') for psc in check_boxes]
    else:
        [canvas1.itemconfigure(psc, state='hidden') for psc in check_boxes]


def THRONE_OF_HEROES():

    # Randomize 6 servants numbers in throne_of_heroes
    return np.random.choice(list(set(range(2, latest_Servant_number)) - set(exclude_these)), 6)


def SPECIAL_SERVANT_TEAM(arguments):
    team = {
        # Getter Team
        1: np.array([52, 38, 273, 2, 0, 0]),
        # Feline
        2: np.array([59, 203, 104, 2, 0, 0]),
        # Suicide Run
        3: np.array([choice([252, 204]), 17, 259, 108, 295, 274]),
        # ONLY DIO
        4: np.array([36, 119, 34, 0, 0, 0])
    }
    return team.get(arguments, np.array([0, 0, 0, 0, 0]))


def SPECIAL_SUMMON_MUSIC(arguments):
    file = {
        1: ["mPw6ecM33QzSi48Y.mp3", 0.1],
        2: ["burunyaa.wav", 10.1],
        3: ["suicide_eng.wav", 10.1],
        4: ["Laughs_in_muda.mp3", 10.1]
    }
    play_the_fanfare = vlc.MediaPlayer('SFX/'+str(file.get(arguments)[0]))
    play_the_fanfare.play()
    print("Team " + str(arguments))


def SUMMON(servant_number, is_special):

    if is_special and servant_number == 0:
        confirmed_servant_data = Image.open("empty.png").resize((138, 150), Image.LANCZOS)
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

    return ImageTk.PhotoImage(confirmed_servant_data)


def SUMMONING_CIRCLE():
    global new_servants
    global special_summon
    global reset_checks
    re_summon = []
    new_servants = []
    no_replacement_request = bool(sum([psc.get() is True for psc in previous_servants_check]) not in range(1, 4))
    allowed = [i for i, x in enumerate(previous_servants_check) if x.get()]

    special_summon = bool(randint(1, 6) == 3)
    random_special = 0
    if special_summon and no_replacement_request:
        random_special = randint(1, 4)
        re_summon = SPECIAL_SERVANT_TEAM(random_special)
    else:
        re_summon = THRONE_OF_HEROES()

    for servant_order, servant_nr in enumerate(re_summon):
        new_servants.append(SUMMON(servant_nr, special_summon))
        if no_replacement_request and special_summon:
            canvas1.itemconfigure(previous_servant[servant_order], image=new_servants[servant_order])

        elif no_replacement_request and special_summon is False:
            canvas1.itemconfigure(previous_servant[servant_order], image=new_servants[servant_order])
            servant_team[servant_order] = new_servants[servant_order]

        elif no_replacement_request is False and servant_order in allowed:
            canvas1.itemconfigure(previous_servant[servant_order], image=new_servants[servant_order])
            servant_team[servant_order] = new_servants[servant_order]

        elif no_replacement_request is False and servant_order not in allowed:
            canvas1.itemconfigure(previous_servant[servant_order], image=servant_team[servant_order])

        else:
            print("Oh oh! We skipped the rest of conditions at " + str(servant_order))

    if reset_checks:
        DISABLE_OR_ENABLE_ALL(reset_checks)
        reset_checks = False

    if random_special > 0:
        SPECIAL_SUMMON_MUSIC(random_special)
        DISABLE_OR_ENABLE_ALL(reset_checks)
        reset_checks = True

    SET_ALL(False)


for servant_order, servant_nr in enumerate(THRONE_OF_HEROES()):
    servant_team.append(SUMMON(servant_nr, False))
    previous_servant.append(canvas1.create_image(15 + (138 * servant_order), 90, anchor="nw",
                                                 image=servant_team[servant_order]))
    psc = tk.BooleanVar()
    previous_servants_check.append(psc)
    check_boxes.append(canvas1.create_window(
        85 + (138 * servant_order), 250,
        window=tk.Checkbutton(canvas1, background="black", activebackground="black",
                              variable=psc)))


btn = tk.Button(root, anchor="s", text="Re-summon", command=lambda: SUMMONING_CIRCLE(), background="#0095E5",
                activebackground="#00A6FF", border=0)

btn_canvas = canvas1.create_window(425, 30, anchor="s", window=btn)


driver.minimize_window()

root.protocol("WM_DELETE_WINDOW", ON_CLOSING)
root.mainloop()

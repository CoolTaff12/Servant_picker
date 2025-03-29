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
# pygame is for the audio only
import pygame
# ----------------
import time
import asyncio
from os import walk

# ----------------


# Runs in Python 3.12.
# Package               version
# certifi               2022.12.7 -> 2024.2.2
# setuptools            60.2.0 -> 70.0.0
# pip                   23.0.1 -> 24.1b1
#                       21.3.1
# Pillow                9.4.0 -> 10.3.0
# idna                  3.4 -> 3.7
# charset-normalizer    3.1.0 -> 3.3.2
# requests              2.28.2 -> 2.32.3
# urllib3               1.26.15 -> 2.2.1
# numpy                 1.24.2 -> 2.0.0rc2
# wheel                 0.37.1 -> 0.43.0
# python-vlc (vlc)      30.0.18122 -> 3.0.20123
# selenium              4.11.2 -> 4.21.0
# asyncio               3.4.3
# pygame                2.5.2

# First, get all servant names that already is downloaded from the directory.
alreadyRegisteredServants = next(walk('Servant_Images/'), (None, None, []))[2]  # [] if no file
alreadyRegisteredServants = [fN.replace('.png', '') for fN in alreadyRegisteredServants]

closetFilledWithMystic: str = next(walk('Mystic_Codec/'), (None, None, []))[2]  # [] if no file

pygame.init()
pygame.mixer.init()

# print(alreadyRegisteredServants)

# Mystic codec randomizer and choose summer codec if summer servants are presence
# Have a harder mode where you can only have 5 to 3 servants on your team.

# Create form root
root = tk.Tk()
root.title("Servant Picker")
root.geometry("1290x350")
colorCode = "#0276B4"
root.configure(background=colorCode)

# Create Canvas             width=850, height=350, name="myCanvas"
canvas1 = tk.Canvas(root, width=1290, height=350, name="myCanvas")

canvas1.pack(fill="both", expand=True)

# Add image file                                (850, 350), Image.LANCZOS
bg = Image.open("7waUcXA3cy8EK6Ct.png").resize((1290, 350), Image.LANCZOS)
bg = ImageTk.PhotoImage(bg)

# Display image
canvas1.create_image(0, 0, image=bg,
                     anchor="nw")

# Properties of the first Mystic codec
clothes = Image.open("Mystic_Codec/" + closetFilledWithMystic[randint(0, 15)]).resize((70, 73), Image.LANCZOS)
clothes = ImageTk.PhotoImage(clothes)

# Draw Oval values, so we can edit it much easier.
circle_x_positions = [1050, 1130]
circle_y_positions = [154, 234]
circle_width = 8

canvas1.create_oval(circle_x_positions[0], circle_y_positions[0],
                    circle_x_positions[1], circle_y_positions[1], outline="dark grey", fill="light grey",
                    width=circle_width)

# Display Mystic codec for the first time
mysticCodec = canvas1.create_image(1055, 160, image=clothes, anchor="nw")

canvas1.create_oval(circle_x_positions[0], circle_y_positions[0],
                    circle_x_positions[1], circle_y_positions[1], outline="dark grey",
                    width=circle_width)

# Add Text
# canvas1.create_text(200, 250, text="Welcome")

# Exclude these servants: 150 152 153 169 241 334
exclude_these = [68, 70, 86, 135, 137, 155, 157, 158, 174, 221, 222, 248, 249, 250, 261, 262, 281, 282, 292, 294, 338,
                 339, 351, 254, 355, 357, 360, 362, 369, 371]
latest_Servant_number = 407  # Setanta (405)
servant_team = []
previous_servant = []
previous_servants_check = []
check_boxes = []
new_servants = []
special_summon = False
reset_checks = False
driver = ""
webCheck = bool(len(alreadyRegisteredServants) < latest_Servant_number - len(exclude_these) - 2)
print(len(alreadyRegisteredServants))
print(latest_Servant_number - len(exclude_these))
print(webCheck)

if webCheck:
    driver = webdriver.Chrome()
    # Old
    # https://tiermaker.com/create/fgo-tier-list-but-actually-with-all-the-servants-55890?ref=button
    driver.get("https://tiermaker.com/create/fgo-all-servants-20-always-updated-1024967?ref=button")


def ON_CLOSING():
    print("Goodbye")
    loop.close()
    if webCheck:
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
    number_list = []
    slots = 6
    hard_mode = bool(randint(1, 2) == 2)
    if hard_mode:
        slots = randint(3, 5)
        number_list = np.random.choice(list(set(range(2, latest_Servant_number)) - set(exclude_these)), slots)
        while len(number_list) < 6:
            number_list = np.append(number_list, [0])
    else:
        number_list = np.random.choice(list(set(range(2, latest_Servant_number)) - set(exclude_these)), slots)
    return number_list


def SPECIAL_SERVANT_TEAM(arguments):
    team = {
        # Umu
        1: np.array([7, 94, 181, 0, 0, 0]),
        # Feline
        2: np.array([60, 208, 107, 154, choice([2, 3]), 0]),
        # Suicide Run
        3: np.array([choice([263, 209]), 18, 270, 111, 310, 287]),
        # ONLY DIO
        4: np.array([37, 122, 35, choice([2, 3]), 0, 0]),
        # Only Elisabeth
        5: np.array([20, 63, 144, 344, 196, 197]),
        # Cooking team
        6: np.array([13, 28, 60, 348, 242, 0])
    }
    return team.get(arguments, np.array([0, 0, 0, 0, 0]))


def SPECIAL_SUMMON_MUSIC(arguments):
    file = {
        1: ["S005_SelectAttack1.mp3", 10],
        2: ["burunyaa.wav", 10],
        3: ["suicide_eng.wav", 10],
        4: ["Laughs_in_muda.mp3", 10],
        5: ["S018_NP2.mp3", 10],
        6: ["Hells_Kitchen_Dramatic_Sound.mp3", 10]
    }

    # play_the_fanfare = vlc.MediaPlayer('SFX/' + str(file.get(arguments)[0]))
    sound = pygame.mixer.Sound('SFX/' + str(file.get(arguments)[0]))
    sound.set_volume(0.9)  # Now plays at 90% of full volume.
    sound.play()
    # print(file.get(arguments)[1])
    # play_the_fanfare.audio_set_volume(10)
    # play_the_fanfare.play()
    print("Team " + str(arguments))


def SUMMON(servant_number, is_special):
    if is_special and servant_number == 0:
        confirmed_servant_data = Image.open("empty.png").resize((138, 150), Image.LANCZOS)
    elif is_special is False and servant_number == 0:
        confirmed_servant_data = Image.open("empty.png").resize((138, 150), Image.LANCZOS)
    else:
        if not webCheck:
            confirmed_servant_data = (Image.open("Servant_Images/" + str(servant_number) + ".png")
                                      .resize((138, 150), Image.LANCZOS))
        else:
            wait = WebDriverWait(driver, timeout=0.2)
            summoning_circle = wait.until(
                ec.presence_of_element_located((By.XPATH,
                                                '//*[@id="create-image-carousel"]/div[' + str(servant_number) + ']')))
            # Get image from div
            summoning_servant = str(summoning_circle.get_attribute("style")).split('"')
            addressing_servant_url = summoning_servant[1]
            # print(servant_number)
            # print(addressing_servant_url)
            servants_response = requests.get(addressing_servant_url)
            confirmed_servant_data = servants_response.content

            # Adds the image and resizes it
            confirmed_servant_data = Image.open(BytesIO(confirmed_servant_data)).resize((138, 150), Image.LANCZOS)
            # And downloads it!
            confirmed_servant_data.save('Servant_Images/' + str(servant_number) + '.png')
            alreadyRegisteredServants.append(servant_number)

    return ImageTk.PhotoImage(confirmed_servant_data)


async def CONTINUES_ASYNC(allowed, no_replacement_request, servant_order, servant_nr):
    new_servants.append(SUMMON(servant_nr, special_summon))
    try:
        match no_replacement_request:
            case True:
                canvas1.itemconfigure(previous_servant[servant_order], image=new_servants[servant_order])
                if special_summon is False:
                    servant_team[servant_order] = new_servants[servant_order]
            case False:
                if servant_order in allowed:
                    canvas1.itemconfigure(previous_servant[servant_order], image=new_servants[servant_order])
                    servant_team[servant_order] = new_servants[servant_order]
                elif servant_order not in allowed:
                    canvas1.itemconfigure(previous_servant[servant_order], image=servant_team[servant_order])
                else:
                    print("Oh oh! We skipped the rest of conditions at " + str(servant_order))
    except:
        print("Oh no! Error at servant_order: " + str(servant_order) + " & servant_nr: " + str(servant_nr))


def SUMMONING_CIRCLE():
    global new_servants, special_summon, reset_checks, newClothes
    new_servants = []
    newClothes = ""
    start = time.time()
    summon_tasks = []
    no_replacement_request = bool(sum([psc.get() is True for psc in previous_servants_check]) not in range(1, 4))
    allowed = [i for i, x in enumerate(previous_servants_check) if x.get()]

    # Chance of special summon
    special_summon = bool(randint(1, 6) == 3)
    # Force special summon  (for testing)
    # special_summon = True
    random_special = 0
    if special_summon and no_replacement_request:
        # Always random
        random_special = randint(1, 6)
        # Not random (for testing)
        # random_special = 2
        re_summon = SPECIAL_SERVANT_TEAM(random_special)
    else:
        re_summon = THRONE_OF_HEROES()
        newClothes = Image.open("Mystic_Codec/" + closetFilledWithMystic[randint(0, 15)]).resize((70, 73),
                                                                                                 Image.LANCZOS)
        newClothes = ImageTk.PhotoImage(newClothes)
        canvas1.itemconfigure(mysticCodec, image=newClothes)

    for servant_order, servant_nr in enumerate(re_summon):
        # Creating tasks here!
        summon_tasks.append(loop.create_task(CONTINUES_ASYNC(
            allowed, no_replacement_request, servant_order, servant_nr)))

    loop.run_until_complete(asyncio.wait(summon_tasks))

    if reset_checks:
        DISABLE_OR_ENABLE_ALL(reset_checks)
        reset_checks = False

    if random_special > 0:
        SPECIAL_SUMMON_MUSIC(random_special)
        DISABLE_OR_ENABLE_ALL(reset_checks)
        reset_checks = True

    SET_ALL(False)
    print('click')
    end = time.time()
    print(f'Time: {end - start:.2f} sec')


async def START_ASYNC(servant_order, servant_nr):
    servant_team.append(SUMMON(servant_nr, False))
    # 15 + (138 * servant_order), 90,
    previous_servant.append(canvas1.create_image(215 + (138 * servant_order), 90, anchor="nw",
                                                 image=servant_team[servant_order]))
    psc = tk.BooleanVar()
    previous_servants_check.append(psc)
    check_boxes.append(canvas1.create_window(
        # 85 + (138 * servant_order), 250,
        285 + (138 * servant_order), 250,
        window=tk.Checkbutton(canvas1, background="black", activebackground="black",
                              variable=psc)))


start = time.time()
print('start')
loop = asyncio.new_event_loop()
tasks = []

for servant_order, servant_nr in enumerate(THRONE_OF_HEROES()):
    tasks.append(loop.create_task(START_ASYNC(servant_order, servant_nr)))

loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print(f'Time: {end - start:.2f} sec')

btn = tk.Button(root, anchor="s", text="Re-summon", command=lambda: SUMMONING_CIRCLE(), background="#0095E5",
                activebackground="#00A6FF", border=0)
# 425, 30, anchor="s", window=btn
btn_canvas = canvas1.create_window(625, 30, anchor="s", window=btn)

if webCheck:
    driver.minimize_window()

root.protocol("WM_DELETE_WINDOW", ON_CLOSING)
root.mainloop()

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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
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
exclude_these = [150, 152, 153, 169, 241]

# Randomize 6 servants numbers in throneOfHeroes
throneOfHeroes = np.array([choice(list(set(range(2, 308)) - set(exclude_these))),
                           choice(list(set(range(2, 308)) - set(exclude_these))),
                           choice(list(set(range(2, 308)) - set(exclude_these))),
                           choice(list(set(range(2, 308)) - set(exclude_these))),
                           choice(list(set(range(2, 308)) - set(exclude_these))),
                           choice(list(set(range(2, 308)) - set(exclude_these)))])

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://tiermaker.com/create/fgo-servant-tier-list-sorted-by-servant-id-1548189?ref=button")


def run_data():

    slots = 1
    global my_img

    # Pick random servant
    for servant in throneOfHeroes:

        # Gets image from the web
        # wait for the Full Time Employees to be visible
        wait = WebDriverWait(driver, 2)
        employees = wait.until(
            EC.visibility_of_element_located((By.XPATH,
                                              '//*[@id="create-image-carousel"]/div[' + str(servant) + ']')))
        # Get image from div
        summoning_servant = str(employees.get_attribute("style")).split('"')
        img_url = "https://tiermaker.com" + summoning_servant[1]
        response = requests.get(img_url)
        img_data = response.content

        # Adds the image and resizes it
        img_data = Image.open(BytesIO(img_data)).resize((138, 150), Image.LANCZOS)
        img = ImageTk.PhotoImage(img_data)

        if slots == 6:
            my_img.append(img)

            # Create panel with added values and chang their size
            for i in my_img:
                panel = tk.Label(root, width=138, height=150, image=i, background=colorCode, name=str(i) + "0")
                panel.pack(side="left", fill="both", expand=0)

            print(my_img[0])
            # check_var1 = tk.IntVar()
            # c1 = tk.Checkbutton(root, text="1", variable=check_var1, onvalue=1, offvalue=0,
                              #  height=5, width=20, background=colorCode)
            # c1.pack()
            break
        elif slots == 1:
            my_img = [img]
        else:
            my_img.append(img)
            print(servant)

        slots = slots + 1


# Reset function
def reset_data():
    print(root.winfo_children())
    # Get name from widget
    print(root.children)
    first_image = root.children["pyimage10"]
    print(first_image)
    print("it doesn't matter who is wrong or who is right")


# Adding and displaying a reset button
btn = tk.Button(root, anchor="s", text="Re-summon", command=reset_data, background="#0095E5",
                activebackground="#00A6FF", border=0)

btn_canvas = canvas1.create_window(425, 30, anchor="s", window=btn)


#btn.pack()

run_data()

driver.close()
root.mainloop()



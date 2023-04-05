import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
import numpy as np

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
root.geometry("750x350")
colorCode = "#0276B4"
root.configure(background=colorCode)

# Fill array with numbers which represents servants
arr = np.arange(307)

# Don't include these numbers  - 59, 83, 149, 151, 152, 168, 240, 333, 9944140
b = np.array([0, 59, 83, 149, 151, 152, 168, 240, 333, 9944140])
arr = np.setdiff1d(arr, b)


def run_data():
    np.random.shuffle(arr)

    slots = 1
    global my_img

    # Pick random servant
    for x in arr:

        # Gets image from the web
        ran = str(x).zfill(3)
        img_url = "https://fgo-tracker.netlify.app/img/servant/" + ran + "-2x.png"
        response = requests.get(img_url)
        img_data = response.content

        # Adds the image and resizes it
        img_data = Image.open(BytesIO(img_data)).resize((120, 120), Image.LANCZOS)
        img = ImageTk.PhotoImage(img_data)

        if slots == 6:
            my_img.append(img)

            # Create panel with added values and chang their size
            for i in my_img:
                panel = tk.Label(root, width=120, height=120, image=i, background=colorCode, name=str(i) + "0")
                panel.pack(side="left", fill="both", expand=0)

            print(my_img[0])
            break
        elif slots == 1:
            my_img = [img]
        else:
            my_img.append(img)
            print(ran)

        slots = slots + 1


# Reset function
def reset_data():
    print(root.winfo_children())
    # Get name from widget
    print(root.children)
    first_image = root.children["pyimage10"]
    print(first_image)
    print("it doesn't matter who is wrong or who is right")


# Adding a reset button
btn = tk.Button(root, anchor="s", text="Re-summon", command=reset_data, background="#0095E5",
                activebackground="#00A6FF", border=0)
btn.pack()

run_data()

root.mainloop()

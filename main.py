import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
import numpy as np

# Runs in Python 3.7.
# Package   version
# numpy     1.21.6
# pip       23.0.1
# requests  2.28.2

# Create form root
root = tk.Tk()
root.title("Servant Picker")
root.geometry("800x400")

# Fill array with numbers which represents servants
arr = np.arange(307)

# Don't include these numbers  - 59, 83, 149, 151, 152, 168, 240, 333, 9944140
b = np.array([0, 59, 83, 149, 151, 152, 168, 240, 333, 9944140])
arr = np.setdiff1d(arr, b)

# Shuffle server order
np.random.shuffle(arr)

slots = 1

# Reset function
def reset_data():
    print("Gerry")

# Reset button
btn = tk.Button(root, text= "Re-summon", command= reset_data)
btn.pack()

# Pick random servant
for x in arr:

    ran = str(x).zfill(3)
    img_url = "https://fgo-tracker.netlify.app/img/servant/" + ran + "-2x.png"
    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    if slots == 6:
        my_img.append(img)
        # Create panel with added values
        panel1 = tk.Label(root, width=64, height=64, image=my_img[0])
        panel2 = tk.Label(root, width=64, height=64, image=my_img[1])
        panel3 = tk.Label(root, width=64, height=64, image=my_img[2])
        panel4 = tk.Label(root, width=64, height=64, image=my_img[3])
        panel5 = tk.Label(root, width=64, height=64, image=my_img[4])
        panel6 = tk.Label(root, width=64, height=64, image=my_img[5])
        panel1.pack(side="left", fill="both", expand=1)
        panel2.pack(side="left", fill="both", expand=1)
        panel3.pack(side="left", fill="both", expand=1)
        panel4.pack(side="left", fill="both", expand=1)
        panel5.pack(side="left", fill="both", expand=1)
        panel6.pack(side="left", fill="both", expand=1)
        root.mainloop()
        # Open form
        username = input("Enter username:")
        print("Rest")
        slots = 0
    elif slots == 1:
        my_img = [img]
    else:
        my_img.append(img)
        print(ran)

    slots = slots + 1


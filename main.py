import tkinter as tk
from PIL import ImageTk, Image
import os
import requests
from io import BytesIO
import numpy as np

#Create form root
root = tk.Tk()
root.title("Servant Picker")
root.geometry("800x400")

#Pick random servant

arr = np.arange(307)
np.random.shuffle(arr)
arr = arr[arr > 0]
# Don't include these servants - 59, 83, 149, 151, 152, 168, 240, 333, 9944140

pack = 1

#Reset function
def resetData():
    print("Gerry")

#Reset botton
btn = tk.Button(root, text ="Resummon", command = resetData)
btn.pack()

for x in arr:

    ran = str(x).zfill(3)
    img_url = "https://fgo-tracker.netlify.app/img/servant/" + ran + "-2x.png"
    response = requests.get(img_url)
    img_data = response.content
    img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

    if pack == 6:
        my_img.append(img)
        # Create pannel with added values
        panel1 = tk.Label(root, width=64, height=64, image=my_img[0])
        panel2 = tk.Label(root, width=64, height=64, image=my_img[1])
        panel3 = tk.Label(root, width=64, height=64, image=my_img[2])
        panel4 = tk.Label(root, width=64, height=64, image=my_img[3])
        panel5 = tk.Label(root, width=64, height=64, image=my_img[4])
        panel6 = tk.Label(root, width=64, height=64, image=my_img[5])
        panel1.pack(side="left", fill="both", expand="yes")
        panel2.pack(side="left", fill="both", expand="yes")
        panel3.pack(side="left", fill="both", expand="yes")
        panel4.pack(side="left", fill="both", expand="yes")
        panel5.pack(side="left", fill="both", expand="yes")
        panel6.pack(side="left", fill="both", expand="yes")
        root.mainloop()
        # Open form
        username = input("Enter username:")
        print("Rest")
        pack = 0
    elif pack == 1:
        my_img = [img]
    else:
        my_img.append(img)
        print(pack)

    pack = pack + 1



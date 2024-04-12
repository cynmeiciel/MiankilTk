import tkinter as tk
import tkinter.font as tkFont

root = tk.Tk()
fonts = tkFont.families(root)
for font in fonts:
    print(font)
root.destroy()
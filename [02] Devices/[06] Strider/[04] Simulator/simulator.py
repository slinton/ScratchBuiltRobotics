#
# To naviate to this directory in PowerShell, you can use the following command:
# $path = "C:\Users\samue\OneDrive\Documents\[01] Projects\[01] 
# ScratchBuiltRobotics\[02] Devices\[06] Strider\[04] Simulator" ; 
# Set-Location -LiteralPath $path ; 
#
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

app = ttk.Window(themename="darkly")
ttk.Label(app, text="Hello, ttkbootstrap!", font=("Helvetica", 16)).pack(pady=20)
ttk.Button(app, text="Click Me", bootstyle=SUCCESS).pack()



# Create and pack the Canvas
canvas = ttk.Canvas(app, width=400, height=200, bg='white')
canvas.pack(pady=20)

# Draw some shapes
canvas.create_rectangle(50, 50, 150, 120, fill='skyblue', outline='black')
canvas.create_oval(200, 60, 280, 140, fill='tomato', outline='black')
canvas.create_text(200, 20, text="Canvas Drawing!", font=('Helvetica', 14))

app.mainloop()

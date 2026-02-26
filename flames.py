import tkinter as tk
from tkinter import messagebox

#Window setup
root = tk.Tk()
root.title("FLAMES")
root.geometry("600x500")
root.resizable(False, False)
root.configure(bg="#120021")
root.attributes("-alpha", 0.97)

#color palette
BG = "#120021"
CARD = "#1F0033"
NEON_PINK = "#FF4EDB"
HOT_PINK = "#FF7AF5"
NEON_PURPLE = "#9B8CFF"
TEXT = "#FFFFFF"
MUTED = "#C9C3E6"

#fonts
TITLE_FONT = ("Segoe UI Semibold", 22)
LABEL_FONT = ("Segoe UI Semibold", 11)
ENTRY_FONT = ("Segoe UI", 13)
BTN_FONT = ("Segoe UI Semibold", 12)
RESULT_FONT = ("Segoe UI Semibold", 20)

#canvas for custom shapes
canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
canvas.pack(fill="both", expand=True)

def rounded_rect(x1, y1, x2, y2, r, color):
    canvas.create_polygon(
        x1+r, y1, x2-r, y1, x2, y1,
        x2, y1+r, x2, y2-r, x2, y2,
        x2-r, y2, x1+r, y2, x1, y2,
        x1, y2-r, x1, y1+r, x1, y1,
        smooth=True, fill=color, outline=""
    )

# Glass card
rounded_rect(60, 60, 540, 440, 35, CARD)

def rounded_input(x, y, width, height, placeholder):
    r = 12

    # background shape
    shape = canvas.create_polygon(
        x+r, y, x+width-r, y, x+width, y,
        x+width, y+r, x+width, y+height-r, x+width, y+height,
        x+width-r, y+height, x+r, y+height, x, y+height,
        x, y+height-r, x, y+r, x, y,
        smooth=True, fill="#2A0047", outline="#3A0066", width=1
    )

    entry = tk.Entry(
        root,
        font=ENTRY_FONT,
        bg="#2A0047",
        fg=MUTED,
        relief="flat",
        insertbackground=TEXT
    )
    entry.insert(0, placeholder)
    entry.place(x=x+12, y=y+8, width=width-24, height=height-16)

    def on_focus_in(e):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg=TEXT)
        canvas.itemconfig(shape, outline=NEON_PINK, width=2)

    def on_focus_out(e):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg=MUTED)
        canvas.itemconfig(shape, outline="#3A0066", width=1)

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

    return entry

#title and subtitle
canvas.create_text(
    300, 95,
    text="FLAMES RELATIONSHIP GAME",
    fill=NEON_PINK,
    font=TITLE_FONT
)

canvas.create_text(
    300, 125,
    text="Enter two names and discover the connection",
    fill=MUTED,
    font=("Segoe UI", 10)
)

#input labels and fields
canvas.create_text(
    150, 155,
    text="Your Name",
    fill=TEXT,
    font=LABEL_FONT,
    anchor="w"
)

entry1 = rounded_input(
    x=150,
    y=175,
    width=300,
    height=45,
    placeholder="Type your name here"
)

canvas.create_text(
    150, 235,
    text="Partner's Name",
    fill=TEXT,
    font=LABEL_FONT,
    anchor="w"
)

entry2 = rounded_input(
    x=150,
    y=255,
    width=300,
    height=45,
    placeholder="Type partner's name here"
)

#main logic
result_var = tk.StringVar()

def calculate_flames():
    n1 = entry1.get().lower().replace(" ", "")
    n2 = entry2.get().lower().replace(" ", "")

    if not n1 or not n2 or "type" in n1 or "type" in n2:
        messagebox.showerror("Input Required", "Please enter both names.")
        return

    l1, l2 = list(n1), list(n2)
    for ch in n1:
        if ch in l2:
            l1.remove(ch)
            l2.remove(ch)

    count = len(l1) + len(l2)
    flames = ["Friends", "Lovers", "Affectionate", "Marriage", "Enemies", "Sibling"]
    result = "Same Name" if count == 0 else flames[(count - 1) % 6]
    animate_result(result)

#result label
result_label = tk.Label(
    root,
    textvariable=result_var,
    font=RESULT_FONT,
    bg=CARD,
    fg=NEON_PURPLE
)
result_label.place(relx=0.5, y=420, anchor="center")

def animate_result(text, i=0):
    if i <= len(text):
        result_var.set(text[:i])
        root.after(50, lambda: animate_result(text, i+1))

#button with hover effect
btn_canvas = tk.Canvas(root, width=320, height=60, bg=BG, highlightthickness=0)
btn_canvas.place(relx=0.5, y=360, anchor="center")

btn_shape = btn_canvas.create_polygon(
    20, 0, 300, 0, 320, 0,
    320, 20, 320, 40, 320, 60,
    300, 60, 20, 60, 0, 60,
    0, 40, 0, 20, 0, 0,
    smooth=True, fill=NEON_PINK
)

btn_text = btn_canvas.create_text(
    160, 30,
    text="CALCULATE RELATIONSHIP",
    fill="white",
    font=BTN_FONT
)

def btn_hover_in(e):
    btn_canvas.itemconfig(btn_shape, fill=HOT_PINK)

def btn_hover_out(e):
    btn_canvas.itemconfig(btn_shape, fill=NEON_PINK)

def btn_click(e):
    calculate_flames()

btn_canvas.bind("<Enter>", btn_hover_in)
btn_canvas.bind("<Leave>", btn_hover_out)
btn_canvas.bind("<Button-1>", btn_click)

root.mainloop()
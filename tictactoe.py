import tkinter as tk
from PIL import Image, ImageTk , ImageFont, ImageDraw
import math
import traceback


def show_custom_message(title, message, img=None):
    win = tk.Toplevel(root)
    win.title(title)
    win.configure(bg="#FFEBF0", cursor="@cursorpng.cur")
    win.resizable(False, False)

    # window size
    width, height = 350, 150
    win.geometry(f"{width}x{height}")
    root.update_idletasks()
    x = root.winfo_x() + (root.winfo_width() - width) // 2
    y = root.winfo_y() + (root.winfo_height() - height) // 2
    win.geometry(f"+{x}+{y}")
    
    #message 
    img_text = Image.new("RGBA", (300, 50), (0,0,0,0))
    font = ImageFont.truetype("PressStart2P.ttf", 20)
    draw = ImageDraw.Draw(img_text)
    draw.text((0,0), message, font=font, fill=(243,168,173,255))
    tk_img_text = ImageTk.PhotoImage(img_text)

    label_img = tk.Label(win, image=tk_img_text, bg="#FFEBF0",cursor="@cursorpng.cur")
    label_img.image = tk_img_text
    label_img.pack(pady=10)

    def close():
        win.destroy()
        root.quit()

    btn_ok = tk.Button(win, text="OK", font=("Terminal", 18),
                       bg="#F57A95", fg="white", width=12, command=close,cursor="@cursorpng.cur")
    btn_ok.pack(pady=10)

    win.grab_set()

try:
    root = tk.Tk()
    root.title("Tic Tac Toe - Minimax AI")
    root.geometry("500x550")
    root.resizable(False, False)


    root.configure(cursor="@cursorpng.cur")
    

    #background
    bg_image = Image.open("sky1.png").resize((500, 550))
    bg_photo = ImageTk.PhotoImage(bg_image)

    canvas_bg = tk.Canvas(root, width=500, height=550)
    canvas_bg.pack(fill="both", expand=True)
    canvas_bg.create_image(0, 0, image=bg_photo, anchor="nw")

    canvas_bg.configure(cursor="@cursorpng.cur")

    #cake and donat
    donut_img = Image.open("donat.png").resize((90, 90), Image.NEAREST)
    donut_photo = ImageTk.PhotoImage(donut_img)

    #cake for AI
    cake_img = Image.open("cake.png").resize((90, 90), Image.NEAREST)
    cake_photo = ImageTk.PhotoImage(cake_img)
    IMAGES = {"bg": bg_photo, "donut": donut_photo, "cake": cake_photo}

    #tic tac toe text 
    font_path = "PressStart2P.ttf" 
    custom_font = ImageFont.truetype(font_path, 26)
    text_img = Image.new("RGBA", (500, 50), (0, 0, 0, 0))
    draw = ImageDraw.Draw(text_img)
    draw.text((0, 0), "Tic Tac Toe", font=custom_font, fill=(255, 133, 160, 255))  
    tk_text_image = ImageTk.PhotoImage(text_img)
    canvas_bg.create_image(110, 20, image=tk_text_image, anchor="nw")

    #ai with cake
    custom_font_ai = ImageFont.truetype(font_path, 18)
    cake_small_img = Image.open("cake.png").resize((60, 60), Image.NEAREST)
    cake_small_photo = ImageTk.PhotoImage(cake_small_img)
    canvas_bg.create_image(150, 100, image=cake_small_photo, anchor="center")
    text_ai = Image.new("RGBA", (100, 30), (0, 0, 0, 0)) 
    draw_ai = ImageDraw.Draw(text_ai)
    draw_ai.text((0, 0), "AI", font=custom_font_ai, fill=(243, 168, 173, 255))
    tk_text_ai = ImageTk.PhotoImage(text_ai)
    canvas_bg.create_image(230, 90, image=tk_text_ai, anchor="n")
    IMAGES["ai_text"] = tk_text_ai


    #you with donat
    custom_font_you = ImageFont.truetype(font_path, 18)  
    donut_small_img = Image.open("donat.png").resize((60, 60), Image.NEAREST)  
    donut_small_photo = ImageTk.PhotoImage(donut_small_img)
    canvas_bg.create_image(25, 100, image=donut_small_photo, anchor="center")
    text_you = Image.new("RGBA", (100, 30), (0, 0, 0, 0))
    draw_you = ImageDraw.Draw(text_you)
    draw_you.text((0, 0), "YOU", font=custom_font_you, fill=(243, 168, 173, 255))
    tk_text_you = ImageTk.PhotoImage(text_you)
    canvas_bg.create_image(100, 90, image=tk_text_you, anchor="n")

    #table size
    BUTTON_SIZE = 100  
    buttons = []       
    board = [""] * 9

    WIN_COMBOS = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]

    def check_winner():
        for a, b, c in WIN_COMBOS:
            if board[a] == board[b] == board[c] != "":
                return board[a]
        return None

    def is_draw():
        return all(cell != "" for cell in board)

    def minimax(is_maximizing):
        winner = check_winner()
        if winner == "⭕":
            return 1
        elif winner == "❌":
            return -1
        elif is_draw():
            return 0

        if is_maximizing:
            best_score = -math.inf
            for i in range(9):
                if board[i] == "":
                    board[i] = "⭕"
                    score = minimax(False)
                    board[i] = ""
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = math.inf
            for i in range(9):
                if board[i] == "":
                    board[i] = "❌"
                    score = minimax(True)
                    board[i] = ""
                    best_score = min(score, best_score)
            return best_score

    def ai_move():
        best_score = -math.inf
        best_move = None
        for i in range(9):
            if board[i] == "":
                board[i] = "⭕"
                score = minimax(False)
                board[i] = ""
                if score > best_score:
                    best_score = score
                    best_move = i
        if best_move is not None:
            make_move(best_move, "⭕")

    def make_move(i, player):
        board[i] = player
        c = buttons[i]
        if player == "❌":
            c.delete("all")
            c.create_image(BUTTON_SIZE//2, BUTTON_SIZE//2, image=IMAGES["donut"])
        else:
            c.delete("all")
            c.create_image(BUTTON_SIZE//2, BUTTON_SIZE//2, image=IMAGES["cake"])

        # win/draw
        winner = check_winner()
        if winner:
            if winner == "⭕": #AI cake
               msg = "AI won!"
            else: #you donat
                msg = "You won! Congratulations"

            show_custom_message("Game Over" , msg)
        elif is_draw():
           show_custom_message("Game Over", "It's a draw!")

        #lock the clicked button on table after movement
        c.unbind("<Button-1>")

    def player_move(i):
        if board[i] == "":
            make_move(i, "❌")
            if not check_winner() and not is_draw():
                ai_move()

    #table
    board_frame = tk.Frame(root, bg="", width=BUTTON_SIZE*3 + 40, height=BUTTON_SIZE*3 + 40)
    board_frame.place(relx=0.5, rely=0.55, anchor="center")

    board_frame.configure(cursor="@cursorpng.cur")

    for i in range(9):
        c = tk.Canvas(board_frame, width=BUTTON_SIZE, height=BUTTON_SIZE,  cursor="@cursorpng.cur",
                      bg="#FFFDF9", highlightthickness=2, highlightbackground="#e0e0e0")
        c.grid(row=i // 3, column=i % 3, padx=1, pady=1)
        c.bind("<Button-1>", lambda e, i=i: player_move(i))
        buttons.append(c)

    root.mainloop()
except Exception:
    print("An error occurred:\n")
    traceback.print_exc()
    raise







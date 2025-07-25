import tkinter as tk
from tkinter import messagebox
import random
import math

# Main window setup
root = tk.Tk()
root.title("🐍 Snake and Ladder Game")
root.geometry("600x720")
root.configure(bg="#f0f8ff")

canvas = tk.Canvas(root, width=500, height=500, bg="white")
canvas.pack(pady=20)

cell_size = 50
player1_pos = 1
player2_pos = 1
current_player = 1
moving = False

# Define snakes and ladders
snakes = {16: 6, 48: 30, 62: 19, 88: 24, 95: 56, 97: 78}
ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
dice_faces = ["⚀", "⚁", "⚂", "⚃", "⚄", "⚅"]

# Get coordinates from position
def get_coords(position):
    row = 9 - (position - 1) // 10
    col = (position - 1) % 10 if ((position - 1) // 10) % 2 == 0 else 9 - ((position - 1) % 10)
    x = col * cell_size + 25
    y = row * cell_size + 25
    return x, y

# Draw the board
def draw_board():
    number = 100
    for i in range(10):
        for j in range(10):
            x1 = j * cell_size
            y1 = i * cell_size
            x2 = x1 + cell_size
            y2 = y1 + cell_size
            fill = "#e6f7ff" if (i + j) % 2 == 0 else "#ccf2ff"
            canvas.create_rectangle(x1, y1, x2, y2, fill=fill)
            canvas.create_text(x1 + 25, y1 + 25, text=str(number), font=("Arial", 10, "bold"))
            number -= 1 if i % 2 == 0 else -1
        number -= 9 if i % 2 == 0 else 11

# Draw snakes and ladders
def draw_snakes_ladders():
    for start, end in ladders.items():
        x1, y1 = get_coords(start)
        x2, y2 = get_coords(end)
        canvas.create_line(x1, y1, x2, y2, fill="green", width=4, arrow="last")
    for start, end in snakes.items():
        x1, y1 = get_coords(start)
        x2, y2 = get_coords(end)
        canvas.create_line(x1, y1, x2, y2, fill="red", width=4, dash=(5, 3), arrow="last")

# Draw player tokens
def draw_players():
    canvas.delete("token")
    x1, y1 = get_coords(player1_pos)
    x2, y2 = get_coords(player2_pos)
    canvas.create_oval(x1 - 15, y1 - 15, x1 + 15, y1 + 15, fill="blue", tags="token")
    canvas.create_oval(x2 - 10, y2 - 10, x2 + 10, y2 + 10, fill="red", tags="token")

# Interpolated line animation
def move_along_line(start, end, color, callback):
    global moving
    moving = True
    x1, y1 = get_coords(start)
    x2, y2 = get_coords(end)
    steps = 30
    points = [(x1 + (x2 - x1) * i / steps, y1 + (y2 - y1) * i / steps + 20 * math.sin(i / steps * math.pi)) for i in range(steps + 1)]

    def animate(i):
        if i <= steps:
            x, y = points[i]
            canvas.delete("token")
            if current_player == 1:
                canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill="blue", tags="token")
            else:
                canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red", tags="token")
            root.after(40, lambda: animate(i + 1))
        else:
            if current_player == 1:
                globals()["player1_pos"] = end
            else:
                globals()["player2_pos"] = end
            draw_players()
            callback()

    animate(0)

# Move player step-by-step
def move_step_by_step(target_pos, callback):
    global current_player, moving
    moving = True
    steps = []

    pos = player1_pos if current_player == 1 else player2_pos
    for p in range(pos + 1, target_pos + 1):
        steps.append(p)

    def animate(i):
        nonlocal steps
        if i < len(steps):
            if current_player == 1:
                globals()["player1_pos"] = steps[i]
            else:
                globals()["player2_pos"] = steps[i]
            draw_players()
            root.after(250, lambda: animate(i + 1))
        else:
            callback()

    animate(0)

# Roll the dice and play
def roll_dice(event=None):
    global current_player, moving
    if moving:
        return

    roll = random.randint(1, 6)
    dice_label.config(text=dice_faces[roll - 1])

    if current_player == 1:
        temp_pos = player1_pos + roll
        if temp_pos > 100:
            switch_turn()
            return
        move_step_by_step(temp_pos, lambda: check_snake_ladder("player1"))
    else:
        temp_pos = player2_pos + roll
        if temp_pos > 100:
            switch_turn()
            return
        move_step_by_step(temp_pos, lambda: check_snake_ladder("player2"))

# Check for snake or ladder
def check_snake_ladder(player):
    global current_player, player1_pos, player2_pos, moving

    pos = player1_pos if player == "player1" else player2_pos
    if pos in ladders:
        new_pos = ladders[pos]
        move_along_line(pos, new_pos, "green", end_turn)
    elif pos in snakes:
        new_pos = snakes[pos]
        move_along_line(pos, new_pos, "red", end_turn)
    else:
        end_turn()

def end_turn():
    global moving
    draw_players()
    if player1_pos == 100:
        result_label.config(text="🎉 Player 1 Wins!")
        dice_label.unbind("<Button-1>")
    elif player2_pos == 100:
        result_label.config(text="🎉 Player 2 Wins!")
        dice_label.unbind("<Button-1>")
    else:
        switch_turn()
    moving = False

def switch_turn():
    global current_player
    current_player = 2 if current_player == 1 else 1
    turn_label.config(text=f"Player {current_player}'s Turn", fg="blue" if current_player == 1 else "red")

# Reset game
def reset_game():
    global player1_pos, player2_pos, current_player, moving
    player1_pos = 1
    player2_pos = 1
    current_player = 1
    moving = False
    draw_players()
    dice_label.config(text="🎲")
    result_label.config(text="Click the dice to roll!")
    turn_label.config(text="Player 1's Turn", fg="blue")
    dice_label.bind("<Button-1>", roll_dice)

# UI Setup
draw_board()
draw_snakes_ladders()
draw_players()

turn_label = tk.Label(root, text="Player 1's Turn", font=("Arial", 14, "bold"), bg="#f0f8ff")
turn_label.pack()

dice_label = tk.Label(root, text="🎲", font=("Arial", 100), bg="#c0f0ff", width=3)
dice_label.pack(pady=10)
dice_label.bind("<Button-1>", roll_dice)

result_label = tk.Label(root, text="Click the dice to roll!", font=("Arial", 14), bg="#f0f8ff")
result_label.pack(pady=5)

tk.Button(root, text="🔄 Reset", font=("Arial", 12), command=reset_game, bg="#d6eaff").pack(pady=5)
tk.Button(root, text="❌ Exit", font=("Arial", 12), command=root.destroy, bg="#ffcccc").pack()

root.mainloop()

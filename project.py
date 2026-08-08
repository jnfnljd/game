import tkinter as tk
import ctypes

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

root = tk.Tk()
root.title("Soccer Game")

try:
    player_right = tk.PhotoImage(file="player_right.png")
    player_left = tk.PhotoImage(file="player_left.png")

    WINDOW_WIDTH = 1655
    WINDOW_HEIGHT = 950

    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.resizable(False, False)

    canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bd=0, highlightthickness=0)
    canvas.pack()

    player_right= tk.PhotoImage(file="C:/Users/APP_11/Documents/GitHub/game/player_right.png").subsample(1, 1)
    player_left.png = tk.PhotoImage(file="C:/Users/APP_11/Documents/GitHub/game/player_left.png").subsample(1, 1)
    bg_image =tk.PhotoImage(file="C:/Users/APP_11/Documents/GitHub/game/field.png")
    current_player_image = player_right
        
    ball_original = tk.PhotoImage(file="C:/Users/APP_11/Documents/GitHub/game/ball.png")
    ball_image = ball_original.subsample(5, 5)
except Exception as e:
    print(e)
    root.destroy()
    exit()

canvas.create_image(0, 0, anchor=tk.NW, image=bg_image)

player = canvas.create_image(
    WINDOW_WIDTH // 2 - 100,
    WINDOW_HEIGHT // 2,
    anchor=tk.CENTER,
    image=current_player_image
)
ball = canvas.create_image(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, anchor=tk.CENTER, image=ball_image)

SPEED = 4
COLLISION_DIST = 30

def check_collision(dx, dy):
    p_pos = canvas.coords(player)
    b_pos = canvas.coords(ball)
    
    if abs(p_pos[0] - b_pos[0]) < COLLISION_DIST and abs(p_pos[1] - b_pos[1]) < COLLISION_DIST:
        next_bx = b_pos[0] + dx
        next_by = b_pos[1] + dy
        
        if 10 <= next_bx <= WINDOW_WIDTH - 10 and 10 <= next_by <= WINDOW_HEIGHT - 10:
            canvas.move(ball, dx, dy)
        else:
            return False
    return True

def move_player(event):
    global current_player_image
    key = event.char.lower()
    dx, dy = 0, 0
    
    if key == 'w':
        dy = -SPEED
    elif key == 's':
        dy = SPEED
    elif key == 'a':
        dx = -SPEED
        
        current_player_image= player_left
        canvas.itemconfig(player, image=current_player_image)
    elif key == 'd':
        dx = SPEED
        
        current_player_image= player_right
        canvas.itemconfig(player, image=current_player_image)
    if dx == 0 and dy == 0:
        return

    p_pos = canvas.coords(player)
    next_px = p_pos[0] + dx
    next_py = p_pos[1] + dy
    
    if 25 <= next_px <= WINDOW_WIDTH - 25 and 25 <= next_py <= WINDOW_HEIGHT - 25:
        if check_collision(dx, dy):
            canvas.move(player, dx, dy)

root.bind("<Key>", move_player)
root.mainloop()

def event_shoot
    
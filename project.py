import tkinter as tk
import ctypes
import time

try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except:
        pass

root = tk.Tk()
root.title("Soccer Game")

fullscreen = True
root.attributes("-fullscreen", fullscreen)
root.update_idletasks()

WINDOW_WIDTH = root.winfo_screenwidth()
WINDOW_HEIGHT = root.winfo_screenheight()

root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
root.resizable(True, True)

canvas = tk.Canvas(
    root,
    width=WINDOW_WIDTH,
    height=WINDOW_HEIGHT,
    bd=0,
    highlightthickness=0
)
canvas.pack()

player_right = tk.PhotoImage(
    file="C:/Users/APP_11/Documents/GitHub/game/player_right.png"
).subsample(1, 1)

player_left = tk.PhotoImage(
    file="C:/Users/APP_11/Documents/GitHub/game/player_left.png"
).subsample(1, 1)

bg_image = tk.PhotoImage(
    file="C:/Users/APP_11/Documents/GitHub/game/field.png"
)

current_player_image = player_right

ball_original = tk.PhotoImage(
    file="C:/Users/APP_11/Documents/GitHub/game/ball.png"
)
ball_image = ball_original.subsample(5, 5)

goal_left_image = tk.PhotoImage(
    file="C:/Users/APP_11/Documents/GitHub/game/left_goal.png"
).subsample(4, 4)

goal_right_image = tk.PhotoImage(
    file="C:/Users/APP_11/Documents/GitHub/game/right_goal.png"
).subsample(4, 4)

FIELD_WIDTH = bg_image.width()
FIELD_HEIGHT = bg_image.height()
MAX_CAMERA_X = max(0, FIELD_WIDTH - WINDOW_WIDTH)

camera_x = 0

bg_layer = canvas.create_image(
    0,
    0,
    anchor=tk.NW,
    image=bg_image
)

player_world_x = WINDOW_WIDTH // 2 - 100
player_world_y = WINDOW_HEIGHT // 2
ball_world_x = WINDOW_WIDTH // 2
ball_world_y = WINDOW_HEIGHT // 2

player = canvas.create_image(
    player_world_x,
    player_world_y,
    anchor=tk.CENTER,
    image=current_player_image
)

ball = canvas.create_image(
    ball_world_x,
    ball_world_y,
    anchor=tk.CENTER,
    image=ball_image
)

SPEED = 4
COLLISION_DIST = 30

ball_vx = 0
ball_vy = 0

SHOT_POWER = 12
SHOT_COOLDOWN = 1
last_shot_time = 0

BALL_FRICTION = 0.96
BALL_OFFSET = 28

player_dir_x = 1
player_dir_y = 0

ball_picked = False

LEFT_GOAL_X = 70
LEFT_GOAL_Y = 390

RIGHT_GOAL_X = 1550
RIGHT_GOAL_Y = 390

left_goal = canvas.create_image(
    LEFT_GOAL_X,
    LEFT_GOAL_Y,
    anchor=tk.CENTER,
    image=goal_left_image
)

right_goal = canvas.create_image(
    RIGHT_GOAL_X,
    RIGHT_GOAL_Y,
    anchor=tk.CENTER,
    image=goal_right_image
)

def render_scene():
    global camera_x

    canvas.coords(bg_layer, -camera_x, 0)
    canvas.coords(player, player_world_x - camera_x, player_world_y)
    canvas.coords(ball, ball_world_x - camera_x, ball_world_y)
    canvas.coords(left_goal, LEFT_GOAL_X - camera_x, LEFT_GOAL_Y)
    canvas.coords(right_goal, RIGHT_GOAL_X - camera_x, RIGHT_GOAL_Y)

def update_camera():
    global camera_x

    deadzone = 80
    center_x = WINDOW_WIDTH / 2

    left_limit = camera_x + center_x - deadzone
    right_limit = camera_x + center_x + deadzone

    if player_world_x < left_limit:
        camera_x = player_world_x - (center_x - deadzone)
    elif player_world_x > right_limit:
        camera_x = player_world_x - (center_x + deadzone)

    camera_x = max(0, min(camera_x, MAX_CAMERA_X))
    render_scene()

def sync_ball_with_player():
    global ball_picked

    if not ball_picked:
        return

    global ball_world_x, ball_world_y

    ball_world_x = player_world_x + player_dir_x * BALL_OFFSET
    ball_world_y = player_world_y + player_dir_y * BALL_OFFSET
    render_scene()

def check_collision(dx, dy):
    global ball_picked

    if (
        abs(player_world_x - ball_world_x) < COLLISION_DIST
        and
        abs(player_world_y - ball_world_y) < COLLISION_DIST
    ):
        ball_picked = True
        sync_ball_with_player()
        return True

    return True

def move_player(event):
    global current_player_image
    global player_dir_x, player_dir_y
    global player_world_x, player_world_y

    key = event.keysym.lower()

    dx = 0
    dy = 0

    if key == "w":
        dy = -SPEED
        player_dir_x = 0
        player_dir_y = -1

    elif key == "d":
        dx = SPEED
        player_dir_x = 1
        player_dir_y = 0
        current_player_image = player_right

    elif key == "s":
        dy = SPEED
        player_dir_x = 0
        player_dir_y = 1

    elif key == "a":
        dx = -SPEED
        player_dir_x = -1
        player_dir_y = 0
        current_player_image = player_left

    else:
        return

    canvas.itemconfig(player, image=current_player_image)

    next_px = player_world_x + dx
    next_py = player_world_y + dy

    if (
        25 <= next_px <= FIELD_WIDTH - 25
        and
        25 <= next_py <= FIELD_HEIGHT - 25
    ):
        if check_collision(dx, dy):
            player_world_x = next_px
            player_world_y = next_py

    sync_ball_with_player()
    update_camera()

def shoot():
    global ball_vx, ball_vy
    global last_shot_time
    global ball_picked

    current_time = time.monotonic()

    if current_time - last_shot_time < SHOT_COOLDOWN:
        return

    dx = ball_world_x - player_world_x
    dy = ball_world_y - player_world_y
    distance = (dx * dx + dy * dy) ** 0.5

    if distance <= 100 and ball_picked:
        ball_picked = False
        ball_vx = player_dir_x * SHOT_POWER
        ball_vy = player_dir_y * SHOT_POWER
        last_shot_time = current_time

def update_ball():
    global ball_vx, ball_vy
    global ball_world_x, ball_world_y

    if ball_picked:
        sync_ball_with_player()
        root.after(16, update_ball)
        return

    if ball_vx != 0 or ball_vy != 0:
        ball_world_x += ball_vx
        ball_world_y += ball_vy

        ball_vx *= BALL_FRICTION
        ball_vy *= BALL_FRICTION

        if abs(ball_vx) < 0.1:
            ball_vx = 0

        if abs(ball_vy) < 0.1:
            ball_vy = 0

        if ball_world_x < 10:
            ball_world_x = 10
            ball_vx *= -0.5

        elif ball_world_x > FIELD_WIDTH - 10:
            ball_world_x = FIELD_WIDTH - 10
            ball_vx *= -0.5

        if ball_world_y < 10:
            ball_world_y = 10
            ball_vy *= -0.5

        elif ball_world_y > FIELD_HEIGHT - 10:
            ball_world_y = FIELD_HEIGHT - 10
            ball_vy *= -0.5

    render_scene()
    root.after(16, update_ball)

def game_key(event):
    if event.keysym.lower() == "space":
        shoot()
        return

    move_player(event)

root.bind("<KeyPress>", game_key)
root.focus_force()
render_scene()
update_ball()
root.mainloop()
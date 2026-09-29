import os
import random
import sys
import time


# -----------------------------
# CROSS-PLATFORM KEYBOARD INPUT
# -----------------------------

if os.name == "nt":
    import msvcrt

    def key_pressed():
        return msvcrt.kbhit()

    def read_key():
        return msvcrt.getwch().lower()

else:
    import select
    import termios
    import tty

    def key_pressed():
        ready, _, _ = select.select([sys.stdin], [], [], 0)
        return bool(ready)

    def read_key():
        old_settings = termios.tcgetattr(sys.stdin)

        try:
            tty.setcbreak(sys.stdin.fileno())
            return sys.stdin.read(1).lower()
        finally:
            termios.tcsetattr(
                sys.stdin,
                termios.TCSADRAIN,
                old_settings
            )


# -----------------------------
# GAME SETTINGS
# -----------------------------

GRID_WIDTH = 30
GRID_HEIGHT = 15

START_LENGTH = 3
START_DELAY = 0.25

SPECIAL_OBJECT_TIME = 10
SPEED_BOOST_TIME = 5

MENU_WIDTH = 40


# -----------------------------
# MOVEMENT SETTINGS
# -----------------------------

DIRECTIONS = {
    "w": (0, -1),
    "s": (0, 1),
    "a": (-1, 0),
    "d": (1, 0)
}


OPPOSITE_DIRECTION = {
    "w": "s",
    "s": "w",
    "a": "d",
    "d": "a"
}


# -----------------------------
# GAME OBJECTS
# -----------------------------

GAME_OBJECTS = {
    "*": "Apple",
    "G": "Golden",
    "S": "Speed",
    "X": "Poison",
    "F": "Freeze",
    "B": "Bomb"
}


# -----------------------------
# SCREEN FUNCTIONS
# -----------------------------

def clear_screen():

    print("\033[2J\033[H", end="")


def print_box_top(width):

    print("+" + "-" * width + "+")


def print_box_line(text, width=MENU_WIDTH):

    print("|" + text.center(width) + "|")


# -----------------------------
# MAIN MENU
# -----------------------------

def show_menu(high_score):

    clear_screen()

    print()
    print_box_top(MENU_WIDTH)
    print_box_line("")
    print_box_line("S N A K E   G A M E")
    print_box_line("")
    print_box_top(MENU_WIDTH)

    print()
    print("MAIN MENU".center(MENU_WIDTH + 2))
    print()

    print("        [1]  Start Game")
    print("        [2]  Instructions")
    print("        [3]  Quit")

    print()
    print(f"        High Score: {high_score}")
    print()

    print_box_top(MENU_WIDTH)

    while True:

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice in ("1", "2", "3"):
            return choice

        print("Invalid choice. Please enter 1, 2, or 3.")


# -----------------------------
# INSTRUCTIONS
# -----------------------------

def show_instructions():

    clear_screen()

    print()
    print_box_top(MENU_WIDTH)
    print_box_line("")
    print_box_line("INSTRUCTIONS")
    print_box_line("")
    print_box_top(MENU_WIDTH)

    print()
    print("CONTROLS")
    print("--------")
    print("  W  = Move Up")
    print("  A  = Move Left")
    print("  S  = Move Down")
    print("  D  = Move Right")
    print("  Q  = Quit Game")
    print()

    print("FRUITS AND OBJECTS")
    print("------------------")
    print("  * = Apple   +10 points, grow by 1")
    print("  G = Golden  +25 points, grow by 2")
    print("  S = Speed   +15 points, faster for 5 seconds")
    print("  X = Poison  -10 points, lose 1 segment")
    print("  F = Freeze  +20 points, protects next collision")
    print("  B = Bomb    Game Over if eaten")
    print()

    print("OBJECT TIMER")
    print("------------")
    print("  Apple stays until it is eaten.")
    print("  Other objects disappear after 10 seconds.")
    print()

    print("RULES")
    print("-----")
    print("  - Do not hit the wall.")
    print("  - Do not hit your own body.")
    print("  - Avoid the bomb.")
    print("  - You cannot immediately reverse direction.")
    print("  - Eat useful fruits to increase your score.")
    print()

    print_box_top(MENU_WIDTH)

    input("\nPress Enter to return to the main menu...")


# -----------------------------
# SNAKE FUNCTIONS
# -----------------------------

def create_snake():

    return [
        (10, 7),
        (9, 7),
        (8, 7)
    ]


def create_food(snake):

    while True:

        x = random.randint(1, GRID_WIDTH)
        y = random.randint(1, GRID_HEIGHT)

        position = (x, y)

        # Do not place an object inside the snake.
        if position not in snake:

            object_symbol = random.choice(
                list(GAME_OBJECTS.keys())
            )

            if object_symbol == "*":
                expiration_time = None
            else:
                expiration_time = (
                    time.time() + SPECIAL_OBJECT_TIME
                )

            return (
                position,
                object_symbol,
                expiration_time
            )


def move_snake(snake, direction):

    change_x, change_y = DIRECTIONS[direction]

    head_x, head_y = snake[0]

    new_head = (
        head_x + change_x,
        head_y + change_y
    )

    snake.insert(0, new_head)

    return new_head


# -----------------------------
# GAME DISPLAY
# -----------------------------

def display_board(
    snake,
    food_position,
    object_symbol,
    score,
    high_score,
    speed_boost,
    freeze_protection
):

    clear_screen()

    board_width = GRID_WIDTH + 2

    print("+" + "-" * board_width + "+")
    print(
        "|" +
        "S N A K E   G A M E".center(board_width) +
        "|"
    )
    print("+" + "-" * board_width + "+")

    print(
        f" Score: {score:<6} "
        f"High Score: {high_score:<6}"
    )

    if speed_boost:
        print(" Power: SPEED BOOST")

    if freeze_protection:
        print(" Power: FREEZE SHIELD")

    print("+" + "-" * board_width + "+")

    for y in range(1, GRID_HEIGHT + 1):

        row = ""

        for x in range(1, GRID_WIDTH + 1):

            position = (x, y)

            if position == snake[0]:

                row += "O"

            elif position in snake:

                row += "o"

            elif position == food_position:

                row += object_symbol

            else:

                row += " "

        print("|" + row + "|")

    print("+" + "-" * board_width + "+")

    print(
        "* = Apple   G = Golden   S = Speed   "
        "X = Poison   F = Freeze   B = Bomb"
    )

    print("W A S D = Move     Q = Quit")


# -----------------------------
# KEYBOARD INPUT
# -----------------------------

def get_direction(current_direction):

    new_direction = current_direction

    if key_pressed():

        key = read_key()

        if key in DIRECTIONS:

            # Prevent an immediate 180-degree turn.
            if key != OPPOSITE_DIRECTION[current_direction]:

                new_direction = key

        elif key == "q":

            return "quit"

    return new_direction


# -----------------------------
# FRUIT EFFECTS
# -----------------------------

def apply_fruit_effect(
    snake,
    object_symbol,
    score,
    current_delay
):

    message = ""

    # Apple
    if object_symbol == "*":

        snake.append(snake[-1])
        score += 10

        message = "Apple eaten! Snake grew by 1."

    # Golden fruit
    elif object_symbol == "G":

        snake.append(snake[-1])
        snake.append(snake[-1])

        score += 25

        message = "Golden Fruit! Snake grew by 2."

    # Speed fruit
    elif object_symbol == "S":

        score += 15

        current_delay = max(
            0.08,
            current_delay - 0.07
        )

        message = "Speed Fruit! You are faster for 5 seconds."

    # Poison fruit
    elif object_symbol == "X":

        score = max(
            0,
            score - 10
        )

        if len(snake) > START_LENGTH:

            snake.pop()

        message = "Poison! Snake lost 1 segment."

    # Freeze fruit
    elif object_symbol == "F":

        score += 20

        message = "Freeze Fruit! Next collision will be ignored."

    # Bomb
    elif object_symbol == "B":

        message = "Bomb eaten!"

    return score, current_delay, message


# -----------------------------
# GAME OVER SCREEN
# -----------------------------

def game_over_screen(
    score,
    high_score,
    death_reason
):

    clear_screen()

    print()
    print_box_top(MENU_WIDTH)
    print_box_line("")
    print_box_line("G A M E   O V E R")
    print_box_line("")
    print_box_top(MENU_WIDTH)

    print()
    print(f"Cause: {death_reason}")
    print()

    print(f"Your Score : {score}")
    print(f"High Score : {high_score}")
    print()

    if score == high_score and score > 0:

        print(
            "★ NEW HIGH SCORE! ★".center(
                MENU_WIDTH + 2
            )
        )

        print()

    print_box_top(MENU_WIDTH)

    print()
    print("        [R]  Restart")
    print("        [Q]  Quit to Menu")
    print()

    print_box_top(MENU_WIDTH)

    while True:

        choice = input(
            "\nEnter your choice: "
        ).strip().lower()

        if choice == "r":

            return "restart"

        elif choice == "q":

            return "quit"

        print("Invalid choice. Enter R or Q.")


# -----------------------------
# RUN GAME
# -----------------------------

def run_game(high_score):

    snake = create_snake()

    (
        food_position,
        object_symbol,
        object_expiration
    ) = create_food(snake)

    score = 0

    direction = "d"

    current_delay = START_DELAY

    speed_boost = False
    speed_boost_end = 0

    freeze_protection = False

    message = ""

    # Start screen
    clear_screen()

    print()
    print_box_top(MENU_WIDTH)
    print_box_line("")
    print_box_line("GET READY!")
    print_box_line("")
    print_box_top(MENU_WIDTH)

    print()
    print("Use W A S D to start moving.")
    print("Press Q to return to the menu.")
    print()
    print("No need to press Enter while playing.")
    print()

    # Wait for the first movement.
    while True:

        if key_pressed():

            key = read_key()

            if key == "q":

                return "quit", high_score

            if key in DIRECTIONS:

                if key != OPPOSITE_DIRECTION[direction]:

                    direction = key
                    break

    # -------------------------
    # MAIN GAME LOOP
    # -------------------------

    while True:

        # End the speed boost after five seconds.
        if (
            speed_boost
            and time.time() >= speed_boost_end
        ):

            speed_boost = False
            current_delay = START_DELAY

        # Special objects disappear after ten seconds.
        if (
            object_symbol != "*"
            and object_expiration is not None
            and time.time() >= object_expiration
        ):

            (
                food_position,
                object_symbol,
                object_expiration
            ) = create_food(snake)

        display_board(
            snake,
            food_position,
            object_symbol,
            score,
            high_score,
            speed_boost,
            freeze_protection
        )

        if message:

            print()
            print(" " + message)

            message = ""

        time.sleep(current_delay)

        direction = get_direction(direction)

        if direction == "quit":

            return "quit", high_score

        # Move the snake.
        new_head = move_snake(
            snake,
            direction
        )

        head_x, head_y = new_head

        # -------------------------
        # COLLISION CHECK
        # -------------------------

        hit_wall = (
            head_x < 1
            or head_x > GRID_WIDTH
            or head_y < 1
            or head_y > GRID_HEIGHT
        )

        hit_self = new_head in snake[1:]

        collision = hit_wall or hit_self

        if collision:

            # Freeze shield protects against one collision.
            if freeze_protection:

                freeze_protection = False

                snake.pop(0)

                message = (
                    "Freeze Shield saved you "
                    "from the collision!"
                )

                continue

            if hit_wall:

                death_reason = "You hit the wall."

            else:

                death_reason = "You hit yourself."

            if score > high_score:

                high_score = score

            result = game_over_screen(
                score,
                high_score,
                death_reason
            )

            return result, high_score

        # -------------------------
        # CHECK FOOD
        # -------------------------

        if new_head == food_position:

            eaten_object = object_symbol

            (
                score,
                current_delay,
                message
            ) = apply_fruit_effect(
                snake,
                eaten_object,
                score,
                current_delay
            )

            # Bomb causes immediate Game Over.
            if eaten_object == "B":

                death_reason = "You ate a bomb."

                if score > high_score:

                    high_score = score

                result = game_over_screen(
                    score,
                    high_score,
                    death_reason
                )

                return result, high_score

            # Activate speed boost.
            if eaten_object == "S":

                speed_boost = True

                speed_boost_end = (
                    time.time() + SPEED_BOOST_TIME
                )

            # Activate freeze protection.
            elif eaten_object == "F":

                freeze_protection = True

            # Generate a new object.
            (
                food_position,
                object_symbol,
                object_expiration
            ) = create_food(snake)

        else:

            # Normal movement removes the last segment.
            snake.pop()


# -----------------------------
# MAIN PROGRAM
# -----------------------------

def main():

    high_score = 0

    while True:

        choice = show_menu(high_score)

        # Start the game.
        if choice == "1":

            result, high_score = run_game(
                high_score
            )

            # Restart directly without returning
            # to the main menu.
            while result == "restart":

                result, high_score = run_game(
                    high_score
                )

            if result == "quit":

                continue

        # Open instructions.
        elif choice == "2":

            show_instructions()

        # Exit the program.
        elif choice == "3":

            clear_screen()

            print()
            print_box_top(MENU_WIDTH)
            print_box_line("")
            print_box_line("THANKS FOR PLAYING!")
            print_box_line("")
            print_box_top(MENU_WIDTH)

            print()

            break


# -----------------------------
# PROGRAM START
# -----------------------------

if __name__ == "__main__":

    main()
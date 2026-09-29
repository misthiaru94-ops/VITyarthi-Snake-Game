"""Print menus, instructions, the game board, and game-over screens."""

from settings import GRID_HEIGHT, GRID_WIDTH, MENU_WIDTH

def clear_screen():

    print("\033[2J\033[H", end="")


def print_box_top(width):

    print("+" + "-" * width + "+")


def print_box_line(text, width=MENU_WIDTH):

    print("|" + text.center(width) + "|")


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

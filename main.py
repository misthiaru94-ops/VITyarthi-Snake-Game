"""Coordinate the main menu and game rounds."""

from display import clear_screen, print_box_line, print_box_top, show_instructions, show_menu
from gameplay import run_game
from settings import MENU_WIDTH

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

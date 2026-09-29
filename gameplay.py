"""Run a game round and handle movement, collisions, and object effects."""

import time

from display import display_board, game_over_screen, print_box_line, print_box_top, clear_screen
from game_objects import apply_fruit_effect, create_food, create_snake, move_snake
from input_handler import key_pressed, read_key
from settings import DIRECTIONS, GRID_HEIGHT, GRID_WIDTH, MENU_WIDTH, OPPOSITE_DIRECTION, SPEED_BOOST_TIME, START_DELAY

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

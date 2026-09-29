"""Create the snake and objects, and apply collected-object effects."""

import random
import time

from settings import DIRECTIONS, GAME_OBJECTS, GRID_HEIGHT, GRID_WIDTH, SPECIAL_OBJECT_TIME, START_LENGTH

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

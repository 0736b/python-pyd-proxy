import random
import time

def thinking_number():
    time.sleep(0.2)
    return random.randint(1000, 9999)

def select_number(thinking_numbers):
    select = random.randint(0, len(thinking_numbers) - 1)
    return thinking_numbers[select]
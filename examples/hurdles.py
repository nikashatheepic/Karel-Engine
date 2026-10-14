# Karel runs to the east edge, jumping over hurdles of any height and picking up
# every beeper on the way, then drops them all in a pile at the finish.

def turn_right():
    turn_left()
    turn_left()
    turn_left()

def collect_beepers():
    while beepers_present():
        pick_beeper()

def jump_hurdle():
    turn_left()
    while right_is_blocked():
        move()
    turn_right()
    move()
    turn_right()
    while front_is_clear():
        move()
    turn_left()

def main():
    for column in range(8):
        if front_is_clear():
            move()
        else:
            jump_hurdle()
        collect_beepers()
    while beepers_in_bag():
        put_beeper()

if __name__ == '__main__':
    main()

import time

operating_world = None
karel = {}
walls = None
beepers = []

def create_world():
    global karel
    with open("world.csv", "r") as f:
        import_world = f.read()

    lines = import_world.strip().split("\n")

    karel["direction"] = lines[0].split(',')[1]
    karel["beepers"] = lines[0].split(',')[2]
    if karel["beepers"] == "inf":
        karel["beepers"] = float("inf")

    for i in range(len(lines)):
        if lines[i].strip() == "":
            wall_grid_row = i
            break

    world = []
    for line in lines[1:wall_grid_row]:
        world.append(line.split(","))

    return world

def copy_world():
    global operating_world
    world = create_world()
    operating_world = [row[:] for row in world]

def extract_ycoordinate():
    global operating_world
    for i in range(len(operating_world)):
        if "K" in operating_world[i]:
            y = i+1
    return y

def extract_xcoordinate(y):
    global operating_world
    for i in range(len(operating_world[y-1])):
        if "K" in operating_world[y-1][i]:  # use "in" to match like y-coordinate
            return i+1

def prepare_karel():
    global karel
    karel_y = extract_ycoordinate()
    karel_x = extract_xcoordinate(karel_y)

    karel["row"] = karel_y
    karel["col"] = karel_x

def build_walls():
    global walls
    with open("world.csv", "r") as f:
        lines = f.read().splitlines()

    for i in range(len(lines)):
        if lines[i].strip() == "":
            wall_grid_row = i
            break
    B_index = lines.index("B")
    wall_lines = lines[wall_grid_row + 1: B_index]

    walls = []
    for line in wall_lines:
        cells = line.split(",")
        row = []
        for cell in cells:
            if cell.strip() == "":
                row.append([0, 0, 0, 0])  # blank cell → all zeros
            else:
                row.append([int(d) for d in cell])  # '0100' → [0,1,0,0]
        walls.append(row)

def build_beepers():
    global beepers
    with open("world.csv", "r") as f:
        lines = f.read().splitlines()

    B_index = lines.index("B")
    beepers_lines = lines[B_index + 1:]

    for i in range(len(beepers_lines)):
        beepers.append([int(x) for x in beepers_lines[i].split(",")])

def move():
    global operating_world, karel

    r = karel["row"] - 1
    c = karel["col"] - 1
    d = karel["direction"]

    if d == "E":
        if c < len(operating_world[r]) - 1 and walls[r][c][3] == 0 and walls[r][c+1][1] == 0:
            new_r = r
            new_c = c + 1
        else:
            print('Blocked by wall')
            return
    elif d == "W":
        if c > 0 and walls[r][c][1] == 0 and walls[r][c-1][3] == 0:
            new_r = r
            new_c = c - 1
        else:
            print('Blocked by wall')
            return
    elif d == "N":
        if r > 0 and walls[r][c][0] == 0 and walls[r-1][c][2] == 0:
            new_r = r - 1
            new_c = c
        else:
            print('Blocked by wall')
            return
    elif d == "S":
        if r < len(operating_world) - 1 and walls[r][c][2] == 0 and walls[r+1][c][0] == 0:
            new_r = r + 1
            new_c = c
        else:
            print('Blocked by wall')
            return

    print_current_world()

    operating_world[r][c] = '0'
    operating_world[new_r][new_c] = "K"

    karel["row"] = new_r + 1
    karel["col"] = new_c + 1

def turn_left():
    global karel
    if karel["direction"] == "E":
        karel["direction"] = "N"
    elif karel["direction"] == "N":
        karel["direction"] = "W"
    elif karel["direction"] == "W":
        karel["direction"] = "S"
    elif karel["direction"] == "S":
        karel["direction"] = "E"

def put_beeper():
    global beepers
    r = karel["row"] - 1
    c = karel["col"] - 1
    if karel["beepers"] > 0:
        beepers[r][c] += 1
        karel["beepers"] -= 1
    else:
        return

    print_current_world()

def pick_beeper():
    global beepers
    r = karel["row"] - 1
    c = karel["col"] - 1
    if beepers[r][c] > 0:
        beepers[r][c] -= 1
        karel["beepers"] += 1

    print_current_world()

def load_user_program(filename="user_program.py"):
    with open(filename, "r") as f:
        code = f.read()
    exec(code, globals())

def main():
    copy_world()
    build_walls()
    prepare_karel()
    build_beepers()
    print_current_world()

    load_user_program()

    print_current_world()

def print_first_row():
    global karel
    current_row = ""
    if operating_world is None:
        return
    for j in range(len(operating_world[0])):
        current_row += "+---"
    current_row += "+"
    print(current_row)

def print_middle_rows():
    global walls, operating_world
    for i in range(len(operating_world)*2):
        karel_row = i//2
        if i % 2 != 0:
            print_karel_row(karel_row)
        else:
            print_wall_row(karel_row)
    return karel_row

def print_karel_row(karel_row):
    global operating_world, walls

    current_row = ""
    for j in range(len(operating_world[karel_row])):

        if j == 0 or walls[karel_row][j][1] == 1 or walls[karel_row][j - 1][3] == 1:
            current_row += "|"
        else:
            current_row += " "

        if operating_world[karel_row][j] == 'K' and beepers[karel_row][j] > 0:
            cell_content = f"K{beepers[karel_row][j]}"
        elif operating_world[karel_row][j] == 'K' and beepers[karel_row][j] == 0:
            cell_content = " K "
        elif operating_world[karel_row][j] == '0' and beepers[karel_row][j] > 0:
            cell_content = f"{beepers[karel_row][j]}"
        else:
            cell_content = "   "

        if len(cell_content) < 3:
            cell_content = cell_content.center(3)

        current_row += cell_content

    current_row += "|"
    print(current_row)

def print_wall_row(karel_row):
    global walls
    current_row = ""
    for j in range(len(walls[karel_row])):
        if karel_row == 0:
            return
        else:
            if (walls[karel_row][j][0] == 1) or (j + 1 < len(walls[karel_row]) and walls[(karel_row-1)][j][2] == 1):
                current_row += "+---"
            else:
                current_row += "+   "
    current_row += "+"
    print(current_row)

def print_last_row(karel_row):
    global karel
    current_row = ""
    for j in range(len(walls[karel_row])):
        current_row += "+---"
    current_row += "+"
    print(current_row)

def print_current_world():
    print_first_row()
    print_middle_rows()
    print_last_row(len(operating_world)-1)
    print()
    time.sleep(0.25)

def front_is_clear():
    r = karel["row"] - 1
    c = karel["col"] - 1
    d = karel["direction"]

    if d == "E":
        if c < len(operating_world[r]) - 1 and walls[r][c][3] == 0 and walls[r][c + 1][1] == 0:
            return True
        else:
            return False
    elif d == "W":
        if c > 0 and walls[r][c][1] == 0 and walls[r][c - 1][3] == 0:
            return True
        else:
            return False
    elif d == "N":
        if r > 0 and walls[r][c][0] == 0 and walls[r-1][c][2] == 0:
            return True
        else:
            return False
    elif d == "S":
        if r < len(operating_world) - 1 and walls[r][c][2] == 0 and walls[r+1][c][0] == 0:
            return True
        else:
            return False

def front_is_blocked():
    return not front_is_clear()

def left_of(d):
    return {"N": "W", "W": "S", "S": "E", "E": "N"}[d]

def right_of(d):
    return {"N":"E", "E":"S", "S":"W", "W":"N"}[d]

def can_move_in_direction(d):
    r = karel["row"] - 1
    c = karel["col"] - 1
    if d == "E":
        return c < len(operating_world[r]) - 1 and walls[r][c][3] == 0 and walls[r][c + 1][1] == 0
    elif d == "W":
        return c > 0 and walls[r][c][1] == 0 and walls[r][c - 1][3] == 0
    elif d == "N":
        return r > 0 and walls[r][c][0] == 0 and walls[r - 1][c][2] == 0
    elif d == "S":
        return r < len(operating_world) - 1 and walls[r][c][2] == 0 and walls[r + 1][c][0] == 0

def left_is_clear():
    return can_move_in_direction(left_of(karel["direction"]))

def right_is_clear():
    return can_move_in_direction(right_of(karel["direction"]))

def left_is_blocked():
    return not left_is_clear()

def right_is_blocked():
    return not right_is_clear()

def facing_north():
    return karel["direction"] == "N"

def not_facing_north():
    return not facing_north()

def facing_south():
    return karel["direction"] == "S"

def not_facing_south():
    return not facing_south()

def facing_east():
    return karel["direction"] == "E"

def not_facing_east():
    return not facing_east()

def facing_west():
    return karel["direction"] == "W"

def not_facing_west():
    return not facing_west()

def beepers_present():
    r = karel["row"] - 1
    c = karel["col"] - 1
    if beepers[r][c] > 0:
        return True
    else:
        return False

def no_beepers_present():
    return not beepers_present()

def beepers_in_bag():
    return karel["beepers"] > 0

def no_beepers_in_bag():
    return not beepers_in_bag()

if __name__ == "__main__":
    main()
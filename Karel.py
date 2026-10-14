import functools
import sys
import time

class KarelError(Exception):
    pass


def find_blank_line(lines):
    for i in range(len(lines)):
        if lines[i].strip() == "":
            return i


def create_world(lines):
    karel = {}
    karel["direction"] = lines[0].split(',')[1]
    if karel["direction"] not in ("N", "E", "S", "W"):
        raise ValueError(f"Starting direction must be N, E, S or W, not {karel['direction']!r}")

    karel["beepers"] = lines[0].split(',')[2]
    if karel["beepers"] == "inf":
        karel["beepers"] = float("inf")
    else:
        karel["beepers"] = int(karel["beepers"])

    wall_grid_row = find_blank_line(lines)

    world = []
    for line in lines[1:wall_grid_row]:
        world.append(line.split(","))

    return world, karel

def extract_ycoordinate(world):
    y = None
    for i in range(len(world)):
        if "K" in world[i]:
            y = i+1
    return y

def extract_xcoordinate(world, y):
    for i in range(len(world[y-1])):
        if "K" in world[y-1][i]:
            return i+1

def prepare_karel(state):
    karel_y = extract_ycoordinate(state["world"])
    if karel_y is None:
        raise ValueError("The world needs a K to show where Karel starts")
    karel_x = extract_xcoordinate(state["world"], karel_y)

    state["karel"]["row"] = karel_y
    state["karel"]["col"] = karel_x

def build_walls(lines, rows):
    wall_grid_row = find_blank_line(lines)
    wall_lines = lines[wall_grid_row + 1: wall_grid_row + 1 + rows]

    walls = []
    for line in wall_lines:
        cells = line.split(",")
        row = []
        for cell in cells:
            if cell.strip() == "":
                row.append([0, 0, 0, 0])  # blank cell → all zeros
            elif len(cell) == 4 and all(d in "01" for d in cell):
                row.append([int(d) for d in cell])  # '0100' → [0,1,0,0]
            else:
                raise ValueError(f"Wall cell {cell!r} should be four 0/1 digits in N W S E order")
        walls.append(row)
    return walls

def build_beepers(lines, rows):
    B_index = lines.index("B")
    beepers_lines = lines[B_index + 1: B_index + 1 + rows]

    beepers = []
    for i in range(len(beepers_lines)):
        beepers.append([int(x) for x in beepers_lines[i].split(",")])
    return beepers

def check_sizes(state):
    rows = len(state["world"])
    cols = len(state["world"][0])
    for name in ("walls", "beepers"):
        section = state[name]
        if len(section) != rows or any(len(row) != cols for row in section):
            raise ValueError(f"The {name} section should be {rows} rows by {cols} columns, the same as the grid")

def load_world(filename="world.csv"):
    with open(filename, "r") as f:
        return build_state(f.read().splitlines())

def build_state(lines):
    world, karel = create_world(lines)
    state = {
        "world": world,
        "karel": karel,
        "walls": build_walls(lines, len(world)),
        "beepers": build_beepers(lines, len(world)),
        "delay": 0.25,
    }
    check_sizes(state)
    prepare_karel(state)
    return state

def move(state):
    world = state["world"]
    karel = state["karel"]

    if front_is_clear(state) is False:
        raise KarelError(f"Blocked by wall at row {karel['row']}, column {karel['col']}, facing {karel['direction']}")

    r = karel["row"] - 1
    c = karel["col"] - 1
    d = karel["direction"]

    if d == "E":
        new_r, new_c = r, c + 1
    elif d == "W":
        new_r, new_c = r, c - 1
    elif d == "N":
        new_r, new_c = r - 1, c
    elif d == "S":
        new_r, new_c = r + 1, c

    world[r][c] = '0'
    world[new_r][new_c] = "K"

    karel["row"] = new_r + 1
    karel["col"] = new_c + 1

    print_current_world(state)

def turn_left(state):
    karel = state["karel"]
    if karel["direction"] == "E":
        karel["direction"] = "N"
    elif karel["direction"] == "N":
        karel["direction"] = "W"
    elif karel["direction"] == "W":
        karel["direction"] = "S"
    elif karel["direction"] == "S":
        karel["direction"] = "E"

def put_beeper(state):
    karel = state["karel"]
    r = karel["row"] - 1
    c = karel["col"] - 1
    if karel["beepers"] > 0:
        state["beepers"][r][c] += 1
        karel["beepers"] -= 1
    else:
        raise KarelError("No beepers left in the bag")

    print_current_world(state)

def pick_beeper(state):
    karel = state["karel"]
    r = karel["row"] - 1
    c = karel["col"] - 1
    if state["beepers"][r][c] > 0:
        state["beepers"][r][c] -= 1
        karel["beepers"] += 1
    else:
        raise KarelError(f"No beeper to pick up at row {karel['row']}, column {karel['col']}")

    print_current_world(state)

def print_border(state):
    current_row = ""
    for j in range(len(state["world"][0])):
        current_row += "+---"
    current_row += "+"
    print(current_row)

def print_middle_rows(state):
    for i in range(len(state["world"])*2):
        karel_row = i//2
        if i % 2 != 0:
            print_karel_row(state, karel_row)
        else:
            print_wall_row(state, karel_row)

def print_karel_row(state, karel_row):
    world = state["world"]
    walls = state["walls"]
    beepers = state["beepers"]

    current_row = ""
    for j in range(len(world[karel_row])):

        if j == 0 or walls[karel_row][j][1] == 1 or walls[karel_row][j - 1][3] == 1:
            current_row += "|"
        else:
            current_row += " "

        if world[karel_row][j] == 'K' and beepers[karel_row][j] > 0:
            cell_content = f"K{beepers[karel_row][j]}"
        elif world[karel_row][j] == 'K' and beepers[karel_row][j] == 0:
            cell_content = " K "
        elif world[karel_row][j] == '0' and beepers[karel_row][j] > 0:
            cell_content = f"{beepers[karel_row][j]}"
        else:
            cell_content = "   "

        if len(cell_content) < 3:
            cell_content = cell_content.center(3)

        current_row += cell_content

    current_row += "|"
    print(current_row)

def print_wall_row(state, karel_row):
    walls = state["walls"]
    if karel_row == 0:
        return

    current_row = ""
    for j in range(len(walls[karel_row])):
        if walls[karel_row][j][0] == 1 or walls[karel_row-1][j][2] == 1:
            current_row += "+---"
        else:
            current_row += "+   "
    current_row += "+"
    print(current_row)

def print_current_world(state):
    print_border(state)
    print_middle_rows(state)
    print_border(state)
    print()
    time.sleep(state["delay"])

def can_move_in_direction(state, d):
    world = state["world"]
    walls = state["walls"]
    r = state["karel"]["row"] - 1
    c = state["karel"]["col"] - 1
    if d == "E":
        return c < len(world[r]) - 1 and walls[r][c][3] == 0 and walls[r][c + 1][1] == 0
    elif d == "W":
        return c > 0 and walls[r][c][1] == 0 and walls[r][c - 1][3] == 0
    elif d == "N":
        return r > 0 and walls[r][c][0] == 0 and walls[r - 1][c][2] == 0
    elif d == "S":
        return r < len(world) - 1 and walls[r][c][2] == 0 and walls[r + 1][c][0] == 0

def left_of(d):
    return {"N": "W", "W": "S", "S": "E", "E": "N"}[d]

def right_of(d):
    return {"N":"E", "E":"S", "S":"W", "W":"N"}[d]

def front_is_clear(state):
    return can_move_in_direction(state, state["karel"]["direction"])

def front_is_blocked(state):
    return not front_is_clear(state)

def left_is_clear(state):
    return can_move_in_direction(state, left_of(state["karel"]["direction"]))

def right_is_clear(state):
    return can_move_in_direction(state, right_of(state["karel"]["direction"]))

def left_is_blocked(state):
    return not left_is_clear(state)

def right_is_blocked(state):
    return not right_is_clear(state)

def facing_north(state):
    return state["karel"]["direction"] == "N"

def not_facing_north(state):
    return not facing_north(state)

def facing_south(state):
    return state["karel"]["direction"] == "S"

def not_facing_south(state):
    return not facing_south(state)

def facing_east(state):
    return state["karel"]["direction"] == "E"

def not_facing_east(state):
    return not facing_east(state)

def facing_west(state):
    return state["karel"]["direction"] == "W"

def not_facing_west(state):
    return not facing_west(state)

def beepers_present(state):
    r = state["karel"]["row"] - 1
    c = state["karel"]["col"] - 1
    return state["beepers"][r][c] > 0

def no_beepers_present(state):
    return not beepers_present(state)

def beepers_in_bag(state):
    return state["karel"]["beepers"] > 0

def no_beepers_in_bag(state):
    return not beepers_in_bag(state)

USER_COMMANDS = [
    move, turn_left, put_beeper, pick_beeper,
    front_is_clear, front_is_blocked, left_is_clear, left_is_blocked,
    right_is_clear, right_is_blocked,
    facing_north, not_facing_north, facing_south, not_facing_south,
    facing_east, not_facing_east, facing_west, not_facing_west,
    beepers_present, no_beepers_present, beepers_in_bag, no_beepers_in_bag,
]

def run_user_code(state, code, filename="<program>"):
    commands = {"__name__": "__main__"}
    for command in USER_COMMANDS:
        commands[command.__name__] = functools.partial(command, state)
    exec(compile(code, filename, "exec"), commands)

def load_user_program(state, filename="user_program.py"):
    with open(filename, "r") as f:
        code = f.read()
    run_user_code(state, code, filename)

def main():
    world_file = sys.argv[1] if len(sys.argv) > 1 else "world.csv"
    program_file = sys.argv[2] if len(sys.argv) > 2 else "user_program.py"

    state = load_world(world_file)
    print_current_world(state)

    try:
        load_user_program(state, program_file)
    except KarelError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    print_current_world(state)

if __name__ == "__main__":
    main()

# Karel-Engine

A text-based engine for Karel the Robot, the robot Stanford uses to teach programming basics. You describe a world in a CSV file, write a Karel program in Python, and watch Karel move through the world as an animated ASCII grid in your terminal. I built this while going through Stanford's Karel exercises during a university course to see if I could.

```
+---+---+---+---+---+
| 1                 |
+   +   +   +   +   +
|                   |
+   +   +---+   +   +
| K             | 2 |
+---+---+---+---+---+
```

Karel is shown as `K`, and beepers (objects Karel can pick up and put down) are shown as numbers. No dependencies, just Python 3.

## Running

```bash
python Karel.py                          # runs user_program.py in world.csv
python Karel.py my_world.csv my_prog.py  # custom world and program
python Karel.py examples/hurdles.csv examples/hurdles.py
```

The hurdles example has Karel jump walls of different heights, collect every beeper on the way and drop them in a pile at the finish.

If Karel hits a wall, picks up a beeper that isn't there, or puts one down with an empty bag, the program stops with an error message.

## Writing a Karel program

Write your program in `user_program.py`:

```python
def main():
    while front_is_clear():
        move()
    put_beeper()

if __name__ == '__main__':
    main()
```

Karel has 4 built-in actions. In Stanford's course, these are enough to get students solving complex problems by combining them with conditions and their own helper functions. Programs can only use the commands below. The engine's internals are not visible to them.

| Actions | Conditions |
|---|---|
| `move()` | `front_is_clear()` / `front_is_blocked()` |
| `turn_left()` | `left_is_clear()` / `left_is_blocked()` |
| `put_beeper()` | `right_is_clear()` / `right_is_blocked()` |
| `pick_beeper()` | `facing_north()` / `not_facing_north()` (also `south`, `east`, `west`) |
| | `beepers_present()` / `no_beepers_present()` |
| | `beepers_in_bag()` / `no_beepers_in_bag()` |

A good problem to try is Stanford's "Midpoint Karel": write a program that finds the middle of the bottom row in *any* world. It has to handle edge cases like a 1x1 world and worlds with an even width, so you need a solution that works for every possible world, not just the one in front of you.

## World file format

A world file has three sections separated by blank lines:

```
Karel Metadata,E,inf,""     <- starting direction (N/E/S/W), beepers in bag (number or inf)
0,0,0,0,0                   <- grid: K marks Karel's start, every other cell is 0
0,0,0,0,0
K,0,0,0,0

,,,,                        <- walls: one cell per grid cell, blank means no walls
,,0010,,                       otherwise four 0/1 digits in N W S E order
,,,0001,                       (0001 = wall on the east side of that cell)

B                           <- beepers: number of beepers on each cell
1,0,0,0,0
0,0,0,0,0
0,0,0,0,2
```

A wall only needs to be recorded on one side of an edge. Karel can't cross it from either direction.

Keep beeper counts under 100 per cell. Each cell is 3 characters wide, so Karel standing on 100 beepers (`K100`) wouldn't fit between the walls.

## Project structure

- `Karel.py`: the engine. `load_world` reads the world file into a single `state` dictionary (grid, Karel, walls, beepers) that every command receives. `run_user_code` runs a program with only the Karel commands available, with `state` already filled in so programs can call plain `move()`.
- `world.csv`, `user_program.py`: a starting world and an empty program to fill in.
- `examples/`: a larger example with walls and beepers.

## Contact

Questions? Email nikasha.datiashvili@gmail.com

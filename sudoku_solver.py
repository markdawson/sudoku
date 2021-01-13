"""
This program takes an unsolved Sudoku puzzle as an argument and returns it solved.

The format for the unsolved Sudoku puzzle is like this:
2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3

The characters are ordered from left to right and top to down.
A number represents a space filled in with a given initial number and a dot (.) represents an empty space.
So the Sudoku puzzle above would looks like this:

2__ | ___ | ___
___ | __6 | 2__
__1 | ___ | _7_
----+-----+-----
__6 | __8 | ___
3__ | _9_ | __7
___ | 6__ | 4__
----+-----+-----
_4_ | ___ | 8__
__5 | 2__ | ___
___ | ___ | __3
"""
import re

assignments = []


# Define some helpful global variables
def cross(A, B):
    """Cross product of elements in A and elements in B."""
    return [a + b for a in A for b in B]


rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(row, cols) for row in rows]
column_units = [cross(rows, col) for col in cols]
square_units = [cross(row, col)
                for row in ['ABC', 'DEF', 'GHI']
                for col in ['123', '456', '789']]
# diagonal_units = [[''.join(z) for z in zip(rows, cols)],
#                   [''.join(z) for z in zip(rows, reversed(cols))]]
unit_list = row_units + column_units + square_units  # + diagonal_units
units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], [])) - {s}) for s in boxes)


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    from collections import Counter
    for unit in unit_list:
        # Collect all the twins in a unit in case there are multiple twins in one unit
        twins = [digits for digits, count in
                 Counter(values[box] for box in unit if len(values[box]) == 2).items()
                 if count > 1]

        for twin in twins:
            for box in unit:
                if set(values[box]) == set(twin):
                    # Skip if this box is exactly equal to the twin
                    # Take set in case order got mixed up
                    continue
                for digit in twin:
                    if digit in values[box]:
                        new_value = values[box].replace(digit, '')
                        assign_value(values, box, new_value)
    return values


def sudoku_input_string_to_grid_dict(grid):
    """Convert grid into a dict of {square: char} with '.' for empties."""
    assert len(grid) == 81
    board = []
    digits = '123456789'
    for val in grid:
        if val in digits:
            board.append(val)
        if val == '.':
            board.append(digits)
    return dict(zip(boxes, board))


def display(grid_dict: dict, debugging_display: bool = False):
    """
    Display these values as a 2-D grid.
    :param grid_dict: A dictionary of the squares and potential values for each square.
    :param debugging_display: Whether we are displaying for debugging purposes or output purposes.
    """
    width = max(len(grid_dict[k]) for k in boxes) + 1 if debugging_display else 1
    for i, row in enumerate(rows):
        if i % 3 == 0:
            if i is 0:
                print('')
            else:
                print((('-' * width * 3 + '-+-') * 3)[:-2])
        display_row = []
        for j, col in enumerate(cols):
            bar = ''
            if j % 3 == 2 and j is not 8:
                bar = ' | '
            if not debugging_display and grid_dict[row + col] == "123456789":
                display_row.append("_".center(width, ' ') + bar)
            else:
                display_row.append(grid_dict[row + col].center(width, ' ') + bar)
        print(''.join(display_row))


def eliminate(grid_dict):
    """
    Eliminate possibilities from a box if one of its
    peers definitely already has that value.
    """
    for box, value in grid_dict.items():
        for peer in peers[box]:
            if len(grid_dict[peer]) == 1:
                value = value.replace(grid_dict[peer][0], '')
        # values[key] = value
        assign_value(grid_dict, box, value)

    return grid_dict


def only_choice(values):
    """
    Assign a box to a value if it's the only box
    in a unit that could contain that value
    """
    for unit in unit_list:
        occurs_only_once = set()
        occurs_more_than_once = set()
        for box in unit:
            for possibility in values[box]:
                if possibility in occurs_more_than_once:
                    continue
                elif possibility in occurs_only_once:
                    occurs_only_once.remove(possibility)
                    occurs_more_than_once.add(possibility)
                else:
                    occurs_only_once.add(possibility)

        for box in unit:
            for possibility in values[box]:
                if possibility in occurs_only_once:
                    assign_value(values, box, possibility)
    return values


def verify_no_empty_boxes(grid_dict, message):
    empty_boxes = [box for box in grid_dict.keys() if len(grid_dict[box]) == 0]
    if empty_boxes:
        print(message)
        raise Exception(f"We've eliminated all the possibilities for a box: {empty_boxes}")


def reduce_puzzle(grid_dict):
    stalled = False
    while not stalled:
        if isinstance(grid_dict, str):
            print('Values is {}'.format(grid_dict))
        number_solved_before = len([box for box in grid_dict.keys() if len(grid_dict[box]) == 1])

        verify_no_empty_boxes(grid_dict, "Before eliminate")
        grid_dict = eliminate(grid_dict)
        verify_no_empty_boxes(grid_dict, "After eliminate")

        grid_dict = only_choice(grid_dict)
        verify_no_empty_boxes(grid_dict, "After only choice")

        number_solved_after = len([box for box in grid_dict.keys() if len(grid_dict[box]) == 1])
        stalled = number_solved_before == number_solved_after

        # Sanity check
        verify_no_empty_boxes(grid_dict, "At end of while loop")
    return grid_dict


def search(grid_dict):
    grid_dict = reduce_puzzle(grid_dict)
    if grid_dict is False:
        return False

    if all((len(grid_dict[k]) == 1 for k in boxes)):
        print("................... all boxes")
        return grid_dict

    min_val, min_box = min((len(grid_dict[box]), box) for box in boxes if len(grid_dict[box]) > 1)
    for possibility in grid_dict[min_box]:
        new_search_values = grid_dict.copy()
        new_search_values[min_box] = possibility
        attempt = search(new_search_values)
        if attempt:
            return attempt


def grid_is_solved(grid_dict: dict) -> bool:
    return all(len(val) == 1 for val in grid_dict.values())


def grid_to_output_format(grid_dict: dict) -> str:
    print(grid_dict)
    print(grid_is_solved(grid_dict))
    if not grid_is_solved(grid_dict):
        raise Exception("This grid is not solved.")
    else:
        result = ""
        for box in boxes:
            result += grid_dict[box]
        return result


def solve(sudoku_input: str, print_results: bool = True):
    """
    Takes an input string and returns a grid with the corresponding values filled in.

    param: sudoku_input: A string in a format like this
            '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    param print_results: Whether we should print the results of the finished Sudoku puzzle to the terminal
    """
    m = re.match("[1-9.]{81}", sudoku_input)
    if not m:
        raise Exception("Improperly formatted input.")

    global_grid = sudoku_input_string_to_grid_dict(sudoku_input)
    print(global_grid)

    if print_results:
        display(global_grid)

    search(global_grid)

    if print_results:
        display(global_grid)

    return grid_to_output_format(global_grid)


if __name__ == "__main__":
    with open("sudoku_puzzle3.txt") as f:
        sample_input = f.read().strip()
        actual_output = solve(sample_input)
        print(actual_output)
    # with open("sudoku_puzzle2_solution.txt") as f:
    #     expected_output = f.read().strip()
    #     assert actual_output == expected_output

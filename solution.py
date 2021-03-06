def cross(A, B):
    """
    NOTE: Code extracted from Udacity's Sudoku project lessons.

    Cross product of elements in A and elements in B.
    """
    return [s+t for s in A for t in B]

# Vars representing various aspects of a Sudoku board
# NOTE: Code extracted from Udacity's Sudoku project lessons.
rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal_units_1 = [rs+cs for rs, cs in zip(rows, cols)]
diagonal_units_2 = [rs+cs for rs, cs in zip(rows, reversed(cols))]
diagonal_units = [diagonal_units_1, diagonal_units_2]
unitlist = row_units + column_units + square_units
square_peers = dict((s, [u for u in square_units if s in u][0]) for s in boxes)
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values: dict) -> dict:
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # GENERAL SOLUTION:
    # Iterate over each box in the grid and check for naked twins by
    # iterating over its peers and determining if it is a column peer or
    # a row peer.
    #
    # For each box, two twins may exist. This algorithm only finds one of them
    # per box, knowing that the other naked twin will be found when iterating
    # over that second box. In other words, all instances of naked twins will
    # be found.

    for box, partial_sols in values.items():
        if len(partial_sols) == 2:
            box_row, box_col = box

            for peer_box in peers[box]:
                peer_sols = values[peer_box]

                if len(peer_sols) == 2 and all([sol in partial_sols for sol in peer_sols]):
                    # Solutions for peer_box are matching.
                    peer_box_row, peer_box_col = peer_box

                    if (peer_box_col == box_col) or (peer_box_row == box_row):
                        # Peer box needs to share column or row to be naked twin.
                        twin = peer_box
                        is_column_twin = peer_box_col == box_col
                        twin_in_square_peers = twin in square_peers[box]
                        break

            else:
                # This box has no naked twin.
                continue

            # Remove the naked twin solutions from its peers.
            for peer_box in peers[box]:
                peer_box_row, peer_box_col = peer_box

                if peer_box == twin:
                    continue

                elif ((is_column_twin and peer_box_col == box_col) or
                    (not is_column_twin and peer_box_row == box_row)):
                    # If peer is in the same row or column as box
                    # then we need to process it.
                    pass

                elif twin_in_square_peers and peer_box in square_peers[box]:
                    # If the naked twin is inside the 3x3 square of peers and
                    # this peer is too, then we need to process it.
                    pass

                else:
                    # None of these conditions apply, so continue with the next
                    # peer box.
                    continue

                for digit in partial_sols:
                    new_value = values[peer_box].replace(digit, '')
                    assign_value(values, peer_box, new_value)

    return values


def grid_values(grid):
    """
    NOTE: Code extracted from Udacity's Sudoku project lessons.

    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))

def display(values):
    """
    NOTE: Code extracted from Udacity's Sudoku project lessons.

    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """
    NOTE: Code extracted from Udacity's Sudoku project lessons.

    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    NOTE: Code extracted from Udacity's Sudoku project lessons.

    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values

def reduce_puzzle(values):
    """
    NOTE: Code extracted from Udacity's Sudoku project lessons.

    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    """
    NOTE: Code extracted from Udacity's Sudoku project lessons.

    Using depth-first search and propagation, try all possible values.
    """
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes):
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    global unitlist
    global units
    global peers

    # update the units to include the two diagonals
    unitlist = row_units + column_units + square_units + diagonal_units
    units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
    peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

    # run algorithm as usual
    values = grid_values(grid)
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')

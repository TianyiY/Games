rows='ABCDEFGHI'
cols='123456789'

def cross(rows, cols):
    return [i+j for i in rows for j in cols]

boxes=cross(rows, cols)
#print boxes

row_units=[cross(r, cols) for r in rows]
#print row_units

col_units=[cross(rows, c) for c in cols]
#print col_units

sqr_units=[cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
#print sqr_units

unitlist=row_units+col_units+sqr_units

units=dict((s, [u for u in unitlist if s in u]) for s in boxes)
#print units

peers=dict((s, set(sum(units[s], []))-set([s])) for s in boxes)
#print peers


def display(values):
    # display the values as a 2-D grid
    # input in dict form
    width=1+max(len(values[s]) for s in boxes)
    line='+'.join(['-'*(width*3)]*3)
    for r in rows:
        print (''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print (line)
    return



def grid_values(grid):
    # input in string form, 81 character long
    # Sudoku grid in dict form: Keys=Box labels; Values=value in corresponding box
    values=[]
    all_num='123456789'
    for n in grid:
        if n=='.':
            values.append(all_num)
        elif n in all_num:
            values.append(n)

    assert len(grid)==81
    # return dict(zip(boxes, grid))
    return dict(zip(boxes, values))

# display(grid_values('..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'))



def eliminate(values):
    """Eliminate values from peers of each box with a single value.

        Go through all the boxes, and whenever there is a box with a single value,
        eliminate this value from the set of values of all its peers.

        Args:
            values: Sudoku in dictionary form.
        Returns:
            Resulting Sudoku in dictionary form after eliminating values.
        """
    existed_values=[box for box in values.keys() if len(values[box])==1]
    for box in existed_values:
        digit=values[box]
        for peer in peers[box]:
            values[peer]=values[peer].replace(digit, '')
    return values


def only_choice(values):
    """Finalize all values that are the only choice for a unit.

        Go through all the units, and whenever there is a unit with a value
        that only fits in one box, assign the value to this box.

        Input: Sudoku in dictionary form.
        Output: Resulting Sudoku in dictionary form after filling in only choices.
        """
    for unit in unitlist:
        for digit in '123456789':
            # if a box contain a number that its peers do not have, the set the number to this box
            only_place=[box for box in unit if digit in values[box]]
            if len(only_place)==1:
                values[only_place[0]]=digit
    return values


def count_healthy_crop(area):
    """
    Count the number of healthy crops in a given 2D area,
    where healthy crop represented by int 1. 
    and validates that `area` is a 2D list of integers, 
    where each inner list represents a row of the area and each 
    element represents a crop status as int.

    Parameters
    ----------------
    area : list of list of int
        A 2D grid representing crops, cell is an integer:
        0 = empty plot, 1 = healthy crop, 2 = diseased crop

    Returns
    ----------------
    int
        The total number of healthy crops

    Raises
    ----------------
    TypeError
        If `area` is not a list of lists of integers.
    
    Examples
    --------
    field = [[0, 1, 1],[1, 0, 0],[0, 1, 0]]
    count_healthy_crop(field)
    4
    """
    if not isinstance(area, list):
        raise TypeError('Area should be a 2D list of integers')
    
    count = 0
    
    for row in area:
        if not isinstance(row, list):
            raise TypeError('Each row in area should be a list')
        for cell in row:
            if not isinstance(cell, int):
                raise TypeError('All elements in area must be integers')
            if cell == 1:
                count += 1

    return count

'''

assert count_healthy_crop([[1, 0, 2], [1, 1, 0]]) == 3
assert count_healthy_crop([[0, 0], [2, 2]]) == 0
assert count_healthy_crop([]) == 0
assert count_healthy_crop([[]]) == 0

try:
    count_healthy_crop("not a list")
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-list input"

try:
    count_healthy_crop([1, 2, 3])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-list rows"

try:
    count_healthy_crop([[1, 2], ["a", 1]])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-integer cell"

try:
    count_healthy_crop([[1, 2], [None, 0]])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-integer cell"
'''


def contaminated(area):
    """
    Identify crops that will be contaminated in the next step.

    The function scans a 2D grid (`area`) where 0 = empty plot, 1 = healthy crop, 2 = diseased crop

    It checks for infected crops and determines 
    which neighboring (up, down, left, and right) healthy crops will become infected
    in the next step.

    Parameters
    ----------
    area : list of list of int
        A 2D grid representing crops, cell is an integer:
        0 = empty plot, 1 = healthy crop, 2 = diseased crop

    Returns
    -------
    set of tuple of int
        A set of coordinates `(row, col)` where healthy crops will
        be contaminated in the next step. If no contamination - an empty set is returned.

    Raises
    ------
    TypeError
        If `area` is not a list of lists of integers.
    ValueError
        If rows in `area` do not all have the same length.

    Examples
    --------
    field = [[2, 1, 0],[1, 1, 1],[0, 1, 2]]
    contaminated(field)
    {(0, 1), (1, 0), (1, 2), (2, 1)}
    """
    if not isinstance(area, list):
        raise TypeError('Area should be a 2D list of integers')
    if not all(isinstance(row, list) for row in area):
        raise TypeError('Each row in area should be a list')
    to_infect = set()
    if not area:
        return to_infect

    row_length = len(area[0])
    for row in area:
        if len(row) != row_length:
            raise ValueError('All rows in area must have the same length')
        if not all(isinstance(cell, int) for cell in row):
            raise TypeError('All elements in area must be integers')

    
    for r, row in enumerate(area):
        
        for c, cell in enumerate(row):
            if not isinstance(cell, int):
                raise TypeError('All elements in area must be integers')
            if cell == 2:
                directional_offset = [(-1,0), (1,0), (0,-1), (0,1)] # 4 directions a disease can spread
                for x, y in directional_offset:
                    neighbor_row, neighbor_column = r + x, c + y
                    if (
                        0 <= neighbor_row < len(area) and 
                        0 <= neighbor_column < len(row) and
                        area[neighbor_row][neighbor_column] == 1
                        ):
                        to_infect.add((neighbor_row, neighbor_column))
                        
    return to_infect              
                        
'''
area = [[1, 2, 1],[0, 1, 0],[1, 0, 2]]
expected = {(0, 0), (0, 2), (1, 1)}
result = contaminated(area)
assert result == expected, "Should return correct infected neighbors"

# Should not mutate original area
import copy
original = [[1, 2],[1, 1]]
area_copy = copy.deepcopy(original)
contaminated(area_copy)
assert area_copy == original, "Function must not change the original area"

assert contaminated([]) == set(), "Empty grid should return empty set"

try:
    contaminated("invalid")
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-list area"

try:
    contaminated([[1, 2], "bad row"])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-list row"

try:
    contaminated([[1, "bad"], [2, 1]])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-integer cell"

try:
    contaminated([[1, 2], [1]])
except ValueError:
    pass
else:
    assert False, "Expected ValueError for uneven row lengths"
'''

def update_field_health(area, to_infect): 
    """
    Update the field by infecting healthy crops.

    takes a 2D grid (`area`) representing crop health and 
    a set of coordinates (`to_infect`) where healthy crops should become 
    infected. If a coordinate points to a healthy crop, updates to infected. 
    returns the number of crops updated.

    Parameters
    ----------
    area : list of list of int
        A 2D grid representing the field, where:
        0 = empty, 1 = healthy crop, 2 = infected crop
    to_infect : set of tuple of int
        A set of coordinates `(row, col)` indicating which crops 
        should be infected.

    Returns
    -------
    int
        The number of crops successfully updated from healthy (1) to infected (2).

    Raises
    ------
    TypeError
        If `to_infect` is not a set, or if it contains values that are not 
        2-element tuples of integers.
    ValueError
        If any coordinate in `to_infect` is out of the field bounds.

    Examples
    --------
    field = [[1, 1, 0],[2, 1, 1],[0, 1, 2]]
    updates = update_field_health(field, {(0, 0), (1, 1), (2, 1)})
    [[2, 1, 0],[2, 2, 1],[0, 2, 2]]
    """
    # type checks
    if not isinstance(to_infect, set):
        raise TypeError('to_infect should be a set')        

    rows = len(area)
    cols = len(area[0]) if area else 0
    updated = 0

    for coord in to_infect:
        if not isinstance(coord, tuple):
            raise TypeError('to_infect should contain only tuples')
        if len(coord) != 2 or not all(isinstance(i, int) for i in coord):
            raise TypeError('to_infect should contain only tuples of integers')
        # bound check
        x, y = coord
        if not (0 <= x < rows and 0 <= y < cols):
            raise ValueError('Coordinate in to_infect is out of bounds')

        if area[x][y] == 1:
            area[x][y] = 2
            updated += 1

    return updated

'''
area1 = [[1, 1],[0, 2]]
infect1 = {(0, 0), (0, 1)}
updated = update_field_health(area1, infect1)
assert updated == 2, "Should update two healthy crops"
assert area1 == [[2, 2],[0, 2]], "Area should reflect updated crops"
area2 = [[2, 1],[0, 0]]
infect2 = {(0, 0), (0, 1)}  # only (0,1) is healthy
updated = update_field_health(area2, infect2)
assert updated == 1, "Should update one healthy crop"
assert area2 == [[2, 2],[0, 0]]
try:
    update_field_health([[1, 1]], [(0, 0)])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-set input"
try:
    update_field_health([[1, 1]], {0})
except TypeError:
    pass
else:
    assert False, "Expected TypeError for set containing non-tuples"
try:
    update_field_health([[1, 1]], {("0", 1)})
except TypeError:
    pass
else:
    assert False, "Expected TypeError for tuples with non-integer elements"

try:
    update_field_health([[1, 1]], {(2, 0)})
except ValueError:
    pass
else:
    assert False, "Expected ValueError for out-of-bounds coordinate"
'''


'''def print_grid(g):
    for row in g:
        print(row)
    print()'''
    
    
def simulate_crops(area):
    """
    Simulate the spread of crop infection in a 2D grid until all healthy crops are infected.

    The grid (`area`) uses the following encoding:
        0 = empty, 1 = healthy crop, 2 = infected crop

    The infection spreads in hours. During each hour:
      currently infected crops contaminate their immediate healthy neighbors in the four cardinal directions:
        up, down, left, right.
      grid is updated in-place

    Behavior:
      grid is empty, returns 0.
      no healthy crops at the start, returns 0.
      there are healthy crops but no infection sources returns -1
      Otherwise, simulates hour by hour until all healthy crops are
        infected, returning the total number of hours required.

    Parameters
    ----------
    area : list of list of int
        A rectangular 2D grid representing crop states, where:
        0 = empty cell, 1 = healthy crop, 2 = infected crop

    Returns
    -------
    int
        0 - grid is empty or no healthy crops.
        -1 - healthy crops exist but no infection.
        Otherwise, the number of hours needed to infect all healthy crops.

    Raises
    ------
    TypeError
        If `area` is not a 2D list of integers.

    Side Effects
    ------------
    Mutates `area` in place by progressively converting healthy crops (1) into infected crops (2).

    Examples
    --------
    field = [[1, 1, 0],[2, 1, 1],[0, 1, 2]]
    simulate_crops(field)
    2
    """
    
    if not isinstance(area, list) or not all(isinstance(row, list) for row in area):
        raise TypeError("area must be a 2D list of ints")
    for row in area:
        if not all(isinstance(cell, int) for cell in row):
            raise TypeError("area must be a 2D list of ints") 

    if not area:
        return 0
    if count_healthy_crop(area) == 0:
        return 0
    if not contaminated(area):
            return -1
        
# Otherwise it returns the number of hours taken to infect all healthy crops.
        
    hours = 0
    while count_healthy_crop(area) > 0:
        to_infect = contaminated(area)
        
        '''print(f"Hour {hours}: Infecting -> {to_infect}")
        print_grid(area)''' # statement for debugging
            
        if not to_infect:      # no progress anymore
            return -1
        update_field_health(area, to_infect)
        hours += 1
    return hours
            
            
'''   
assert simulate_crops([]) == 0, "Empty grid should return 0"
assert simulate_crops([[2, 0], [0, 2]]) == 0, "No healthy crops should return 0"
assert simulate_crops([[1, 1], [0, 1]]) == -1, "Healthy with no diseased should return -1"
area1 = [[2, 1, 1],[1, 1, 0],[0, 1, 1]]
assert simulate_crops(area1) == 4, "Should take 4 hours to infect all"
area2 = [[2, 0, 1]]
assert simulate_crops(area2) == -1, "Separated healthy should return -1"
area3 = [[2, 1, 0],[1, 1, 1]]
assert simulate_crops(area3) == 3, "Should take 3 hours to infect all"
area4 = [[2, 1],[0, 1]]
assert simulate_crops(area4) == 2, "Should take 2 hours to infect all"
area = [[2]]
assert simulate_crops(area) == 0, "Only infected cell – should return 0"
area = [[1, 1], [1, 1]]
assert simulate_crops(area) == -1, "All healthy, no infected – should return -1"
area = [[2, 1, 1, 1],[0, 0, 0, 1],[1, 1, 1, 1]]
assert simulate_crops(area) == 8, "Should take 8 hours in L-shaped spread"
area = [[0, 0],[0, 0]]
assert simulate_crops(area) == 0, "Only empty – should return 0"
area = [[2, 1, 1],[1, 1, 1]]
assert simulate_crops(area) == 3, "Should infect all in 3 hours"
area = [[2, 2],[0, 2]]
assert simulate_crops(area) == 0, "All infected already – should return 0"


try:
    simulate_crops("not a grid")
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-list area"

try:
    simulate_crops([1, 2, 3])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-list rows"

try:
    simulate_crops([[1, "x"], [2, 0]])
except TypeError:
    pass
else:
    assert False, "Expected TypeError for non-integer cell"
'''
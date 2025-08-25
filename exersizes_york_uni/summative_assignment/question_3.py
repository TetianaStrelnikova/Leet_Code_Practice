class FamilyTree:
    """Family tree with people and their relationships.

    The tree stores people in a private mapping from string IDs to a record
    containing:
      - ``name`` (str): Person's display name.
      - ``birth_year`` (Optional[int]): Four-digit birth year if known.
      - ``parents`` (Set[str]): Up to two parent IDs.
      - ``children`` (Set[str]): Child IDs.
      - ``partners`` (Set[str]): Partner IDs (no constraints on count).

    Notes:
        - Person IDs are generated incrementally as strings: "1", "2", ...
        - The data structure allows multiple partners and any number of children.
        - A child can have at most two parents. Attempting to add more raises ``ValueError``.

    Examples:
    ft = FamilyTree()
    a = ft.add_person("Alex", 1980)
    b = ft.add_person("Blake", 1982)
    c = ft.add_person("Casey", 2012)
    ft.add_partner(a, b)
    ft.add_child([a, b], c)
    ft.find_by_name("casey")
    ['3']
    sorted(ft.get_ancestors(c)) == sorted([a, b])
    True
    """
    
    def __init__(self):
        """Initialize an empty family tree."""
        self._people = {}
        self._next_id = 1
    
    # Adding and Finding People
    def add_person(self, name, birth_year=None):
        """Add a new person to the tree.

        Args:
            name: Person's name. Case is preserved.
            birth_year: Optional four-digit year of birth.

        Returns:
            The newly created person's unique ID (string).

        Raises:
            ValueError: If ``name`` is empty or not a string.
        """
        if not name or not isinstance(name, str):
            raise ValueError('The name should not be empty')
        new_id = str(self._next_id)
        self._people[new_id] = {}
        self._people[new_id]['name'] = name
        self._people[new_id]['birth_year'] = birth_year
        self._people[new_id]['parents'] = set()
        self._people[new_id]['children'] = set()
        self._people[new_id]['partners'] = set()
        self._next_id += 1
        return new_id
    
    def find_by_name(self, name):
        """Find all people whose name matches ``name`` case-insensitively.

        Args:
            name: Name to search for (case-insensitive exact match).

        Returns:
            A list of person IDs (strings) whose ``name`` equals ``name``
            ignoring case. If no matches are found, returns an empty list.
        """
        result = []
        for person_id in self._people:
            if self._people[person_id]['name'].lower() == name.lower():
                result.append(person_id)
        return result  
      
    # Relationships
    def add_child(self, parent_ids, child_id):
        """Record a parent-child relationship.

        Adds each parent in ``parent_ids`` as a parent of ``child_id`` and
        adds ``child_id`` to each parent's set of children.

        Args:
            parent_ids: Iterable of parent IDs (strings). Can be 1 or 2 items.
            child_id: ID (string) of the child.

        Raises:
            TypeError: If ``parent_ids`` is not an iterable of strings or is a string itself.
            KeyError: If ``child_id`` or any parent ID does not exist in the tree.
            ValueError: If adding these parents would cause the child to have more than two parents.
        """
        if (
            not hasattr(parent_ids, '__iter__') 
            or isinstance(parent_ids, str) 
            or not all(isinstance(p, str) for p in parent_ids)
            ):
            raise TypeError("parent_ids must be an iterable of string IDs")
        if child_id not in self._people:
            raise KeyError('child_id is not found')
        if not all(parent_id in self._people for parent_id in parent_ids):
            raise KeyError ('ID in parent_ids is not found')
        if len(self._people[child_id]['parents'] | set(parent_ids)) > 2:
            raise ValueError("Child cannot have more than two parents")
        for parent_id in parent_ids:
            self._people[child_id]['parents'].add(parent_id)
            self._people[parent_id]['children'].add(child_id)
            
    def add_partner(self, id1, id2):
        """Add a bidirectional partner relationship between two people.

        Args:
            id1: First person's ID.
            id2: Second person's ID.

        Raises:
            KeyError: If either ID is not found in the tree.
        """
        if (
            id1 not in self._people 
            or id2 not in self._people
            ):
            raise KeyError('Partner id is not found')
        self._people[id1]['partners'].add(id2)
        self._people[id2]['partners'].add(id1)
        
    #Ancestors
    def get_ancestors(self, person_id, visited=None, ancestors=None):
        """Return all (transitive) ancestors of a person.

        This performs a depth-first traversal up the parent links, collecting
        unique ancestor IDs. Cycles are prevented with the ``visited`` set.

        Args:
            person_id: The starting person's ID.
            visited: (Internal) Set of visited IDs used to avoid cycles.
            ancestors: (Internal) Accumulator set for results.

        Returns:
            A set of person IDs representing all known ancestors of ``person_id``.

        Raises:
            KeyError: If ``person_id`` does not exist in the tree.
        """
        if person_id not in self._people:
            raise KeyError( 'Person_id is not found') 
        if visited == None:
            visited = set()
        if ancestors == None:
            ancestors = set()
        for parent in self._people[person_id]['parents']:
            ancestors.add(parent)     
            if parent not in visited:
                visited.add(parent)
                self.get_ancestors(parent, visited, ancestors)
        return ancestors 




'''
# (i) Constructor
ft = FamilyTree()
assert isinstance(ft._people, dict), "Constructor must create a _people dict"
assert ft._people == {}, "_people should be empty on initialization"
assert hasattr(ft, '_next_id'), "Constructor should initialize _next_id"
assert ft._next_id == 1, "_next_id should start at 1"

# (ii) add_person: valid cases
person_id1 = ft.add_person("Alice")
assert isinstance(person_id1, str), "add_person must return string ID"
assert person_id1 in ft._people, "Returned ID must exist in _people"
rec1 = ft._people[person_id1]
assert rec1['name'] == "Alice", "Record must store correct name"
assert rec1['birth_year'] is None, "Default birth_year should be None"
assert rec1['parents'] == set(), "Parents must start empty"
assert rec1['children'] == set(), "Children must start empty"
assert rec1['partners'] == set(), "Partners must start empty"
assert ft._next_id == int(person_id1) + 1, "_next_id must increment"

person_id2 = ft.add_person("Bob", birth_year=1980)
assert int(person_id2) == int(person_id1) + 1, "IDs should be sequential"
rec2 = ft._people[person_id2]
assert rec2['name'] == "Bob", "Name correctly stored"
assert rec2['birth_year'] == 1980, "Birth year correctly stored"

# add_person: invalid cases
for invalid in ["", 12345]:
    try:
        ft.add_person(invalid)
    except ValueError:
        pass
    else:
        assert False, "add_person should ValueError on invalid name"

# (ii) find_by_name
ft2 = FamilyTree()
idA1 = ft2.add_person("Alice")
idA2 = ft2.add_person("alice")  # case variation
idB = ft2.add_person("Bob")
matches = ft2.find_by_name("ALICE")
assert set(matches) == {idA1, idA2}, "find_by_name must be case-insensitive"
assert ft2.find_by_name("Charlie") == [], "No match should return []"

# (iii) add_child
ft3 = FamilyTree()
p1 = ft3.add_person("Anna")
p2 = ft3.add_person("Ben")
c = ft3.add_person("Chris")

ft3.add_child([p1, p2], c)
assert ft3._people[c]['parents'] == {p1, p2}, "Child must record both parents"
assert c in ft3._people[p1]['children'], "Parent1 must list child"
assert c in ft3._people[p2]['children'], "Parent2 must list child"

# invalid add_child cases
p3 = ft3.add_person("Donna")
try:
    ft3.add_child([p3], c)
except ValueError:
    pass
else:
    assert False, "Adding third parent should ValueError"

try:
    ft3.add_child("not_iterable", c)
except TypeError:
    pass
else:
    assert False, "Non-iterable parent_ids should TypeError"

try:
    ft3.add_child([p1], "999")
except KeyError:
    pass
else:
    assert False, "Nonexistent child_id should KeyError"

try:
    ft3.add_child(["999"], c)
except KeyError:
    pass
else:
    assert False, "Nonexistent parent_id should KeyError"

# (iii) add_partner
ft4 = FamilyTree()
a = ft4.add_person("Tom")
b = ft4.add_person("Jerry")
ft4.add_partner(a, b)
assert b in ft4._people[a]['partners'], "Partner should be added both ways"
assert a in ft4._people[b]['partners'], "Partner should be added both ways"
try:
    ft4.add_partner(a, "999")
except KeyError:
    pass
else:
    assert False, "Invalid ID should raise KeyError"

# (iv) get_ancestors
ft5 = FamilyTree()
gp = ft5.add_person("Grandpa")
par = ft5.add_person("Parent")
ch = ft5.add_person("Child")
ft5.add_child([gp], par)
ft5.add_child([par], ch)
anc1 = ft5.get_ancestors(ch)
assert anc1 == {par, gp}, "Should return parent and grandparent"
assert ft5.get_ancestors(gp) == set(), "Root ancestor should have no ancestors"
try:
    ft5.get_ancestors("999")
except KeyError:
    pass
else:
    assert False, "Invalid person_id should raise KeyError"

# All tests passed if no assertion errors
print("All FamilyTree tests passed! ")
'''
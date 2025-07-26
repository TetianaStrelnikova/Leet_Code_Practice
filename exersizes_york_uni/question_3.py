class PouleSheet:
    
    """Represents a fencing poule sheet for managing bouts and determining rankings."""

    def __init__(self, number, size):
        
        """Initializes a PouleSheet instance.

        Args:
            number (int): The poule number.
            size (int): The number of competitors in the poule.

        Attributes:
            _poule_number (int): The identifier number of the poule.
            _poule_size (int): Total number of competitors.
            _competitors (List[Optional[str]]): List of competitor names (None if slot is empty).
            _results (List[List[Optional[int]]]): 2D list of scores; 
                _results[i][j] is the hits scored by fencer i against fencer j.
        """
        self._poule_number = number  #int 
        self._poule_size = size #int
        self._competitors = [None for _ in range(size)] #list of str
        self._results = [[None for _ in range(size)]for _ in range(size)] #2D list of int
        
    def add_competitor(self, name):
        
        """Adds a competitor to the next available slot.

        Args:
            name (str): The name of the competitor to add.

        Returns:
            bool: True if the competitor was added successfully,
                  False if the name is None, already present, or the poule is full.
        """
        
        if name is None or name in self._competitors or not isinstance(name, str):
            return False
        for i in range(self._poule_size):
            if self._competitors[i] is None:
                self._competitors[i] = name
                return True
        return False
    
    def record_bout(self, fencer1, fencer2, h1, h2):
        
        """Records the result of a bout between two fencers.

        Args:
            fencer1 (int): Index of the first fencer.
            fencer2 (int): Index of the second fencer.
            h1 (int): Hits scored by fencer1.
            h2 (int): Hits scored by fencer2.

        Raises:
            ValueError: If inputs are not integers or hits are negative.
            IndexError: If any fencer index is out of bounds.
        """

        if not all(isinstance(x , int) for x in (fencer1, fencer2, h1, h2)):
            raise ValueError("Fencer indices and hits must be integers")
        if not (0 <= fencer1 < self._poule_size) or not (0 <= fencer2 < self._poule_size):
            raise IndexError("Fencer index out of range")
        if h1 < 0 or h2 < 0:
            raise ValueError("Hits must be non-negative")
        
        self._results[fencer1][fencer2] = h1
        self._results[fencer2][fencer1] = h2
        
    def get_winners(self):
        
        """Determines the winner(s) of the poule based on recorded bouts.

        Ranking is computed using:
        1. Number of victories
        2. Difference between hits scored and received (HS - HR)
        3. Total hits scored (HS)

        Returns:
            Optional[Set[str]]: A set of winner names ranked first, 
                                or None if the poule is not fully completed.
        """
        
        stat =[]
        for i, row in enumerate(self._results):
            v, hs, hr = 0, 0, 0
            
            for j, hits in enumerate(row):
                if i == j:
                    continue  # skip diagonal
                if hits is None:
                    return None
                hs += hits
                hr += self._results[j][i]
                v += int(hits == 5 and self._results[j][i] < 5)
            stat.append({'name': self._competitors[i], 'v': v, 'hs': hs, 'hr': hr, 'diff': hs - hr})
        stat.sort(key = lambda x: (-x['v'], -x['diff'], -x['hs']))    
        first = stat[0]
        winners = set(f['name'] for f in stat if (f['v'], f['diff'], f['hs']) == (first['v'], first['diff'], first['hs']))           
        return winners if winners else None
from backend.position import Position
import numpy as np
SEED = 42

class Grid:
    def __init__(self):
        self.rows = None
        self.columns = None
        self.A = None
        self.positions = None
        self.rng = None

        self.set_seed()


    """
    Set the grid positions and the artifact location

    Attributes
    ----------
    rows : integer
         Number of rows
    columns : integer
            Number of columns
    positions : array of Position instances
              Escavation site positions
    """
    def set_grid(self, rows, columns):
        self.rows = int(rows)
        self.columns = int(columns)
        self.positions = np.empty((self.rows, self.columns), dtype=object)
        
        for i in range(self.rows):
            for j in range(self.columns):
                self.positions[i, j] = Position(i, j)

        self.A = self.get_artifact()

    """
    Calculate the artifact coordinates

    Returns
    -------
        Position
            The aritifact position
    """
    def get_artifact(self):

        x = self.rng.integers(self.rows)
        y = self.rng.integers(self.columns)
        return Position(x,y)


    """
    Set the randomizer seed

    Parameters
    ----------
        iseed : int
              randomizer seed (optional)

    Attributes
    ---------
        rng
           Random function
    """
    def set_seed(self, iseed=None):
        if iseed == None:
            iseed = SEED
        try:
            self.rng = np.random.default_rng(iseed)
        except (ValueError, TypeError):
            self.rng = np.random.default_rng(SEED)
            
    
    """
    Set initial probabilities

    Attributes
    ----------
        p
           Probabilities set for each position
    """
    def set_initial_probabilities(self):
        
        p = 1.0 / float(self.rows * self.columns)
        
        for i in range(self.rows):
            for j in range(self.columns):
                self.positions[i,j].set_probability(p)


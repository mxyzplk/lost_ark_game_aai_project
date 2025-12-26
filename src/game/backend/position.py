class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.p = None
        self.gpr = None
        self.mag = None
        self.vis = None

    """
    Return the Manhattan Distance

    Parameters
    ----------
        other
             Another position

    Returns
    -------
        manhattan_distance : integer
                           Manhatan Distance to the artifact
    """
    def manhattan_distance(self, other):
        return abs(self.x - other.x) + abs(self.y - other.y)
    
    """
    Set probability

    Parameters
    ----------
        p : float
          Position probability

    Attributes
    ----------
        p : float
          Position probability

    Raises
    ------
    ValueError
         If the probability is above one or negative
    """
    def set_probability(self, p):
        if (p > 1.0 or p < 0.0):
            raise ValueError("Probability out of the boundaries")
        else:
            self.p = p

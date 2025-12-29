class Position:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.p = None
        self.p0= None
        self.status = {'GPR': "Not Used",'MAG': "Not Used",'VIS': "Not Used"}

    def manhattan_distance(self, other):
        """
        Return the Manhattan Distance
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


    def set_initial_state(self, p):
        """
        Set initial state probability
        """
        if (p > 1.0 or p < 0.0):
            raise ValueError("Probability out of the boundaries")
        else:
            self.p0 = p
            self.p = p


    def set_probability(self, p):    
        """
        Set probability
        """
        if (p > 1.0 or p < 0.0):
            raise ValueError("Probability out of the boundaries")
        else:
            self.p = p

    def set_status(self, sensor, status):
        """
        Set the sensor status        
        """
        self.status[sensor] = status

    
    def get_probability(self):
        """
        Return probability
        """
        return self.p

from backend.position import Position
from backend.cpts import CPT
import numpy as np
SEED = 42

class Grid:
    def __init__(self):
        self.rows = None
        self.columns = None
        self.A = None
        self.positions = None
        self.rng = None
        self.gpr = None
        self.mag = None
        self.vis = None

        self.set_seed()
        self.set_cpts()


    def set_grid(self, rows, columns):
        """
        Set the grid positions, the artifact location and the initial probabilities
        """
        self.rows = int(rows)
        self.columns = int(columns)
        self.positions = np.empty((self.rows, self.columns), dtype=object)
        
        for i in range(self.rows):
            for j in range(self.columns):
                self.positions[i, j] = Position(i, j)

        self.A = self.get_artifact()
        self.set_initial_probabilities()


    def get_artifact(self) -> Position:
        """
        Calculate the artifact coordinates
        """
        x = self.rng.integers(self.rows)
        y = self.rng.integers(self.columns)
        return Position(x,y)


    def set_seed(self, iseed=None):
        """
        Set the randomizer seed
        """
        if iseed == None:
            iseed = SEED
        try:
            self.rng = np.random.default_rng(iseed)
        except (ValueError, TypeError):
            self.rng = np.random.default_rng(SEED)
            
    
    def set_initial_probabilities(self):
        """
        Set initial probabilities
        """        
        p = 1.0 / float(self.rows * self.columns)
        
        for i in range(self.rows):
            for j in range(self.columns):
                self.positions[i,j].set_initial_state(p)

    def set_cpts(self):
        """
        Set the sensors
        """
        self.gpr = CPT("GPR")
        self.mag = CPT("MAG")
        self.vis = CPT("VIS")

        self.sensors = {"GPR": self.gpr, "MAG": self.mag, "VIS": self.vis}


    def eval_sensor(self, position: Position, target: Position, sensor_type: str) -> str:
        """
        Attributes the sensor status to the position. Return the sensor reading
        """
        reading = self.sensors[sensor_type].get_reading(position.manhattan_distance(target))
        position.set_status(sensor_type, reading)

        return reading
import numpy as np
from backend.grid import Grid
from backend.observations import Observations

class BayesianInference:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.total_cells = self.grid.rows * self.grid.columns
        self.prior = np.zeros((self.grid.rows, self.grid.columns))
        self.set_prior()
    
  
    def set_prior(self):
        """
        Stores the initial prior
        """
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                self.prior[i,j] = self.grid.positions[i,j].p0
        
    def compute_posterior(self, observations: Observations) -> np.ndarray:
        """
        Computes P(A | readings)
        """
        posterior = self.prior.copy()
        
        for (row, col), sensor_readings in observations.get_all_observations().items():
            for sensor_type, reading in sensor_readings.items():
                likelihood = self._compute_likelihood(row, col, sensor_type, reading)
                posterior *= likelihood
        
        total = np.sum(posterior)
        posterior /= total

            
        return posterior
    
    def _compute_likelihood(self, obs_row: int, obs_col: int, 
                           sensor_type: str, reading: str) -> np.ndarray:
        """
        Computes P(readings | A=(i,j)) for all cells (i,j)
        """
        likelihood = np.ones((self.grid.rows, self.grid.columns))
        
        sensor = self.grid.sensors[sensor_type]
        
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                distance = abs(self.grid.positions[i,j].x - obs_row) + abs(self.grid.positions[i,j].y - obs_col)
                prob = sensor.get_conditional_probability(distance, reading)
                likelihood[i, j] = prob
                
        return likelihood
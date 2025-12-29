import numpy as np
from typing import Dict
from backend.grid import Grid
from backend.observations import Observations

class BayesianInference:
    def __init__(self, grid: Grid):
        self.grid = grid
        self.rows = grid.rows
        self.cols = grid.columns
        self.total_cells = self.rows * self.cols
        
    def compute_posterior(self, observations: Observations) -> np.ndarray:
        """
        Computa P(A | todas as observações)
        usando o teorema de Bayes
        """
        # Prior uniforme
        posterior = np.ones((self.rows, self.cols)) / self.total_cells
        
        # Para cada observação, multiplica pelo likelihood
        for (row, col), sensor_readings in observations.get_all_observations().items():
            for sensor_type, reading in sensor_readings.items():
                likelihood = self._compute_likelihood(row, col, sensor_type, reading)
                posterior *= likelihood
        
        # Normaliza
        total = np.sum(posterior)
        if total > 0:
            posterior /= total
        else:
            # Caso extremo: volta para uniforme
            posterior = np.ones((self.rows, self.cols)) / self.total_cells
            
        return posterior
    
    def _compute_likelihood(self, obs_row: int, obs_col: int, 
                           sensor_type: str, reading: str) -> np.ndarray:
        """
        Computa P(leitura | A=(i,j)) para todas as células (i,j)
        """
        likelihood = np.ones((self.rows, self.cols))
        
        # Obtém sensor
        sensor = self.grid.sensors[sensor_type]
        
        # Calcula likelihood para cada célula
        for i in range(self.rows):
            for j in range(self.cols):
                # Distância entre célula de observação e célula hipotética do artefato
                distance = abs(i - obs_row) + abs(j - obs_col)
                
                # Probabilidade condicional
                prob = sensor.get_conditional_probability(distance, reading)
                likelihood[i, j] = prob
                
        return likelihood
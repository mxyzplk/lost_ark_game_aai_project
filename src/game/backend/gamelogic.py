from backend.grid import Grid
from backend.observations import Observations
from backend.bayesian import BayesianInference
import numpy as np

class GameLogic:
    def __init__(self, rows: int, columns: int, seed: int, budget: int):
        self.grid = Grid()
        self.grid.set_grid(rows, columns)
        self.grid.set_seed(seed)
        self.budget = budget
        self.observations = Observations()
        self.bayesian = BayesianInference(self.grid)
        self.game_over = False
        self.score = 0
        self.survey_history = []
        self.survey_count = 0

    def survey(self, row: int, col:int, sensor_type: str):
        if self.game_over:
            return "Game Over", False
        
        cost = self.grid.sensors[sensor_type].get_cost()
        if self.budget < cost:
            return "Insuficient Funds", False
        else:
            self.budget = self.budget - cost
        pos = self.grid.positions[row, col]
        reading = self.grid.eval_sensor(pos, self.grid.A, sensor_type)
        self.observations.add_observation(row, col, sensor_type, reading)
        self._update_probabilities()
        pos.set_status(sensor_type, reading)
        self.survey_count += 1
        return reading, True, cost
            
    def _update_probabilities(self):
        posterior = self.bayesian.compute_posterior(self.observations)
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                self.grid.positions[i, j].set_probability(posterior[i, j])
    
    def excavate(self, row: int, col: int) -> tuple[bool, int]:
        if self.game_over:
            return False, 0
        
        self.game_over = True
        if row == self.grid.A.x and col == self.grid.A.y:
            self.score = self.budget
            return True, self.score
        else:
            self.score = 0
            return False, 0
    
    def get_probability_grid(self) -> np.ndarray:
        grid = np.zeros((self.grid.rows, self.grid.columns))
        for i in range(self.grid.rows):
            for j in range(self.grid.columns):
                grid[i, j] = self.grid.positions[i, j].get_probability()
        return grid
    
    def get_heatmap_data(self) -> list[list[float]]:
        return self.get_probability_grid().tolist()
    
    def get_status(self) -> dict:
        return {
            'budget': self.budget,
            'score': self.score,
            'game_over': self.game_over,
            'artifact_location': (self.artifact.x, self.artifact.y),
            'grid_size': (self.grid.rows, self.grid.columns),
            'survey_count': self.survey_count
        }
    
    def get_cell_info(self, row: int, col: int) -> dict:
        """Retorna informações de uma célula para a UI"""
        pos = self.grid.positions[row, col]
        
        return {
            'P:': pos.get_probability(),
            'GPR:': pos.status['GPR'],
            'MAG:': pos.status['MAG'],
            'VIS:': pos.status['VIS']
        }
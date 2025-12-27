from backend.grid import Grid
from backend.observations import Observations
from backend.bayesian import BayesianNetwork

class GameLogic:
    def __init__(self, rows: int, columns: int, seed: int, budget: int):
        self.grid = Grid()
        self.grid.set_grid(rows, columns)
        self.budget = budget
        self.observations = Observations()
        self.bayesian = BayesianNetwork()
        self.game_over = False
        self.score = 0
        self.survey_history = []

        def survey(row: int, col:int, sensor_type: str):

            if self.game_over:
                return "Game Over", False
            
            cost = self.grid.sensors[sensor_type].get_cost()

            if self.budget < cost:
                return "Insuficient Funds", False
            else:
                self.budget = self.budget - cost

            pos = self.grid.positions[row, col]

            reading = self.grid.eval_sensor(pos, self.grid.A, sensor_type)

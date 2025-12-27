import yaml
from pathlib import Path
import numpy as np
from typing import Dict

class CPT:
    def __init__(self, ctype):
        self.type = None
        self.cost = None
        self.cpt = None

        self.read_config(ctype)


    def read_config(self, ctype):
        ifile = Path(__file__).parent.parent / "resources" / "probabilities.yaml"
        
        with open(ifile, 'r') as f:
            data = yaml.safe_load(f)

        self.type = ctype
        self.cost = data["costs"][ctype]
        self.cpt = data["cpts"][ctype]


    def get_distribution(self, distance: int) -> Dict[str, float]:
        """
        Return the CPT
        """
        if distance in self.cpt:
            return self.cpt[distance]
        elif "default" in self.cpt:
            return self.cpt["default"]
        else:
            numeric_keys = [k for k in self.cpt.keys() if isinstance(k, int)]
            if numeric_keys:
                last_key = max(numeric_keys)
                return self.cpt[last_key]
            else:
                raise ValueError(f"Nenhuma distribuição encontrada para distância {distance}")
            

    def get_reading(self, distance):
        """
        Roll a random number between 0 and 1.
        Return the sensor reading based on the CPT.
        """

        distribution = self.get_distribution(distance)
        
        readings = list(distribution.keys())
        probabilities = list(distribution.values())
        
        roll = np.random.choices(readings, weights=probabilities, k=1)[0]
        
        return roll


    def get_conditional_probability(self, distance: int, reading: str):
        """
        Return probability given reading
        """
        distribution = self.get_distribution(distance)

        return distribution.get(reading, 0.0)
    

    def get_cost(self):
        """
        Return sensor cost
        """
        return self.cost
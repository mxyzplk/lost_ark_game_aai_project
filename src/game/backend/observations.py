from typing import Dict, Tuple, Optional


class Observations:
    def __init__(self):
        """
        Store observations in a dictionary format:
        {(row, col): {'GPR': 'X | FALSE', 'MAG': 'X | FALSE', 'VIS': 'X | FALSE' }}
        """
        self.observations = {}
        
    def add_observation(self, row: int, col: int, 
                        sensor_type: str, reading: str):
        """Add a observation"""
        key = (row, col)
        
        if key not in self.observations:
            self.observations[key] = {}
            
        # Substitui leitura anterior do mesmo sensor (política do projeto)
        self.observations[key][sensor_type] = reading
        
    def get_observation(self, row: int, col: int, 
                       sensor_type: str) -> Optional[str]:
        """Obtém leitura mais recente de um sensor em uma célula"""
        key = (row, col)
        if key in self.observations:
            return self.observations[key].get(sensor_type)
        return None
    
    def get_all_observations(self) -> Dict:
        """Retorna todas as observações"""
        return self.observations.copy()
    
    def clear(self):
        """Limpa todas as observações"""
        self.observations.clear()
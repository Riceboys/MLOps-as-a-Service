from numpy import ndarray
from typing import Dict, List, Callable


class BaseTrigger:
    def __init__(self, trigger_func: Callable[..., bool], input_trigger=None) -> None:
        pass

    def check_for_new_data(self) -> bool:
        pass

    def etl(self) -> ndarray:
        pass

    def model_evaluation(self, model, feature_vectors: ndarray) -> Dict[str, float]:
        pass

    def train_model(self, feature_vectors: ndarray) -> None:
        pass
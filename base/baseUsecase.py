from abc import ABC, abstractmethod
from typing import Any


class BaseUseCase(ABC):

    def __init__(self, repo: Any):
        self.repo = repo

    def execute(self, *args, **kwargs):
        self.validate(*args, **kwargs)
        return self.perform(*args, **kwargs)

    def validate(self, *args, **kwargs):
        ...

    @abstractmethod
    def perform(self, *args, **kwargs):
        raise NotImplementedError("Метод perform должен быть переопределен")

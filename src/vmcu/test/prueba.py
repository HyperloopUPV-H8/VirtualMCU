from abc import ABC, abstractmethod

class Prueba(ABC):
    def __init__(self):
        self._x = True

class PruebaImp(Prueba):
    def getX(self):
        return self._x
    
prueba = PruebaImp()
print(prueba.getX())
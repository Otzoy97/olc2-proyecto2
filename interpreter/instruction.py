from abc import ABC, abstractmethod

class Instruction(ABC):
    #this is an abstract class
    @abstractmethod
    def firstRun(self, input1, input2, input3):
        #this is an abstract function
        print("Create 3D code")
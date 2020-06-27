from interpreter.instruction import Instruction

@Instruction.register
class Expression(Instruction):
    '''this is an abstract class'''

    def firstRun(self):
        print("aea")

if __name__ == "__main__":
    e = Expression()
    e.firstRun()
    #print(str(e))
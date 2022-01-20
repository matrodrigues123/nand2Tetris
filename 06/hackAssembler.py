import auxData
import re


class Parser:
    def __init__(self, textLine):
       self.assemblyLine = textLine.strip().replace(" ", "")
    
    def isLineValid(self):
        # ignore empty lines and commentaries
        if self.assemblyLine[:2] != '//' and len(self.assemblyLine) != 0:
            # throw away inline commentaries if existent
            splitComent = re.split('[//]', self.assemblyLine)
            self.assemblyLine = splitComent[0]
            return True
        return False

    def isLabel(self):
        if self.assemblyLine[0] == '(':
            self.assemblyLine = self.assemblyLine.replace('(', '')
            self.assemblyLine = self.assemblyLine.replace(')', '').strip()
            return True
        return False

    def isA(self):
        if self.assemblyLine[0] == '@':
            return True
        return False

    def handleCInstruction(self):
        self.splittedCInstruction = [None] * 3
        if '=' in self.assemblyLine:
            textSplit = re.split('[= ;]', self.assemblyLine)
            for i, item in enumerate(textSplit):
                self.splittedCInstruction[i] = item
        else:
            textSplit = re.split('[;]', self.assemblyLine)
            self.splittedCInstruction[1] = textSplit[0]
            self.splittedCInstruction[2] = textSplit[1]

    def dest(self):
        return self.splittedCInstruction[0]
    
    def comp(self):
        return self.splittedCInstruction[1]
    
    def jump(self):
        return self.splittedCInstruction[2]


    
class Code:
    def __init__(self):
        pass

    def codeAInstruction(self, numberString):
        num = int(numberString)
        return bin(num)[2:].zfill(16)

    def dest(self, d):
        return auxData.destCodes[d]
    
    def comp(self, c):
        return auxData.compCodes[c]

    def jump(self, j):
        return auxData.jumpCodes[j]

class SymbolTable:
    def __init__(self):
        self.symbols = auxData.baseSymbols
        self.address = 16
    
    def labelToInstruction(self, label, instCount):
        if label not in self.symbols:
            self.symbols[label] = instCount
    
    def symbolToAddress(self, symbol):
        if symbol not in self.symbols:
            self.symbols[symbol] = self.address
            self.address += 1
        return str(self.symbols[symbol])


def main():
    fo1 = open("pong\\Pong.asm", "r")
    fo2 = open("pong\\Pong.asm", "r")
    output = open("pong\\Pong.hack", "w")

    code = Code()
    symbolTable = SymbolTable()

    # First pass: labels
    validLineCount = -1
    for line in fo1.readlines():
        parser = Parser(line)
        if parser.isLineValid():
            if parser.isLabel():
                symbolTable.labelToInstruction(parser.assemblyLine, validLineCount + 1)
            else:
                validLineCount += 1

    # Second pass: instruction translation
    for line in fo2.readlines():
        parser = Parser(line)
        if parser.isLineValid() and not parser.isLabel():
            if parser.isA():
                aContent = parser.assemblyLine[1:]
                if not aContent.isdigit():
                    aContent = symbolTable.symbolToAddress(aContent)

                aInst = code.codeAInstruction(aContent)
                output.write(aInst + '\n')
            else:
                parser.handleCInstruction()
    
                comp = code.comp(parser.comp())
                dest = code.dest(parser.dest())
                jump = code.jump(parser.jump())

                cInst = '111' + comp + dest + jump
                output.write(cInst + '\n')


main()

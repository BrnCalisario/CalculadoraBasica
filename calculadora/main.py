from tkinter import *
from tkinter import messagebox
from buttonDict import buttonDict
from operations import *


class Application:

    def __init__(self, master=None):

        # Cores
        self.corFundo = "#141E27"
        self.corFonte = "#EEEDDE"
        self.corFundoInput = "#203239"
        self.corFundoBotao = "#203239"
        self.corBotaoContraste = "#3d4d54"
        #"#3d4d54"
        #"#a9bcc4"
        #"#768b94"

        # Listas
        self.buttonList = []
        self.calculatorMemory = []
        self.simbolos = ["+", "-", "x", "÷"]

        # Fontes
        self.defaultFont = ("Bahnschrift Light", "15", "bold")
        self.btnFont = ("Bahnschrift Light", "15")

        #  Criando Widget e Título da Aplicação
        self.titleContainer = Frame(master)
        self.titleContainer["pady"] = 5
        self.titleContainer["bg"] = self.corFundo
        self.titleContainer.pack()
        self.lbl_Title = Label(self.titleContainer, text=" Calculadora", font=self.defaultFont, bg=self.corFundo, fg= self.corFonte)
        self.lbl_Title.pack()

        # Caixa Input de Dados
        self.containerInput = Frame(master)
        self.containerInput.pack()
        self.actualValue = ""
        self.inputBox = Entry(self.containerInput, font=("Bahnschrift Light", "15"), state=DISABLED,disabledbackground= self.corFundoInput, disabledforeground= self.corFonte)
        self.inputBox.pack()

        # Definindo tamanho padrão dos botões
        self.btnSize = (1, 3)
        self.btnHeight, self.btnWidth = self.btnSize

        # Criando widget e botões
        self.containerBtn = Frame(master)
        self.containerBtn["bg"] = self.corFundo
        self.containerBtn.pack()
        self.createButtons()

    # Insere valor
    def insertValue(self, value):
        if any(simbolo in self.inputBox.get() for simbolo in self.simbolos):
            self.clearInput()
        if self.inputBox.get() == "0":
            self.clearInput()
        self.inputBox['state'] = NORMAL
        self.inputBox.insert(END, value)
        self.inputBox['state'] = DISABLED

    def clearInput(self):
        self.inputBox['state'] = NORMAL
        self.inputBox.delete(0, END)
        self.inputBox['state'] = DISABLED

    def clearMemory(self):
        self.calculatorMemory = []

    def clearBoth(self):
        self.clearInput()
        self.clearMemory()

    # Criando botões a partir do dict importado do buttons.py
    def createButtons(self):
        for i in range(len(buttonDict)):
            indexDict = 1 + i

            self.buttonList.append(Button(
                self.containerBtn,
                text=buttonDict[indexDict]['char'],
                font=self.btnFont,
                bg= self.corFundoBotao,
                fg= self.corFonte,
                activebackground= self.corBotaoContraste,
                width=self.btnWidth,
                height=self.btnHeight))

            actualName = self.buttonList[i]['text']

            try:
                int(buttonDict[indexDict]['char'])
                value = self.buttonList[i]['text']
                self.buttonList[i].configure(command=lambda actualValue=value: self.insertValue(actualValue))
            except ValueError:
                pass

            if actualName == "=":
                self.buttonList[i].configure(command=self.calculate)
            elif actualName == "C":
                self.buttonList[i].configure(command=self.clearBoth)
            elif actualName == ".":
                self.buttonList[i].configure(command=lambda actualValue=".": self.insertValue(actualValue))

            self.buttonList[i].grid(row=buttonDict[indexDict]['row'], column=buttonDict[indexDict]['column'], padx=1,
                                    pady=8)

        # Botões + / - / x / ÷
        self.arithmeticButtons()

    def arithmeticButtons(self):
        symbolIndex = [3, 7, 11, 15]

        for symbol in symbolIndex:
            self.buttonList[symbol].configure(
                command=lambda simbolo=self.buttonList[symbol]['text']: self.addOperator(simbolo))

    def addOperator(self, symbol):
        if len(self.inputBox.get()) > 0:
            if self.inputBox.get() in self.simbolos:
                self.calculatorMemory.remove(self.calculatorMemory[-1])
                self.clearInput()
                self.insertValue(symbol)
                self.calculatorMemory.append(symbol)
            else:
                self.calculatorMemory.append(float(self.inputBox.get()))
                self.calculatorMemory.append(symbol)
                print(self.calculatorMemory)
                self.clearInput()
                self.insertValue(symbol)

    def calculate(self):
        try:
            self.calculatorMemory.append(float(self.inputBox.get()))
        except ValueError:
            return

        self.clearInput()
        print(self.calculatorMemory)

        if len(self.calculatorMemory) % 2 == 0:
            return

        while not len(self.calculatorMemory) == 1:
            if '÷' in self.calculatorMemory:
                self.executeCalc(self.getSymbolIndex("÷"))

            elif 'x' in self.calculatorMemory:
                self.executeCalc(self.getSymbolIndex("x"))

            elif '+' in self.calculatorMemory:
                self.executeCalc(self.getSymbolIndex("+"))

            elif '-' in self.calculatorMemory:
                self.executeCalc(self.getSymbolIndex("-"))
            else:
                break

        if self.calculatorMemory[0].is_integer():
            self.insertValue(int(self.calculatorMemory[0]))
        else:
            self.insertValue(self.calculatorMemory)

        print(self.calculatorMemory)
        self.clearMemory()

    def executeCalc(self, valTuple):
        valA, valB, symIndex, symbol = valTuple

        if valB == 0 and symbol == "÷":
            messagebox.showerror("BURRO", "Dividiu valor por 0")
            self.clearBoth()
            return

        result = operations[symbol](valA, valB)
        del self.calculatorMemory[symIndex]
        self.calculatorMemory.remove(valA)
        self.calculatorMemory.remove(valB)
        self.calculatorMemory.append(result)

    def getSymbolIndex(self, symbol):
        symIndex = self.calculatorMemory.index(symbol)
        valA = self.calculatorMemory[symIndex - 1]
        valB = self.calculatorMemory[symIndex + 1]
        valTuple = (valA, valB, symIndex, symbol)
        return valTuple


root = Tk(className=' Calculadora')
root.geometry("280x360+1000+300")
root.configure(background= "#141E27")
Application(root)
root.mainloop()

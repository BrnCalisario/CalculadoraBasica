import os
import sys
from tkinter import *
from tkinter import messagebox
from turtle import right
from buttonDict import buttonDict
from operations import *
from colorpallet import *


class Application(Tk):

    def __init__(self, master=None):
        super().__init__()
        
        # Definição de tema e cores da calculadora
        self.actualTheme = ""
        self.setTheme()
        self.changeWidgetColor()

        # Tamanho, posição e nome da janela
        self.geometry("280x380+1000+300")
        self.title('Calculadora')

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
        self.containerInput.pack(pady= 5)
        self.actualValue = ""
        self.inputBox = Entry(self.containerInput, 
                        font=("Bahnschrift Light", "15"), 
                        state=DISABLED,
                        disabledbackground= self.corFundoInput, 
                        disabledforeground= self.corFonte,
                        justify='right',
                        width=18)

        self.inputBox.pack()

        # Definindo tamanho padrão dos botões
        self.btnSize = (1, 3)
        self.btnHeight, self.btnWidth = self.btnSize

        # Criando widget e botões
        self.containerBtn = Frame(master)
        self.containerBtn["bg"] = self.corFundo
        self.containerBtn.pack()
        self.createButtons()

    # ------------------ Adicionando botões de forma prática atraves da lista no arquivo buttonDict.py
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
                self.buttonList[i].configure(command=self.calculate, bg= self.corBotaoEqual, activebackground= self.corBotaoEqualC)
            elif actualName == "C":
                self.buttonList[i].configure(command=self.clearInput)
            elif actualName == "CC":
                self.buttonList[i].configure(command=self.clearBoth)
            elif actualName == ".":
                self.buttonList[i].configure(command=lambda actualValue=".": self.insertValue(actualValue))
            elif actualName in self.simbolos:
                self.buttonList[i].configure(command=lambda simbolo=actualName: self.addOperator(simbolo),
                bg=  self.corBotaoSimbolo, activebackground= self.corBotaoSimboloC)
            elif actualName == ":)":
                self.buttonList[i].configure(command=lambda theme='blackTheme': self.changeTheme(theme))
            elif actualName == ":D":
                self.buttonList[i].configure(command=lambda theme='whiteTheme': self.changeTheme(theme))
    
            self.buttonList[i].grid(
                row=buttonDict[indexDict]['row'], 
                column=buttonDict[indexDict]['column'], 
                padx=1,
                pady=8)


    # --------------------- Adicionando a função dos botões aritiméticos
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


    # ----------------------- Lógica da Calculadora
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
            messagebox.showerror("Erro", "Dividiu valor por 0")
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

    # --------------------- Funções de Inserção e Memória -----------------------------
    def insertValue(self, value):
        if any(simbolo in self.inputBox.get() for simbolo in self.simbolos):
            self.clearInput()
        if self.inputBox.get() == "0":
            self.clearInput()
        if value == "." and len(self.inputBox.get()) == 0:
            return 
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


    def changeWidgetColor(self):
        self.corFundo = themes[self.actualTheme]["corBackground"]
        self.corFonte = themes[self.actualTheme]["corFonte"]
        self.corFundoInput = themes[self.actualTheme]["corInput"]
        self.corFundoBotao = themes[self.actualTheme]["corInput"]
        self.corBotaoContraste = themes[self.actualTheme]["corContraste"]
        self.corBotaoSimbolo = themes[self.actualTheme]["corBotaoSimbolo"]
        self.corBotaoSimboloC = themes[self.actualTheme]["corBotaoSimboloC"]
        self.corBotaoEqual = themes[self.actualTheme]["corBotaoEqual"]
        self.corBotaoEqualC = themes[self.actualTheme]["corBotaoEqualC"]
        self.configure(bg=self.corFundo)

    def setTheme(self):
        with open('calculadora/theme-select.txt', 'r+') as f:
            theme = f.readline()
            if len(theme) == 0 or not theme in themes:
                f.write('blackTheme')
                self.actualTheme = 'blackTheme'
            else:
                self.actualTheme = theme

    def changeTheme(self, theme):
        if not theme == self.actualTheme:
            with open('calculadora/theme-select.txt', 'w') as f:
                f.write(theme)
            self.setTheme()
            self.restart_program()
        
    
    def restart_program(self):
        python = sys.executable
        os.execl(python, python, * sys.argv)
        

        




if __name__ == "__main__":
    app = Application()
    app.lift()
    app.mainloop()

from tkinter import *
from tkinter import messagebox

class Board(Tk) :
    def __init__(self, master=None, withComputer = None):
        super().__init__(master)
        self.master = master
        # self.geometry('1600x800+0+0')
        self.title('Tic Tac Toe')
        self.__first__ = 'X'
        self.__second__ = 'O'
        self.__empty__ = '_'
        self.__board__ = []
        self.choices = [self.__first__, self.__second__]


        self.createFrames()
        self.createTopView()
        self.createTTTView()
        self.createRightView()

        self.resetBoard()

    def createFrames(self):
        self.topFrame = Frame(self, width=1600, height=100)
        self.middleFrame = Frame(self, width=1600, height=500)
        # self.bottomFrame = Frame(self, width=1600, height=200)

        # self.leftFrame = Frame(self.middleFrame, width=200, height=500)
        self.TTTFrame = Frame(self.middleFrame, width=600, height=500)
        self.rightFrame = Frame(self.middleFrame, width=200, height=500)

        self.topFrame.pack(side=TOP)
        self.middleFrame.pack(side=TOP)
        # self.bottomFrame.pack(side=TOP)

        # self.leftFrame.pack(side=LEFT)
        self.TTTFrame.pack(side=LEFT)
        self.rightFrame.pack(side=LEFT)

    def createTopView(self):
        self.labelInfo = Label(self.topFrame, font=('arial',30, 'bold'), text="Tic Tac Toe", fg= 'gray', bd=10, anchor=W)
        self.labelInfo.grid(row=0, column=0)

    def createTTTView(self):
        self.editTTTFrame = Frame(self.TTTFrame, bg="white", bd=20)
        self.editTTTEntry = []
        self.inputTTTEntry = []
        for i in range(0,3):
            temp_entry = []
            temp_input = []
            for j in range(0,3):
                optionInput = StringVar()
                optionInput.set(self.choices[0])
                popupMenu = OptionMenu(self.editTTTFrame, optionInput, *(self.choices))
                popupMenu.grid(row = i, column =j)
                optionInput.trace('w', self.changeBoardElement)
                temp_entry.append(popupMenu)
                temp_input.append(optionInput)
            self.editTTTEntry.append(temp_entry)
            self.inputTTTEntry.append(temp_input)

        self.editTTTFrame.pack(fill = X)

    def createRightView(self):
        bg = 'cyan'
        fg = 'black'
        bd = 2
        padx = None
        pady = None
        font = ('arial',14,'bold')
        self.resetButton = Button(self.rightFrame, padx=padx, pady=pady, bd=bd, font=font, fg=fg, text="Reset", bg="orange", command=self.resetBoard)
        self.bestMoveButton = Button(self.rightFrame, padx=padx, pady=pady, bd=bd, font=font, fg=fg, text="Best Move", bg="orange", command=self.makeBestMove)
        self.resetButton.pack(fill=X)
        self.bestMoveButton.pack(fill=X)

    def changeTurn(self):
        if self.__turn__==1:
            self.__turn__ = 2
        else:
            self.__turn__ = 1

    def setTurn(self,turn):
        self.__turn__ = turn


    def move(self, row, col, move, original=False):
        if type(move) == type('X') :
            self.__board__[row][col] = move
            self.inputTTTEntry[row][col].set(move)
        else :
            choices = [self.__empty__,self.__first__, self.__second__]
            self.__board__[row][col] = choices[move]
            self.inputTTTEntry[row][col].set(choices[move])

        if original:
            victory = self.isVictory()
            if(victory > 0):
                messagebox.showinfo('Result', "You are Loser :-(")
                self.resetBoard()
                return;
            if(victory<0):
                messagebox.showinfo('Result', "You are Winner :)")
                self.resetBoard()
                return;
            if not self.isMoveLeft():
                messagebox.showinfo('Result', "Its a Tie :(")
                self.resetBoard()
                return;
            self.changeTurn()

        # self.show()
        # print()

    def changeBoardElement(self, *args):
        temp = int(args[0][-1])
        i = temp//3
        j = temp%3
        self.move(i,j,self.inputTTTEntry[i][j].get())

    def isEmpty(self, row, col):
        return self.__board__[row][col] == self.__empty__

    def resetBoard(self):
        import random
        self.setTurn(random.randint(0,101)%2 +1)
        del self.__board__
        self.__board__ = [
            [self.__empty__, self.__empty__, self.__empty__],#[self.__first__, self.__second__, self.__first__], #
            [self.__empty__, self.__empty__, self.__empty__],#[self.__second__, self.__second__, self.__first__], #
            [self.__empty__, self.__empty__, self.__empty__]
        ]
        for i in range(3):
            for j in range(3):
                self.inputTTTEntry[i][j].set(self.__board__[i][j])

    def show(self):
        for row in self.__board__:
            for col in row:
                print(col, end=" ")
            print()

    def isMoveLeft(self):
        for row in self.__board__:
            for col in row:
                if col == self.__empty__:
                    return True
        return False

    def isVictory(self):        # talking about first player victory
        # check in rows
        for row in self.__board__:
            if row[0] == row[1] and row[1] == row[2]:
                if row[0] == self.__first__:
                    return 1
                elif row[0] == self.__second__:
                    return -1

        for col in range(3):
            if self.__board__[0][col] == self.__board__[1][col] and self.__board__[1][col] == self.__board__[2][col]:
                if self.__board__[0][col] == self.__first__:
                    return 1
                elif self.__board__[0][col] == self.__second__:
                    return -1

        if self.__board__[0][0] == self.__board__[1][1] and self.__board__[1][1] == self.__board__[2][2]:
            if self.__board__[0][0] == self.__first__:
                return 1
            elif self.__board__[0][0] == self.__second__:
                return -1


        if self.__board__[0][2] == self.__board__[1][1] and self.__board__[1][1] == self.__board__[2][0]:
            if self.__board__[0][2] == self.__first__:
                return 1
            elif self.__board__[0][2] == self.__second__:
                return -1

        return 0

    def minMax(self, isMax):
        score = self.isVictory()

        if score > 0:
            # print('victory')
            return score
        if score < 0:
            # print('skip defeat')
            return score
        # if score != 0:
        #     print()
        #     return score

        if not self.isMoveLeft():
            return 0

        if isMax:
            best = -10
            for i in range(3):
                for j in range(3):
                    if self.isEmpty(i,j):
                        self.move(i,j,1)
                        best = max(best, self.minMax(not isMax))
                        self.move(i,j,0);   # undo the previous move

            # print('best: ',best,'\n')
            return best

        else:
            best = 10
            for i in range(3):
                for j in range(3):
                    if self.isEmpty(i,j):
                        self.move(i,j,2)
                        best = min(best, self.minMax(not isMax))
                        self.move(i,j,0);   # undo the previous move
            # print("best : ",best, '\n')
            return best

    def findBestMove(self):
        bestValue = -100
        row = -1
        col = -1

        for i in range(3):
            for j in range(3):
                print(i,j)
                if self.isEmpty(i,j):
                    self.move(i,j,1)
                    moveValue = self.minMax(False)
                    self.move(i,j,0)

                    if moveValue > bestValue:
                        row = i
                        col = j
                        bestValue = moveValue
        # print('bestValue : ',bestValue)
        return row,col

    def makeBestMove(self):
        row, col = self.findBestMove()
        self.move(row,col, 1, True)


    def play():
        while True:
            victory = tictactoe.isVictory()
            if not tictactoe.isMoveLeft():
                print('Its Tie')
                break;
            if(victory > 0):
                print("You Loose")
                break;
            if(victory<0):
                print("You Win")
                break;

            if( self.__turn__ == 1):
                self.makeBestMove()

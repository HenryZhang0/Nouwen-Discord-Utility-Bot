import chess
import chess.variant
import chess.engine
import xboard


board = chess.Board()
emojis = {
    'P':'♟','p':'♙',
    'R':'♜','r':'♖',
    'N':'♞','n':'♘',
    'B':'♝','b':'♗',
    'K':'♚','k':'♔',
    'Q':'♛','q':'♕'
}
emotes = {
    'R':'<:wr:843596931791847535>','r':'<:br:843596932017946685>',
    'Q':'<:wq:843596932165009438>','q':'<:bq:843596932353359883>',
    'P':'<:wp:843596931963551755>','p':'<:bp:843596931775332393>',
    'N':'<:wn:843596932417191946>','n':'<:bn:843596932516806666>',
    'K':'<:wk:843596932324261898>','k':'<:bk:843596932014276641>',
    'B':'<:wb:843596932341563463>','b':'<:bb:843596932088987739>',
    '1':'1️⃣','2':'2️⃣️','3':'3️⃣','4':'4️⃣','5':'5️⃣','6':'6️⃣','7':'7️⃣','8':'8️⃣','.':'⬛',',':'⬜'
}

class Chess():
    def __init__(self):
        self.board = chess.Board()
    def load_board(self,load):
        self.board = chess.Board(load)
    def print(self):
        print(self.board)
    def undo(self):
        self.board.pop()
    def move(self, mov):
        k = chess.Move.from_uci(mov)
        if k in self.board.legal_moves:
            self.board.push(k)
            return True
        else:
            return False
    def str(self):
        x = str(self.board)
        total = '```cs\n'
        for i, row in enumerate(x.split("\n")):
            pieces = ''
            for j,col in enumerate(row):
                if ((i+j/2)%2 and col=='.'):
                    #print(i,j,col, (i+j)%2)
                    pieces +=','
                else:
                    pieces += col
            #print(pieces)

            total += str(8-i) + '|' + pieces + ' | ' +"\n"
        return total 
    
    def engine_move(self):
        fenn = self.board.fen()
        k = xboard.makeMove(fenn)
        print(k)
        if not k=='resign':
            self.move(k)
        return k

    def checkmate(self):
        return self.board.is_checkmate()

    def fen(self):
        return self.board.fen()

    def emoji(self):
        x = self.str().replace(" ","").replace("| ","|").replace("."," ")
        for i, j in emojis.items():
            x = x.replace(i, j)
        return x + "#  a b c d e f g h\n```"
    def emote(self):
        x = self.str()[6:].replace('|','║')
        k = ''
        for i in x:
            if i in list(emotes.keys()):
                k+=(emotes.get(i))
            else:
                k += (i)
        return "✴️╔═════════════════╗\n"+k + "✴️╠═════════════════╝\n"+"✴️║🇦 🇧 🇨 🇩 🇪 🇫 🇬 🇭 "
    def reset(self):
        self.board = chess.Board()
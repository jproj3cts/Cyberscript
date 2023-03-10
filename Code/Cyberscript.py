#%%
import tkinter as tk
root = tk.Tk()
screen = tk.Canvas(root, bg='black')
screen.config(width=1920, height=1080)
screen.grid()

def getParity(n):
    parity = 0
    while n:
        parity = ~parity
        n = n & (n - 1)
    return parity

def genEvil(n):
    c = 0
    i = 0
    while True:
        if getParity(i) == 0:
            if c == n:
                return i
            c+=1
        i+=1

def genStar(n):
    if n%2 != 1:
        return -1
    return [1+(n-3)/2, [2*(genEvil(e)%-2)+1 for e in range(n)]]

offsets = (
    (0, 0, 1, 0),  # top
    (1, 0, 1, 1),  # upper right
    (1, 1, 1, 2),  # lower right
    (0, 2, 1, 2),  # bottom
    (0, 1, 0, 2),  # lower left
    (0, 0, 0, 1),  # upper left
    (0, 1, 1, 1),  # middle
)

class Digit:
    def __init__(self, canvas, *, x=10, y=10, length=20, width=3):
        self.canvas = canvas
        l = length
        self.segs = []
        for x0, y0, x1, y1 in offsets:
            self.segs.append(canvas.create_line(
                x + x0*l, y + y0*l, x + x1*l, y + y1*l,
                width=width, state = 'hidden', fill = 'red'))
    def show(self, dis):
        for iid, on in zip(self.segs, dis):
            self.canvas.itemconfigure(iid, state = 'normal' if on else 'hidden')


codex = {'a' : [1,1,1,-1,1,1,1],
        'b' : [-1,-1,1,1,1,1,1],
        'c' : [1,-1,-1,1,1,1,-1],
        'd' : [-1,1,1,1,1,-1,1],
        'e' : [1,-1,-1,1,1,1,1],
        'f' : [1,-1,-1,-1,1,1,1],
        'g' : [1,1,1,1,-1,1,1],
        'h' : [-1,-1,1,-1,1,1,1],
        'i' : [-1,-1,-1,-1,1,1,-1],
        'j' : [-1,1,1,1,-1,-1,-1],
        'k' : [-1,1,1,-1,1,1,1],
        'l' : [-1,-1,-1,1,1,1,-1],
        'm' : [1,1,1,-1,1,1,-1],
        'n' : [1,1,1,-1,1,1,-1],
        'o' : [1,1,1,1,1,1,-1],
        'p' : [1,1,-1,-1,1,1,1],
        'q' : [1,1,1,-1,-1,1,1],
        'r' : [1,-1,-1,-1,1,1,-1],
        's' : [1,-1,1,1,-1,1,1],
        't' : [-1,-1,-1,-1,1,1,1],
        'u' : [-1,1,1,1,1,1,-1],
        'v' : [-1,1,1,1,1,1,-1],
        'w' : [-1,1,1,1,1,1,-1],
        'x' : [-1,1,1,-1,1,1,1],
        'y' : [-1,1,1,-1,-1,1,1],
        'z' : [1,1,-1,1,1,-1,1],
        ' ' : [-1,-1,-1,-1,-1,-1,-1]
}
test  = "It was a bright cold day in April, and the clocks were striking thirteen. Winston Smith, his chin nuzzled into his breast in an effort to escape the vile wind, slipped quickly through the glass doors of Victory Mansions, though not quickly enough to prevent a swirl of gritty dust from entering along with him."
utterance = input('Scrawl...').lower()
if utterance == '':
    utterance = test

star = genStar(7)
digs = [Digit(screen, x = 10 + 30*(i%63),
        y = 50*(i//63)) for i in range(len(utterance))]
n=0
def update():
    global n
    if utterance[n] in codex:
        plain = codex[utterance[n]]
        cyphered = [(plain[i]*star[1][int((i + star[0]*n)%7)] + 1)/2 for i in range(7)]
        digs[n].show(cyphered)
    n = (n+1)%len(utterance)
    root.after(10, update)
root.after(10, update)
root.mainloop()


# %%

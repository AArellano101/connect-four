from pyfirmata import ArduinoMega, util
import connect_four_ai as cfai
import time
 
# run standardPyfirmatarotocolP
# find arduino/usb port

board = ArduinoMega(" port ")
it = util.Iterator(board)
it.start()

col1 = board.get_pin('d:0:o')
col2 = board.get_pin('d:1:o')
col3 = board.get_pin('d:2:o')
col4 = board.get_pin('d:3:o')
col5 = board.get_pin('d:4:o')
col6 = board.get_pin('d:5:o')
col7 = board.get_pin('d:6:o')

blue1 = board.get_pin('d:7:o')
blue2 = board.get_pin('d:8:o')
blue3 = board.get_pin('d:9:o')
blue4 = board.get_pin('d:10:o')
blue5 = board.get_pin('d:11:o')
blue6 = board.get_pin('d:12:o')

red1 = board.get_pin('d:22:o')
red2 = board.get_pin('d:24:o')
red3 = board.get_pin('d:26:o')
red4 = board.get_pin('d:28:o')
red5 = board.get_pin('d:30:o')
red6 = board.get_pin('d:32:o')

pot = board.get_pin('a:0:i')

E = 'e'
B = 'b'
R = 'r'

EMPTY = 0
PLAYER = 1
AI = 2

DEPTH = 5

REFRESHRATE = 10

maxPot = 675
maxPush = 1022
bound1 = 54
bound2 = 162
bound3 = 284
bound4 = 392
bound5 = 500
bound6 = 621

LOW = 0
HIGH = 1

def colour(redRow, blueRow, colour):
    if (colour == R):
        redRow.write(HIGH)
        blueRow.write(LOW)
    if (colour == B):
        redRow.write(LOW)
        blueRow.write(HIGH)
    if (colour == E):
        redRow.write(LOW)
        blueRow.write(LOW)

def column(col, r1, r2, r3, r4, r5, r6):
    col1.write(HIGH)
    col2.write(HIGH)
    col3.write(HIGH)
    col4.write(HIGH)
    col5.write(HIGH)
    col6.write(HIGH)

    col.write(LOW)

    colour(red1, blue1, r1)
    colour(red2, blue2, r2)
    colour(red3, blue3, r3)
    colour(red4, blue4, r4)
    colour(red5, blue5, r5)
    colour(red6, blue6, r6)

def to_colour_board(board):
    colour_board = [[E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E],
                    [E, E, E, E, E, E, E]]

    for row in range(len(board)):
        for column in range(len(board)):
            if board[row][column] == EMPTY:
                colour_board[row][column] = E
            if board[row][column] == PLAYER:
                colour_board[row][column] = B
            if board[row][column] == AI:
                colour_board[row][column] = R

    return colour_board

gamemode = None
run = True
current_player = PLAYER
board = cfai.initial_state()
cB = []
gameover = False

V = 0
while True: 
    prevV = V
    V = pot.read()
    if current_player == PLAYER and not gameover:
        if ((prevV > maxPot) and (V != maxPush)):
            if ((V >= 0) and (V <= bound1)):
                column = 0 
            if ((V >= bound1 + 1) and (V <= bound2)):
                column = 1
            if ((V >= bound2 + 1) and (V <= bound3)):
                column = 2
            if ((V >= bound3 + 1) and (V <= bound4)):
                column = 3
            if ((V >= bound4 + 1) and (V <= bound5)):
                column = 4
            if ((V >= bound5 + 1) and (V <= bound6)):
                column = 5
            if ((V >= bound6 + 1) and (V <= maxPot)):
                column = 6

        board = cfai.result(board, column, PLAYER)
        current_player = AI
        cB = to_colour_board(board)
    elif current_player == AI and not gameover:
        column = cfai.minimax(board, DEPTH, True)[0]
        board = cfai.result(board, column, AI)
        current_player = PLAYER
        cB = to_colour_board(board)

    if cfai.terminal(board):
        gameover = True


    column(col1, cB[0][0], cB[1][0], cB[2][0], cB[3][0], cB[4][0], cB[5][0])
    time.sleep(REFRESHRATE/1000)
    column(col2, cB[0][1], cB[1][1], cB[2][1], cB[3][1], cB[4][1], cB[5][1])
    time.sleep(REFRESHRATE/1000)
    column(col3, cB[0][2], cB[1][2], cB[2][2], cB[3][2], cB[4][2], cB[5][2])
    time.sleep(REFRESHRATE/1000)
    column(col4, cB[0][3], cB[1][3], cB[2][3], cB[3][3], cB[4][3], cB[5][3])
    time.sleep(REFRESHRATE/1000)
    column(col5, cB[0][4], cB[1][4], cB[2][4], cB[3][4], cB[4][4], cB[5][4])
    time.sleep(REFRESHRATE/1000)
    column(col6, cB[0][5], cB[1][5], cB[2][5], cB[3][5], cB[4][5], cB[5][5])
    time.sleep(REFRESHRATE/1000)
    column(col7, cB[0][6], cB[1][6], cB[2][6], cB[3][6], cB[4][6], cB[5][6])
    time.sleep(REFRESHRATE/1000)
    

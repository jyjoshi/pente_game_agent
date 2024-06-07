file = open("pente.txt", "r")
color = file.readline()
time = file.readline()
captures = file.readline()
board = []
for i in range(19):
    board.append(file.readline())
file.close()

if color == "BLACK\n":
    piece = 'w'
else:
    piece = 'b'

move = "L9"
alphabets = "ABCDEFGHJKLMNOPQRST"
x_index = alphabets.index(move[0])
y_index = 19 - int(move[1:])

string_list = list(board[y_index])
string_list[x_index] = piece
string = "".join(string_list)
print(string)
board[y_index] = string


file = open("pente.txt", "w")
file.write(color)
file.write(time)
file.write(captures)
for line in board:
    file.write(line)
file.close()

# y_coordinate = str(19 - move[0])
# x_coordinate = alphabets[move[1]]




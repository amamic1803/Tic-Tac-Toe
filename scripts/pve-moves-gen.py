import copy
import lzma
import pickle
from itertools import combinations


# magic square for tic tac toe
MAG = {0: {0: 2,
           1: 7,
           2: 6},
       1: {0: 9,
           1: 5,
           2: 1},
       2: {0: 4,
           1: 3,
           2: 8}}

def minimax(board, cur_depth, turn_minmax):
	match win_check(board):
		case "O":
			return 10 * abs(cur_depth - 9)
		case "X":
			return -10 * abs(cur_depth - 9)
		case "DRAW":
			return 0

	match turn_minmax:
		case "min":
			turn_minmax = "max"
			best_val = 100
			for i in range(3):
				for j in range(3):
					if board[i][j] == "_":
						board[i][j] = "X"
						value_cur = minimax(board, cur_depth + 1, turn_minmax)
						board[i][j] = "_"
						if value_cur < best_val:
							best_val = value_cur
			return best_val
		case "max":
			turn_minmax = "min"
			best_val = -100
			for i in range(3):
				for j in range(3):
					if board[i][j] == "_":
						board[i][j] = "O"
						value_cur = minimax(board, cur_depth + 1, turn_minmax)
						board[i][j] = "_"
						if value_cur > best_val:
							best_val = value_cur
			return best_val

def win_check(field):
	x_mag, o_mag = [], []
	for i in range(3):
		for j in range(3):
			match field[i][j]:
				case "X":
					x_mag.append(MAG[i][j])
				case "O":
					o_mag.append(MAG[i][j])
	for i in combinations(x_mag, 3):
		if sum(i) == 15:
			return "X"
	for i in combinations(o_mag, 3):
		if sum(i) == 15:
			return "O"
	if len(x_mag) + len(o_mag) == 9:
		return "DRAW"
	return False

def find_best(field):
	best_move_val = -100
	best_move = (10, 10)

	for i in range(3):
		for j in range(3):
			if field[i][j] == "_":
				field[i][j] = "O"
				cur_val = minimax(field, 0, "min")
				field[i][j] = "_"

				if cur_val > best_move_val:
					best_move_val = cur_val
					best_move = [i, j]

	field[best_move[0]][best_move[1]] = "O"
	return field

def rec(field, turn, best_moves):
	status_pobjede = win_check(field)

	match turn:
		case "X":
			if status_pobjede == "O" or status_pobjede == "DRAW":
				best_moves[encode_field(field)] = encode_field(field)
			else:
				for i in range(3):
					for j in range(3):
						if field[i][j] == "_":
							og_field = copy.deepcopy(field)
							field[i][j] = "X"
							rec(field, "O", best_moves)
							field = og_field
		case "O":
			if status_pobjede == "X" or status_pobjede == "DRAW":
				best_moves[encode_field(field)] = encode_field(field)
			else:
				key_value = encode_field(field)
				field = find_best(field)
				best_moves[key_value] = encode_field(field)
				rec(field, "X", best_moves)

def encode_field(lista):
	""" Turns 2d list into string """

	return "".join([item for row in lista for item in row])

def main():
	field = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
	turn = "X"
	best_moves = {}

	rec(field, turn, best_moves)

	# save best_moves dict to file (using pickle with lzma compression)
	with lzma.open("../resources/pve-moves.pickle.xz", "wb") as file:
		pickle.dump(best_moves, file, protocol=pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
	main()

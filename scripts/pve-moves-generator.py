from itertools import combinations


def deep_copy(lista: list):
	temp_list = []
	for x in lista:
		if type(x) == list:
			temp_list.append(deep_copy(x))
		else:
			temp_list.append(x)
	return temp_list

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
					if board[i][j] == "":
						board[i][j] += "X"
						value_cur = minimax(board, cur_depth + 1, turn_minmax)
						board[i][j] = ""
						if value_cur < best_val:
							best_val = value_cur
			return best_val
		case "max":
			turn_minmax = "min"
			best_val = -100
			for i in range(3):
				for j in range(3):
					if board[i][j] == "":
						board[i][j] += "O"
						value_cur = minimax(board, cur_depth + 1, turn_minmax)
						board[i][j] = ""
						if value_cur > best_val:
							best_val = value_cur
			return best_val

def win_check(field):
	global mag
	x_mag, o_mag = [], []
	for i in range(3):
		for j in range(3):
			match field[i][j]:
				case "X":
					x_mag.append(mag[i][j])
				case "O":
					o_mag.append(mag[i][j])
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
			if field[i][j] == "":
				field[i][j] += "O"
				curVal = minimax(field, 0, "min")
				field[i][j] = ""

				if curVal > best_move_val:
					best_move_val = curVal
					best_move = [i, j]

	field[best_move[0]][best_move[1]] += "O"
	return field

def rec(field, turn):
	global best_moves

	status_pobjede = win_check(field)

	match turn:
		case "X":
			if status_pobjede == "O" or status_pobjede == "DRAW":
				best_moves[encode(field)] = encode(field)
			else:
				for i in range(3):
					for j in range(3):
						if field[i][j] == "":
							og_field = deep_copy(field)
							field[i][j] = "X"
							rec(field, "O")
							field = og_field
		case "O":
			if status_pobjede == "X" or status_pobjede == "DRAW":
				best_moves[encode(field)] = encode(field)
			else:
				key_value = encode(field)
				field = find_best(field)
				best_moves[key_value] = encode(field)
				rec(field, "X")

def encode(lista):
	save_str = ""
	for i in range(3):
		for j in range(3):
			match lista[i][j]:
				case "":
					save_str += "_"
				case "X":
					save_str += "X"
				case "O":
					save_str += "O"
	return save_str

def decode(str_liste):
	return [[str_liste[x] if str_liste[x] != "_" else "" for x in range(0, 3)], [str_liste[x] if str_liste[x] != "_" else "" for x in range(3, 6)], [str_liste[x] if str_liste[x] != "_" else "" for x in range(6, 9)]]

def main():
	global best_moves
	global mag

	mag = {0: {0: 2,
	           1: 7,
	           2: 6},
	       1: {0: 9,
	           1: 5,
	           2: 1},
	       2: {0: 4,
	           1: 3,
	           2: 8}}
	field = [["", "", ""], ["", "", ""], ["", "", ""]]
	best_moves = {}
	rec(field, "X")
	print(best_moves)
	print(len(list(best_moves.keys())))

	with open("../pve-moves-test.txt", "w", encoding="utf-8") as file:
		prvi = True
		for x in best_moves.keys():
			if prvi:
				prvi = False
				file.write(f"{x}={best_moves[x]}")
			else:
				file.write(f"\n{x}={best_moves[x]}")


if __name__ == '__main__':
	main()

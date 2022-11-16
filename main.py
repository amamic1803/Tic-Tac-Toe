import os
import sys
from itertools import combinations
from tkinter import *
from tkinter import messagebox


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)

def update_gui(endgame=None):
	global field, turn
	global status
	global status_text
	global photo_o
	global photo_o_small
	global btns

	for i in range(3):
		for j in range(3):
			btns[i][j].delete("all")
			match field[i][j]:
				case "X":
					btns[i][j].create_line(35, 35, 116, 116, width=25, capstyle=PROJECTING)
					btns[i][j].create_line(35, 115, 116, 34, width=25, capstyle=PROJECTING)
				case "O":
					btns[i][j].create_image(75, 75, anchor="center", image=photo_o)

	status.delete("all")
	if turn == "X":
		status.create_line(23, 23, 78, 78, width=17, capstyle=PROJECTING)
		status.create_line(23, 77, 78, 22, width=17, capstyle=PROJECTING)
	else:
		status.create_image(50, 50, anchor="center", image=photo_o_small)

	match endgame:
		case "X":
			status_text.configure(text="WINNER")
			status.delete("all")
			status.create_line(23, 23, 78, 78, width=17, capstyle=PROJECTING)
			status.create_line(23, 77, 78, 22, width=17, capstyle=PROJECTING)
		case "O":
			status_text.configure(text="WINNER")
			status.create_image(50, 50, anchor="center", image=photo_o_small)
		case "DRAW":
			status.delete("all")
			status_text.configure(text="DRAW")

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

def click(event, i, j):
	global field, turn, started, mode
	global best_moves

	if (not win_check(field)) and started and len(field[i][j]) == 0:
		if turn == "X":
			field[i][j] += "X"
			turn = "O"
		else:
			field[i][j] += "O"
			turn = "X"

		if mode == "PvE":
			field = decode(best_moves[encode(field)])
			turn = "X"

		state_pobjede = win_check(field)
		if state_pobjede:
			started = False
		update_gui(state_pobjede)

def start(event):
	global field, turn, started, mode, status_mode

	if [x for i in field for x in i].count("") != 9 and not win_check(field) and event is not None:
		if not messagebox.askyesno("Game in progress!", "Game is not finished!\nDo you want to start new game?"):
			return

	field = [["", "", ""], ["", "", ""], ["", "", ""]]

	turn = "X"

	status.delete("all")
	status_text.configure(text="")

	for i in range(3):
		for j in range(3):
			btns[i][j].delete("all")

	status.create_line(23, 23, 78, 78, width=17, capstyle=PROJECTING)
	status.create_line(23, 77, 78, 22, width=17, capstyle=PROJECTING)
	status_text.configure(text="TURN")
	started = True
	mode = status_mode

def mode_select(event):
	global status_mode
	global mode_btn

	if [x for i in field for x in i].count("") != 9 and not win_check(field):
		if not messagebox.askyesno("Game in progress!", "Game is not finished!\nDo you want to reset current game?"):
			return

	match status_mode:
		case "PvE":
			mode_btn.configure(text="PvP")
			status_mode = "PvP"
		case "PvP":
			mode_btn.configure(text="PvE")
			status_mode = "PvE"
	start(None)

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
	global field
	global turn
	global started
	global mode
	global status_mode
	global mag
	global status
	global status_text
	global photo_o
	global photo_o_small
	global btns
	global best_moves
	global mode_btn

	root_width = 470
	root_height = 630
	root = Tk()
	root.geometry(f"{root_width}x{root_height}+{(root.winfo_screenwidth() - root_width) // 2}+{(root.winfo_screenheight() - root_height) // 2}")
	root.resizable(width=False, height=False)
	root.title("TIC-TAC-TOE")
	root.iconbitmap(resource_path("data/tic-tac-toe-icon.ico"))
	root.configure(background="#ffffff")

	# using images for o because tkinter's circle is not anti-aliased (not pretty)
	photo_o = PhotoImage(file=resource_path("run_data/o-image.png"))
	photo_o_small = PhotoImage(file=resource_path("run_data/o-image-small.png"))

	naslov = Label(root, text="TIC-TAC-TOE", background="#ffffff", font=("Helvetica", 30, "italic", "bold"))
	naslov.place(width=470, height=60, x=0, y=0)

	for i in range(4):
		line_ver = Label(root, background="#000000")
		line_ver.place(width=5, height=root_width, x=((((root_width - 20) // 3) * i) + (5 * i)), y=root_height - root_width)
		line_hor = Label(root, background="#000000")
		line_hor.place(width=root_width, height=5, x=0, y=((((root_width - 20) // 3) * i) + (5 * i) + (root_height - root_width)))

	cnv_1 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_2 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_3 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_4 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_5 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_6 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_7 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_8 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_9 = Canvas(root, background="#ffffff", highlightthickness=0, cursor="tcross")
	cnv_1.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 0) + (5 * 1)), y=((root_height - root_width) + ((root_width - 20) // 3) * 0 + 5 * 1))
	cnv_2.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 1) + (5 * 2)), y=((root_height - root_width) + ((root_width - 20) // 3) * 0 + 5 * 1))
	cnv_3.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 2) + (5 * 3)), y=((root_height - root_width) + ((root_width - 20) // 3) * 0 + 5 * 1))
	cnv_4.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 0) + (5 * 1)), y=((root_height - root_width) + ((root_width - 20) // 3) * 1 + 5 * 2))
	cnv_5.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 1) + (5 * 2)), y=((root_height - root_width) + ((root_width - 20) // 3) * 1 + 5 * 2))
	cnv_6.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 2) + (5 * 3)), y=((root_height - root_width) + ((root_width - 20) // 3) * 1 + 5 * 2))
	cnv_7.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 0) + (5 * 1)), y=((root_height - root_width) + ((root_width - 20) // 3) * 2 + 5 * 3))
	cnv_8.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 1) + (5 * 2)), y=((root_height - root_width) + ((root_width - 20) // 3) * 2 + 5 * 3))
	cnv_9.place(width=((root_width - 20) // 3), height=((root_width - 20) // 3), x=((((root_width - 20) // 3) * 2) + (5 * 3)), y=((root_height - root_width) + ((root_width - 20) // 3) * 2 + 5 * 3))
	cnv_1.bind("<ButtonRelease-1>", lambda event: click(event, 0, 0))
	cnv_2.bind("<ButtonRelease-1>", lambda event: click(event, 0, 1))
	cnv_3.bind("<ButtonRelease-1>", lambda event: click(event, 0, 2))
	cnv_4.bind("<ButtonRelease-1>", lambda event: click(event, 1, 0))
	cnv_5.bind("<ButtonRelease-1>", lambda event: click(event, 1, 1))
	cnv_6.bind("<ButtonRelease-1>", lambda event: click(event, 1, 2))
	cnv_7.bind("<ButtonRelease-1>", lambda event: click(event, 2, 0))
	cnv_8.bind("<ButtonRelease-1>", lambda event: click(event, 2, 1))
	cnv_9.bind("<ButtonRelease-1>", lambda event: click(event, 2, 2))

	btn_start = Button(root, text="START", cursor="tcross", borderwidth=0, background="#ffffff", font=("Helvetica", 15, "bold"), foreground="blue", activeforeground="blue", activebackground="#ffffff")
	btn_start.place(width=160, height=50, x=0, y=80)
	btn_start.bind("<ButtonRelease-1>", start)

	mode_lbl = Label(root, text="MODE:", borderwidth=0, background="#ffffff", font=("Helvetica", 15, "bold"), activebackground="#ffffff")
	mode_btn = Button(root, text="PvE", cursor="tcross", borderwidth=0, background="#ffffff", font=("Helvetica", 15, "bold"), activebackground="#ffffff")
	mode_lbl.place(x=5, y=135, height=20, width=75)
	mode_btn.place(x=80, y=135, height=20, width=80)
	mode_btn.bind("<ButtonRelease-1>", mode_select)

	status = Canvas(root, background="#ffffff", highlightthickness=0)
	status.place(width=100, height=100, x=370, y=60)

	status_text = Label(root, background="#ffffff", font=("Helvetica", 20, "bold", "italic"), foreground="red")
	status_text.place(x=220, y=60, width=150, height=100)

	# program
	mag = {0: {0: 2,
	           1: 7,
	           2: 6},
	       1: {0: 9,
	           1: 5,
	           2: 1},
	       2: {0: 4,
	           1: 3,
	           2: 8}}

	btns = {0: {0: cnv_1,
	            1: cnv_2,
	            2: cnv_3},
	        1: {0: cnv_4,
	            1: cnv_5,
	            2: cnv_6},
	        2: {0: cnv_7,
	            1: cnv_8,
	            2: cnv_9}}

	best_moves = {}
	with open(resource_path("run_data/pve-moves.txt"), "r") as file:
		run = True
		while run:
			red = file.readline().rstrip("\n")
			if red == "":
				run = False
			else:
				k, v = red.split("=")
				best_moves[k] = v

	field = [["", "", ""], ["", "", ""], ["", "", ""]]

	turn = "X"

	started = False
	mode = "PvE"
	status_mode = "PvE"
	root.mainloop()


if __name__ == '__main__':
	main()

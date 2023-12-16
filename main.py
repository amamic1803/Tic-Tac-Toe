import lzma
import os
import pickle
import sys
from itertools import combinations
import tkinter as tk
from tkinter import messagebox


def resource_path(relative_path):
	""" Get absolute path to resource, works for dev and for PyInstaller """
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except AttributeError:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)


# magic square for win check
MAG = {0: {0: 2,
           1: 7,
           2: 6},
       1: {0: 9,
           1: 5,
           2: 1},
       2: {0: 4,
           1: 3,
           2: 8}}

class App:
	def __init__(self):
		self.started = False
		self.field = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]
		self.turn = "X"
		self.mode = "PvE"
		self.selected_mode = "PvE"
		with lzma.open(resource_path("resources/pve-moves.pickle.xz"), "rb") as file:
			self.best_moves = pickle.load(file)

		self.width = 470
		self.height = 630

		self.root = tk.Tk()
		self.root.geometry(f"{self.width}x{self.height}"
		                   f"+{(self.root.winfo_screenwidth() - self.width) // 2}"
		                   f"+{(self.root.winfo_screenheight() - self.height) // 2}")
		self.root.resizable(width=False, height=False)
		self.root.title("Tic-Tac-Toe")
		self.root.iconbitmap(resource_path("resources/tic-tac-toe-icon.ico"))
		self.root.configure(background="#ffffff")

		# using images for Os because tkinter's circle is not anti-aliased
		self.o_img = tk.PhotoImage(file=resource_path("resources/o-img.png"))
		self.o_img_small = tk.PhotoImage(file=resource_path("resources/o-img-small.png"))

		self.naslov = tk.Label(self.root, text="Tic-Tac-Toe", font=("Helvetica", 30, "italic", "bold"),
		                       background="#ffffff")
		self.naslov.place(width=470, height=60, x=0, y=0)

		# grid lines
		for i in range(4):
			line_ver = tk.Label(self.root, background="#000000")
			line_ver.place(width=5, height=self.height,
			               x=((((self.width - 20) // 3) * i) + (5 * i)),
			               y=self.height - self.width)
			line_hor = tk.Label(self.root, background="#000000")
			line_hor.place(width=self.width, height=5,
			               x=0,
			               y=((((self.width - 20) // 3) * i) + (5 * i) + (self.height - self.width)))

		# grid buttons
		self.btns = dict()
		cnv_width = cnv_height = (self.width - 20) // 3
		y_offset = self.height - self.width
		for row in range(3):
			for col in range(3):
				cnv = tk.Canvas(self.root, background="#ffffff", highlightthickness=0, cursor="hand2")
				cnv.place(width=cnv_width,
				          height=cnv_height,
				          x=((cnv_width * col) + (5 * (col + 1))),
				          y=(y_offset + cnv_height * row + 5 * (row + 1)))
				cnv.bind("<ButtonRelease-1>", lambda event, row=row, col=col: self.click(row, col))
				self.btns.setdefault(row, dict())  # if row not exists, create it
				self.btns[row][col] = cnv

		self.btn_start = tk.Button(self.root, text="START", font=("Helvetica", 15, "bold"), cursor="hand2",
		                           borderwidth=0, background="#ffffff", foreground="blue",
		                           activeforeground="blue", activebackground="#ffffff")
		self.btn_start.place(width=160, height=50, x=0, y=80)
		self.btn_start.bind("<ButtonRelease-1>", lambda event: self.start())

		self.mode_lbl = tk.Label(self.root, text="MODE:", font=("Helvetica", 15, "bold"),
		                         borderwidth=0, background="#ffffff", activebackground="#ffffff")
		self.mode_lbl.place(x=5, y=135, height=20, width=75)

		self.mode_btn = tk.Button(self.root, text="PvE", font=("Helvetica", 15, "bold"), cursor="hand2",
		                          borderwidth=0, background="#ffffff", activebackground="#ffffff")
		self.mode_btn.place(x=80, y=135, height=20, width=80)
		self.mode_btn.bind("<ButtonRelease-1>", lambda event: self.mode_select())

		self.status = tk.Canvas(self.root, background="#ffffff", highlightthickness=0)
		self.status.place(width=100, height=100, x=370, y=60)

		self.status_text = tk.Label(self.root, font=("Helvetica", 20, "bold", "italic"),
		                            background="#ffffff", foreground="red")
		self.status_text.place(x=220, y=60, width=150, height=100)

		self.root.mainloop()

	def start(self, skip_confirmation=False):
		if [x for i in self.field for x in i].count("_") != 9 and not self.game_ended() and not skip_confirmation:
			if not messagebox.askyesno("Game in progress!", "Game is not finished!\nDo you want to start new game?"):
				return

		self.field = [["_", "_", "_"], ["_", "_", "_"], ["_", "_", "_"]]

		self.turn = "X"

		self.status.delete("all")
		self.status_text.configure(text="")

		for i in range(3):
			for j in range(3):
				self.btns[i][j].delete("all")

		self.status.create_line(23, 23, 78, 78, width=17, capstyle=tk.PROJECTING)
		self.status.create_line(23, 77, 78, 22, width=17, capstyle=tk.PROJECTING)
		self.status_text.configure(text="TURN")

		self.started = True
		self.mode = self.selected_mode

	def click(self, row, col):
		if (not self.game_ended()) and self.started and self.field[row][col] == "_":
			if self.turn == "X":
				self.field[row][col] = "X"
				self.turn = "O"
			else:
				self.field[row][col] = "O"
				self.turn = "X"

			if self.mode == "PvE":
				self.decode_field(self.best_moves[self.encode_field()])
				self.turn = "X"

			if state_pobjede := self.game_ended():
				self.started = False
				self.update_gui(state_pobjede)
			else:
				self.update_gui()

	def mode_select(self):
		if [x for i in self.field for x in i].count("_") != 9 and not self.game_ended():
			if not messagebox.askyesno("Game in progress!",
			                           "Game is not finished!\nDo you want to reset current game?"):
				return

		match self.selected_mode:
			case "PvE":
				self.mode_btn.configure(text="PvP")
				self.selected_mode = "PvP"
			case "PvP":
				self.mode_btn.configure(text="PvE")
				self.selected_mode = "PvE"

		self.start(skip_confirmation=True)

	def encode_field(self):
		""" Turns 2d field into string """

		return "".join([item for row in self.field for item in row])

	def decode_field(self, string):
		""" Turns field string into 2d list """

		self.field = [[string[x] if string[x] != "_" else "_" for x in range(0, 3)],
		              [string[x] if string[x] != "_" else "_" for x in range(3, 6)],
		              [string[x] if string[x] != "_" else "_" for x in range(6, 9)]]

	def game_ended(self):
		x_mag, o_mag = [], []
		for i in range(3):
			for j in range(3):
				match self.field[i][j]:
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

	def update_gui(self, game_end=None):
		for i in range(3):
			for j in range(3):
				self.btns[i][j].delete("all")
				match self.field[i][j]:
					case "X":
						self.btns[i][j].create_line(35, 35, 116, 116, width=25, capstyle=tk.PROJECTING)
						self.btns[i][j].create_line(35, 115, 116, 34, width=25, capstyle=tk.PROJECTING)
					case "O":
						self.btns[i][j].create_image(75, 75, anchor="center", image=self.o_img)

		self.status.delete("all")
		if self.turn == "X":
			self.status.create_line(23, 23, 78, 78, width=17, capstyle=tk.PROJECTING)
			self.status.create_line(23, 77, 78, 22, width=17, capstyle=tk.PROJECTING)
		else:
			self.status.create_image(50, 50, anchor="center", image=self.o_img_small)

		match game_end:
			case "X":
				self.status_text.configure(text="WINNER")
				self.status.delete("all")
				self.status.create_line(23, 23, 78, 78, width=17, capstyle=tk.PROJECTING)
				self.status.create_line(23, 77, 78, 22, width=17, capstyle=tk.PROJECTING)
			case "O":
				self.status_text.configure(text="WINNER")
				self.status.create_image(50, 50, anchor="center", image=self.o_img_small)
			case "DRAW":
				self.status.delete("all")
				self.status_text.configure(text="DRAW")


def main():
	App()


if __name__ == '__main__':
	main()

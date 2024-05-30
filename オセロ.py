import tkinter as tk

class Reversi:
    def __init__(self, root):
        self.root = root
        self.root.title("リバーシ（オセロ）")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.size = 8
        self.cell_size = 50
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.current_player = "●"  # 黒石が先手
        self.pass_count = 0  # 連続パスの回数
        self.draw_board()
        self.initialize_board()
        self.canvas.bind("<Button-1>", self.click)
        self.update_status()

    def draw_board(self):
        for i in range(self.size):
            for j in range(self.size):
                x0 = j * self.cell_size
                y0 = i * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black")

    def initialize_board(self):
        self.board[3][3] = "○"
        self.board[3][4] = "●"
        self.board[4][3] = "●"
        self.board[4][4] = "○"
        self.update_board()

    def update_board(self):
        self.canvas.delete("piece")
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] is not None:
                    x0 = j * self.cell_size + self.cell_size // 2
                    y0 = i * self.cell_size + self.cell_size // 2
                    self.canvas.create_text(x0, y0, text=self.board[i][j], tags="piece", font=("Arial", 24))

    def click(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        if self.is_valid_move(x, y):
            self.make_move(x, y)
            self.update_board()
            self.switch_player()
            self.check_for_pass()
            self.update_status()

    def is_valid_move(self, x, y):
        if self.board[y][x] is not None:
            return False

        opponent = "○" if self.current_player == "●" else "●"
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        valid = False

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False
            while 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == opponent:
                found_opponent = True
                nx += dx
                ny += dy
            if found_opponent and 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == self.current_player:
                valid = True
                break

        return valid

    def make_move(self, x, y):
        self.board[y][x] = self.current_player
        self.flip_stones(x, y)
        self.pass_count = 0  # パスカウントをリセット

    def flip_stones(self, x, y):
        opponent = "○" if self.current_player == "●" else "●"
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            stones_to_flip = []
            while 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == opponent:
                stones_to_flip.append((nx, ny))
                nx += dx
                ny += dy
            if stones_to_flip and 0 <= nx < self.size and 0 <= ny < self.size and self.board[ny][nx] == self.current_player:
                for flip_x, flip_y in stones_to_flip:
                    self.board[flip_y][flip_x] = self.current_player

    def switch_player(self):
        self.current_player = "○" if self.current_player == "●" else "●"

    def has_valid_moves(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.is_valid_move(j, i):
                    return True
        return False

    def check_for_pass(self):
        if not self.has_valid_moves():
            self.pass_count += 1
            self.canvas.create_text(200, 200, text="パス", tags="pass", font=("Arial", 24), fill="red")
            self.root.after(1000, self.canvas.delete, "pass")
            self.switch_player()
            if not self.has_valid_moves():
                self.end_game()
            else:
                self.update_status()
        else:
            self.pass_count = 0

    def end_game(self):
        black_count = sum(row.count("●") for row in self.board)
        white_count = sum(row.count("○") for row in self.board)
        if black_count > white_count:
            winner = "黒"
        elif white_count > black_count:
            winner = "白"
        else:
            winner = "引き分け"
        self.canvas.create_text(200, 200, text=f"ゲーム終了\n{winner}の勝ち", tags="end", font=("Arial", 24), fill="red")
        self.canvas.unbind("<Button-1>")

    def update_status(self):
        status_text = f"リバーシ（オセロ） - {self.current_player}のターン"
        if self.pass_count > 0:
            status_text += " (パス)"
        self.root.title(status_text)

if __name__ == "__main__":
    root = tk.Tk()
    reversi = Reversi(root)
    root.mainloop()

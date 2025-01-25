import tkinter as tk
from tkinter import messagebox

# スクレイピング用のダミープログラム
def scrape():
    input_value = entry.get()
    messagebox.showinfo("情報", f"'{input_value}'のレビューをスクレイピングを開始します。")
    # ここに実際のスクレイピングコードを追加
    # print(f"'{input_value}'のレビューをスクレイピングを開始します。")

# Tkinterのウィンドウを作成
root = tk.Tk()
root.title("楽天レビュースクレイピング")
root.geometry("800x450")

# フレーム
frame = tk.Frame(root, width=750, height=200, bg='#888888', relief="solid")
frame.pack(padx=10, pady=10)

# ラベルを作成
label = tk.Label(frame, text="レビューをスクレイピングするURLを入力してください：", font=("游ゴシック", 12))
label.place(x=10, y=10)

# 入力項目を作成
entry = tk.Entry(frame, width=80, font=("游ゴシック", 12) )
entry.place(x=10, y=50)

# ボタンを作成
button = tk.Button(frame, text="スクレイピング開始", font=("游ゴシック", 12), command=scrape)
button.place(x=10, y=110)

# メインループを開始
root.mainloop()

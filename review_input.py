import tkinter as tk
from tkinter import messagebox

# スクレイピング用のダミープログラム
def scrape():
    input_value = entry.get()
    messagebox.showinfo("情報", f"'{input_value}'のレビューをスクレイピングを開始します。")
    # ここに実際のスクレイピングコードを追加
    print(f"'{input_value}'のレビューをスクレイピングを開始します。")

# Tkinterのウィンドウを作成
root = tk.Tk()
root.title("楽天レビュースクレイピング")

# ラベルを作成
label = tk.Label(root, text="レビューをスクレイピングする商品名を入力してください：")
label.pack()

# 入力項目を作成
entry = tk.Entry(root)
entry.pack()

# ボタンを作成
button = tk.Button(root, text="スクレイピング開始", command=scrape)
button.pack()

# メインループを開始
root.mainloop()

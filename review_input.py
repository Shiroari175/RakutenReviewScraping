import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from subprocess import Popen,PIPE
import review

def start_scraping():
    """
    スクレイピングプログラムを呼び出す
    :return:
    """
    url = entry.get()
    review.scrape(url, int(selected_number.get()))
    result_label.config(text="*** 対象商品の抽出処理が完了しました。 *** :")

# 数値が変更されたときにラベルを更新する関数
# def update_label(*args):
#     label.config(text=f"選択した数値: {selected_number.get()}")

# Tkinterのウィンドウを作成
root = tk.Tk()
root.title("楽天レビュースクレイピング")
root.geometry("800x450")

# フレーム
frame = tk.Frame(root, width=750, height=400, bg='#EEEEEE', relief="solid")
frame.pack(padx=10, pady=10)

# URLラベル
label = tk.Label(frame, text="レビューをスクレイピングするURLを入力してください：", font=("游ゴシック", 12))
label.place(x=10, y=10)

# URL入力
entry = tk.Entry(frame, width=80, font=("游ゴシック", 12) )
entry.place(x=10, y=50)

# ページラベル
page_label = tk.Label(frame, text="スクレイピングする、ページ数を入力してください：", font=("游ゴシック", 12))
page_label.place(x=10, y=100)

# ページ入力
# page_entry = tk.Entry(frame, width=10, font=("游ゴシック", 12) )
# page_entry.place(x=400, y=100)

# 数値のリストを作成
numbers = [str(i) for i in range(1, 31)]  # 1から10までの数値

# 選択された数値を保持する変数
selected_number = tk.StringVar()
selected_number.set(numbers[0])  # デフォルト値を設定

# プルダウンメニューを作成し、背景色を白に設定
dropdown = ttk.OptionMenu(frame, selected_number, *numbers)
dropdown.place(x=425, y=100)

# プルダウンメニューのスタイルを設定
style = ttk.Style()
style.configure('TMenubutton', background='white', font=("游ゴシック", 12))

# 処理結果
result_label = tk.Label(frame, text="※ここに処理結果が表示されます。", font=("游ゴシック", 9) )
result_label.place(x=10, y=160)

# ボタンを作成
button = tk.Button(frame, text="スクレイピング開始", font=("游ゴシック", 12), command=start_scraping)
button.place(x=10, y=275)

# 変数が変更されたときに関数を呼び出す
# selected_number.trace("w", update_label)

# メインループを開始
root.mainloop()

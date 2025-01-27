import tkinter as tk
from tkinter import messagebox
from subprocess import Popen,PIPE
import review

def start_scraping():
    """
    スクレイピングプログラムを呼び出す
    :return:
    """
    url = entry.get()
    review.scrape(url)
    result_label.config(text="*** 対象商品の抽出処理が完了しました。 *** :")

    # messagebox.showinfo("スクレイピング開始", f"レビューのスクレイピングを開始します。")
    # process = Popen(['python', 'review.py', url,], stdout=PIPE, stderr=PIPE)
    # output, error = process.communicate()
    # if error:
    #     result_label.config(text=error.decode())
    # else:
    #     result_label.config(text=output.decode())

# Tkinterのウィンドウを作成
root = tk.Tk()
root.title("楽天レビュースクレイピング")
root.geometry("800x450")

# フレーム
frame = tk.Frame(root, width=750, height=400, bg='#EEEEEE', relief="solid")
frame.pack(padx=10, pady=10)

# ラベルを作成
label = tk.Label(frame, text="レビューをスクレイピングするURLを入力してください：", font=("游ゴシック", 12))
label.place(x=10, y=10)

# 入力項目を作成
entry = tk.Entry(frame, width=80, font=("游ゴシック", 12) )
entry.place(x=10, y=50)

# 処理結果
result_label = tk.Label(frame, text="※ここに処理結果が表示されます。", font=("游ゴシック", 9) )
result_label.place(x=10, y=80)

# ボタンを作成
button = tk.Button(frame, text="スクレイピング開始", font=("游ゴシック", 12), command=start_scraping)
button.place(x=10, y=275)

# メインループを開始
root.mainloop()

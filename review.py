import sys
import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

"""
 楽天レビュー スクレイピング
  Ver3.0.0 2025/01/18 Xpathを主体としてデータ取得していた為
                        WebDriverを主体としたプログラムに変更
  
  麹 https://review.rakuten.co.jp/item/1/236315_10011235/1.1/
    https://review.rakuten.co.jp/item/1/236315_10011235?p=3#itemReviewList
"""

def shorten_text(edit_text, max_length=100):
    """
    指定された文字数に文字列をカットし、末尾に"..."を追加します。

    Parameters:
    text (str): カットする対象の文字列。
    max_length (int): 最大文字数。デフォルトは100。

    Returns:
    str: カットされた文字列の末尾に"..."を追加した結果。
    """
    if len(edit_text) > max_length:
        return edit_text[:max_length] + "..."
    return edit_text

def scrape(url, page) :

    """
    スクレイピング実行

    Parameters:
    url (str): スクレイピングターゲットURL

    Returns:
    iCount : 登録処理件数
    """

    # 接続情報
    config = {
        'user': 'root',
        'password': '',
        'host': 'localhost',
        'database': 'rak_rev'
    }

    # データベースに接続
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()

    # Options 設定 -----
    option = Options()
    # ヘッドレスモードON ブラウザをバックグランドで起動
    # うまく取得できない場合は、OFFにする
    option.add_argument("--headless")
    driver = webdriver.Chrome(options=option)

    i_count = 0

    for i in range(page + 1): #+1補正

        # 0は飛ばす
        if i == 0:
            continue

        # URL生成
        edit_url = f"{url}?p={i}#itemReviewList"
        print(f"処理URL:{edit_url}")

        # WEBドライバ実行 -----
        driver.get(edit_url)

        # html・BeautifulSoup 設定 -----
        html = driver.page_source.encode('utf-8')
        html_text = BeautifulSoup(html, "html.parser")
        # ---

        # Find_ALL実行で1次抽出
        content_list = html_text.find_all('li')

        # ファイルに書き込む
        # with open('./temp/output2.txt', 'w', encoding='utf-8') as file:
        #     file.write(str(content_list))

        # 商品名
        item_name_element = html_text.find('span', class_='ellipsis--3cNjo')
        if item_name_element is not None:
            # 100文字以上は、カットする
            # 比較チェック時に、問題があるので一旦廃止する
            # item_name = shorten_text(item_name_element.text, 100)
            item_name = item_name_element.text
        else:
            item_name = None

        # i_count = 0 # INSERTした件数
        # edit_url = []
        for content in content_list:

            # 購入者名
            purchaser_name_element = content.find('div', class_='reviewer-name--3Ouhw')
            if purchaser_name_element is not None:
                # 末尾'さん'を除去
                purchaser_name = purchaser_name_element.text[:-2]
            else:
                # purchaser_name = None
                # ただし、購入者データがない場合は、つぎへ
                continue

            # 評価
            evaluation_element = content.find('span',
                                                  class_= [
                                                      'text-container--IAFCr',
                                                      'size-body-1-low--3HTHO',
                                                      'style-bold--1Rhly',
                                                      'color-gray-dark--2ebP7'
                                                      ])
            if evaluation_element is not None:
                evaluation = evaluation_element.text
            else:
                evaluation = None

            # レビュータイトル（任意項目）
            review_title_element = content.find('div', class_='type-header--18XjX')
            if review_title_element is not None:
                review_title = review_title_element.text
            else:
                review_title = None

            # レビュー本文
            review_text_element = content.find('div', class_= re.compile(r'(review-body--1pESv|no-ellipsis--IKXkO)'))
            if review_text_element is not None:
                review_text = review_text_element.text
            else:
                review_text = None

            # 商品詳細：サイズ・カラーなど
            # 最初はfind_allで取得して、分解して各個取得する
            sub_content_list = content.find_all('div', class_= 'color-gray-dark--2N4Oj')
            item_detail_list = []
            for sub_content in sub_content_list :
                if sub_content is not None:
                    item_detail_list.append(sub_content.text)
                else:
                    item_detail_list.append(None)

            # フィールド数（横の長さ）がまちまちなので、リスト項目数を調整する
            default_word = "不明"
            if len(item_detail_list) > 1:
                if not re.search('性', item_detail_list[1]) :
                    item_detail_list.insert(1,default_word)
                if not re.search('代', item_detail_list[2]) :
                    item_detail_list.insert(2,default_word)
                if not re.search('サイズ', item_detail_list[3]) :
                    item_detail_list.insert(3,default_word)
                if not re.search('実用品', item_detail_list[4]) :
                    item_detail_list.insert(4,default_word)
                if not re.search('注文日', item_detail_list[5]) :
                    item_detail_list.insert(5,None)

            # 追加前データチェック
            # 注文日の修正
            # 1.None以外の場合、"注文日："をreplaceする
            # 2."yyyy-mm-dd"に変換する
            if item_detail_list[5] is not None :
                order_date = item_detail_list[5].replace('注文日：', '')
                order_date = order_date.replace('/', '-')
            else :
                order_date = None

            # 重複チェック
            # レビュー本文が12文字以下の場合は、飛ばす
            if len(review_text) < 13:
                print(f"レビュー本文が短すぎるので、登録をスキップします。："
                      f"{item_name},{purchaser_name},{review_text[:12]}...")
                continue

            # 1.商品名が同じ
            # 2.かつ購入者名が同じ
            # 3.かつレビュー本文が先頭から12文字あっていたならば
            # 追加しないで、スキップする
            cursor.execute('SELECT ITEM_NM,'
                           ' PURCHASER_NM,'
                           ' REVIEW_TEXT FROM T_REVIEW '
                           ' WHERE '
                           ' PURCHASER_NM = %s '
                           ' and REVIEW_TEXT LIKE %s', (purchaser_name,f'{review_text[:12]}%' ))
            row = cursor.fetchone()
            if row is not None :
                if item_name == row[0] \
                        and purchaser_name == row[1] \
                        and review_text[:12] == row[2][:12]:
                    print(f"すでに登録されています。登録をスキップします：{row[0]},{row[1]},{row[2][:12]}...")
                    continue

            # データ追加
            cursor.execute("INSERT INTO T_REVIEW ( HAKI_FLG ,"
                           "ITEM_NM ,"
                           "PURCHASER_NM ,"
                           "EVALUATION ,"
                           "REVIEW_TITLE ,"
                           "REVIEW_TEXT ,"
                           "SEX ,"
                           "AGE ,"
                           "ITEM_DETAIL ,"
                           "ORDER_DATE"
                           ") VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                           ,( 0
                             , item_name
                             , purchaser_name
                             , evaluation
                             , review_title
                             , review_text
                             , item_detail_list[1]
                             , item_detail_list[2]
                             , item_detail_list[3]
                             , order_date
                             )
                           )

            # コミット
            conn.commit()
            i_count += 1

    # ドライバ終了
    driver.quit()
    # 接続を閉じる
    cursor.close()
    conn.close()

    return f"** 処理が終了しました。 処理件数：{i_count} **"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        scrape(url) # スクレイピング実行
        # print(f"*** 楽天レビューデータ抽出END *** : 登録した件数：{iCount}")
    else:
        print("URLを引数として提供してください")


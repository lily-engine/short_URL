import sqlite3
import re
from hashids import Hashids
from flask import Flask, request, abort

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

app = Flask(__name__)
app.config['SECRET_KEY'] = 'this should be a secret random string' # 開発用
hashids = Hashids(min_length=4, salt=app.config['SECRET_KEY'])

@app.route('/register-url', methods=['POST'])
def get_register_url():
    conn = get_db_connection()

    url = request.form['url']
    url_pattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    if not re.match(url_pattern, url):
        return abort(404)

    url_data = conn.execute('INSERT INTO urls (original_url) VALUES (?)',
                            (url,))
    conn.commit()
    conn.close()

    # データベースに挿入したURLのIDを格納
    url_id = url_data.lastrowid
    # IDから一意のhashを生成
    hashid = hashids.encode(url_id)
    # 短縮URLを作成
    short_url = request.host_url + hashid

    return {
        "short_url": short_url
    }

@app.route('/urls')
def urls():
    conn = get_db_connection()
    db_urls = conn.execute('SELECT id, created, original_url, clicks FROM urls'
                           ).fetchall()
    conn.close()

    urls = []
    for url in db_urls:
        url = dict(url)
        url['short_url'] = request.host_url + hashids.encode(url['id'])
        urls.append(url)
    
    original_urls = [d.get("original_url") for d in urls]

    return {
        "urls": original_urls
    }

@app.route('/<short_url>')
def url_response(short_url):
    conn = get_db_connection()

    # hashを元の整数値に変換
    original_id = hashids.decode(short_url)
    # original_idに値があることを確認し、値がある場合はIDを抽出
    if original_id:
        original_id = original_id[0]
        url_data = conn.execute('SELECT original_url, clicks FROM urls'
                                ' WHERE id = (?)', (original_id,)
                                ).fetchone()
        original_url = url_data['original_url']
        clicks = url_data['clicks']

        conn.execute('UPDATE urls SET clicks = ? WHERE id = ?',
                     (clicks+1, original_id))

        conn.commit()
        conn.close()
        return {
            "original_url": original_url
        }
    else:
        abort(404)

if __name__ == '__main__':
    app.run(debug=True)
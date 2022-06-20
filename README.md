# 短縮URLの発行API
短縮URLを発行できるAPIの実装例です。

## 機能
- ユーザから渡されたURLに紐づく短縮URLを発行して、DBに保存する。
- DBに登録されている全URLの一覧を取得する。
- 短縮されたURLから元のURLを取得する。

## 起動方法
1. Python環境をアクティブにする。
    1. Pythonのパッケージ管理ツール「pip」を[インストールする](https://pip.pypa.io/en/stable/getting-started/)。
    1. 作業ディレクトリで、仮想環境を作成する（venv）。  
        `python3 -m venv venv`
    1. 仮想環境をアクティブにする。  
        `source venv/bin/activate`
    1. FlaskとHashidsライブラリをインストールする。  
        `(venv) $ pip install flask hashids`
1. Flaskの環境変数を設定して実行する。
    1. 環境変数を設定する。  
        `(venv) $ export FLASK_APP=app.py  
        (venv) $ export FLASK_ENV=development`
    1. app.pyの12,13行目にある`['SECRET_KEY']`に、秘密のランダムな文字列を設定する（セキュリティ上の理由により、公開しないよう注意する。参照：[# SECRET_KEYの発行方法](https://study-flask.readthedocs.io/ja/latest/02.html) ）。  
    1. app.pyがあるディレクトリで、Flaskを実行する。  
        `(venv) $ flask run`

## APIの使用方法
### 短縮URLを発行して、DBに保存する
1. メソッド：POST
1. URL：http://127.0.0.1:5000/register_url
1. パラメータ：{"url":"https://github.com/"}
1. レスポンス：{"short_url": "http://127.0.0.1:5000/q7BR"}
1. エラー：404

### 短縮URLの一覧を取得する
1. メソッド：GET
1. URL：http://127.0.0.1:5000/urls
1. パラメータ：なし
1. レスポンス：{"short_url": "http://127.0.0.1:5000/q7BR"}

### 短縮URLから元のURLを取得する
1. メソッド：GET
1. URL：http://127.0.0.1:5000/<short_url>
1. パラメータ：なし
1. レスポンス：{"original_url": "https://github.com/"}

## 主な参考資料
1. [小学生でもわかるWebAPI入門。ゼロからWebAPIを作ってみよう](https://www.youtube.com/watch?v=6_zIN-bByB4&t=1409s)
1. [【Flask】簡単なAPIを実装](https://amateur-engineer-blog.com/flask-api/)
1. [FLASKとSQLITEでURL短縮サービスを作成する方法](https://ja.getdocs.org/how-to-make-a-url-shortener-with-flask-and-sqlite)
1. [Python3.10.4 Documentation](https://docs.python.org/ja/3/library/re.html#re.match)
1. [はじめての Flask #5 ~JSONを返すWebAPIを書こう~](https://qiita.com/nagataaaas/items/24e68a9c736aec31948e)
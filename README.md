# Ameyadar
以下、作者の方のREADME.

ツイッターアカウント名に，京都大学上空の予想降水量に応じた絵文字を貼付する。

Yahoo! Open Local Platform(YOLP)の[気象情報API](https://developer.yahoo.co.jp/webapi/map/openlocalplatform/v1/weather.html)を使ってます。  
こういう無料の気象系APIは，精度が悪かったり(海外産)，二次利用不可だったり(日本産)するのだが，これは非商用目的なら使える([商用目的でも問い合わせれば使えるかも](https://www.yahoo-help.jp/app/answers/detail/p/537/a_id/43405))ので有難い。1時間先までの降水量しか分からないけど日常生活ではそれで充分。  

## License
MIT

以下、追記

## Dependents
### 必須
- python
- pip
- 利用するクライアントのAPI Key各種
- Yahoo API
### 推奨
- virtualenv or venv

## Usage
### twitterで使う場合
```bash
  $ cp .env.example .env
  # edit `.env` file
  $ pip install -r requirements.txt
  $ python ameyadar.py
```

### mastodon
```bash
  $ cp .env.example .env
  # edit `.env` file
  $ pip install -r requirements.txt
  # APIのKeyの取得を行う
  $ python scripts/initialize_mastodon.py # 初回だけ実行して下さい
  # data/mastodon/ フォルダが出来ていれば成功です
  $ python ameyadar.py mastodon
```

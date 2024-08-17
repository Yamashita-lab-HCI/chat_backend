# chat_backend

## setup（仮装環境がない場合）
```bash
python3 -m venv chat
```

## start
1. 
```bash
source chat/bin/activate
```
2.
```bash
# start websocket server
export DJANGO_SETTINGS_MODULE=chat_backend.settings
export PYTHONPATH="/Users/keis/dev/chat_backend:$PYTHONPATH"
daphne -p 8001 chat_backend.asgi:application
```
また、別のCUIで
```bash
# start server
python manage.py migrate
python manage.py runserver
```
⚠️`python3`はインタプリターが変わるので使ってはいけない！

## add requirements.txt
何か追加でpipに入れたときは、
```bash
pip freeze > requirements.txt
```
で書き込む。pip環境を再度作るときは、
```bash
pip install -r requirements.txt
```
でやる。

## initialize database
`db.sqlite3`がデータベースにあたる。
要はこれを削除して、作り直せば良い。
```bash
rm -d -r migrations/
rm -d pr db.sqlite3
python manage.py makemigrations chat
python manage.py migrate
```

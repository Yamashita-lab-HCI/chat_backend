# chat_backend

## Ubuntuサーバーでのデプロイの流れ
### sslアクセスの有効化
HTTP接続ではブラウザ警告が出てきてしまうので、HTTPS接続に。
HTTPS接続でも自己証明書を作ったが、これも警告が出るのでドメインを発行して証明書を取得
1. AWS Route53で新しいドメインを発行（今回は`chatawesome.net`）
2. Route53にレコードを追加して、EC2のIPアドレス（IPv4）で登録
3. `nginx`のインストール
4. `nginx`の設定ファイル`/etc/nginx/sites-available/default`にHTTPS接続`443`をプロキシパス`http://127.0.0.1:8000;`からできるように設定
5. Let’s Encryptから証明書を取得し、Nginxの設定を自動的に更新
```bash
sudo certbot --nginx -d chatawesome.net
```
6. 起動時に以下が正しく作動してればOK
```bash
sudo systemctl status gunicorn
sudo systemctl status nginx
sudo systemctl status custom-startup.service
```
## database
`mysql`をEC2サーバー内に設置。
### boot
```bash
mysql -u ubuntu -p
Enter password: 'saku1003`
```
### setup
```bash
sudo mysql
sudo mysql
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 13
Server version: 8.0.37-0ubuntu0.24.04.1 (Ubuntu)

Copyright (c) 2000, 2024, Oracle and/or its affiliates.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> CREATE DATABASE chat;
Query OK, 1 row affected (0.01 sec)

mysql> CREATE USER 'ubuntu'@'localhost' IDENTIFIED BY 'saku1003';
Query OK, 0 rows affected (0.02 sec)

mysql>
mysql> GRANT ALL PRIVILEGES ON chat.* TO 'ubuntu'@'localhost';
Query OK, 0 rows affected (0.01 sec)

mysql>
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)

mysql> EXIT;
Bye
```

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
export DJANGO_SETTINGS_MODULE=chat_backend.settings
export PYTHONPATH="/Users/keis/dev/chat_backend:$PYTHONPATH"
daphne -p 8001 chat_backend.asgi:application
python manage.py migrate
python manage.py runserver
```
⚠️`python3`はインタプリターが変わるので使ってはいけない！

## add requirements.txt
何か追加でpipに入れたときは、
```bash
pip install -r requirements.txt
```

## initialize database
`db.sqlite3`がデータベースにあたる。
要はこれを削除して、作り直せば良い。
```bash
rm -d -r migrations/
rm -d pr db.sqlite3
python manage.py makemigrations chat
python manage.py migrate
```

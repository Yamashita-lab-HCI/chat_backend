# chat_backend

## Ubuntuサーバーでのデプロイの流れ（まだ試行錯誤中）
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

## RDSとの接続設定
```bash
mysql -h database-1.cxcik2aa211v.ap-northeast-3.rds.amazonaws.com -u admin -p
# パスワードはsaku1003
```
### MySQLのセットアップ
```bash
sudo apt-get update
sudo apt-get install mysql-client
```
```mysql
CREATE DATABASE chat;
```

## setup（仮装環境がない場合）
```bash
conda create --name chat
conda activate chat
conda install pip
conda install --file requirements.txt
```

## start
1. 
```bash
conda activate chat
```
2.
```bash
python manage.py migrate
python manage.py runserver
```
⚠️`python3`はインタプリターが変わるので使ってはいけない！

## add requirements.txt
何か追加でcondaに入れたときは、
```bash
conda list --export | grep -v "^#" | cut -d '=' -f 1-2 > requirements.txt
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

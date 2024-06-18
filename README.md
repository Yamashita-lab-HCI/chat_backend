# chat_backend

# Ubuntuサーバーでのデプロイの流れ
```bash
sudo systemctl start nginx
cd /home/ubuntu/chat_backend
source activate chat
python manage.py runserver 0.0.0.0:8000
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

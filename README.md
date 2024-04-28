# chat_backend

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
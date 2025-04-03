#### Активация venv для локальной разработки
```
source ~/venv/bin/activate
```

#### Запуск
1. `vim .env.prod`
   Вписать в него:
   ```
   TELEGRAM_API_TOKEN='<token>'
   TG_IDS='<id1> <id2> ...'
   ```

   sudo docker compose up --build -d

#### Установить docker compose на ubuntu 22.04:
```
1. https://stackoverflow.com/questions/76031884/sudo-apt-get-install-docker-compose-plugin-fails-on-jammy

2. sudo apt-get install docker-compose-plugin
```
#### Активация venv для локальной разработки
```
source ~/venv/bin/activate
```

#### Запуск
1. `vim .env.dev`
   Вписать в него:
   ```
   TELEGRAM_API_TOKEN='<token>'
   TG_IDS='<id1> <id2> ...'
   ```

   sudo docker compose up --build -d

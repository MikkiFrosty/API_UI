
# API UI — Тестирование корзины

Мини-проект для диплома: API-тестирование с подготовкой данных для UI на примере интернет-магазина **Demo Web Shop** (корзина).

## Стек
- Python, Pytest
- Requests
- Pydantic — модели для запросов/ответов
- Allure — красивые отчёты (вложения request/response)
- Selene — для `browser.config.base_url` и проверки UI-состояния после действий по API

## Покрытый функционал
- Авторизация по API и получение cookie
- Добавление товара в корзину по API (`POST /addproducttocart/details/{id}/1`) с валидацией JSON
- Очистка/удаление позиции из корзины по API (`POST /cart`)
- Проверка UI после подготовки данных по API (корзина содержит/пуста)
- Тест для метода `DELETE` (на публичном API `reqres.in`)

## Структура проекта
```
api_ui_cart_project/
  api/
    client.py               
    demowebshop_flows.py    
  models/
    cart.py                 
  utils/
    logger.py
tests/
  resources/                
  conftest.py               
  test_cart_flow.py         
pictures/                 
requirements.txt
.gitignore
README.md
UNMET_REQUIREMENTS.md
```

## Запуск
```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -v --alluredir=allure-results
# allure serve allure-results   # при наличии allure CLI
```

## Jenkins / Allure (заглушки)
- Job: https://jenkins.example.com/job/api_ui_cart/
- Allure Report: https://jenkins.example.com/job/api_ui_cart/AllureReport/

Скриншот уведомления в Telegram (заглушка) — в каталоге `pictures/`.



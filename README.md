# API + UI Cart — учебный проект по автоматизации

> Репозиторий демонстрирует **два набора автотестов**:  
> 1) **Тренажёрные API‑тесты** на сервисе Reqres.in,  
> 2) **Комбинированные UI+API‑тесты** для корзины Demo Web Shop.  
>
> Проект учебный: отработка REST‑проверок (CRUD, статус‑коды, JSON‑схемы) и базовой связки через API в UI.

## Технологический стек

<p  align="center">
<img src="images/logos/python-original.svg" width="50" title="Python"> <img src="images/logos/pytest.png" width="50" title="Pytest"> <img src="images/logos/intellij_pycharm.png" width="50" title="PyCharm"> <img src="images/logos/selene.png" width="50" title="Selene"> <img src="images/logos/selenium.png" width="50" title="Selenium"> <img src="images/logos/selenoid.png" width="50" title="Selenoid"> <img src="images/logos/jenkins.png" width="50" title="Jenkins"> <img src="images/logos/allure_report.png" width="50" title="Allure Report"> <img src="images/logos/github.png" width="50" title="GitHub">
</p>

## Покрытый функционал

### 1) Тренажёрные **API-тесты** (папка `tests_api/`) — сервис **Reqres.in**

- Проверка получения списка пользователей (GET)
- Проверка получения конкретного пользователя (GET)
- Проверка ошибки при запросе несуществующего пользователя (GET)
- Проверка создания пользователя по схеме (POST)
- Проверка ошибки при регистрации без пароля (POST)
- Проверка обновления данных пользователя (PUT)
- Проверка удаления пользователя (DELETE)

---

### 2) Комбинированные **UI+API-тесты корзины** (папка `tests/`) — **Demo Web Shop**

- Авторизация через API и получение cookie
- Добавление товара в корзину через API и проверка успешного ответа
- Очистка корзины через API и проверка, что в UI корзина пуста
- Проверка, что добавленный через API товар отображается в UI

## Запуск

Установить зависимости и запустить все тесты:
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pytest -q
```

Только **API‑тесты** (Reqres):
```bash
pytest tests_api -q
```

Только **UI+API** (Demo Web Shop):
```bash
pytest tests -q
```
Локальная генерация отчёта Allure:
```bash
allure serve allure-results
```
## Allure Report
[Пример Allure Report](https://jenkins.autotests.cloud/job/API_UI-main)

<p align="center">
  <img src="images/allure_overview.png" alt="Allure Report: успешные тесты" width="800">
</p>

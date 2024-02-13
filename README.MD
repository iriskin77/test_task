## Описание

см. подробное описание в ветке "description-task"

Выполненные условия на скриншоте:

![](https://github.com/iriskin77/test_task/blob/master/images/descr_task.png)

## Как запустить

#### 1) Запуск из docker контейнера

+ Клонировать репозиторий: git clone
+ Создать и запустить docker контейнер комендами:
  + docker-compose build
  + docker-compose up
+ После этого приложение будет доступно на порте 8090

#### 2) Запуск как python-script

+ Клонировать репозиторий: git clone
+ Создать виртуальное окружение: python3 -m venv venv
+ Активировать виртуальное окружение: source venv/bin/actibate
+ Установить зависимости: pip install -r requirements.txt
+ Запустить приложение: uvicorn main:app --reload



Порядок установки

git clone https://github.com/BFront/FR.git

установить зависимости:
pip install -r requirements.txt

запустить и применить миграции:
python manage.py makemigrations
python manage.py migrate

Запустить проект:
python manage.py runserver


Клиенты:
http://127.0.0.1:8000/api/clients/ Список клиентов при GET, при POST принимает список атрибутов для добавления нового
http://127.0.0.1:8000/api/client/{id} GET PUT DELETE (Просмотр изменение и удаление клиента и его атрибутов)

Рассылки:
http://127.0.0.1:8000/api/mailings/ Список рассылок при GET, при POST принимает список атрибутов для добавления новой рассылки
http://127.0.0.1:8000/api/mailing/{id} GET PUT DELETE (Просмотр изменение и удаление рассылки и ее атрибутов)

Cron
Добавить задание в Cron на ежеминутку например
http://127.0.0.1:8000/api/cron Проверяет текущее дату и время, если текущее время Больше старта указанного в рассылке НО меньше чем время окончания, то запускает рассылку по клиентам с тэгом как указано в рассылке.

Статистика:
http://127.0.0.1:8000/api/statistic/mailings Общая статистика по рассылкам
http://127.0.0.1:8000/api/statistic/mailing/{id} Статистика по конкретной рассылке
http://127.0.0.1:8000/api/statistic/mesages Общая статистика по сообщениям
http://127.0.0.1:8000/api/statistic/clients Общая статистика по клиентам

Все разделы доступны через админку http://127.0.0.1:8000/admin/ username:admin password:xxpFHecUdbMh8RL

# team_force
Инструкция по запуску программы приложения на Linux и MACos

    git clone https://github.com/diomaxer/team_force.git
    cd team_force
    python3 -m venv venv
    source venv/bin/activate
    pip3 install -r requirements.txt
    python manage.py runserver

Изменять навыки можно только в личном кабинете. Личный кабинет доступен только после авторизации.
Чтобы добавить навык нужно поставить галочку напротив имеющихсся навыков в базе или написать свои через запятую в форму.
Чтобы удалить навык достаточно убрать с него галочку.

Данные для входа в админку 

      почта: admin@g.com
      пароль: admin
      
Данные юзеров

      почты: user1@mail.ru user2@mail.ru user3@mail.ru
      пароль: password

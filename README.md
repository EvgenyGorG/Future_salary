# Сравниваем вакансии программистов

Программа позволяет получить и сравнить информацию по 10 самым популярным
языкам программирования. Вакансии взяты с сайта [HeadHunter.ru](https://hh.ru/)
и [SuperJob.ru](https://www.superjob.ru/). Информация представлена
в виде таблиц с полями:

- Язык программирования;
- Количество найденных вакансий;
- Количество обработанных вакансий;
- Средняя заработная плата.

Программа 'вытягивает' информацию по актуальным вакансиям
за последние 30 дней.

### Как установить

[Python3](https://www.python.org/downloads/) должен быть уже установлен.
Затем используйте `pip` (или `pip3`, есть конфликт с Python2)
для установки зависимостей:
```
pip install -r requirements.txt
```

Рекомендуется использовать [virtualenv/venv](https://docs.python.org/3/library/venv.html)
для изоляции проекта.

Необходимо создать `.env` файл, для хранения переменной окружения,
которая будет использоваться в программе. В файле должна быть переменная
`SUPER_JOB_SECRET_KEY`, которая хранит секретный ключ вашего приложения. Чтобы зарегистрировать
приложение и получить секретный ключ следуйте инструкции
[SuperJob API Docs](https://api.superjob.ru/).

### Пример запуска:
```
>>> python print_job_statistic.py
```
![hh table](screenshots/hh%20statistic.png)
![sj table](screenshots/sj%20statistic.png)

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).


# Comparing Programmer Vacancies

The program allows you to obtain and compare information
on the 10 most popular programming languages.
The vacancies are taken from [HeadHunter.ru](https://hh.ru/)
and [SuperJob.ru](https://www.superjob.ru/).
The information is presented in tables with the following
fields:

- Programming Language;
- Number of vacancies found;
- Number of processed vacancies;
- Average salary.

The program 'pulls' information on current vacancies
for the last 30 days.

### How to Install

[Python3](https://www.python.org/downloads/) should already be installed.
Then use `pip` (or `pip3`, if there is a conflict with Python2)
to install the dependencies:
```
pip install -r requirements.txt
```

It is recommended to use [virtualenv/venv](https://docs.python.org/3/library/venv.html)
for project isolation.

You need to create a `.env` file to store the environment variable
that will be used in the program. The file should contain
the variable `SUPER_JOB_SECRET_KEY`, which stores your application's
secret key. To register your application and obtain a secret key,
follow the instructions in the
[SuperJob API Docs](https://api.superjob.ru/).

### Example of Running:
```
>>> python print_job_statistic.py
```
![hh table](screenshots/hh%20statistic.png)
![sj table](screenshots/sj%20statistic.png)

### Project Goal

The code is written for educational purposes
as part of an online course for web developers
at [dvmn.org](https://dvmn.org/).
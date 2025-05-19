import os
from pprint import pprint


import requests
from dotenv import load_dotenv


def predict_rub_salary_for_super_job(vacancy):
    currency = vacancy['currency']
    min_salary = vacancy['payment_from']
    max_salary = vacancy['payment_to']

    if currency != 'rub' or (not min_salary and not max_salary):
        return None
    if min_salary and max_salary:
        return (min_salary + max_salary) / 2
    elif min_salary:
        return min_salary * 1.2
    else:
        return max_salary * 0.8


def main():
    load_dotenv()
    super_job_secret_key = os.environ['SUPER_JOB_SECRET_KEY']

    super_job_api_url = 'https://api.superjob.ru/2.0/vacancies'
    headers = {
        'X-Api-App-Id': super_job_secret_key
    }
    params = {
        'town': 4,
        'catalogues': 48
    }

    super_job_vacancies = requests.get(super_job_api_url, headers=headers, params=params)
    super_job_vacancies.raise_for_status()
    super_job_vacancies = super_job_vacancies.json()

    for vacancy in super_job_vacancies['objects']:
        print(
            f'{vacancy['profession']}, '
            f'{vacancy['town']['title']}, '
            f'{predict_rub_salary_for_super_job(vacancy)}'
        )


if __name__ == '__main__':
    main()
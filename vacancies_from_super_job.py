import os
from pprint import pprint


import requests
from dotenv import load_dotenv


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
        print(f'{vacancy['profession']}, {vacancy['town']['title']}')


if __name__ == '__main__':
    main()
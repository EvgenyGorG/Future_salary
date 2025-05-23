import os


import requests
from dotenv import load_dotenv
from terminaltables import AsciiTable


def predict_rub_salary(salary_from, salary_to):
    if salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    else:
        return salary_to * 0.8


def predict_rub_salary_hh(vacancy):
    currency = vacancy['salary']['currency']
    salary_from = vacancy['salary']['from']
    salary_to = vacancy['salary']['to']

    if currency != 'RUR' or (not salary_from and not salary_to):
        return None
    else:
        return predict_rub_salary(salary_from, salary_to)


def predict_rub_salary_sj(vacancy):
    currency = vacancy['currency']
    salary_from = vacancy['payment_from']
    salary_to = vacancy['payment_to']

    if currency != 'rub' or (not salary_from and not salary_to):
        return None
    else:
        return predict_rub_salary(salary_from, salary_to)


def search_vacancies_from_hh():
    hh_vacancies_url = 'https://api.hh.ru/vacancies'

    programming_languages = [
        'GO', 'C', 'C#', 'C++', 'PHP', 'Ruby',
        'Python', 'Java', 'JavaScript', 'Kotlin'
    ]

    average_salaries_by_languages = {}

    for programming_language in programming_languages:
        page = 0
        pages = 1

        all_hh_vacancies_by_specific_language = []

        while page < pages:
            hh_vacancy_parameters = {
                'professional_role': 96,
                'area': 1,
                'period': 30,
                'only_with_salary': True,
                'text': f'Программист {programming_language}',
                'page': page
            }

            hh_vacancies = requests.get(hh_vacancies_url, params=hh_vacancy_parameters)
            hh_vacancies.raise_for_status()
            hh_vacancies = hh_vacancies.json()

            pages = hh_vacancies['pages']
            page += 1

            all_hh_vacancies_by_specific_language += hh_vacancies['items']

        predict_rub_salaries = []

        for vacancy in all_hh_vacancies_by_specific_language:
            if predict_rub_salary_hh(vacancy):
                predict_rub_salaries.append(predict_rub_salary_hh(vacancy))

        if predict_rub_salaries:
            average_salary = int(sum(predict_rub_salaries) / len(predict_rub_salaries))
        else:
            average_salary = None

        average_salaries_by_languages[programming_language] = {
            'vacancies_found': len(all_hh_vacancies_by_specific_language),
            'vacancies_processed': len(predict_rub_salaries),
            'average_salary': average_salary
        }

    return average_salaries_by_languages


def search_vacancies_from_sj():
    load_dotenv()
    super_job_secret_key = os.environ['SUPER_JOB_SECRET_KEY']

    super_job_api_url = 'https://api.superjob.ru/2.0/vacancies'

    headers = {
        'X-Api-App-Id': super_job_secret_key
    }

    programming_languages = [
        'GO', 'C', 'C#', 'C++', 'PHP', 'Ruby',
        'Python', 'Java', 'JavaScript', 'Kotlin'
    ]

    average_salaries_by_languages = {}

    for programming_language in programming_languages:
        page = 0
        more = True

        all_sj_vacancies_by_specific_language = []

        while more:
            sj_vacancy_params = {
                'town': 4,
                'catalogues': 48,
                'period': 30,
                'page': page,
                'keyword': programming_language
            }

            sj_vacancies = requests.get(super_job_api_url, headers=headers, params=sj_vacancy_params)
            sj_vacancies.raise_for_status()
            sj_vacancies = sj_vacancies.json()

            more = sj_vacancies['more']
            page += 1

            all_sj_vacancies_by_specific_language += sj_vacancies['objects']

        predict_rub_salaries = []

        for vacancy in all_sj_vacancies_by_specific_language:
            if predict_rub_salary_sj(vacancy):
                predict_rub_salaries.append(predict_rub_salary_sj(vacancy))

        if predict_rub_salaries:
            average_salary = int(sum(predict_rub_salaries) / len(predict_rub_salaries))
        else:
            average_salary = None

        average_salaries_by_languages[programming_language] = {
            'vacancies_found': len(all_sj_vacancies_by_specific_language),
            'vacancies_processed': len(predict_rub_salaries),
            'average_salary': average_salary
        }

    return average_salaries_by_languages


def create_table(job_statistic, title):
    table_data = [
        (
            'Язык программирования',
            'Вакансий найдено',
            'Вакансий обработано',
            'Средняя зарплата'
        )
    ]

    for language in job_statistic:
        table_data.append(
            (
                language,
                job_statistic[language]['vacancies_found'],
                job_statistic[language]['vacancies_processed'],
                job_statistic[language]['average_salary']
            )
        )

    table_instance = AsciiTable(table_data, title)

    return table_instance.table


def main():
    hh_job_statistic = search_vacancies_from_hh()
    sj_job_statistic = search_vacancies_from_sj()

    hh_title = 'HeadHunter Moscow'
    sj_title = 'SuperJob Moscow'

    print(create_table(hh_job_statistic, hh_title))
    print(create_table(sj_job_statistic, sj_title))


if __name__ == '__main__':
    main()

from pprint import pprint


import requests


def get_require_vacancies(vacancies_url, programming_language, page):
    vacancy_parameters = {
        'professional_role': 96,
        'area': 1,
        'period': 30,
        'only_with_salary': True,
        'text': f'Программист {programming_language}',
        'page': {page}
    }

    vacancies = requests.get(vacancies_url, params=vacancy_parameters)
    vacancies.raise_for_status()

    return vacancies.json()


def get_number_of_vacancies_in_programming_languages(
        programming_languages, vacancies_url
):
    vacancy_parameters = {
        'professional_role': 96,
        'area': 1,
        'period': 30,
        'text': ''
    }

    number_of_vacancies_in_programming_languages = {}

    for programming_language in programming_languages:
        vacancy_parameters['text'] = f'Программист {programming_language}'

        vacancies = requests.get(vacancies_url, params=vacancy_parameters)
        vacancies.raise_for_status()
        vacancies = vacancies.json()

        number_of_vacancies_in_programming_languages[programming_language] = vacancies['found']

    return number_of_vacancies_in_programming_languages


def get_salaries_of_the_desired_programming_language(vacancies_url):
    vacancy_parameters = {
        'professional_role': 96,
        'area': 1,
        'period': 30,
        'only_with_salary': True,
        'text': 'Программист Python'
    }

    salaries_of_the_desired_programming_language = []

    vacancies = requests.get(vacancies_url, params=vacancy_parameters)
    vacancies.raise_for_status()
    vacancies = vacancies.json()

    for vacancy in vacancies['items']:
        salaries_of_the_desired_programming_language.append(vacancy['salary'])

    return salaries_of_the_desired_programming_language


def predict_rub_salary(vacancy):
    currency = vacancy['salary']['currency']
    min_salary = vacancy['salary']['from']
    max_salary = vacancy['salary']['to']

    if currency != 'RUR':
        return None
    if min_salary and max_salary:
        return (min_salary + max_salary) / 2
    elif min_salary:
        return min_salary * 1.2
    else:
        return max_salary * 0.8


def main():
    vacancies_url = 'https://api.hh.ru/vacancies'

    programming_languages = [
        'GO', 'C', 'C#', 'C++', 'PHP', 'Ruby',
        'Python', 'Java', 'JavaScript'
    ]

    number_of_vacancies_in_programming_languages = (
        get_number_of_vacancies_in_programming_languages(
            programming_languages, vacancies_url
        )
    )

    average_salary_by_language = {}

    for programming_language in programming_languages:
        page = 0
        pages = 1

        all_vacancies = []

        while page < pages:
            actual_vacancies = get_require_vacancies(vacancies_url, programming_language, page)
            pages = actual_vacancies['pages']
            page += 1
            all_vacancies += actual_vacancies['items']

        predict_rub_salaries = []

        for vacancy in all_vacancies:
            if predict_rub_salary(vacancy):
                predict_rub_salaries.append(predict_rub_salary(vacancy))

        average_salary_by_language[programming_language] = {
            'vacancies_found': number_of_vacancies_in_programming_languages[programming_language],
            'vacancies_processed': len(predict_rub_salaries),
            'average_salary': int(sum(predict_rub_salaries) / len(predict_rub_salaries))
        }


    pprint(average_salary_by_language)


if __name__ == '__main__':
    main()
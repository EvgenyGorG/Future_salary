from pprint import pprint


import requests


def get_require_vacancies(vacancies_url, vacancy_parameters):
    vacancies = requests.get(vacancies_url, params=vacancy_parameters)
    vacancies.raise_for_status()

    return vacancies.json()


def get_number_of_vacancies_in_programming_languages(
        programming_languages, vacancies_url, vacancy_parameters
):
    number_of_vacancies_in_programming_languages = {}

    for programming_language in programming_languages:
        vacancy_parameters['text'] = f'Программист {programming_language}'
        vacancies = requests.get(vacancies_url, params=vacancy_parameters)
        vacancies.raise_for_status()
        vacancies = vacancies.json()
        number_of_vacancies_in_programming_languages[programming_language] = vacancies['found']

    return number_of_vacancies_in_programming_languages


def main():
    vacancies_url = 'https://api.hh.ru/vacancies'

    vacancy_parameters = {
        'professional_role': 96,
        'area': 1,
        'period': 30
    }

    programming_languages = [
        'GO', 'C', 'C#', 'C++', 'PHP', 'Ruby',
        'Python', 'Java', 'JavaScript'
    ]

    actual_vacancies = get_require_vacancies(vacancies_url, vacancy_parameters)

    number_of_vacancies_in_programming_languages = (
        get_number_of_vacancies_in_programming_languages(
            programming_languages, vacancies_url, vacancy_parameters
        )
    )


if __name__ == '__main__':
    main()
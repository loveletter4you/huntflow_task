import pandas as pd
import os


def get_vacancy_by_position(vacancies, position):
    try:
        vacancy = next(vacancy for vacancy in vacancies if vacancy['position'] == position)
        return vacancy
    except StopIteration:
        return None


def get_vacancy_status_by_name(statuses, name):
    try:
        status = next(status for status in statuses if status['name'] == name)
        return status
    except StopIteration:
        return None


def get_cv_path(path, name):
    try:
        cv_path = next(filename for filename in os.listdir(path) if filename.startswith(name))
        return cv_path
    except StopIteration:
        return None


def get_all_applicants(path):
    df = pd.read_excel(path)
    return df.to_dict(orient='records')

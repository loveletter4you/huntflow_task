from services.api_service import SessionService
from services.service import get_vacancy_by_position, get_all_applicants, get_vacancy_status_by_name, get_cv_path


def main():
    token = input("Enter access token: ")
    file_path = input("Enter data directory path: ")
    api_server = "https://dev-100-api.huntflow.dev/v2"
    session_service = SessionService(token, api_server)
    organization_id = session_service.get_organizations()[0]['id']
    vacancies = session_service.get_vacancies(organization_id)
    vacancy_statues = session_service.get_vacancy_statuses(organization_id)
    applicants = get_all_applicants(file_path + '/Тестовая база.xlsx')
    for applicant in applicants:
        full_name = applicant['ФИО'].strip()
        full_name_split = full_name.split()
        if len(full_name_split) == 3:
            first_name, last_name, middle_name = full_name_split
        elif len(full_name_split) == 2:
            first_name, last_name = full_name_split
            middle_name = None
        else:
            first_name = full_name
            last_name = ""
            middle_name = None

        vacancy = get_vacancy_by_position(vacancies, applicant['Должность'])
        if vacancy is None:
            continue

        status = get_vacancy_status_by_name(vacancy_statues, applicant['Статус'])
        if status is None:
            continue

        filename = get_cv_path(f'{file_path}/{applicant["Должность"]}', full_name)
        if not (filename is None):
            file = open(f'{file_path}/{applicant["Должность"]}/{filename}', 'rb')
            cv_id = session_service.upload_cv(organization_id, filename, file)['id']
            file.close()
        else:
            cv_id = None

        session_service.post_applicant(organization_id, vacancy['id'], first_name, last_name, middle_name,
                                       applicant['Комментарий'], status['id'], applicant['Ожидания по ЗП'], cv_id)


if __name__ == '__main__':
    main()

import requests
import mimetypes
from requests_toolbelt import MultipartEncoder


class SessionService:
    def __init__(self, token: str, api_server: str):
        self.headers = {"Authorization": f"Bearer {token}"}
        self.api_server = api_server

    def get_organizations(self):
        return requests.get(f"{self.api_server}/accounts", headers=self.headers).json()['items']

    def get_vacancies(self, organization_id):
        response = requests.get(f'{self.api_server}/accounts/{organization_id}/vacancies?count=100',
                                headers=self.headers).json()
        vacancies = response['items']
        count = response['total_pages']
        page = 1
        while page < count:
            page += 1
            response = requests.get(f'{self.api_server}/accounts/{organization_id}/vacancies?count=100&page={page}',
                                    headers=self.headers).json()
            vacancies = vacancies + response['items']
        return vacancies

    def get_vacancy_statuses(self, organization_id):
        return requests.get(f'{self.api_server}/accounts/{organization_id}/vacancies/statuses',
                            headers=self.headers).json()['items']

    def upload_cv(self, organization_id, file_name, file):
        headers = self.headers.copy()
        file_type = mimetypes.guess_type(file_name)
        data = MultipartEncoder({'file': (file_name, file.read(), file_type[0])})
        headers['Content-Type'] = data.content_type
        response = requests.post(f'{self.api_server}/accounts/{organization_id}/upload',
                                 headers=headers, data=data)
        return response.json()

    def post_applicant(self, organization_id, vacancy_id, first_name, last_name,
                       middle_name, comment, status_id, money, cv_id):
        data = {
            'first_name': first_name,
            'last_name': last_name,
            'money': money,
        }
        if not (middle_name is None):
            data['middle_name'] = middle_name
        if not (cv_id is None):
            data['externals'] = [
                {
                    'auth_type': 'NATIVE',
                    'files': [int(cv_id)]
                }
            ]

        response = requests.post(f'{self.api_server}/accounts/{organization_id}/applicants',
                                 headers=self.headers, json=data)
        applicant_id = response.json()['id']
        data = {
            'vacancy': int(vacancy_id),
            'status': int(status_id),
            'comment': comment
        }
        requests.post(f'{self.api_server}/accounts/{organization_id}/applicants/{applicant_id}/vacancy',
                      headers=self.headers, json=data)



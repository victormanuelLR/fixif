

import requests
from bs4 import BeautifulSoup



def suap_login(username,password):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    url_login = 'https://suap.ifpi.edu.br/accounts/login/'
    url_profile = f'https://suap.ifpi.edu.br/edu/aluno/{username}/'

    user_data = {
        'session': requests.Session(),
        'details': {
            'picture':'',
            'username': '',
            'nickname': '',
            'name': '',
            'course': '',
            'since': '',
            'matriz': '',
            'situation': '',
            'lastLogin':'',
        }
    }

    response = user_data['session'].get(url_login,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']
    payload = {
    'csrfmiddlewaretoken': csrf_token,
    'username': username,
    'password': password
    }

    response = user_data['session'].post(url_login, data=payload,headers=headers)
    if response.status_code != 200:
        return {
            'success': False,
            'error': 'Erro ao conectar no SUAP'
        }
    response = user_data['session'].get(url_profile)
    soup = BeautifulSoup(response.content, 'html.parser')
    if response.url != url_profile or soup.select_one('#content > div.box > div > dl > div:nth-child(9) > dd') == None:
        return {
            'success': False,
            'error': 'Credenciais Incorretas no SUAP'
        }

    
    user_data['details']['name'] = soup.select_one('#content > div:nth-child(3) > div > dl > div:nth-child(1) > dd').get_text()
    user_data['details']['course'] = soup.select_one('#content > div.box > div > dl > div:nth-child(9) > dd').get_text().strip()
    user_data['details']['username'] = username
    user_data['details']['nickname'] = soup.select_one('#user-tools > a.user-profile > span').get_text()
    user_data['details']['since'] = soup.select_one('#content > div.box > div > dl > div:nth-child(3) > dd').get_text().strip()
    user_data['details']['situation'] = soup.select_one('#content > div.box > div > dl > div:nth-child(12) > dd > span').get_text()
    user_data['details']['matriz'] = soup.select_one('#content > div.box > div > dl > div:nth-child(10) > dd').get_text().strip()

    photo = soup.select_one('#content > div.box > div > div > img')
    if photo:
        url = photo.get('src')
        parts = url.split('/')
        nfile = parts[-1]
        user_data['details']['picture'] = f'https://suap.ifpi.edu.br/media/alunos/{nfile}'
    else:
        user_data['details']['picture'] = False
    user_data['success'] = True    
    return user_data
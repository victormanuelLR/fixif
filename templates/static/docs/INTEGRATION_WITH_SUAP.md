# Integração com SUAP

O sistema utiliza **métodos de web scraping** para a obtenção dos dados do usuário, escolha motivada pela maior facilidade de implementação e pela ampla disponibilidade de documentação sobre o assunto, especialmente quando comparado às APIs oficiais do SUAP. Entretanto, há plena consciência das **possíveis falhas no login**, caso a estrutura HTML da página `https://suap.ifpi.edu.br/edu/aluno` seja alterada, o que poderia comprometer a extração correta dos dados.

## Fluxo de Login

O processo de autenticação é iniciado a partir de uma requisição **POST** enviada pelo formulário em **`/account/login/`**, direcionada para a **`LoginView`** (localizada em `apps.core.views`).

### 1. Recebimento e verificação inicial

1. A `LoginView` verifica se o usuário já está autenticado.
2. Caso **não esteja**, o método `dispatch()` é chamado, iniciando o fluxo de autenticação.
3. Os dados do formulário (`username` e `password`) são extraídos de `request.POST`.
4. Esses dados são passados para o método auxiliar `pre_login`, que chama a função `suap_login()` definida em **`core/scrap.py`**.
    

### 2. A função `suap_login()` (`core/scrap.py`)

O módulo `core/scrap` é responsável por realizar o **web scraping no SUAP** para autenticação e coleta de dados do perfil.  
Ele importa as bibliotecas:

- `requests` — para gerenciamento de sessão HTTP;
- [`BeautifulSoup`](https://beautiful-soup-4.readthedocs.io/en/latest/) — para parsing e extração de dados HTML.
    
#### Estrutura interna:

1. **Criação da sessão:**
    
    - `user_data["session"] = requests.Session()`
    - Essa sessão será usada em **todas as requisições subsequentes** para manter cookies e autenticação.
        
2. **Obtenção do CSRF Token:**
    
    - Uma requisição `GET` é enviada para `url_login` usando a sessão (`user_data["session"].get(url_login, headers=headers)`).
    - O conteúdo retornado é convertido em um objeto `BeautifulSoup` (`soup = BeautifulSoup(response.content, 'html.parser')`).
    - O token CSRF é extraído via `soup.find()`.
        
3. **Envio do formulário de login:**
    
    - Um `payload` é criado contendo:
        `{     'csrfmiddlewaretoken': csrf_token,     'username': username,     'password': password }`
    - A sessão envia um `POST` para `url_login`, com `payload` e `headers`.
        
4. **Acesso ao perfil do usuário:**
    
    - Caso a autenticação seja bem-sucedida, a sessão realiza um novo `GET` em `url_profile`.
    - Um novo objeto `BeautifulSoup` é criado com o conteúdo da página do usuário.
        
5. **Validação e extração de dados:**
    
    - É verificado se:
        
        - O `response.url` corresponde ao `url_profile`;
        - O campo do curso não está vazio.
            
    - Caso aprovado, `user_data["details"]` é preenchido com:
        
        - `name`, `course`, `username`, `nickname`, `since`, `situation`, `matriz`.
            
6. **Avatar do usuário:**
    
    - Caso exista uma foto de perfil, `user_data['details']['picture']` recebe a URL correspondente.
    - Caso contrário, permanece vazio.
        

### 3. Retorno à `LoginView`

1. `suap_login()` retorna `user_data` com todas as informações validadas.
2. `LoginView` verifica se já existe um **`UserProfile`** vinculado ao usuário:
    
    - Se **não existir**, o perfil é **criado e populado** com os dados retornados.
    - Se já existir, as informações podem ser **atualizadas**.
        
3. O usuário é então autenticado e redirecionado para o sistema.







# Estrutura dos Views

## 1. `LoginView`

**Localização:** `apps.core.views.LoginView`  
**Herança:** `FormView`  
**Template:** `registration/login.html`  
**Formulário associado:** `AuthenticationForm`

### Principais métodos

#### dispatch 

Garante que apenas usuários **não autenticados** possam acessar a página de login.  
Caso o usuário já esteja autenticado, é redirecionado automaticamente para a URL de sucesso configurada.
##### Fluxo
1.  Verifica se `request.user.is_authenticated` e `self.redirect_authenticated_user` são ambos `True`. 
	- Se sim, redireciona para o caminho, que o método `self.get_success_url` retorna.
	- Se não, retorna o método `dispatch` padrão da superclasse `FormView`.

#### pre_login

Responsável por autenticar um usuário por meio do sistema **SUAP**, validando as credenciais e criando/atualizando seu perfil local conforme necessário.
##### Fluxo

1. Obtém `username` e `password` do corpo do `POST`;
2. Se faltar qualquer um dos dois, retorna `None`;
3. Chama `suap_login(username, password)` (função definida em `core/scrap`) - Para uma melhor detalhação sobre a função, acesse: <a class="docs-content-link" data-index=3>Integração com o SUAP</a>;
4. Caso a autenticação no SUAP falhe (`success=False`), interrompe o processo;
5. Se o login for bem-sucedido:
	- Extrai os **detalhes** do usuário (`name`, `nickname`, `picture`, `course`);
	    - Obtém o **campus** a partir do curso e garante sua existência no banco via:
	        `campus_obj, created = Campus.objects.get_or_create(campus_name=campus)`
	    - Verifica se já existe um `UserProfile` associado ao `suap_username`.
	    
	        - Se **sim**, atualiza os dados com as informações mais recentes do SUAP;
	            
	        - Se **não**, cria tanto o `User` padrão do Django quanto o `UserProfile` correspondente.
	            
	    - Por fim, autentica o usuário no sistema com `auth_login(request, user)`.
	    
6. Retorna o objeto `user` autenticado, ou `None` caso algo falhe.

#### post

Responsável por prevenir o comportamento padrão do `post` do `FormView`, permitindo que a autenticação via SUAP seja tratada antes do fluxo padrão.
##### Fluxo
1. Defini `user`como o retorno de `self.pre_login(request)`.   
2.  Verifica se `user` é diferente de `None`. 
	- Se sim, redireciona para o caminho, que o método `self.get_success_url` retorna.
	- Se não, retorna o método `post` padrão da superclasse `FormView`.

#### get_success_url

Responsável por obter a URL correta do usuário.

##### Fluxo
1. Defini `redirect_to` como o retorno de `self.request.POST.get(self.redirect_field_name)` ou `self.request.GET.get(self.redirect_field_name)`
2. Verifica se `redirect_to` existe e se  `url_has_allowed_host_and_scheme()` confirma que o destino é seguro e pertence ao mesmo host..
	- Se sim, retorna o ``redirect_to``
	- Se não, retorna o valor padrão configurado em `settings.LOGIN_REDIRECT_URL`, ou `"/"` caso a configuração não exista, utilizando `resolve_url()` para garantir que o caminho seja resolvido corretamente.

## 2. `LogoutView` 

**Localização:** `apps.core.views.LoginView`  
**Herança:** `FormView`  
**Template:** `registration/login.html`  

### Principal método

#### get 

Responsável por prevenir o comportamento padrão do `get` do `FormView`, possibilitando  o `logout` .

##### Fluxo 
1. Chama a função logout que recebe um `response`.
2. Retorna chamando o redirect que recebe `'webapp:index'` como parâmetro.

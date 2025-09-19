## FixIF

FixIF é um sistema web desenvolvido por alunos do IFPI para facilitar o registro e acompanhamento de problemas de infraestrutura nos campi.
A plataforma conecta alunos, docentes e coordenadores à equipe de manutenção, garantindo mais organização, transparência e eficiência nos reparos.

## Rodando localmente

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/diaslui/fixif
   ```

2. **Navegue até o diretório do projeto:**
   ```bash
   cd fixif
   ```

3. **Crie um ambiente virtual e ative-o:**
   ```bash
   python3 -m venv venv
   ```
   Se estiver no Windows:
   ```bash
   venv\Scripts\activate
   ```
    Se estiver no macOS/Linux:
    ```bash
    source venv/bin/activate
    ```

4. **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Aplique as migrações do banco de dados:**
    ```bash
    python manage.py migrate
    ```
6. **Rode o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```
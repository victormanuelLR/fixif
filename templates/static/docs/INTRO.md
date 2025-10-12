# FixIF

FixIF é um sistema web desenvolvido por alunos do IFPI para facilitar o registro e acompanhamento de problemas de infraestrutura nos campi.
A plataforma conecta alunos, docentes e coordenadores à equipe de manutenção, garantindo mais organização, transparência e eficiência nos reparos.

O sistema é desenvolvido com o framework [Django](https://www.djangoproject.com/), utilizando [Bootsrap](https://getbootstrap.com/) para a estilização da interface e [PostgreSQL](https://www.postgresql.org/) para persistência dos dados.

## Arquitetura e Stack

Este sistema se integra com a plataforma [SUAP](https://suap.ifpi.edu.br/), utilizando-se de seu mecanismo de autenticação de usuários, permitindo o login unificado e o reconhecimento automático de perfis institucionais (alunos, docentes e técnicos).


## Detalhes do stack e integrações:


- A implementação é feita em [python 3](https://docs.python.org/3/)
- Uso dos framework :
	- [Django](https://www.djangoproject.com/)
	- [Bootsrap](https://getbootstrap.com/)
- A persistência de dados é feita em um banco [PostgreSQL](https://www.postgresql.org/).
- As bibliotecas utilizadas podem ser vistas no arquivo **requirement.txt** localizado na raiz do projeto.
- O sistema usa da biblioteca [Beautiful Soup](https://beautiful-soup-4.readthedocs.io/en/latest/) para obter informações do [SUAP](https://suap.ifpi.edu.br/) através de web scraping
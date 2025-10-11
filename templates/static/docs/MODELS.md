## Estrutura de Models

### Campus

- `campus_name` - Nome do campus (`CharField`)
#### Relações
```mermaid
classDiagram
    class Campus {
		+campus_name
		
    }
    
    class UserProfile
    class Report

    UserProfile --> Campus : ManyToOne (campus)
    Report --> Campus : ManyToOne (campus)
```

### UserProfile

- `user` - Referência ao `User` do Django (`OneToOneField`)
- `campus` - Referência ao campus do IFPI (`ForeignKey` para `Campus`)
- `suap_username` - Nome de usuário único fornecido pelo SUAP (`CharField`)
- `suap_avatar_url` - URL do avatar do usuário no SUAP (`URLField`)
- `suap_nickname` - Apelido ou nome social (`CharField`)
- `suap_full_name` - Nome completo do usuário (`CharField`)
- `suap_course` - Curso ao qual o usuário está vinculado (`CharField`)
- `bio` - Descrição livre do perfil (`TextField`)
#### Relações

```mermaid
classDiagram

    class UserProfile {
		+suap_username
		+suap_avatar_url
		+suap_nickname
		+suap_full_name
		+suap_course
		+bio
    }
    
    class User
	class Campus


    UserProfile --> User : OneToOne (user)
    UserProfile --> Campus : ManyToOne (campus)
```



### Report

- `campus` – Referência ao campus do IFPI (`ForeignKey` para `Campus`).
- `report_user` – Usuário que criou o relatório (`ForeignKey` para `UserProfile`).
- `is_anonim` – Define se o relatório foi enviado anonimamente (`BooleanField`).
- `description` – Descrição detalhada do problema (`TextField`).
- `priority` – Nível de prioridade do problema (`CharField` usando `Report.Priority.choices`).
- `location` – Localização do problema dentro do campus (`CharField`).
- `report_type` – Tipo de problema (`CharField` usando `Report.ProblemType.choices`).
- `report_status` – Estado atual do chamado (`CharField` usando `Report.Status.choices`).
- `assigned_to` – Usuário designado para resolver o problema (`ForeignKey` para `UserProfile`, opcional).
- `attachments` – Arquivo opcional anexado ao relatório (`FileField`).
- `resolved_at` – Data e hora de resolução do chamado (`DateTimeField`, opcional).

#### Choices
- `Priority` - Define as prioridades possíveis do relatório (baixa, média, alta).
- `ProblemType` - Define os tipos de problema (hardware, software, rede, etc).
- `Status` - Define os estados do relatório (aberto, em andamento, resolvido ou fechado).
#### Relações

```mermaid
classDiagram
	
    class Report {
        +is_anonim : Boolean
        +description : TextField
        +priority : Priority
        +location : CharField
        +report_type : ProblemType
        +report_status : Status
        +assigned_to : UserProfile
        +attachments : FileField
        +resolved_at : DateTime
        %% Subclasses internas
        class Priority
        class Status
        class ProblemType
    }
    
    class ReportLike 
    class ReportComment
    class Campus
	class UserProfile

    ReportLike --> Report :  ManyToOne (report)
    ReportComment --> Report : ManyToOne (report)
    Report --> Campus : ManyToOne (campus)
    Report --> UserProfile : ManyToOne (report_user)
    Report --> UserProfile : ManyToOne (assigned_to)
```



### ReportLike

- `user` - Usuário que curtiu o relatório (`ForeignKey` para `User`)
- `report` - Relatório que recebeu a curtida (`ForeignKey` para `Report`)
#### Relações
```mermaid
classDiagram
    class ReportLike {

    }

    class Report
    class User

	ReportLike --> User : ManyToOne (user)
    ReportLike --> Report : ManyToOne (report)
```
### ReportComment

- `report` - Relatório comentado (`ForeignKey` para `Report`)
- `user` - Usuário que fez o comentário (`ForeignKey` para `User`)
- `content` - Texto do comentário (`TextField`)
- `is_anonim` - Indica se o comentário foi feito anonimamente (`BooleanField`)
- `attachment` - Arquivo opcional anexado ao comentário (`FileField`)
#### Relações

```mermaid
classDiagram
    class ReportComment {
        +content : TextField
        +is_anonim : Boolean
        +attachment : FileField
    }

	class CommentLike
    class Report
    class User

    CommentLike --> ReportComment : ManyToOne (comment)
    ReportComment --> Report : ManyToOne (report)
    ReportComment --> User : ManyToOne (user)
```


### CommentLike

- `user` - Usuário que curtiu o comentário (`ForeignKey` para `User`)
- `comment` - Comentário que recebeu a curtida (`ForeignKey` para `ReportComment`)
#### Relações

```mermaid
classDiagram
    class CommentLike {

    }

    class User
    class ReportComment

	CommentLike --> User : ManyToOne (user)
    CommentLike --> ReportComment : ManyToOne (comment)
```

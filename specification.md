# API Portal de notícias

## Requisitos não funcionais

### Obrigatórios

* Python como linguagem back-end
* MongoDB como base de dados

### Opcionais

* Pipeline de build no github
* API publicada no heroku


## Requisitos Funcionais

* Gerência de notícias do portal
    * Criar notícia
    * Editar notícia
    * Excluir notícia
    * Pesquisar notícia
    * Visualizar notícia ???
* Gerência de autores
    * Criar autor
    * Editar autor
    * Excluir autor
    * Pesquisar autor

### Modelos

**Notícia**

    {
        _id: ObjectId,
        title: str,
        content: str,
        created_on: Date(),
        author_id: ObjectId()
    }


**Autor**

    {
        _id: ObjectId,
        name: str
    }


## Testes

* Testes unitários
* Cobertura de testes
* Postman testes

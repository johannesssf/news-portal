# API Portal de notícias

## Requisitos não funcionais

* Python como linguagem back-end
* MongoDB como base de dados


## Requisitos Funcionais

* Gerência de notícias do portal
    * Criar notícia
    * Editar notícia
    * Excluir notícia
    * Pesquisar notícia por palavra-chave (título, conteúdo e author)
    * Visualizar todas as notícia
* Gerência de autores
    * Criar autor
    * Excluir autor
    * Pesquisar autor

### Modelos

**Notícia**

    {
        id: str,
        title: str,
        content: str,
        author_id: str
    }


**Autor**

    {
        id: str,
        name: str
    }


## Testes

* Testes unitários
* Cobertura de testes
* Testes de integração


## Endpoints

### Autores

Recupera todos os autores cadastrados:

    GET:  /authors

Procura um author pelo nome, a pesquisa é *case sensitive* e ela retornará
apenas o author que combina exatamente como o nome pesquisado:

    GET: /author/<name>

Cadastra um novo autor utilizando seu nome, não podem existir nomes repetidos:

    POST: /author/<name>

Exclui um author pelo seu nome que é *case sensitive*:

    DELETE: /author/<name>

### Notícias

Existem duas formas de pesquisa, se não for passada a chave de busca, todas as
notícias serão retornadas pela consulta e, caso ela seja informada, a pesquisa
retornará apenas as notícias que contenham a palavra chave no título, conteúdo
ou no nome do autor:

    GET: /news/search
    GET: /news/search?search_key=<palavra>

Cadastro de notícias, enviar os campos título, conteúdo e id do autor,
todos os campos são obrigatórios:

    POST: /news

Editar notícias, ela deve ser identificada pelo seu id e os mesmos campos do
cadastro podem ser alterados, todos são obrigatórios mas, caso não possuam
conteúdo, a informação anterior será preservada:

    PUT: /news/<id>

Excluir notícias, ela deve ser identificada pelo seu id:

    DELETE: /news/<id>


## Rodando os testes localmente

1- Subir um servidor mongo (sugestão: um container docker):

    docker run --rm --name mongo-server -p 27017:27017 -d mongo:latest

2- Instalar os pacotes necessários (pode-se utilizar um ambiente virtual):

    pip install -r requirements.txt

3- Subir a aplicação Portal de Notícias:

    cd code
    python app.py

4- Executar os testes unitários:

    coverage run testes.py
    coverate report

5- Executar os testes de integração:

    pytest integration_tests.py

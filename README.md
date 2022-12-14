# Demonstração de Api Rest para cadastro de alunos e notas

### O QUE É

Um projeto para mostrar o desenvolvimento de uma Api Rest com Python/Django/Django Rest Framework, possibilitando o
cadastro de alunos e suas respectivas matérias e notas

### A QUEM SE DESTINA / OBJETIVO

* Este projeto destina aos interessados em ver como funciona uma APi Rest pode simples de ser criada, documentada e com
  segurança nos dados

### INSTALAÇÃO LOCAL

* Em seu PC baixe o projeto usando `git clone https://github.com/wagnerrafa/student_system` ou baixando no formato zip e
  extraindo;
* `python -m venv` na raiz do diretório do projeto para isolar seu ambiente;

> Windows
>* `.\\venv\\Scripts\\activate`

> Linux
>* `source venv/bin/activate`

* `pip install -r requirements.txt` para instalar as dependências necessárias para o projeto;

### USO LOCAL

* `python manage.py makemigrations` para analisar as mudanças feitas nos modelos e gerar as migrações para o banco de
  dados
* `python manage.py migrate` para aplicar as migrações feitas no makemigrations
* `python manage.py runserver` para inicializar o servidor
* Acesse a documentação na url http://127.0.0.1:8000/api/v1/docs/
* De início terá apenas a documentação para a criação de um usuário utilizando o método POST. Após a criação do usuário,
  pode atualizar a página e será mostrada as demais documentações, podendo iterar com a api diretamente por essa
  documentação, bem como ver os modelos, schema, parâmetros, formato de envio e respostas
* #### Adicionais
    * `python manage.py test` para realizar os testes e ver como é a iteração das chamadas de Apis com o servidor
    * `python manage.py fake_database` para usar o terminal com instruções SQL já implementas, entregando uma lista de
      opções para inserção de valores e consultas nas tabelas

* Na raiz do projeto crie um arquivo com o nome ".env". Dentro dele coloque o texto "DEBUG=True" para ativar o modo
  debug

### BIBLIOTECAS DO PROJETO

* Django e Django Rest Framework para a criação das apis, gerenciamento do banco de dados

* Banco de dados Sqlite para o desenvolvimento por não precisar de nenhuma configuração adicional, e MySQL no servidor
  Heroku

#### Muito obrigado pela atenção

Para ver o resultado acesse o site https://sistema-alunos.herokuapp.com/

#### SOBRE O AUTOR

* Wagner Oliveira
* Desenvolvedor Full Stack
* https://www.linkedin.com/in/wagner-rafael/
* wagner_rafa@hotmail.com.br

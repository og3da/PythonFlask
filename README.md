# PythonFlask
repositório para o curso que estou fazendo na Udemy "REST APIs com Python e Flask"
link do curso: https://www.udemy.com/course/rest-apis-com-python-e-flask

<h2>Introdução</h2>
Nesse curso estamos desenvolvendo uma API REST "Hoteis". Essa API realiza as seguintes ações:
- GET de todos Hoteis
- GET de hoteis especificos
- POST de novos hoteis
- PUT para atualizar informações de hoteis existentes
- DELETE para deletar hoteis

ou seja, basicamente essa API faz um CRUD de informações de Hoteis.

<h2>SEÇÃO 6 - API REST com CRUD em memória</h2>
Nessa seção foi dado início ao desenvolvimento da API REST "Hoteis" com possibilidade de fazer CRUD
gravando os dados em memória. 

<h2>SEÇÃO 7 - API REST com CRUD em banco de dados SQLite</h2>
Nessa seção estamos aprimorando o código e dessa vez usando um banco de dados.

<h2>SEÇÃO 8 - AUTENTICAÇÃO DE USUARIOS COM JWT</h2>
Nessa seção foi implementada autenticação de usuarios da API com JWT, as funcionalidades são Cadastro, Login e Logout.
Também qualquer requisição que envolve alteração no Banco de dados como POST, PUT e DELETE solicitam um usuário logado.
Esse login é feito através de um AccessToken gerado pelo JWT e ao fazer logout esse token é invalidado.

<h2>SEÇÃO 9 - FILTROS AVANÇADOS COM PARAMETROS DE CONSULTA</h2>
Nessa seção implementamos no código consultas SQL para possibilitar filtros ao fazer o request.
Por exemplo caso queira filtrar os hoteis por estrelas, cidade, diaria, agora é possível.
![image](https://github.com/og3da/PythonFlask/assets/71846924/575281c5-04fd-4597-bf90-be458c447d68)

# Trabalho Prático de Testes de Software

Grupo:
 - Eduardo Henrique Dias Melgaço
 - Lucas Starling de Paula Salles
 - Lucas Caetano Lopes Rodrigues

# Divide-Esperto

O Divide-Esperto é um sistema para o cálculo de divisão de despesas em grupo inspirado no SplitWise.
O sistema é capaz de criar grupos de pessoas, adicionar despesas, e dividí-las entre os membros do grupo.

As despesas podem ser divididas de três formas:
 - Divisão igual para cada membro do grupo
 - Divisão para cada membro do grupo baseado em uma porcentagem do valor total
 - Divisão para cada membro do grupo baseado em quanto cada membro pagou do valor total

Para interagir com o sistema, o usuário deve fazê-lo através da CLI.

```sh
$ pwd
/path/to/repository/divide-esperto
$ python -m src.main
Welcome! Type ? to list available commands
divide> adduser Lucas
User 'Lucas' added
divide> adduser Eduardo
User 'Eduardo' added
divide> addexpense
addexpense> type (one of equal, percentage, value): equal
addexpense> total value: 100
addexpense> description: test expense
addexpense> paid by: 1
addexpense> used by: 1 2
divide> get_user_balance 1
Overall situation of Lucas:
	You are owed 50.0
Balance by user:
	Eduardo owes you a total of 50.0

divide> get_user_balance 2
Overall situation of Eduardo:
	You owe 50.0
Balance by user:
	You owe a total of 50.0 to Lucas
divide> exit
Exiting
```

Para executar os testes unitários, utilize `coverage run -m unittest tests/*_tests.py`
Para isso, você precisa instalar as dependências do sistema:

```sh
$ pwd
/path/to/repository/divide-esperto
$ python3 -m venv virtualenv
$ source virtualenv/bin/activate
$ pip install -r requirements.txt
```

# Tecnologias utilizadas

Para desenvolver o sistema, utilizamos Python 3.7+. Para desenvolver a interface de CLI, utilizamos a biblioteca padrão do Python [CMD](https://docs.python.org/3/library/cmd.html). 
Os testes unitários foram escritos utilizando [Unittest](https://docs.python.org/3/library/unittest.html), e a ferramenta [Coverage](https://coverage.readthedocs.io/en/6.4/) é utilizada para gerar relatórios dos testes unitários.

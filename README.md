# Microserviço: produto premium

<p float="left">

 <img src="https://user-images.githubusercontent.com/59067501/267109015-98556724-6c57-4212-9d5f-36a9a0b20426.jpg" width="600" />

O objetivo da aplicação é trazer, em uma única tela interativa, o setor de previsões premium da aplicação Let Me Sea. Dados como temperatura da água, temperatura do dia e localização da praia compõe as previsões premium, que rendem aos usuários que colaborarem a participação em sorteios.

O objetivo principal é estimular o compartilhamento de informações premium e facilitar a escolha do wetsuit do dia. 

---
## Como executar 


Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.

Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```

Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

## Como executar através do Docker


Certifique-se de ter o Docker instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile e o requirements.txt no terminal. Execute como administrador o seguinte comando para construir a imagem Docker:

```
(env)$ docker build -t componente-b .
```

Uma vez criada a imagem, para executar o container basta executar, como administrador, seguinte o comando:

```
(env)$ docker run -p 5000:5000 componente-b
```

Uma vez executando, para acessar a API, basta abrir o [http://localhost:5000/#/](http://localhost:5002/#/) no navegador para verificar o status da API em execução.

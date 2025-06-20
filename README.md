# Weather API Wrapper Service

Este é um serviço de wrapper de API de clima, construído em Python com Flask. Ele consome a API da Visual Crossing, otimiza as respostas e implementa um sistema de cache com Redis para melhorar a performance e reduzir o número de chamadas externas.

Este projeto foi desenvolvido como parte do [Backend Roadmap]([https://roadmap.sh/backend](https://roadmap.sh/projects/weather-api-wrapper-service)).

## Tecnologias Utilizadas

* [Python 3.11+](https://www.python.org/)
* [Flask](https://flask.palletsprojects.com/)
* [Redis](https://redis.io/)
* [Docker](https://www.docker.com/)
* [python-dotenv](https://pypi.org/project/python-dotenv/)
* [requests](https://pypi.org/project/requests/)

## Pré-requisitos

Antes de começar, você vai precisar ter instalado em sua máquina:

* Python 3.9 ou superior
* Docker e Docker Compose

## Como Rodar o Projeto

Siga os passos abaixo para executar o projeto localmente:

1. **Clone o repositório:**

    ```bash
    git clone https://URL_DO_SEU_REPOSITORIO.git
    cd nome-da-pasta-do-projeto
    ```

2. **Crie e ative o ambiente virtual:**

    ```bash
    # Criar
    python -m venv venv
    # Ativar (Mac/Linux)
    source venv/bin/activate
    # Ativar (Windows)
    .\venv\Scripts\activate
    ```

3. **Instale as dependências:**

    Instale o arquivo `requirements.txt` com:

    ```bash
    pip install -r requirements.txt
    ```

4. **Inicie o container do Redis:**

    ```bash
    docker run --name meu-redis -p 6379:6379 -d redis
    ```

5. **Configure as variáveis de ambiente:**

    Crie uma cópia do arquivo `.env.example` e renomeie para `.env`. Em seguida, preencha a variável `API_KEY` com sua chave da [Visual Crossing API](https://www.visualcrossing.com/weather-api/).

    ```bash
        cp .env.example .env
    ```

6. **Rode a aplicação:**

    ```bash
    flask run
    # ou
    python app.py
    ```

    O servidor estará disponível em `http://127.0.0.1:5000`.

## Como Usar a API

### Buscar Clima por Cidade

Retorna os dados de clima atuais e do dia para a cidade especificada.

* **URL:** `/clima/<nome_da_cidade>`
* **Método:** `GET`
* **Exemplo:**

    ```bash
    curl [http://127.0.0.1:5000/clima/lisboa](http://127.0.0.1:5000/clima/lisboa)
    ```

* **Resposta de Sucesso (200 OK):**

    ```json
    {
      "condicao_clima": "Partly Cloudy",
      "endereco_resolvido": "Lisboa, Portugal",
      "nascer_do_sol": "06:11:53",
      "por_do_sol": "20:55:04",
      "sensacao_termica_c": 25.0,
      "temp_atual_c": 25.0,
      "temp_max_hoje_c": 27.1,
      "temp_min_hoje_c": 17.0,
      "umidade_percentual": 57.8
    }
    ```

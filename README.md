# CAA Board - Comunicação Aumentativa e Alternativa

Este repositório contém o projeto CAA Board. Ele foi dividido em duas partes independentes: o **Backend** (API) e o **Frontend** (Interface do Usuário).

Esta separação permite que o board seja executado localmente sem a necessidade de um servidor web complexo para o frontend, facilitando o uso e a distribuição.

## Estrutura do Projeto

*   `backend/`: Contém a API REST construída em Python com Flask. Responsável por gerenciar os usuários, cards, layouts de boards e autenticação.
*   `frontend/`: Contém a interface do usuário construída com HTML, CSS e JavaScript puros. Comunica-se intimamente com a API do backend.

---

## 1. Como Subir o Backend (API)

O backend precisa estar rodando para que o frontend consiga salvar os dados, registrar usuários e carregar os cards.

### Pré-requisitos
*   [Python 3](https://www.python.org/downloads/) instalado na sua máquina.

### Executando Localmente no Windows

1.  Abra o terminal (PowerShell ou Prompt de Comando) e navegue até a pasta do projeto:
    ```bash
    cd caminho\para\CAA_Board\backend
    ```

2.  *(Opcional, mas recomendado)* Crie e ative um ambiente virtual:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate
    ```

3.  Instale as dependências necessárias:
    ```bash
    pip install -r requirements.txt
    ```

4.  Inicialize o banco de dados com as configurações e os cards padrão:
    ```bash
    python init_db.py
    ```

5.  Inicie o servidor do backend:
    ```bash
    python run.py
    ```
    O servidor estará rodando em `http://127.0.0.1:5000/`. Você pode acessar este link no seu navegador para ver a tela de confirmação de que o backend está online.

---

## 2. Como Abrir o Frontend (Páginas)

O frontend foi projetado para ser executado de forma extremamente simples, sem a necessidade de iniciar outro servidor (como o Node.js).

### Executando Localmente

1.  Com o **Backend rodando** como descrito no passo anterior, abra a pasta do projeto no seu Explorador de Arquivos do Windows.
2.  Entre na pasta `frontend`.
3.  Dê um **duplo clique** no arquivo `index.html`.
4.  O seu navegador padrão (Chrome, Edge, Firefox) abrirá a página. 

*Nota: Na primeira vez que abrir, você precisará clicar no botão "Registrar" no topo para criar a sua conta.*

## Resolvendo Problemas Comuns

*   **A página abre, mas os botões de API e o carregamento infinito acontecem:** 
    Verifique se o terminal rodando o `python run.py` (na pasta `backend/`) não foi fechado ou se houve algum erro de carregamento (você pode verificar o terminal para consultar as mensagens).

*   **Os cards padrão não apareceram depois de registrar uma conta:**
    Certifique-se de que de fato executou o arquivo `python init_db.py` antes de rodar a sua aplicação com `python run.py`.

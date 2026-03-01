
---

# **Pegasus Sports com PostgreSQL**

Este projeto implementa a aplicação **Pegasus-Sports** com integração ao banco de dados **PostgreSQL**.

---

## **Passo 1: Comandos do Banco de Dados (PostgreSQL)**

1. **Apagar o Banco de Dados (se existir)**

   Execute o seguinte comando para apagar o banco de dados **pegasus_db**, se ele já existir:

   ```bash
   "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "DROP DATABASE IF EXISTS pegasus_db;"
   ```

2. **Criar o Banco de Dados**

   Agora, crie o banco de dados **pegasus_db**:git push origin main

   ```bash
   "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "CREATE DATABASE pegasus_db;"
   ```

3. **Verificar se o Banco foi Criado**

   Para verificar se o banco foi criado corretamente, execute:

   ```bash
   "C:\Program Files\PostgreSQL\18\bin\psql.exe" -U postgres -c "\l" | findstr pegasus_db
   ```

---

## **Passo 2: Configuração do Ambiente Virtual (venv)**

1. **Criar o Ambiente Virtual**

   No diretório do seu projeto, execute:

   ```bash
   python -m venv venv
   ```

2. **Ativar o Ambiente Virtual**

   Para ativar o ambiente virtual, execute:

   **Windows (PowerShell):**

   ```bash
   .\venv\Scripts\Activate
   ```

---

## **Passo 3: Instalar as Dependências**

1. **Instalar as Dependências do Projeto**

   No ambiente virtual, instale as dependências necessárias com o comando:

   ```bash
   pip install -r requirements.txt
   ```

---

## **Passo 4: Executar o Aplicativo**

1. **Iniciar o Servidor Flask**

   Após instalar as dependências, inicie o servidor Flask com o comando:

   ```bash
   python app.py
   ```

   O servidor estará disponível em **[http://localhost:5000](http://localhost:5000)**.

---

## **Passo 5: Teste dos Endpoints**

Agora, você pode testar os endpoints da API usando **Postman** ou **Insomnia**.

---

### **1. Criar um Novo Agendamento (POST)**

* **URL**: `http://localhost:5000/agendamentos/`

* **Método**: POST

* **Body (JSON)**:

  ```json
  {
    "nome": "João Silva",
    "telefone": "11999999999",
    "email": "joao@email.com",
    "veiculo": "Fusca",
    "servico": "Revisão",
    "dataPreferencial": "2025-04-15",
    "horarioPreferencial": "09:00",
    "mensagem": "",
    "status": "pendente"
  }
  ```

* **Resposta Esperada**:

  ```json
  {
    "message": "Agendamento criado com sucesso!",
    "agendamento": {
      "id": 1,
      "nome": "João Silva",
      "telefone": "11999999999",
      "email": "joao@email.com",
      "veiculo": "Fusca",
      "servico": "Revisão",
      "dataPreferencial": "2025-04-15",
      "dataFormatada": "15/04/2025",
      "horarioPreferencial": "09:00",
      "mensagem": "",
      "status": "pendente"
    }
  }
  ```

---

### **2. Listar Todos os Agendamentos (GET)**

* **URL**: `http://localhost:5000/agendamentos/`

* **Método**: GET

* **Resposta Esperada**:

  ```json
  [
    {
      "id": 1,
      "nome": "João Silva",
      "telefone": "11999999999",
      "email": "joao@email.com",
      "veiculo": "Fusca",
      "servico": "Revisão",
      "dataPreferencial": "2025-04-15",
      "dataFormatada": "15/04/2025",
      "horarioPreferencial": "09:00",
      "mensagem": "",
      "status": "pendente"
    }
  ]
  ```

---

### **3. Buscar um Agendamento pelo ID (GET)**

* **URL**: `http://localhost:5000/agendamentos/{id}`

  * Substitua `{id}` pelo ID do agendamento que você deseja buscar.

* **Método**: GET

* **Resposta Esperada**:

  ```json
  {
    "id": 1,
    "nome": "João Silva",
    "telefone": "11999999999",
    "email": "joao@email.com",
    "veiculo": "Fusca",
    "servico": "Revisão",
    "dataPreferencial": "2025-04-15",
    "dataFormatada": "15/04/2025",
    "horarioPreferencial": "09:00",
    "mensagem": "",
    "status": "pendente"
  }
  ```

---

### **4. Atualizar um Agendamento pelo ID (PUT)**

* **URL**: `http://localhost:5000/agendamentos/{id}`

  * Substitua `{id}` pelo ID do agendamento que você deseja atualizar.

* **Método**: PUT

* **Body (JSON)**:

  ```json
  {
    "status": "confirmado"
  }
  ```

* **Resposta Esperada**:

  ```json
  {
    "message": "Agendamento atualizado com sucesso!",
    "agendamento": {
      "id": 1,
      "nome": "João Silva",
      "telefone": "11999999999",
      "email": "joao@email.com",
      "veiculo": "Fusca",
      "servico": "Revisão",
      "dataPreferencial": "2025-04-15",
      "dataFormatada": "15/04/2025",
      "horarioPreferencial": "09:00",
      "mensagem": "",
      "status": "confirmado"
    }
  }
  ```

---

### **5. Excluir um Agendamento pelo ID (DELETE)**

* **URL**: `http://localhost:5000/agendamentos/{id}`

  * Substitua `{id}` pelo ID do agendamento que você deseja excluir.

* **Método**: DELETE

* **Resposta Esperada**:

  ```json
  {
    "message": "Agendamento deletado com sucesso!",
    "agendamento": {
      "id": 1,
      "nome": "João Silva",
      "telefone": "11999999999",
      "email": "joao@email.com",
      "veiculo": "Fusca",
      "servico": "Revisão",
      "dataPreferencial": "2025-04-15",
      "dataFormatada": "15/04/2025",
      "horarioPreferencial": "09:00",
      "mensagem": "",
      "status": "confirmado"
    }
  }
  ```

---

### **6. Verificar Horários Disponíveis em uma Data (GET)**

* **URL**: `http://localhost:5000/agendamentos/horarios-disponiveis/{data}`

  * Substitua `{data}` pela data desejada no formato `YYYY-MM-DD`.

* **Método**: GET

* **Resposta Esperada**:

  ```json
  [
    {
      "horario": "08:00",
      "disponivel": true,
      "vagas_restantes": 3
    },
    {
      "horario": "09:00",
      "disponivel": false,
      "vagas_restantes": 0
    },
    ...
  ]
  ```

---

### **Passo 6: Configuração do Banco de Dados (PostgreSQL)**

1. **Configurar a String de Conexão no Arquivo `config.py`:**

   No arquivo `config.py`, verifique a string de conexão com o PostgreSQL:

   ```python
   class Config:
       SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123456@localhost/pegasus_db'
       SQLALCHEMY_TRACK_MODIFICATIONS = False
   ```

   Onde:

   * **Username**: `postgres`
   * **Password**: `123456`
   * **Host**: `localhost`
   * **Database**: `pegasus_db`

---

Pronto! Agora você tem um **README** mais organizado e fácil de seguir, com todos os passos necessários para rodar a aplicação e testar os endpoints da API com **Postman** ou **Insomnia**.

Se precisar de mais ajustes ou explicações, estou à disposição!

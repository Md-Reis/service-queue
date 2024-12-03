# service-queue
API para Fila de Atendimento Presencial

API desenvolvida através do fastAPI conteudo os seguintes recursos

@app.get("/fila") - Retorna todos os clientes que estão aguardando para ser atendidos

@app.get("/fila/{id}") - Retorna os dados de atendimento de um cliente conforme a sua posição no atendimento

@app.post("/fila") - Adiciona um novo cliente a fila

@app.put("/fila") - Atualiza a fila de atendimento, chamando o cliente da primeira posição

@app.delete("/fila/pos/{pos}") - Remove um cliente da fila, conforme a posição informada

@app.delete("/fila/pos/{id}") - Remove um cliente da fila, conforme o seu numero de identificação

O repositorio tambem conta com uma base teste (painel.py) que simula um atendimento real utilizando a API para que possa ser testado.
O mesmo simula um banco de dados (em memoria) hospedado em um servido através do Uvicorn.

Para testar a API, baixe os arquivos, instale as bibliotecas de requirements.txt e execute o arquivo "painel.py"

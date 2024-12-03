from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime

app = FastAPI()

class Cliente(BaseModel): #modelo base para os clientes da fila
    nome: str =  Field(..., max_length=20) #limita o nome a 20 caracteres
    tipo_atendimento: str
    
fila_atendimento = [] #fila de atendimento do tipo lista com o padrão cliente

def gera_id_automatico():
    if fila_atendimento:
        id_maior = max([cliente['id_cliente'] for cliente in fila_atendimento]) + 1
    else:
        id_maior = 1
    return id_maior

def obter_data_entrada():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.get("/fila") #exibe todos os clientes na fila que ainda nao foram atendidos
def exibe_fila():
    if len(fila_atendimento) == 0:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail="Lista Vazia!")

    return [{"posicao": index, "ID": cliente['id_cliente'], "nome": cliente['nome'], "data_entrada": cliente['data_entrada']}
        for index, cliente in enumerate(fila_atendimento) if not cliente['atendido']]

@app.get("/fila/{id}") #recupera os dados de um cliente na posição (id) dele.
def obter_cliente(id: int):
    if id < 0 or id >= len(fila_atendimento):
        raise HTTPException(status_code=404, detail="Cliente não encontrado na posição especificada.")
    cliente = fila_atendimento[id]

    return {"posicao": id, "nome": cliente['nome'], "data_entrada": cliente['data_entrada']}

@app.post("/fila") # Adiciona um novo cliente a fila e organiza por prioridade
def adiciona_cliente(cliente: Cliente):
    pos: int = 0
    id = gera_id_automatico()
    data_entrada = obter_data_entrada()
    novo_cliente = {
        "id_cliente": id,
        "nome": cliente.nome,
        "tipo_atendimento": cliente.tipo_atendimento,
        "atendido": False,
        "data_entrada": data_entrada
    }
    if cliente.tipo_atendimento not in ['N','P']: #valida se a entrada do tipo de atendimento é normal ou prioritario
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Tipo de atendimento invalido. O tipo de atendimento deve ser (N) para normal ou (P) para prioritarios.)")
    if not fila_atendimento:
        fila_atendimento.append(novo_cliente)
    else:
        index = [index for index, atend in enumerate(fila_atendimento) if atend["atendido"] == False]
        if not index:
            fila_atendimento.insert(1, novo_cliente)
        else:
            if cliente.tipo_atendimento == "P":
                index = [index for index, tipo in enumerate(fila_atendimento) if tipo["tipo_atendimento"] == "N" and fila_atendimento[index]["atendido"] != True]
                if index:
                    fila_atendimento.insert(index[0], novo_cliente)
                    pos = index[0]
            else:
                if not fila_atendimento or len(fila_atendimento) == 1:
                    pos = len(fila_atendimento)
                    fila_atendimento.append(novo_cliente)
                else:
                    index = [index for index, atendido in enumerate(fila_atendimento) if atendido["atendido"] and index != 0]
                    if index:
                        fila_atendimento.insert(index[0], novo_cliente)
                        pos = index[0]
                    else:
                        pos = len(fila_atendimento)
                        fila_atendimento.append(novo_cliente) 
                        
    return {"pos": pos, "id_cliente": id, "nome": cliente.nome, "tipo_atendimento": cliente.tipo_atendimento,
            "atendimento": False, "data_entrada": data_entrada}

@app.put("/fila")
def atualiza_fila_atendimento(): # Atualiza a fila de atendimento
    cliente_atendido: bool = False
    if not fila_atendimento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Fila Vazia!")
    
    for index in range(len(fila_atendimento)):
        if fila_atendimento[0]['atendido'] == False:
            fila_atendimento[0]['atendido'] = True
            cliente_atendido = fila_atendimento[0]['nome']
            break
        else:
            fila_atendimento.append(fila_atendimento[0])
            fila_atendimento.pop(0)
    
    if not cliente_atendido: mensagem = "Todos os clientes já foram atendidos." 
    else: mensagem = f"Cliente {cliente_atendido} foi atendido." 
    
    return fila_atendimento, {"mensagem": f"{mensagem} Fila atualizada!"}

@app.delete("/fila/pos/{pos}") # Deleta um cliente da fila de atendimento conforme posição
def remove_cliente(pos: int):
    if pos <0 or pos >= len(fila_atendimento): #verifica se o id esta dentro da quantidade de clientes
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cliente não encontrado!")
    else:
        cliente_removido = fila_atendimento[pos]['nome']
        fila_atendimento.pop(pos)

    return {"mensagem": f"Cliente {cliente_removido} removido da fila."}

@app.delete("/fila/id/{id}") # Deleta um cliente da fila de atendimento conforme ID
def remove_cliente(id: int):
    index = [index for index, cliente in enumerate(fila_atendimento) if cliente['id_cliente'] == id]
    if index:
        cliente_removido = fila_atendimento[index[0]]['nome']
        fila_atendimento.pop(index[0])
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cliente não encontrado!")

    return {"mensagem": f"Cliente {cliente_removido} removido da fila."}

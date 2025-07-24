import json
from sistema_clinica.modelos import Paciente,Medico,Consulta
from sistema_clinica.funcoes_auxiliares import dados_pacientes,dados_medicos,dados_consulta

# FUNÇÕES JSON #

def salvar_arquivo(caminho,dados):
    with open(caminho,'w',encoding = 'utf-8') as arquivo:
        json.dump(dados,arquivo,ensure_ascii = False,indent = 4)

def carregar_arquivo(caminho):
    try:
        with open(caminho,'r',encoding='utf-8') as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return {"pacientes": [], "medicos" : [], "consultas" : []}    

def inicializar_dados_ao_abrir_o_app():
    dados_json = carregar_arquivo("dados.json")

    for p in dados_json["pacientes"]:

        paciente = Paciente(p["nome"], p["cpf"], p["telefone"])
        dados_pacientes.append(paciente)

    for m in dados_json["medicos"]:
        
        medico = Medico(m["nome"], m["cpf"], m["telefone"], m["especialidade"], m["crm"])
        dados_medicos.append(medico)

    for c in dados_json["consultas"]:

        paciente = next((p for p in dados_pacientes if p.cpf == c["paciente"]), None)
        medico = next((m for m in dados_medicos if m.crm == c["medico"]), None)

        if paciente and medico:

            consulta = Consulta(paciente, medico, c["data"], c["hora"], c["exame"], c["id"])
            dados_consulta.append(consulta)

def salvar_dados_ao_fechar_o_app():
    dados_para_salvar = {
        "pacientes": [{"nome": p.nome, "cpf": p.cpf, "telefone": p.telefone} for p in dados_pacientes],
        "medicos":   [{"nome": m.nome,"cpf":  m.cpf,"telefone": m.telefone,"especialidade": m.especialidade,"crm": m.crm} for m in dados_medicos],
        "consultas": [{"id":   c.id, "paciente": c.paciente.cpf, "medico": c.medico.crm,"data": c.data,"hora": c.hora,"exame": c.exame, "status": c.status } for c in dados_consulta]
        }
    
    salvar_arquivo("dados.json", dados_para_salvar)


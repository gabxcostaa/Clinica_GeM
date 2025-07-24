from sistema_clinica.dados import (valores_comuns,valores_medico,dados_medicos,dados_pacientes,dados_consulta,dados,campos_comuns,campos_medico)
from sistema_clinica.modelos import Paciente, Medico, Consulta
from sistema_clinica.funcoes_auxiliares import validar_dado,verificar_se_tem_pessoas,validar_cpf_crm,validar_data_hora,validar_exame_por_especialidade,validar_id,exibir_tabela,exibir_tabela_consulta,validar_busca_ou_remover_pessoa,validar_busca_ou_remover_consulta,frase_voltar_limpar

# CRUD PACIENTE & MÉDICO #

def adicionar_pessoa(tipo_pessoa):
  
    campos = valores_comuns + valores_medico if tipo_pessoa == "médico" else valores_comuns

    for campo, padrao, correcao in campos:
        dados[campo] = validar_dado(tipo_pessoa, campo, padrao, correcao)
   
    if tipo_pessoa == "paciente":
        paciente = Paciente(dados["nome"], dados["cpf"], dados["telefone"])
        dados_pacientes.append(paciente)

    elif tipo_pessoa == "médico":
        medico = Medico(dados["nome"], dados["cpf"], dados["telefone"], dados["especialidade"], dados["crm"])
        dados_medicos.append(medico)

    frase_voltar_limpar(f"✅ Todas as informações do {tipo_pessoa} foram cadastradas com sucesso!",f"voltar a Gerenciar {tipo_pessoa.capitalize()}")

def ver_tabela(tipo_pessoa):

    campos = campos_comuns | campos_medico if tipo_pessoa == "médico" else campos_comuns
  
    if tipo_pessoa == "paciente":
        exibir_tabela(dados_pacientes,tipo_pessoa,campos)
    if tipo_pessoa == "médico":
        exibir_tabela(dados_medicos,tipo_pessoa,campos)

def buscar_pessoa(tipo_pessoa):
    campos = campos_comuns | campos_medico if tipo_pessoa == "médico" else campos_comuns
    
    if tipo_pessoa == "paciente":
        validar_busca_ou_remover_pessoa(tipo_pessoa,"cpf",dados_pacientes,r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$',"CPF deve ser no formato : XXX.XXX.XXX-XX",campos)
    if tipo_pessoa == "médico":
        validar_busca_ou_remover_pessoa(tipo_pessoa,"crm",dados_medicos,r'^\d{4,7}-?[A-Z]{2}$', "CRM deve ser no formato : 4-7 dígitos, hífen, e UF em letras maiúsculas. Exemplo : XXXXX-UF",campos)

def remover_pessoa(tipo_pessoa):
    campos = campos_comuns | campos_medico if tipo_pessoa == "médico" else campos_comuns
    
    if tipo_pessoa == "paciente":
        validar_busca_ou_remover_pessoa(tipo_pessoa,"cpf",dados_pacientes,r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$',"CPF deve ser no formato : XXX.XXX.XXX-XX",campos,True)
    if tipo_pessoa == "médico":
        validar_busca_ou_remover_pessoa(tipo_pessoa,"crm",dados_medicos,r'^\d{4,7}-?[A-Z]{2}$', "CRM deve ser no formato : 4-7 dígitos, hífen, e UF em letras maiúsculas. Exemplo : XXXXX-UF",campos,True)
       
# CRUD CONSULTA #

def adicionar_consulta():

    if not verificar_se_tem_pessoas():
        return
   
    paciente = validar_cpf_crm("cpf", r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$', "CPF deve ser no formato : XXX.XXX.XXX-XX") # Pegando paciente pelo CPF #
    medico= validar_cpf_crm("crm", r'^\d{4,7}-?[A-Z]{2}$', "CRM deve ser no formato : 4-7 dígitos, hífen, e UF em letras maiúsculas. Exemplo : XXXXX-UF") # Pegando Médico pelo CRM #
    data = validar_data_hora("data",r'^(0?[1-9]|[12][0-9]|3[01])/(0?[1-9]|1[0-2])/\d{4}$',"A data deve ser no padrão : DD/MM/AAAA")
    hora = validar_data_hora("hora",r'^(6|[7-9]|1[0-9]|2[0-2]):(00|15|30|45)$',"A hora deve ser no padrão : HH/MM (06h até as 22h)",data)
    exame = validar_exame_por_especialidade(medico.especialidade)
    id = validar_id()

    consulta = Consulta(paciente,medico,data,hora,exame,id)
    dados_consulta.append(consulta)  

    frase_voltar_limpar("✅ Todas as informações da Consulta foram cadastradas com sucesso!","voltar a Gerenciar Consulta")  

def ver_tabela_consulta():
    exibir_tabela_consulta(dados_consulta)
    
def buscar_consulta():
    validar_busca_ou_remover_consulta()      
    
def remover_consulta():
    validar_busca_ou_remover_consulta(True,False) 
    
def atualizar_consulta():
    validar_busca_ou_remover_consulta(False,True)
    
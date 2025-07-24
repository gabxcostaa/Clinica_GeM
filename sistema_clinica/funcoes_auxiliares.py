import os,time,re,random
from sistema_clinica.dados import (especialidade_e_exame,dados_pacientes,dados_medicos,dados_consulta)
from datetime import datetime
from sistema_clinica.manipulacao_json import salvar_dados_ao_fechar_o_app

# FUNÇÕES PACIENTE & MÉDICO #

def validar_dado(tipo_pessoa, dado, padrao, correcao):
    while True:
        if dado == "especialidade":

            print("\n🩺 Especialidades disponíveis \n")
            for especialidade, dados in especialidade_e_exame.items():
                print(f"[{dados['id']}] {dados['emoji_especialidade']} {especialidade}")

            try:
                especialidade_input = int(input("\n⚕️  Especialidade do médico : ").strip())

            except ValueError:
                frase_sleep_limpar("❌ Digite um número válido.",2)
                continue

            especialidade_nome = next((especialidade for especialidade, dados in especialidade_e_exame.items() if dados['id'] == especialidade_input),None)

            if especialidade_nome is None:
                frase_sleep_limpar("❌ Especialidade inválida. Tente novamente.",2)
                continue

            dado_pessoa = especialidade_nome
            limpa_tela()

        else:
            # Para os outros dados, pede a entrada normalmente #
            dado_pessoa = input(f"📝 {dado.capitalize()} do {tipo_pessoa.lower()} : ").strip()
            limpa_tela()

            # Verifica se está vazio #
            if not dado_pessoa:
                frase_sleep_limpar(f"⚠️  O {dado} é obrigatório!",2)
                continue

            # Verifica se está no padrão #
            if not re.fullmatch(padrao, dado_pessoa):
                frase_voltar_limpar(f"❌ {correcao}",f"voltar a validar o {dado}")
                continue

        # Verifica se o dado está duplicado (cpf, telefone, crm) #
        if dado.lower() in ["cpf", "telefone", "crm"]:
            registros = dados_pacientes + dados_medicos
            duplicado = any(getattr(pessoa, dado, None) == dado_pessoa for pessoa in registros)
            if duplicado:
                frase_voltar_limpar(f"❌ O {dado} já existe.",f"voltar a validar o {dado}")
                continue

        if dado.lower() == "crm":
            return dado_pessoa.upper()
        
        # Verifica se nome está entre o minimo e maximo de caracteres #
        if dado.lower() == "nome":
            dado_pessoa = dado_pessoa.title()
            if not (7 <= len(dado_pessoa) <= 50):
                frase_voltar_limpar(f"⚠️  O {dado} deve conter entre 7 e 50 caracteres.",f"voltar a validar o {dado}")
                continue

        # Se chegou aqui, o dado está ok #
        frase_voltar_limpar(f"✅ {dado.capitalize()} cadastrado com sucesso!","prosseguir o formulário")
        return dado_pessoa 
           
def exibir_tabela(dados_pessoa, tipo_pessoa, lista_campos):

    # Verifica se há dados #
    if not dados_pessoa:
        frase_voltar_limpar(f"⚠️  Não há dados de nenhum {tipo_pessoa} para preencher a tabela.",f"voltar a Gerenciar {tipo_pessoa.capitalize()}")
        return 
    
    # Se tiver dados, exibe a tabela # 
    if dados_pessoa:
        print(f"📋 Tabela dos {tipo_pessoa.capitalize()}" + "s\n\n" if len(dados_pessoa) > 1 else f"📋 Tabela do {tipo_pessoa.capitalize()}\n")

        total_qtd_espacos = sum(qtd_espacos for _, (_, qtd_espacos) in lista_campos.items())
        total_separadores = (len(lista_campos) - 1) * 3 + 4  
        largura_linha = total_qtd_espacos + total_separadores
        qtd_tracos = "-" * largura_linha

        print(qtd_tracos)
        linha_fixa = "| " + " | ".join(f"{titulo:^{qtd_espacos}}" for titulo, (_, qtd_espacos) in lista_campos.items()) + " |"
        print(linha_fixa)
        print(qtd_tracos)

        for pessoa in dados_pessoa:
            linha_com_dados = "| " + " | ".join(f"{getattr(pessoa, atributo):^{qtd_espacos}}" for _, (atributo, qtd_espacos) in lista_campos.items()) + " |"
            print(linha_com_dados)
            print(qtd_tracos)

        voltar(f"voltar a Gerenciar {tipo_pessoa.capitalize()}")
        limpa_tela()
        
def validar_busca_ou_remover_pessoa(tipo_pessoa,dado,dados_pessoa,padrao,correcao,lista_campos,remover=None):
    
    if not dados_pessoa:
        frase_voltar_limpar(f"⚠️  Não há nenhum {tipo_pessoa} cadastrado ainda.",f"voltar a Gerenciar {tipo_pessoa.capitalize()}")
        
    if dados_pessoa:
        
        while True:
            
            dado_procurado = input(f"{"🗑️ " if remover else "🔍"} Digite o {dado.upper()} do {tipo_pessoa} que deseja {"remover" if remover else "buscar"} : ").strip()
            limpa_tela()

            if not dado_procurado:
                frase_sleep_limpar(f"⚠️  O {dado.upper()} é obrigatório!",2)
                continue
            
            if not re.fullmatch(padrao,dado_procurado):
                frase_voltar_limpar(f"❌ {correcao}",f"voltar a validar o {dado.upper()}")
                continue
            
            dado_encontrado = next((pessoa for pessoa in dados_pessoa if dado_procurado == getattr(pessoa,dado)),None)
            
            if not dado_encontrado:
                frase_voltar_limpar(f"❌ Não há registro desse {dado.upper()}",f"voltar a validar o {dado.upper()}")
                continue
            
            if remover:
                dados_pessoa.remove(dado_encontrado)
                frase_voltar_limpar(f"✅ {tipo_pessoa.capitalize()} {dado_encontrado.nome} removido com sucesso!",f"voltar a Gerenciar {tipo_pessoa.capitalize()}")  
            else:
                print(f"✅ {dado.upper()} encontrado : {dado_encontrado.nome}\n")
                exibir_tabela([dado_encontrado],tipo_pessoa,lista_campos)
    
            return dado_encontrado
            
# FUNÇÕES CONSULTA #

def verificar_se_tem_pessoas():

    while True:

        if not dados_medicos and not dados_pacientes:
            frase_voltar_limpar("⚠️  Não há médico e nem paciente para marcar a consulta.","voltar a Gerenciar Consulta")
            return False

        if not dados_pacientes:
            frase_voltar_limpar("⚠️  Não há paciente para marcar a consulta.","voltar a Gerenciar Consulta")
            return False

        if not dados_medicos:
            frase_voltar_limpar("⚠️  Não há médico para marcar a consulta.","voltar a Gerenciar Consulta")
            return False

        if dados_medicos and dados_pacientes:
            return True
      
def validar_cpf_crm(dado,padrao,correcao):

    while True:
        mensagem_pessoa = "paciente" if dado == "cpf" else "médico"
        dado_buscado = input(f"📝 Digite o {dado.upper()} do {mensagem_pessoa} : ").strip()
        limpa_tela()

         # Verifica se está vazio #
        if not dado_buscado:
            print(f"⚠️  O {dado.upper()} é obrigatório!")
            time.sleep(2)
            limpa_tela()
            frase_sleep_limpar(f"⚠️  O {dado.upper()} é obrigatório!",2)
            continue

         # Verifica se está no padrão #
        if not re.fullmatch(padrao,dado_buscado):
            frase_voltar_limpar(f"❌ {correcao}",f"voltar a validar o {dado.upper()}")
            continue

        registros = dados_medicos if dado == "crm" else dados_pacientes
        
        # Acha o paciente e médico depois de todas as verificações #
        for pessoa in registros:
            if hasattr(pessoa, dado) and getattr(pessoa, dado) == dado_buscado:
                frase_voltar_limpar(f"✅ {dado.upper()} encontrado: {getattr(pessoa, 'nome')}",f"prosseguir o fomulário")
                return pessoa  

        frase_voltar_limpar(f"❌ Nenhum registro com esse {dado.upper()} foi encontrado.",f"tentar digitar outro {dado.upper()}")

def validar_data_hora(dado,padrao,correcao,data_existente=None):
    while True:
        dado_consulta = input(f"📝 Digite a {dado} da Consulta : ").strip()
        limpa_tela()

        if not dado_consulta:
            frase_voltar_limpar(f"A {dado} é obrigatório.",f"voltar a definir a {dado}")
            continue

        if not re.fullmatch(padrao,dado_consulta):
            frase_voltar_limpar(f"{correcao}",f"voltar a definir a {dado}")
            continue

        agora = datetime.now()
        data_atual = agora.strftime("%d/%m/%Y")
        hora_atual = agora.strftime("%H:%M:%S")
        
        if dado == "data":
            data_informada = datetime.strptime(dado_consulta, "%d/%m/%Y").date()
            if data_informada < agora.date():
                frase_voltar_limpar("❌ A data não pode ser no passado.","voltar e digitar uma data válida")
                continue
            
        if dado == "hora" and data_existente:     
        
            if data_existente == data_atual and dado_consulta < hora_atual:
                frase_voltar_limpar(f"❌ O horário não pode ser anterior ao horário atual ({hora_atual}).","voltar e digitar um horário válido")
                continue
            
            conflito = any(consulta.data == data_existente and consulta.hora == dado_consulta for consulta in dados_consulta)
            
            if conflito:
                frase_voltar_limpar(f"❌ Já existe uma consulta marcada para {data_existente} às {dado_consulta}.","voltar e definir outro horário")
                continue 
        
        frase_voltar_limpar(f"✅ {dado.capitalize()} definada com sucesso.","para prosseguir o formulário")
        return dado_consulta

def validar_exame_por_especialidade(especialidade_nome):

    exames_disponiveis = especialidade_e_exame[especialidade_nome]['exames']
    emoji_exame = especialidade_e_exame[especialidade_nome]['emoji_exame']

    while True:
        print(f"\n🧪 Exames disponíveis para {especialidade_nome}:\n")
        for i, exame in enumerate(exames_disponiveis, start=1):
            print(f"[{i}] {emoji_exame} {exame}")

        escolha = input("\n📝 Exame do paciente : ").strip()
        limpa_tela()

        if not escolha:
            frase_sleep_limpar("⚠️ Apresentar o exame é obrigatório!",1.5)
            continue

        if not escolha.isdigit() or not (1 <= int(escolha) <= len(exames_disponiveis)):
            frase_voltar_limpar("❌ Escolha inválida. Digite um número de exame válido.","voltar a escolher o exame")
            continue

        exame_escolhido = exames_disponiveis[int(escolha) - 1]

        frase_voltar_limpar(f"✅ Exame '{exame_escolhido}' definido com sucesso!","voltar a Gerenciar Consulta")
        return exame_escolhido

def validar_id():
    while True:
        id = random.randint(1000,9999)
        id_existente = any(id == consulta.id for consulta in dados_consulta)
        if not id_existente:
            print(f"🆔 Consulta : {id}\n")
            return id

def exibir_tabela_consulta(dados_consulta):
    
    
    # Verifica se há dados #
    if not dados_consulta:
        frase_voltar_limpar("⚠️  Não há consulta marcada ainda.","voltar a Gerenciar Consulta")

    # Se tiver dados, imprime a tabela #
    if dados_consulta:
        print("📋 Tabela de Consultas\n" if len(dados_consulta) > 1 else "📋 Tabela de Consulta\n")
        tracos = "-" * 214
        print(tracos)
        print(f"| {'ID Consulta':^11} | {'Paciente':^50} | {'Médico / Especialidade':^70} | {'Exame':^35} | {'Data':^12} | {'Hora':^7} | {'Status':^7} |")
        print(tracos)
        
        for consulta in dados_consulta:
            status = "✅" if consulta.status else "❌"
            medico_e_especialidade = f"{consulta.medico.nome} / {consulta.medico.especialidade}" 
            print(f"| {consulta.id:^11} | {consulta.paciente.nome:^50} | {medico_e_especialidade:^70} | {consulta.exame:^35} | {consulta.data:^12} | {consulta.hora:^7} | {status:^6} |")
            print(tracos)
        voltar("voltar a Gerenciar Consulta")
        limpa_tela()

def validar_busca_ou_remover_consulta(remover=None,atualizar=None):
    if not dados_consulta:
        frase_voltar_limpar("⚠️  Não há consulta marcada ainda.","voltar a Gerenciar Consulta")
        
    if dados_consulta:
    
        padrao = r"\b[1-9][0-9]{3}\b"

        while True:
            
            id_consulta_procurada = input(f"{"🗑️" if remover else "🔄" if atualizar else "🔍"} Digite o ID Consulta que deseja {"remover" if remover else "atualizar" if atualizar else "buscar"} : ").strip()
            limpa_tela()
            
            if not id_consulta_procurada:
                frase_voltar_limpar("⚠️  O ID Consulta é obrigatório!","voltar a validar o ID Consulta")
                continue
            
            if not re.fullmatch(padrao,id_consulta_procurada):
                frase_voltar_limpar("❌ O ID Consulta deve ser no padrão : NNNN","voltar a validar o ID Consulta")
                continue
                
            consulta_encontrada = next((consulta for consulta in dados_consulta if id_consulta_procurada == str(consulta.id)),None)
            
            if not consulta_encontrada:
                frase_voltar_limpar("❌ Esse ID Consulta não existe.","voltar a validar o ID Consulta")
                continue
            
            if remover:
                print(f"✅ Consulta {consulta_encontrada.id} removida com sucesso!")
                exibir_tabela_consulta([consulta_encontrada])
                dados_consulta.remove(consulta_encontrada)
                
            if atualizar:
                print(f"✅ Consulta {consulta_encontrada.id} realizada com sucesso!")
                consulta_encontrada.status = "✅"
                exibir_tabela_consulta([consulta_encontrada])
                    
            else:
                print("✅ ID Consulta encontrado!\n")    
                exibir_tabela_consulta([consulta_encontrada])
            return consulta_encontrada   

#  FUNÇÕES ESSENCIAIS #

def frase_voltar_limpar(frase,frase_voltar):
    print(frase)
    voltar(frase_voltar)
    limpa_tela()

def frase_sleep_limpar(frase,tempo):
    print(frase)
    time.sleep(tempo)
    limpa_tela()

def sobre():
    print("""
🏥 Clínica G&M
📅 Fundação: 18/06/2024
📍 Localização: Rua das Palmeiras, 123 – Maceió/AL

📖 Nossa História

A Clínica G&M nasceu no dia 18/06/2024 com a missão de oferecer
atendimento médico de qualidade e humanizado. Desde o primeiro dia,
buscamos unir tecnologia, conforto e profissionais qualificados.

🏗  Estrutura e Capacidade

✔ 5 consultórios modernos e equipados
✔ Capacidade para atender até 100 pessoas por dia
✔ Funcionamento: 06h às 22h, todos os dias

💼 Serviços Oferecidos

🩺 Consultas médicas em diversas especialidades
💉 Exames laboratoriais e de imagem
💊 Farmácia interna
📲 Agendamento online e suporte via WhatsApp

🌟 Diferenciais

✅ Equipe multiprofissional
✅ Atendimento humanizado
✅ Infraestrutura confortável
✅ Acessibilidade para todos
""")
    voltar("voltar para Menu Incial")
    limpa_tela()

def limpa_tela():
    os.system('cls')

def voltar(frase):
    input(f"\n↩️  Pressione Enter para {frase}.\n")

def sair():
    salvar_dados_ao_fechar_o_app()
    print("🔚 Saindo de Consultas Médicas G&M...")
    time.sleep(2)
    limpa_tela()
    exit()
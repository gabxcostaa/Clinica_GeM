# DICIONÁRIO DE CAMPOS DE DADOS PACIENTE & MÉDICO | OBS: Usei somente pra fazer a tabela de paciente e médico #
campos_comuns = {"Nome Completo" : ("nome",50), "CPF" : ("cpf",15), "Telefone" : ("telefone",15)}
campos_medico = {"Especialidade" : ("especialidade",50), "CRM" : ("crm",15)}

# DICIONÁRIO DE ESPECIALIDADE E EXAME #
especialidade_e_exame = {
    "Cardiologista": {"emoji_especialidade": "❤️ ","id": 1,"exames": ["Eletrocardiograma", "Ecocardiograma", "Teste Ergométrico"],"emoji_exame": "📈"},
    "Neurologista":  {"emoji_especialidade": "🧠","id": 2,"exames": ["Eletroencefalograma", "Ressonância Magnética do Crânio", "Tomografia Computadorizada"],"emoji_exame": "💀"},
    "Ortopedista":   {"emoji_especialidade": "🦴","id": 3,"exames": ["Raio-X dos ossos", "Ressonância Magnética do Joelho", "Ultrassom Musculoesquelético"],"emoji_exame": "🩻"},
    "Pediatra":      {"emoji_especialidade": "🧒","id": 4,"exames": ["Exame de Crescimento e Desenvolvimento", "Hemograma Completo", "Exame de Urina"],"emoji_exame": "🧸"}, 
    "Pneumologista": {"emoji_especialidade": "🫁 ","id": 5,"exames": ["Espirometria", "Raio-X do Tórax", "Gasometria Arterial"],"emoji_exame": "🌬️"}
}

# ARRAYS DADOS PACIENTE & MÉDICO #
dados_pacientes = []
dados_medicos = []
dados_consulta = []
dados = {}

# ARRAYS DE TUPLAS (DADO,PADRÃO,CORREÇÃO) #
valores_comuns = [
    ("nome",r'^[A-Za-zÀ-ÿ]+(?:\s+[A-Za-zÀ-ÿ]+){1,}$', "O nome deve ser completo."),
    ("cpf", r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{11})$', "CPF deve ser no formato : XXX.XXX.XXX-XX"),
    ("telefone", r'^(\(?\d{2}\)?\s?)?9\d{4}-?\d{4}$', "Telefone deve ser no formato : XX 9XXXX-XXXX")
]
valores_medico = [
    ("especialidade", r"[1-5]", "Somente números de 1 a 5"),
    ("crm", r'^\d{4,7}-?[A-Z]{2}$', "CRM deve ser no formato : 4-7 dígitos, hífen, e UF em letras maiúsculas. Exemplo : XXXXX-UF")
]

# ARRAYS DE MENUS #
opcoes_menu_inicial = ["☰  Menu","🛈  Sobre", "✖  Sair"]
opcoes_menu_pricipal = ["👤 Paciente", "🩺 Médico", "📅 Consultas", "↩️  Voltar"]
opcoes_menu_crud_pessoa = ["➕ Adicionar", "📄 Ver Tabela", "🗑️  Remover", "🔍 Buscar", "↩️  Voltar"]
opcoes_menu_crud_consulta = ["➕ Adicionar", "📄 Ver Tabela", "🗑️  Remover", "🔍 Buscar","♻️  Atualizar", "↩️  Voltar"]
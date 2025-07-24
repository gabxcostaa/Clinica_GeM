class Pessoa():
    def __init__(self,nome,cpf,telefone):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone

class Paciente(Pessoa):
    def __init__(self, nome, cpf, telefone):
        super().__init__(nome, cpf, telefone)

class Medico(Pessoa):
    def __init__(self, nome, cpf, telefone,especialidade,crm):
        super().__init__(nome, cpf, telefone)
        self.especialidade = especialidade
        self.crm = crm

class Consulta():
    def __init__(self,paciente,medico,data,hora,exame,id):
        self.paciente = paciente
        self.medico = medico
        self.data = data
        self.hora = hora
        self.exame = exame
        self.id = id
        self.status = False
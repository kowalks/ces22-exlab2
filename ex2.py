# CES-22: Programação Orientada a Objetos
# Aluno: Guilherme Kowalczuk (COMP-23)

# # Descrição da Atividade:

# Uma aplicação para um Banco executa operações tais como verificar saldos, extratos
# e realizar transferências. Utilize o Padrão de Projeto Command para modelar o
# processamento de solicitações do cliente para a aplicação do Banco. Implemente um
# programa em Python para simular a interação entre a aplicação cliente e a aplicação
# do Banco. O Diagrama de Classes deve ser elaborado.

from abc import ABC, abstractmethod


class Order(ABC):  # Classe Command
    def __init__(self, session):
        self.session = session

    @abstractmethod
    def execute(self):
        raise NotImplementedError


class VerificacaoSaldo(Order):  # Classe ConcreteCommandA
    def __init__(self, session):
        super().__init__(session)

    def execute(self):
        saldo = self.session.get_saldo()
        nome = self.session.get_name()
        print(f'saldo de {saldo} reais na conta de {nome}.')
        return True

    def __str__(self):
        return f'verificacao de saldo na conta {self.session.get_id()}'


class Deposito(Order):  # Classe ConcreteCommandB
    def __init__(self, session, valor):
        super().__init__(session)
        self.valor = valor

    def execute(self):
        if self.valor > 0:
            self.session.change_saldo(self.valor)
            return True
        return False

    def __str__(self):
        return f'deposito de {self.valor} na conta {self.session.get_id()}'


class Retirada(Order):  # Classe ConcreteCommandC
    def __init__(self, session, valor):
        super().__init__(session)
        self.valor = valor

    def execute(self):
        if 0 < self.valor <= self.session.get_saldo():
            self.session.change_saldo(-self.valor)
            return True
        return False

    def __str__(self):
        return f'retirada de {self.valor} da conta {self.session.get_id()}'


class Transferencia(Order):  # Classe ConcreteCommandD
    def __init__(self, session, session_to, valor):
        super().__init__(session)
        self.session_to = session_to
        self.valor = valor

    def execute(self):
        if 0 < self.valor <= self.session.get_saldo():
            self.session.change_saldo(-self.valor)
            self.session_to.change_saldo(self.valor)
            return True
        return False

    def __str__(self):
        id_from = self.session.get_id()
        id_to = self.session_to.get_id()
        return f'transferencia de {self.valor} de {id_from} para {id_to}'


class Sessao:  # Classe Receiver
    def __init__(self, name, userid):
        self.name = name
        self.id = userid
        self.saldo = 0

    def get_saldo(self):
        return self.saldo

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def change_saldo(self, valor):
        self.saldo = self.saldo + valor


class Agent:  # Classe Invoker (Chamador)
    def __init__(self):
        self.__pending_orders = []
        self.__executed_orders = []
        self.__failed_orders = []

    def place_order(self, order):
        self.__pending_orders.append(order)

    def place_orders(self, orders):
        self.__pending_orders.extend(orders)

    def has_pending_orders(self):
        return len(self.__pending_orders) != 0

    def execute_orders(self):
        for order in self.__pending_orders:
            if order.execute():
                self.__executed_orders.append(order)
            else:
                self.__failed_orders.append(order)
        self.__pending_orders.clear()

    def print_extract(self):
        print(50*'-')
        print('Pending orders:')
        for order in self.__pending_orders:
            print(f'\t{order}')
        print('\nExecuted orders:')
        for order in self.__executed_orders:
            print(f'\t{order}')
        print('\nFailed orders:')
        for order in self.__failed_orders:
            print(f'\t{order}')
        print(50*'-')


# Iniciar sessão com o nome do usuário e o id (em uma conta de verdade, seria exigido senha, mas aqui
# vamos pular essa etapa para simplificar a aplicação).
sessao_gui = Sessao('guilherme', 'id#123')

# Criação de três depósitos simultâneos
deposito1 = Deposito(sessao_gui, 100)
deposito2 = Deposito(sessao_gui, 200)
deposito3 = Deposito(sessao_gui, -100)  # Esse é para ser inválido de propósito

# Lado do agente (Invoker). Colocando as ordens na fila de execução
agente = Agent()
agente.place_order(deposito1)
agente.place_order(deposito2)
agente.place_order(deposito3)

# Executando as ordens e conferindo o extrato de orders feitas pelo Agente
agente.execute_orders()
agente.print_extract()

# Conferir saldo
saldo1 = VerificacaoSaldo(sessao_gui)
agente.place_order(saldo1)
agente.execute_orders()

# Novas operações
retirada1 = Retirada(sessao_gui, 50)
retirada2 = Retirada(sessao_gui, -500)  # Esse é para ser inválido de propósito
retirada3 = Retirada(sessao_gui, 1500)  # Esse é para ser inválido de propósito

agente.place_orders([retirada1, retirada2, retirada3])  # Outra maneira de colocar na fila de execução

# Executando as ordens e conferindo o extrato de orders feitas pelo Agente
agente.execute_orders()
agente.print_extract()

# Conferir saldo
saldo2 = VerificacaoSaldo(sessao_gui)
agente.place_order(saldo1)
agente.execute_orders()

# Ultimo teste corresponde a fazer transferências entre dois usuários
sessao_edu = Sessao('eduardo', 'id#456')
transf1 = Transferencia(sessao_gui, sessao_edu, 100)
transf2 = Transferencia(sessao_gui, sessao_edu, -100)  # Esse é para ser inválido de propósito
transf3 = Transferencia(sessao_gui, sessao_edu, 1500)  # Esse é para ser inválido de propósito
saldo_gui = VerificacaoSaldo(sessao_gui)
saldo_edu = VerificacaoSaldo(sessao_edu)

# Executando as ordens pelo agente
agente.place_orders([transf1, transf2, transf3, saldo_gui, saldo_edu])
agente.print_extract()
agente.execute_orders()

# Por fim, vendo as ordens de transferência inválidas
agente.print_extract()

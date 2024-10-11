from abc import ABC, abstractmethod

from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.resistrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod #property adicionado pois as variaveis são privadas e serão acessadas por aqui
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property #property adicionado pois as variaveis são privadas e serão acessadas por aqui
    def saldo(self):
        return self.saldo
    
    @property  #property adicionado pois as variaveis são privadas e serão acessadas por aqui
    def numero(self):
        return self._numero
    
    @property #property adicionado pois as variaveis são privadas e serão acessadas por aqui
    def agencia(self):
        return self._agencia
    
    @property #property adicionado pois as variaveis são privadas e serão acessadas por aqui
    def cliente(self):
        return self._cliente
    
    @property #property adicionado pois as variaveis são privadas e serão acessadas por aqui
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou, saldo insuficiente!")
        
        elif valor > 0:
            self._saldo -= valor
            print("\nSaque realizado com sucesso!")
            return True
    
        else:
            print("\nOperação falhou, o valor informado não é valido!")
        
        return False
    
    def depostirar(self, valor):
        saldo = self.saldo
        
        if valor > 0:
            self._saldo += valor
            print("\nDepósito concluido!")
            return True
        
        else:
            print("\nOperação falhou, por favor insira um valor válido!")
            return False

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([transacao for transacao in self.historico.transacoes if transacao["tipo"] == "Saque"])

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\n Operação falhou, valor execedeu o limite!")
        
        elif excedeu_saques:
            print("\nOperação falhou, número máximo de saques excedido")

        else:
            return super().sacar(valor)
        
        return False
    
    def __str__(self):
        return f"""\
            AgênciaL \t{self.agencia}
            C\C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(Self, transacao):
        Self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime
                ("%d-%m-%Y %H:%M:%s"),
            }
        )

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass
    @abstractmethod
    def registrar(Self, conta):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
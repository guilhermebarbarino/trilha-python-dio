from contas.historico import Historico
from transacoes.deposito import Deposito  # Certifique-se de que esta linha está presente
from transacoes.saque import Saque        # Certifique-se de que esta linha está presente

class Conta:
    def __init__(self, cliente, numero):
        self.saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.cliente = cliente
        self.historico = Historico()

    def sacar(self, valor):
        saque = Saque(valor)
        return saque.registrar(self)

    def depositar(self, valor):
        deposito = Deposito(valor)
        return deposito.registrar(self)

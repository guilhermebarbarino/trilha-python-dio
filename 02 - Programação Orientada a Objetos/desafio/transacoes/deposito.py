from transacoes.transacao import Transacao

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
        return True

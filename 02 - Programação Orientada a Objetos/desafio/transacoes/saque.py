from transacoes.transacao import Transacao

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.saldo >= self.valor:
            conta.saldo -= self.valor
            conta.historico.adicionar_transacao(self)
            return True
        else:
            print("Saldo insuficiente!")
            return False

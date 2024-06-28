import textwrap
from clientes.pessoa_fisica import PessoaFisica
from contas.conta_corrente import ContaCorrente
from transacoes.deposito import Deposito
from transacoes.saque import Saque

MENU = textwrap.dedent("""
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [l] Listar Contas
    [c] Cadastrar Usuário
    [n] Cadastrar Conta Bancária
    [u] Listar Contas do Usuário
    [q] Sair

    => """)

LIMITE_SAQUES = 3
LIMITE_SAQUE = 500
prox_num_conta = 1

usuarios = []
contas = []

def cadastrar_usuario():
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    cpf = input("Informe o CPF (somente números): ")
    endereco = input("Informe o endereço (formato: logradouro, nro - bairro - cidade/sigla estado): ")

    if any(u.cpf == cpf for u in usuarios):
        print("CPF já cadastrado! Não é possível cadastrar o mesmo CPF novamente.")
        return

    novo_usuario = PessoaFisica(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")

def criar_conta_bancaria():
    global prox_num_conta
    cpf = input("Informe o CPF do usuário: ")

    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    if not usuario:
        print("Usuário não encontrado! Cadastre o usuário primeiro.")
        return
    
    nova_conta = ContaCorrente(usuario, prox_num_conta, LIMITE_SAQUE, LIMITE_SAQUES)
    contas.append(nova_conta)
    usuario.adicionar_conta(nova_conta)

    print(f"Conta número {prox_num_conta} cadastrada com sucesso!")
    prox_num_conta += 1

def listar_contas():
    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print(f"Agência: {conta.agencia} | Número da Conta: {conta.numero}")
        print(f"CPF do Titular: {conta.cliente.cpf}")
        print(f"Nome do Titular: {conta.cliente.nome}")
        print(f"Saldo: R$ {conta.saldo:.2f}")
        print("-----------------------------------------------")
    print("===============================================")

def listar_contas_usuario():
    cpf = input("Informe o CPF do usuário: ")

    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    if not usuario:
        print("Usuário não encontrado!")
        return
    
    print(f"\n================ CONTAS DO USUÁRIO {usuario.nome} ================")
    for conta in usuario.contas:
        print(f"Agência: {conta.agencia} | Número da Conta: {conta.numero}")
        print(f"Saldo: R$ {conta.saldo:.2f}")
        print("-----------------------------------------------")
    print("===============================================")

def menu_principal():
    while True:
        opcao = input(MENU)

        if opcao == "d":
            listar_contas()
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta.depositar(valor)
            else:
                print("Conta não encontrada!")
        elif opcao == "s":
            listar_contas()
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta.sacar(valor)
            else:
                print("Conta não encontrada!")
        elif opcao == "e":
            listar_contas()
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c.numero == numero_conta), None)
            if conta:
                print("\n================ EXTRATO ================")
                if not conta.historico.transacoes:
                    print("Não foram realizadas movimentações.")
                else:
                    for transacao in conta.historico.transacoes:
                        if isinstance(transacao, Deposito):
                            print(f"Depósito: R$ {transacao.valor:.2f}")
                        elif isinstance(transacao, Saque):
                            print(f"Saque: R$ {transacao.valor:.2f}")
                print(f"\nSaldo: R$ {conta.saldo:.2f}")
                print("==========================================")
            else:
                print("Conta não encontrada!")
        elif opcao == "l":
            listar_contas()
        elif opcao == "c":
            cadastrar_usuario()
        elif opcao == "n":
            criar_conta_bancaria()
        elif opcao == "u":
            listar_contas_usuario()
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

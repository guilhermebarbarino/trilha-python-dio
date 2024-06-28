import textwrap

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
AGENCIA_PADRAO = "0001"
prox_num_conta = 1

usuarios = []
contas = []

def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"
        print("Depósito realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")
    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

def mostrar_extrato(saldo, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def listar_contas():
    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        usuario = next((u for u in usuarios if u['cpf'] == conta['cpf']), {})
        print(f"Agência: {conta['agencia']} | Número da Conta: {conta['numero_conta']}")
        print(f"CPF do Titular: {conta['cpf']}")
        print(f"Nome do Titular: {usuario.get('nome', 'Desconhecido')}")
        print(f"Saldo: R$ {conta['saldo']:.2f}")
        print("-----------------------------------------------")
    print("===============================================")

def cadastrar_usuario():
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    cpf = input("Informe o CPF (somente números): ")
    endereco = input("Informe o endereço (formato: logradouro, nro - bairro - cidade/sigla estado): ")

    # Verifica se o CPF já está cadastrado
    if any(u['cpf'] == cpf for u in usuarios):
        print("CPF já cadastrado! Não é possível cadastrar o mesmo CPF novamente.")
        return

    # Cria o usuário com os dados informados
    novo_usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco,
        "contas": []
    }
    usuarios.append(novo_usuario)
    print("Usuário cadastrado com sucesso!")

def criar_conta_bancaria():
    global prox_num_conta
    cpf = input("Informe o CPF do usuário: ")

    # Busca o usuário pelo CPF na lista de usuários
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    if not usuario:
        print("Usuário não encontrado! Cadastre o usuário primeiro.")
        return
    
    # Cria uma nova conta bancária
    nova_conta = {
        "agencia": AGENCIA_PADRAO,
        "numero_conta": prox_num_conta,
        "cpf": cpf,
        "saldo": 0,
        "extrato": "",
        "numero_saques": 0
    }

    # Adiciona a nova conta à lista de contas
    contas.append(nova_conta)

    # Atualiza a lista de contas do usuário
    usuario["contas"].append(prox_num_conta)

    print(f"Conta número {prox_num_conta} cadastrada com sucesso!")
    prox_num_conta += 1

def listar_contas_usuario():
    cpf = input("Informe o CPF do usuário: ")

    # Busca o usuário pelo CPF na lista de usuários
    usuario = next((u for u in usuarios if u['cpf'] == cpf), None)
    if not usuario:
        print("Usuário não encontrado!")
        return
    
    print(f"\n================ CONTAS DO USUÁRIO {usuario['nome']} ================")
    for num_conta in usuario["contas"]:
        conta = next((c for c in contas if c['numero_conta'] == num_conta), None)
        if conta:
            print(f"Agência: {conta['agencia']} | Número da Conta: {conta['numero_conta']}")
            print(f"CPF do Titular: {conta['cpf']}")
            print(f"Saldo: R$ {conta['saldo']:.2f}")
            print("-----------------------------------------------")
    print("===============================================")

def main():
    while True:
        opcao = input(MENU)

        if opcao == "d":
            listar_contas()
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do depósito: "))
                conta["saldo"], conta["extrato"] = depositar(conta["saldo"], valor, conta["extrato"])
            else:
                print("Conta não encontrada!")
        elif opcao == "s":
            listar_contas()
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)
            if conta:
                valor = float(input("Informe o valor do saque: "))
                conta["saldo"], conta["extrato"], conta["numero_saques"] = sacar(
                    saldo=conta["saldo"], 
                    valor=valor, 
                    extrato=conta["extrato"], 
                    limite=LIMITE_SAQUE, 
                    numero_saques=conta["numero_saques"], 
                    limite_saques=LIMITE_SAQUES
                )
            else:
                print("Conta não encontrada!")
        elif opcao == "e":
            listar_contas()
            numero_conta = int(input("Informe o número da conta: "))
            conta = next((c for c in contas if c['numero_conta'] == numero_conta), None)
            if conta:
                mostrar_extrato(conta["saldo"], extrato=conta["extrato"])
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

if __name__ == "__main__":
    main()

import csv
from datetime import datetime, timezone, timedelta

# ---------- Variáveis Globais ---------- #
lista_produto = []
historico_atividades = []
nome_limite = 18
# ---------- Variáveis Globais ---------- #


# ---------- Função para Carregar Dados do CSV ---------- #

def carregar_dados_csv():
    try:
        with open('produtos.csv', 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Códigos para converter os valores que serão gravados no arquivo CSV
                row['codigo'] = int(row['codigo'])
                row['tamanho'] = float(row['tamanho'])
                row['quantidade'] = int(row['quantidade'])

                lista_produto.append(row) # Lista para os dados serem gravados por linha

            print('Dados carregados!!')
    except FileNotFoundError:
        print("Arquivo 'produtos.csv' não encontrado. Criando um novo arquivo.")
# ---------- FIM ---------- #

# ---------- Adicionar Atividades ---------- #
def adicionar_atividade(acao, produto): # Função para mostrar todas as atividades realizadas
    fuso_horario = timezone(timedelta(hours=-3))  # -3 horas para o fuso horário de São Paulo
    timestamp_atual = datetime.now(fuso_horario).strftime('%y-%m-%d %H:%M:%S')

    atividade = {
        'acao': acao,
        'produto': produto,
        'timestamp': timestamp_atual
    }

    historico_atividades.append(atividade)
# ---------- FIM ---------- #

# ---------- Funções de carregamento de arquivo ---------- #
carregar_dados_csv()
# ---------- FIM ---------- #

# ---------- Visualizar Histórico de atividades ---------- #
def visualizar_historico():
    print('=' * 120)
    print("{:<20} {:<20} {:<50} {:<30}".format('Timestamp', 'Ação', 'Produto', 'Detalhes'))
    print('-' * 120)

    for atividade in historico_atividades:
        timestamp = atividade['timestamp']
        acao = atividade['acao']
        produto = atividade['produto']
        detalhes = atividade.get('detalhes', '')

        print("{:<20} {:<20} {:<50} {:<30}".format(timestamp, acao, produto, detalhes))

    print('=' * 120)
# ---------- FIM ---------- #

# ---------- Salvar atividades no CSV ---------- #
def salvar_atividades_csv(): # Função para salvar as atividades no arquivo CSV
    with open('atividades.csv', 'w', newline='') as csvfile:
        fieldnames = ['acao', 'produto', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for atividade in historico_atividades:
            writer.writerow(atividade)
# ---------- FIM ---------- #

# ---------- Função para Salvar Dados em CSV ---------- #
def salvar_dados_csv(): # Diferente de salvar_atividades, essa função vai salvar os dados que serão cadastrados e utilizados
    with open('produtos.csv', 'w', newline='') as csvfile:
        fieldnames = ['codigo', 'nome', 'tamanho', 'unidade', 'quantidade', 'categoria', 'cor', 'dataCadastro']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for produto in lista_produto:
            writer.writerow(produto)
# ---------- FIM ---------- #

# ---------- Função para Mostrar Tabela Produtos ---------- #
def mostrar_produtos():
  for produto in lista_produto:
        print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format(
            produto['codigo'],
            produto['nome'],
            produto['tamanho'],
            produto['unidade'],
            produto['quantidade'],
            produto['categoria'],
            produto['cor'],
            produto['dataCadastro']
        ))
# ---------- FIM ---------- #

# ---------- Cadastrar Produto ---------- #
def cadastrar_produto():
    print('='*35, '  BEM-VINDO AO MENU CADASTRAR PRODUTO  ', '='*35)
    # Validação da entrada de dados e algumas exceções para números int e float
    while True:
        try:
            codigo = int(input('Digite o Código "ID" do produto: '))
            break
        except ValueError:
            print('Digite um número inteiro válido')

    while True:
        nome = input(f'NOME do produto (limite de {nome_limite} caracteres): ')
        if nome and len(nome) <= nome_limite:
            break
        else:
          print(f"O nome deve ter no máximo {nome_limite} caracteres. Tente novamente.\n")

    while True:
        unidade = input('UNIDADE DE MEDIDA do produto (ml,cm,g ou un): ').strip()
        if unidade and unidade.lower() in ['ml', 'cm', 'g', 'un']:
            break
        else:
          print("Opção inválida. Por favor, escolha entre ml, cm ou g.\n")

    while True:
        try:
            tamanho = float(input('Digite o TAMANHO do produto: '))
            break
        except ValueError:
          print('Por favor, digite um número válido.\n')

    while True:
        try:
            quantidade = int(input('Digite a QUANTIDADE atual em unidade: '))
            break
        except ValueError:
          print('Por favor, digite um número inteiro válido.\n')

    while True:
        categoria = input('CATEGORIA do produto (insumo, limpeza, escritorio, eletronico): ').strip()
        if categoria and categoria.lower() in ['insumo', 'limpeza', 'escritorio', 'eletronico']:
            break
        else:
          print("Opção inválida. Por favor, escolha entre insumo, limpeza, escritorio ou eletronico.\n")

    while True:
        cor = input('COR do produto (preto, branco, marrom, vermehlho, amarelo, azul): ').strip()
        if cor and cor.lower() in ['preto', 'branco', 'marrom', 'vermelho', 'amarelo', 'azul']:
          break
        else:
          print("Opção Inválida. Por favorm escolha entre preto, branco, marrom, vermelho, amarelo ou azul.\n")

    # Mostra a data que foi cadastrado o produto, no caso que será
    data_atual = datetime.now()
    data_formatada = data_atual.strftime("%Y-%m-%d")
    dataCadastro = data_formatada
    print("Data de Cadastro:", dataCadastro)

    dicionario_produto = {'codigo': codigo,
                          'nome': nome,
                          'tamanho': tamanho,
                          'unidade': unidade,
                          'quantidade': quantidade,
                          'categoria': categoria,
                          'cor': cor,
                          'dataCadastro': dataCadastro
                          }

    lista_produto.append(dicionario_produto.copy()) # Cria uma cópia da lista de produtos ao invés de modificala
    adicionar_atividade('Cadastrar Produto', dicionario_produto)
    salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
    salvar_dados_csv()  # função para salvar as alterações
# ---------- FIM ---------- #

# ---------- Alterar Produto ---------- #
def alterar_produto(): # Função para alterar o produto cadastrado pelo código ou 'ID'
    print('='*35, '  BEM-VINDO AO MENU ALTERAR PRODUTO  ', '='*35)
    if not lista_produto:
        print('Nenhum produto cadastrado')
        return

    while True:
        alterar_menu = input('Escolha a opção desejada:\n' +
                             '1 - Alterar todos:\n' +
                             '2 - Alterar Código:\n' +
                             '3 - Alterar Nome:\n' +
                             '4 - Alterar Tamanho:\n' +
                             '5 - Alterar Unidade:\n' +
                             '6 - Alterar Quantidade:\n' +
                             '7 - Alterar Categoria:\n' +
                             '8 - Alterar Cor:\n' +
                             '9 - Sair\n'
                             '-> ')
        if alterar_menu == '1':
            alterar_todos()
        elif alterar_menu == '2':
            alterar_codigo()
        elif alterar_menu == '3':
            alterar_nome()
        elif alterar_menu == '4':
            alterar_tamanho()
        elif alterar_menu == '5':
            alterar_unidade()
        elif alterar_menu == '6':
            alterar_quantidade()
        elif alterar_menu == '7':
            alterar_categoria()
        elif alterar_menu == '8':
            alterar_cor()
        elif alterar_menu == '9':
            return
        else:
            print('Opção Inválida. Tente novamente')
            continue
# ---------- FIM ---------- #

# ---------- Função alterar todos ---------- #
def alterar_todos(): # Função para alterar tudo de uma vez só
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()
    # Validação de dados e tratando algumas exceções
    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto: # Busca na lista de produtos o cósigo digitado
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
                try:
                    produto['codigo'] = int(input('Novo Código do produto: '))
                    break
                except ValueError:
                    print('Por favor, digite um número inteiro válido:\n')

            while True:
                produto['nome'] = input('Novo Nome do produto: ')
                if len(produto['nome']) <= nome_limite:
                  break
                else:
                  print(f'NOME do produto (limite de {nome_limite} caracteres): ')

            while True:
                try:
                    produto['tamanho'] = float(input('Novo TAMANHO do produto: '))
                    break
                except ValueError:
                  print('Por favor, digite um número.\n')

            while True:
              produto['unidade'] = input('Nova UNIDADE DE MEDIDA do produto: ').strip()
              if produto['unidade'].lower() in ['ml', 'cm', 'g', 'un']:
                break
              else:
                print('Opção Inválida. Por favor, escolha entre, ml, cm ou g.\n')

            while True:
                try:
                    produto['quantidade'] = int(input('Nova QUANTIDADE do produto: '))
                    break
                except ValueError:
                  print('Por favor, digite um número inteiro válido.\n')

            while True:
                produto['categoria'] = input('Nova CATEGORIA do produto: ').strip()
                if produto['categoria'].lower() in ['insumo', 'limpeza', 'escritorio', 'eletronico']:
                  break
                else:
                  print('Opção Inválida. Por favor, escolha entre insumo, limpeza, escritorio ou eletronico.\n')

            while True:
                produto['cor'] = input('Nova COR do produto: ').strip()
                if produto['cor'].lower() in ['preto', 'branco', 'marrom', 'vermelho', 'amarelo', 'azul']:
                  break
                else:
                  print('Opção Inválida. Por favor escolha entre preto, branco, marrom, vermelho, amarelo ou azul.\n')


            adicionar_atividade('Alterar Produto', produto)
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # Função para salvar as alterações

            print('Produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Função alterar codigo ---------- #
def alterar_codigo():
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto:
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
                try:
                    produto['codigo'] = int(input('Novo Código do produto: '))
                    break
                except ValueError:
                    print('Por favor, digite um número inteiro válido:\n')

            adicionar_atividade('Alterar Código Produto', produto['codigo'])
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # função para salvar as alterações

            print('Codigo do produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Função alterar nome ---------- #
def alterar_nome():
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto:
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
                produto['nome'] = input('Novo Nome do produto: ').strip()
                if len(produto['nome']) <= nome_limite:
                  break
                else:
                  print(f'NOME do produto (limite de {nome_limite} caracteres): ')

            adicionar_atividade('Alterar Nome Produto', produto['nome'])
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # função para salvar as alterações

            print('Nome do produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Função alterar tamanho ---------- #
def alterar_tamanho():
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto:
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
              try:
                  produto['tamanho'] = float(input('Novo TAMANHO do produto: ')).strip()
                  break
              except ValueError:
                print('Por favor, digite um número.\n')

            adicionar_atividade('Alterar Tamanho Produto', produto['tamanho'])
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # função para salvar as alterações

            print('Tamanho do produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Função alterar unidade ---------- #
def alterar_unidade():
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto:
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
                produto['unidade'] = input('Nova UNIDADE DE MEDIDA do produto: ').strip()
                if produto['unidade'].lower() in ['ml', 'cm', 'g', 'un']:
                  break
                else:
                  print('Opção Inválida. Por favor, escolha entre, ml, cm ou g.\n')

            adicionar_atividade('Alterar Unidade Produto', produto['unidade'])
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # função para salvar as alterações

            print('Unidade do produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Função alterar quantidade ---------- #
def alterar_quantidade():
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto:
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
              try:
                  produto['quantidade'] = int(input('Nova QUANTIDADE do produto: '))
                  break
              except ValueError:
                print('Por favor, digite um número inteiro válido.\n')

            adicionar_atividade('Alterar Quantidade Produto', produto['quantidade'])
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # função para salvar as alterações

            print('QUANTIDADE do produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Função alterar CATEGORIA ---------- #
def alterar_categoria():
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto:
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
              produto['categoria'] = input('Nova CATEGORIA do produto: ').strip()
              if produto['categoria'].lower() in ['insumo', 'limpeza', 'escritorio', 'eletronico']:
                break
              else:
                print('Opção Inválida. Por favor, escolha entre insumo, limpeza, escritorio ou eletronico.\n')

            adicionar_atividade('Alterar CATEGORIA Produto', produto['categoria'])
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # função para salvar as alterações

            print('CATEGORIA do produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Função alterar cor ---------- #
def alterar_cor():
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_alterar = int(input('Digite o código do produto que deseja alterar: '))
    for produto in lista_produto:
        if produto['codigo'] == codigo_alterar:
            print('Produto encontrado. Corrige os dados desejados:')
            while True:
                produto['cor'] = input('Nova COR do produto: ').strip()
                if produto['cor'].lower() in ['preto', 'branco', 'marrom', 'vermelho', 'amarelo', 'azul']:
                  break
                else:
                  print('Opção Inválida. Por favor escolha entre preto, branco, marrom, vermelho, amarelo ou azul.\n')

            adicionar_atividade('Alterar Cor Produto', produto['cor'])
            salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
            salvar_dados_csv()  # função para salvar as alterações

            print('Cor do produto alterado com sucesso!')
            return
    print('Produto não encontrado com o código fornecido\n')
# ---------- FIM ---------- #

# ---------- Alterar Produto ---------- #

# ---------- Remover Produto ---------- #
def remover_produto(): # Função para remover produto pelo código
    print('='*35, '  BEM-VINDO AO MENU REMOVER PRODUTO  ', '='*35)
    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    remover = int(input('Digite com o CÓDIGO com produto que deseja remover: '))

      # Verifica se o código do produto a ser removido existe
    if any(produto['codigo'] == remover for produto in lista_produto):
          for produto in lista_produto:
              if produto['codigo'] == remover:
                  adicionar_atividade('Remover Produto', produto)
                  lista_produto.remove(produto)
                  salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
                  salvar_dados_csv()  # função para salvar as alterações
                  print('Produto Removido!!')
                  break
                  return
    else:
        print('Produto não encontrado com o código fornecido.\n')
        return
# ---------- FIM ---------- #

# ---------- Adicionar ---------- #
def adicionar_quantidade(): # Função para somente adicionar quantidade em quantidade
    print('='*35, '  BEM-VINDO AO MENU ADICIONAR QUANTIDADE  ', '='*35)

    if not lista_produto:
        print('Nenhum produto cadastrado')
        return

    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_adicionar = int(input('Digite o código do produto que deseja adicionar quantidade: '))

    for i, produto in enumerate(lista_produto):
        if produto['codigo'] == codigo_adicionar:
            while True:
                try:
                    quantidade_adicionar = int(input('Digite a quantidade que deseja adicionar: '))
                    lista_produto[i]['quantidade'] += quantidade_adicionar
                    adicionar_atividade('Quantidade adicionada', quantidade_adicionar)
                    salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
                    salvar_dados_csv()  # função para salvar as alterações
                    print(f'Quantidade adicionada com sucesso! Nova quantidade: {lista_produto[i]["quantidade"]}')
                    break
                except ValueError:
                    print('Por favor, digite um número inteiro válido.')
            return

    print('Produto não encontrado com o código fornecido')
# ---------- FIM ---------- #

# ---------- Retirar ---------- #
def retirar_quantidade(): # Função para apenas retirar quantidade em retirar
    print('='*35, '  BEM-VINDO AO MENU RETIRAR QUANTIDADE  ', '='*35)

    if not lista_produto:
        print('Nenhum produto cadastrado')
        return

    print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho', 'Unidade',
                                                                          'Quantidade', 'Categoria', 'Cor',
                                                                          'Data Cadastro'))
    print("-" * 120)

    mostrar_produtos()

    codigo_retirar = int(input('Digite o código do produto que deseja retirar quantidade: '))

    for i, produto in enumerate(lista_produto):
        if produto['codigo'] == codigo_retirar:
            while True:
                try:
                    quantidade_retirar = int(input('Digite a quantidade que deseja retirar: '))
                    if 0 < quantidade_retirar <= produto['quantidade']:
                        lista_produto[i]['quantidade'] -= quantidade_retirar
                        adicionar_atividade('Quantidade retirada', quantidade_retirar)
                        salvar_atividades_csv()  # Função para salvar todas as atividades no histórico no CSV
                        salvar_dados_csv()  # função para salvar as alterações
                        print(f'Quantidade retirada com sucesso! Nova quantidade: {lista_produto[i]["quantidade"]}')
                        break
                    else:
                        print(
                            'Quantidade inválida. Certifique-se de que a quantidade é maior que zero e menor ou igual à quantidade atual.')
                except ValueError:
                    print('Por favor, digite um número inteiro válido.')
            return

    print('Produto não encontrado com o código fornecido')
# ---------- FIM ---------- #

# ---------- Exibir Relatório ---------- #
def exibir_relatorio(): # Função para exibir o relatório de tudo, quanto por categoria para fazer uma divisão de departamentos ou também um relatório de tudo e com tudo
    print('='*35, '  BEM-VINDO AO MENU EXIBIR RELATÓRIO  ', '='*35)

    while True:
        opcao_relatorio = input('Escolha a opção desejada:\n' +
                                '1 - Exibir Relatório Geral\n' +
                                '2 - Exibir Relatório Categoria\n' +
                                '3 - Retornar\n' +
                                '-> ')

        if opcao_relatorio == '1':
            print(' ---------- Relatório Geral ---------- \n')
            if not lista_produto:
                print("Nenhum produto cadastrado.")
            else:
                print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho',
                                                                                      'Unidade', 'Quantidade',
                                                                                      'Categoria', 'Cor',
                                                                                      'Data Cadastro'))
                print("-" * 120)

                mostrar_produtos()

                print("-" * 120)
        elif opcao_relatorio == '2':
            print(' ---------- Relatório Por Categoria ---------- \n')
            categoria_desejada = input('Digite a categoria do produto:')
            produtos_categoria = [produto for produto in lista_produto if produto['categoria'] == categoria_desejada]
            if not produtos_categoria:
                print("Nenhum produto cadastrado nessa categoria.")
            else:
                print("{:<10} {:<20} {:<8} {:<15} {:<15} {:<15} {:<15} {:<10}".format('Código', 'Nome', 'Tamanho',
                                                                                      'Unidade', 'Quantidade',
                                                                                      'Categoria', 'Cor',
                                                                                      'Data Cadastro'))
                print("-" * 120)

                mostrar_produtos()

                print("-" * 120)
        elif opcao_relatorio == '3':
            return
        else:
            print('Opção Inválida. Tente novamente\n' +
                  '=' * 50)
            continue
# ---------- FIM ---------- #


# ---------- Inicio Main ---------- #
while True: # Main principal com todas outras opção de função
    opcao_principal = input('CntEstoque - P.I.P.E.\n'
                            "================================"
                            "       MENU PRINCIPAL        "
                            "================================\n"
                            'Escolha a opção desejada:\n' +
                            "================================\n"
                            '1 - Cadastrar Produto\n' +
                            '2 - Alterar Produto\n' +
                            '3 - Remover Produto\n' +
                            '4 - Adicionar Quantidade\n' +
                            '5 - Retirar Quantidade\n' +
                            '6 - Exibir Relatório\n' +
                            '7 - Visualizar Histórico\n' +
                            '8 - Sair\n' +
                            "===============================\n"
                            '-> ')
    if opcao_principal == '1':
        cadastrar_produto()
    elif opcao_principal == '2':
        alterar_produto()
    elif opcao_principal == '3':
        remover_produto()
    elif opcao_principal == '4':
        adicionar_quantidade()
    elif opcao_principal == '5':
        retirar_quantidade()
    elif opcao_principal == '6':
        exibir_relatorio()
    elif opcao_principal == '7':
        visualizar_historico()
    elif opcao_principal == '8':
        break
    else:
        print('Opção Inválida. Tente novamente')
        continue
# ---------- Fim Main ---------- #
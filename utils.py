from configs import *


#Gera o menuzinho maroto
#####################################################################
def gerar_botoes(categoria_menu):

    if categoria_menu == "tutu_money_bud":
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(
            InlineKeyboardButton("Consultar Saldo", callback_data="consultarSaldo"),
            InlineKeyboardButton("Lançar Gasto", callback_data="lancarGasto"),
            InlineKeyboardButton("Investimentos TBB", callback_data="investimentosTBB"),
            InlineKeyboardButton("Acessar Dashboard", callback_data="acessarDashboard"),
        )

    return markup
#####################################################################


#Funcao para fazer query em tabelas do BQ
#####################################################################
def envia_menu(message):
    bot.send_message(message.chat.id,"💰 Selecione um comando abaixo para continuar! 💰",reply_markup=gerar_botoes("tutu_money_bud"))
#####################################################################


#Funcao para fazer query em tabelas do BQ
#####################################################################
def query_table(query):
    #encoding: utf-8
    #project_id gcp_credentials -- Já configuradas em configs.py
    """
    Requisita uma tabela do BigQuery | Realiza uma consulta

    Args:
        query (string): Consulta que será realizada no BigQuery
        project_id (string): Id do projeto a qual a tabela pertence
        gcp_credentials (client credentials object): Credenciais autenticadas da conta de servico
    Returns:
        dataframe: pandas dataframe com o retorno da consulta
    """
    print("-------------------------------------------")
    print("A funcao query_table foi chamada!")
    print(query)
    print("-------------------------------------------")

    df = pandas_gbq.read_gbq(query, project_id=project_id,credentials=scoped_credentials)
    return (df)
#####################################################################


#Determina a data do cartao. Retorna yearMonth e data
#####################################################################
def dataCartao():
    #Determina qual será o YearMonth consultado de acordo com o fechamento da fatura.
    diaHoje = int(dt.datetime.today().strftime("%d"))
    if(diaHoje>=8):
        dataTrintaDias = dt.datetime.today() + dt.timedelta(days=25)
        yearMonth = str(int(dataTrintaDias.strftime("%Y%m")))

        year = yearMonth[:4]
        month = yearMonth[4:]
        data = f"15/{month}/{year}"
        #print(f'yearMonth: {yearMonth} -- data: {data}')
    else:
        yearMonth = str(int(dt.datetime.today().strftime("%Y%m")))
        year = yearMonth[:4]
        month = yearMonth[4:]
        data = f"15/{month}/{year}"
        #print(f'yearMonth: {yearMonth} -- data: {data}')
    
    dicData = {
                'data':data,
                'yearMonth':yearMonth
            }
    
    return dicData

#dataCartao()
#####################################################################


#Determina a categoria do lancamento
#####################################################################
def categorizadorGasto(descricao):
    #encoding: utf-8
    descricao = descricao.lower()

    dicionario_categoria_classificacao_natureza = {
        "uber":"Uber/99_Normal_Manutencao",
        "99":"Uber/99_Normal_Manutencao",

        "chines":"Mercado_Normal_Manutencao",
        "mercado":"Mercado_Normal_Manutencao",
        "feira":"Mercado_Normal_Manutencao",
        "chocolandia":"Mercado_Normal_Manutencao",
        "larsol":"Mercado_Normal_Manutencao",

        "farmacia":"Farmácia/Saúde_Normal_Manutencao",
        "médico":"Farmácia/Saúde_Essencial_Saúde",
        "goya":"Farmácia/Saúde_Essencial_Saúde",

        "banho dino":"Animais_Normal_Manutencao",
        "petz":"Animais_Normal_Manutencao",

        "bar":"Roles_Normal_Experiencias",
        "pizza":"Rangos_Essencial_Experiencias",
        "papi pizza":"Rangos_Essencial_Experiencias",

        "estacionamento":"Carro_Normal_Manutencao",
        "estacionamento mooca":"Carro_Normal_Manutencao",
        "estacionamento shopping":"Carro_Normal_Manutencao",
        "gasolina":"Carro_Normal_Manutencao",
        "gasolina uno":"Carro_Normal_Manutencao",

        "soho":"Moda_Normal_Manutencao",
        "cabeleireiro":"Moda_Normal_Manutencao",
        "cabelereiro soho":"Moda_Normal_Manutencao",

        "tbb":"Investimentos -- TBB_Investimentos_Investimentos"  
    }

    try:
        categoria = dicionario_categoria_classificacao_natureza[descricao].split("_")[0]
        classificacao = dicionario_categoria_classificacao_natureza[descricao].split("_")[1]
        natureza = dicionario_categoria_classificacao_natureza[descricao].split("_")[2]
    except: 
        categoria = "A Definir"
        classificacao = "A Definir"
        natureza = "A Definir"

    dicionarioCategorizado = {
                        'categoria':categoria,
                        'classificacao':classificacao,
                        'natureza':natureza
                        }

    return dicionarioCategorizado

#print(categorizador("UBER"))
#####################################################################
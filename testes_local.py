from configs import *
from utils import *
from tutuMoneyBud import *

    
#Ações que devem ser realizadas pelos comandos
#####################################################################

#Tutu MB - Funções principais
#############################
def consultar_saldo(call):
    bot.send_message(call.message.chat.id,'Você selecionou a opção Consultar Saldo! Calculando o orçamento disponível...',parse_mode='html')
    bot.send_chat_action(call.message.chat.id,"typing")


    #Saldo Banco
    yearMonth = dataCartao()['yearMonth']
    select = f'Select YearMonth, ROUND(sum(ValorCorrigido),2) as ValorCorrigido from `tutu-money-bud.Tutu_Money_Bud_Sheets.Livro_Diario_Consolidado` where YearMonth = {yearMonth} group by 1'
    tbLivroDiario_df = query_table(select)
    bot.send_chat_action(call.message.chat.id,"typing")
    agrupaYearMonth = tbLivroDiario_df.groupby(by = 'YearMonth')
    somaValorAnual = agrupaYearMonth['ValorCorrigido'].sum().reset_index()
    df = pd.DataFrame(somaValorAnual)
    filtroYearMonth = df['YearMonth'] == int(yearMonth)
    saldoBanco = df.loc[filtroYearMonth,'ValorCorrigido'].apply(lambda x: '%.2f' % x)[0]
    bot.send_message(call.message.chat.id,f"Limite do Cartão de Crédito: R${saldoBanco}")


    #Saldo VR
    bot.send_chat_action(call.message.chat.id,"typing")
    select = 'SELECT * FROM `tutu-money-bud.Tutu_Money_Bud_Sheets.Saldo_VR`'
    tbSaldoVR = query_table(select)
    saldoVR = tbSaldoVR['Saldo_VR'][0]
    bot.send_message(call.message.chat.id,f"Saldo no VR: {saldoVR}")

    bot.send_message(call.message.chat.id,"Enviando informação ao chat TuBoo")
    bot.send_chat_action(call.message.chat.id,"typing")
    tutuMoneyBot(saldoBanco,saldoVR)
    bot.send_message(call.message.chat.id,"Pronto!")

def lancar_gasto(call):
    mensagemBot = bot.send_message(call.message.chat.id,'Você selecionou a opção Lançar Gasto! Por favor, digite o gasto no seguinte padrão: 42.13,uber')
    bot.register_next_step_handler(mensagemBot, lancamento_handler_tutumb) 
#############################



#Tutu MB - Funções secundárias
#############################
def investimentos_tbb(call):
    bot.send_message(call.message.chat.id,'Certo... Vou consultar os dados registrados como TBB. Um segundo, por favor.',parse_mode='html')

    bot.send_message(call.message.chat.id,"-- PENDENTES segmentados por ano/mês --")
    bot.send_chat_action(call.message.chat.id,"typing")

    select = 'SELECT yearMonth,totalPendentesAReceber FROM `tutu-money-bud.Tutu_Money_Bud_Sheets.TBB_Yearmonth` where Status = "Pendente"'
    tbSaldoTbbYearMonth = query_table(select)
    bot.send_chat_action(call.message.chat.id,"typing")
    listaYearMonth = tbSaldoTbbYearMonth.values.tolist()

    table = pt.PrettyTable(['yearMonth', 'Pendentes'])

    for yearMonth, totalPendentesAReceber in listaYearMonth:
        table.add_row([yearMonth, totalPendentesAReceber])

    bot.send_message(call.message.chat.id,f'<pre>{table}</pre>',parse_mode='html')


    yearMonth = str(int(dt.datetime.today().strftime("%Y%m")))
    bot.send_message(call.message.chat.id,f"-- Dados Detalhados do mês Atual ({yearMonth}) --")
    
    select = f'SELECT SUBSTRING(Descricao, 0, 17) as Descricao, Valor FROM `tutu-money-bud.Tutu_Money_Bud_Sheets.TBB_Detalhado`  where yearMonth = {yearMonth} order by Data asc'
    tbDetalhadoTbb = query_table(select)
    bot.send_chat_action(call.message.chat.id,"typing")
    listaDetalhado = tbDetalhadoTbb.values.tolist()

    table = pt.PrettyTable(['Descricao', 'Valor'])

    for Descricao, Valor in listaDetalhado:
        table.add_row([Descricao, Valor])

    bot.send_message(call.message.chat.id,f'<pre>{table}</pre>',parse_mode='html')


    tbDetalhadoTbb_df = pd.DataFrame(tbDetalhadoTbb)
    somaTotal = tbDetalhadoTbb_df['Valor'].sum()
    bot.send_message(call.message.chat.id,f"Valor total deste mês: R${somaTotal}")

def acessar_dashboard(call):
    bot.send_message(call.message.chat.id,'O link para o dashboard é este aqui: LINK DASHBOARD')
#############################


#Acionador Inicial
#####################################################################
@bot.message_handler(content_types=["text"])
def responder(message):
    #print(message) #Útil para debugar
    if message.chat.id == USER_ID_1 or message.chat.id == USER_ID_2:
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        textoEntrada = f'Olá, <b>{first_name} {last_name}</b>! Bem vindo ao Tutu Money Bot!'
        bot.reply_to(message,textoEntrada,parse_mode='html')
        
        envia_menu(message)
    else:
        texto = "Você não é o Tutu ou a Carol!! Saia já daqui!"
        bot.reply_to(message,texto)
#####################################################################



#Acionador Funções
#####################################################################
@bot.callback_query_handler(func=lambda message: True)
def callback_query(call):
    if call.data == "consultarSaldo":
        bot.answer_callback_query(call.id, "Consultar Saldo Ativado!")
        consultar_saldo(call)

    if call.data == "lancarGasto":
        bot.answer_callback_query(call.id, "Lançar Gasto Ativado!")
        lancar_gasto(call)

    if call.data == "investimentosTBB":
        bot.answer_callback_query(call.id, "Investimentos TBB Ativado!")
        investimentos_tbb(call)
        #testes_teste3(call)

    if call.data == "acessarDashboard":
        bot.answer_callback_query(call.id, "Acessar Dashboard Ativado!")
        acessar_dashboard(call)
#####################################################################


#Ativa o bot.
bot.infinity_polling(timeout=10, long_polling_timeout = 5)
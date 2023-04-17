from utils import *
from configs import *


#Lança um gasto
#####################################################################
def lancarGastoSheets(valor,descricao):

    dataLog = str(dt.datetime.now())
    status = "Pendente"
    tipo = "Despesa"
    data = dataCartao()['data']
    print("data:" + data)
    valor = valor
    contaCartao = "Mastercard Nubank"
    categoria = categorizadorGasto(descricao)['categoria']
    descricao = descricao
    recorrencia = 'Variado'
    classificacao = categorizadorGasto(descricao)['classificacao']
    natureza = categorizadorGasto(descricao)['natureza']

    listaNovosLancamentosLivroDiario = [
                                        dataLog,
                                        status,
                                        tipo,
                                        data.replace("'",""),
                                        str(valor).replace(".",","),
                                        contaCartao,
                                        categoria,
                                        descricao,
                                        recorrencia,
                                        classificacao,
                                        natureza
                                    ]
    sheetLivroDiario = client.open("Tutu Money Bud - Gestor").get_worksheet_by_id(123456789) ##Incluir aqui o id da planilha a ser consultada!
    sheetLivroDiario.insert_row(listaNovosLancamentosLivroDiario,3,value_input_option="user_entered")
    
#lancarGastoSheets(666,'Uber')
#####################################################################


#Handler para pegar o input do usuário
#####################################################################
def lancamento_handler_tutumb(message):
    lancamento = message.text
    bot.send_message(message.chat.id, f"Obrigado! Seu registro entrará no Tutu Money Bud.")

    valor = lancamento.split(",")[0]
    descricao = lancamento.split(",")[1]

    bot.send_chat_action(message.chat.id,"typing")
    
    lancarGastoSheets(valor,descricao)

    bot.send_message(message.chat.id,"Lançamento registrado com sucesso!")

    bot.send_chat_action(message.chat.id,"typing")

    #bot.send_message(message.chat.id,"Saldo atualizado: R$"+consultarSaldoBanco())

#####################################################################


#TutuMoneyBot - Envia notificação para o chat TuBoo
#####################################################################
def tutuMoneyBot(saldoBanco,saldoVR):

    #Variáveis da API
    tokenTutuMoneyBot = TOKEN_TUTU_MONEY_BOT
    url = f"https://api.telegram.org/bot{tokenTutuMoneyBot}/sendMessage";
    userID = USER_ID_BOT

    message = f"Saldo atual no Nubank (Crédito): {saldoBanco}. Saldo disponível no VR: {saldoVR}."

    data = {
        "method": "post",
        "chat_id": userID,
        "text": str(message)
    };

    requests.post(url, data)

#tutuMoneyBot()
#####################################################################
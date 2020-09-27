import pika, sys

def SendMessage(body):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='queueMessage', durable=True)
        # message = ' '.join(sys.argv[1:])
        # for i in range(3):
        #    print("mensagem "  + str(i) + " enviada")
        #    channel.basic_publish(exchange='', routing_key='hello', body=message, properties=pika.BasicProperties(delivery_mode=2, ))
        channel.basic_publish(exchange='', routing_key='queueMessage', body=body,
                              properties=pika.BasicProperties(delivery_mode=2, ))
        print("mensagem [ " + body + " ] enviada")
        connection.close()
    except Exception as error:
        print("Erro ao Enviar: " + error)

cont = 0
while True:
    print("------------ <|Mensagem " + str(cont) + "|> ---------------")
    mess = input("\tDigite a Mensagem " + str(cont) + ": ")
    #print(mess)
    while mess == '':
        mess = input("\tDigite a Mensagem " + str(cont) + ": ")
    #print(mess)
    SendMessage(mess)
    print("-----------------------------\n")
    cont = cont+1

#SendMessage("teste")
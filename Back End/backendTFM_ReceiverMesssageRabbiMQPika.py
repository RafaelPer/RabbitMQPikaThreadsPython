import pika
import time
import sys
import threading
from queue import Queue
queue = "queueMessage"
connection = None
#listMessage = []

def check_acknowledge(channel, connection, ack_queue):
    delivery_tag = None
    #print("\nAnalisando Arquivos Não Empacotados")
    while(True):
        try:
            delivery_tag = ack_queue.get_nowait()
            #print(delivery_tag)
            channel.basic_ack(delivery_tag=delivery_tag)
            break
        except:
            connection.process_data_events()
            #print("check_acknowledge execption")
        time.sleep(1)


def process_message(body, delivery_tag, ack_queue):
    print("\tFoi Recebido a mensagem [ %s ] " % (body))
    print("\tEspera de 2 segundos para a proxima mensagem\n")
    start = time.time()
    #print(start)
    elapsed = 0
    while elapsed < 2:
        elapsed = time.time() - start
        print("\n\t\tTempo do Loop: %f, \n\t\tSegundos Passados: %02d" %(time.process_time(), elapsed))
        time.sleep(1)
    ack_queue.put(delivery_tag)
    message = "Mensagem: " + str(body)
    #listMessage.append(message)
    #print(listMessage)
    #print(list(ack_queue.queue))




def callback(ch, method, properties, body):
    global connection
    ack_queue = Queue()
    t = threading.Thread(target=process_message, args=(body, method.delivery_tag, ack_queue))
    t.start()

    #t_acknowledge = threading.Thread(target=check_acknowledge, args=(ch, connection, ack_queue))
    #t_acknowledge.start()
    check_acknowledge(ch, connection, ack_queue)


while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        print('\n[*] Esperando Mensagens')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue, on_message_callback=callback)
        channel.start_consuming()
        #print(listMessage)
    except KeyboardInterrupt:
        #print(KeyboardInterrupt)
        print("Terminando Programa")
        break


channel.close()
connection.close()
print("Fechando Programa")
exit(0)

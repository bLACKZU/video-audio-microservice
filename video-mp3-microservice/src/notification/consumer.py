import pika, sys, os
from send import email
def main():
    

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    ) 
    channel = connection.channel()

    def callback(channel, method, properties, body):
        err = email.notification(body)

        #Send negative ack if there is an error. This denotes that if there is any error in the above function, the channel will basically know there is still a video that needs to be processed. 
        #Opposite happens if there is no error.
        #delivery_tag is an unique identifier for each message

        if err:

            channel.basic_nack(delivery_tag=method.delivery_tag) #delivery_tag identifies a specific channel 
        else:
            
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("MP3_QUEUE"), on_message_callback=callback

    )

    print("Waiting for messages. To exit, press CTRL+C")

    channel.start_consuming()

if __name__ == "__main__":
    try:   
        main()
    except KeyboardInterrupt:
        print("Interrupted by user")
        try:
            sys.exit(0)
        except SystemExit:    
            os._exit(0)
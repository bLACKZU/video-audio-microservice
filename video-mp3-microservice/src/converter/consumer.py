import pika, sys, os, time
from pymongo import MongoClient
import gridfs
from convert import to_mp3

def main():
    client = MongoClient("host.minikube.internal", 27017)
    mongo_videos = client.videos
    mongo_mp3s = client.mp3s

    fs_videos = gridfs.GridFS(mongo_videos)
    fs_mp3s = gridfs.GridFS(mongo_mp3s)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    ) 
    channel = connection.channel()

    def callback(channel, method, properties, body):
        err = to_mp3.start(body, fs_videos, fs_mp3s, channel)

        #Send negative ack if there is an error. This denotes that if there is any error in the above function, the channel will basically know there is still a video that needs to be processed. 
        #Opposite happens if there is no error.
        #delivery_tag is an unique identifier for each message

        if err:
            print(f"Error during conversion: {err}")
            channel.basic_nack(delivery_tag=method.delivery_tag) #delivery_tag identifies a specific channel 
        else:
            print("Conversion successful")
            channel.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(
        queue=os.environ.get("VIDEO_QUEUE"), on_message_callback=callback

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
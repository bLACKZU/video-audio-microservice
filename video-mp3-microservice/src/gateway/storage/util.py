import pika, json

def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as err:
        print(err)
        return "Internal server error", 500
    
    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access["username"],   
    }

    try:
        channel.basic_publish(
            exchange = "",
            routing_key = "video",
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE # it tells the queue to be persistent or durable and the messages to persist in queue even if the pod crashes, as the message broker will be deployed as a stateful set
            ),
        )
    except:
        fs.delete(fid) #delete the file from db since the MQ doesnt know there is any file that is needed to be processed. As a result the file is stale in the db
        return "Internal server error", 500
    
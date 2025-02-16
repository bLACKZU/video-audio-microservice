import pika, json, tempfile, os
from bson.objectid import ObjectId
import moviepy.editor

def start(message, fs_videos, fs_mp3s, channel):
    message = json.loads(message)
    print("Message received:", message)

    tf = tempfile.NamedTemporaryFile()
    print("Temporary file created:", tf.name)

    #read video contents
    out = fs_videos.get(ObjectId(message["video_fid"]))

    tf.write(out.read())
    #create audio from temp video file
    audio = moviepy.editor.VideoFileClip(tf.name).audio
    tf.close()
    #create directory for mp3 to be stored
    tf_path = tempfile.gettempdir() + f"/{message['video_fid']}.mp3"
    audio.write_audiofile(tf_path)
    print("Audio file saved:", tf_path)

    #Save file to mongo
    f = open(tf_path, "rb")
    data = f.read()
    fid = fs_mp3s.put(data)
    f.close()
    os.remove(tf_path)
    print("MP3 file stored in GridFS:", fid)

    message["mp3_fid"] = str(fid)
    try:
        channel.basic_publish(
            exchange = "",
            routing_key = os.environ.get("MP3_QUEUE"),
            body = json.dumps(message),
            properties = pika.BasicProperties(
                delivery_mode = pika.spec.PERSISTENT_DELIVERY_MODE 
            ),
        )
        print("Message published to MP3 queue")

    except Exception as err:
        print(f"Error in MP3 conversion: {err}")
        fs_mp3s.delete(fid)
        return "failed to publish message"
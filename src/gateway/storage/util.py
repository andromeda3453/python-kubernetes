import pika, json, gridfs


def upload(f, fs, channel, access):
    try:
        fid = fs.put(f)
    except Exception as e:
        return "internal server error", 500

    message = {
        "video_fid": str(fid),
        "mp3_fid": None,
        "username": access[
            "username"
        ],  # username is the users email which is unique for each user
    }

    try:
        channel.basic_publish(
            exchange = "",
            routing_key = "video",
            body=json.dumps(message),
            properties= pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE #This makes sure the messages persist in the queue in the event of a pod crash
            )
        )
    except Exception:
        
        # if message publishing fails, delete video from database to prevent stale data 
        fs.delete(fid)
        return "internal server error. Please try uploading file again", 500
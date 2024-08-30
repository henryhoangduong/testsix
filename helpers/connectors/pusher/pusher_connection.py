import pusher

class Pusher:
    
    def __init__(self) -> None:
        self.pusher_client = pusher.Pusher(
            app_id='1800274',
            key='d7115eff4bc75b67430b',
            secret='1bb2a9cbac90e50d0881',
            cluster='ap1',
            ssl=True
        )

    def subcribe(self, channel, data):
        self.pusher_client.trigger('public-channel', channel, data)
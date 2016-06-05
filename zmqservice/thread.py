import threading
import Queue

from pubsub import Subscriber

class SubscriberThread(threading.Thread):
    """ This class uses the Subscriber in a way that handles the "slow subscriber"
    problem gracefully. The subscriber handles IO in a background thread and
    queues all revieved messages. The main thread needs only to call handler()
    to invoke the desired callback for each message tag recieved off the queue.
    In this way all callback functions are called from the main thread and
    messages are taken off of the network stack ASAP in the background thread.
    """
    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self)
        self.subscriber = Subscriber(*args, **kwargs)
        self.queue = Queue.Queue()
        self.methods = {}
        self.daemon = True

        def queue(tag, message):
            self.queue.put( (tag, message) )

        self.callback = queue

    def subscribe(self, tag, fun, description=None):
        self.methods[tag] = fun
        self.subscriber.subscribe(tag, self.callback, description)

    def handler(self, block=True, timeout=None):
        tag, message = self.queue.get(block, timeout)
        self.methods[tag](tag, message)

    def run(self):
        self.subscriber.start()

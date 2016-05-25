import zmq
from zmqservice import Subscriber


def log_line(line):
    print('Line is: {}'.format(line))


def cap_line(line):
    print('Line capitalized is: {}'.format(line.upper()))


#s = Subscriber('ipc:///tmp/pubsub-service.sock')
s = Subscriber('tcp://127.0.0.1:5554')
s.subscribe('log_line', log_line)
s.subscribe('cap_line', cap_line)
s.start()

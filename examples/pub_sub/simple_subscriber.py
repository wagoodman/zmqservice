import zmq
from zmqservice import Subscriber


def log_line(tag, line):
    print('Line is: {}'.format(line))


def cap_line(tag, line):
    print('Line capitalized is: {}'.format(line.upper()))

counter = 0
def count(tag, line):
    global counter
    #print "LINE: %s" % repr(line)
    thisNum = int(line)
    if thisNum != counter:
        print "ERROR: expected %d got %d" % (counter, thisNum)
    #else:
    #    print "Good: %d" % counter
    counter += 1

def monitor(tag, line):
    print "MONITOR:%s"%repr(line)

#s = Subscriber('ipc:///tmp/pubsub-service.sock')
s = Subscriber('tcp://127.0.0.1:5554')
s.subscribe('log_line', log_line)
s.subscribe('cap_line', cap_line)
s.subscribe('counter', count)
#s.subscribe('', monitor)
s.start()

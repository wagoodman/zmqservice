from zmqservice import Publisher

import time
#p = Publisher('ipc:///tmp/pubsub-service.sock')
p = Publisher('tcp://*:5554')
time.sleep(1)# Wait for the publisher to connect, otherwise everyone will miss the first message
#p = Publisher('tcp://127.0.0.1:5554', bind=False)
counter = 0
while True:
    print "Publishing", time.ctime(), counter
    p.publish('log_line', 'hello world')
    p.publish('cap_line', 'this is uppercase: %s' % time.ctime())
    p.publish('counter', str(counter))
    counter += 1
    time.sleep(1)

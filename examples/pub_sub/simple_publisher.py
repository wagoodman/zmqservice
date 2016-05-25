from zmqservice import Publisher

import time
#p = Publisher('ipc:///tmp/pubsub-service.sock')
p = Publisher('tcp://*:5554')
while True:
    print "Publishing", time.ctime()
    p.publish('log_line', 'hello world')
    p.publish('cap_line', 'this is uppercase: %s' % time.ctime())
    time.sleep(1)

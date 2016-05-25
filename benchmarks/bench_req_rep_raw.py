import time
from multiprocessing import Process
from zmqservice import Responder, Requester

import util


def start_service(addr, n):
    """ Start a service """
    s = Responder(addr)

    started = time.time()
    for _ in range(n):
        msg = s.socket.recv()
        s.socket.send(msg)
    s.socket.close()
    duration = time.time() - started

    print('Raw REP service stats:')
    util.print_stats(n, duration)
    return


def bench(client, n):
    """ Benchmark n requests """
    items = list(range(n))

    # Time client publish operations
    # ------------------------------
    started = time.time()
    msg = b'x'
    for i in items:
        client.socket.send(msg)
        res = client.socket.recv()
        assert msg == res
    duration = time.time() - started

    print('Raw REQ client stats:')
    util.print_stats(n, duration)


def run(N, addr):

    # Fork service
    service_process = Process(target=start_service, args=(addr, N))
    service_process.start()

    time.sleep(0.1)  # Wait for service connect
    # Create client and make reqs
    c = Requester(addr)
    bench(c, N)
    c.socket.close()

    time.sleep(0.2)
    service_process.terminate()


if __name__ == '__main__':

    N = 50000

    print('')
    print('Req-Rep over IPC (raw)')
    print('-----------------------------')
    run(N, 'ipc:///tmp/bench-raw-reqrep-ipc.sock')

    print('')
    print('Req-Rep over TCP (raw)')
    print('-----------------------------')
    run(N, 'tcp://127.0.0.1:5052')

zmqservice
===========
zmqservice is a small Python library for writing lightweight networked services
using [zmq](http://zeromq.org/).

With zmqservice you can break up monolithic applications into small,
specialized services which communicate with each other.

**This is a port of 'nanoservice' to use zmq instead of nanomsg. Protip: when [nanomsg](http://nanomsg.org/) is out of beta I'd recommend moving to  [nanoservice](https://github.com/walkr/nanoservice) instead.**

## Install

1) Install zmqservice:

From project directory

```shell
$ make install
```

## Example Usage

The service:

```python
from zmqservice import Responder

def echo(msg):
    return msg

s = Responder('ipc:///tmp/service.sock')
s.register('echo', echo)
s.start()
```

```shell
$ python echo_service.py
```

The client:

```python
from zmqservice import Requester

c = Requester('ipc:///tmp/service.sock')
res, err = c.call('echo', 'hello world’)
print('Result is {}'.format(res))
```

```shell
$ python my_client.py
$ Result is: hello world
```

## Other

To run tests:

```shell
$ make test
```

To run benchmarks

```shell
$ make bench
```

Check out examples directory for more examples.

MIT Licensed

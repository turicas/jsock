# coding: utf-8

import cPickle
import json
import time

import jsock
import msgpack
import simplejson


def bench(data, times, serializer, deserializer):
    server = jsock.ServerSocket(key='myprecious', serdes=(serializer,
        deserializer))
    server.bind(('127.0.0.1', 5554))
    client = jsock.ClientSocket(key='myprecious', serdes=(serializer,
        deserializer))
    client.connect(('127.0.0.1', 5554))
    sclient = server.accept() # get socket for incoming connection

    send = recv = 0
    for i in range(times):
        start_time = time.time()
        sclient.send(data)
        end_time = time.time()
        send += end_time - start_time

        start_time = time.time()
        assert client.receive() == data
        end_time = time.time()
        recv += end_time - start_time

    assert client.receive() is None
    assert sclient.receive() is None

    client.close()
    sclient.close()
    server.close()

    return send, recv


data = {'test': 123, 'message': 'alvaro Justen'}
# TODO: deal correctly with unicode
times = 50000

send, recv = bench(data, times, json.dumps, json.loads)
print '      json: send[{} op/s], recv[{} op/s], total = {}s'\
        .format(times / send, times / recv, send + recv)

send, recv = bench(data, times, simplejson.dumps, simplejson.loads)
print 'simplejson: send[{} op/s], recv[{} op/s], total = {}s'\
        .format(times / send, times / recv, send + recv)

send, recv = bench(data, times, msgpack.packb, msgpack.unpackb)
print '   msgpack: send[{} op/s], recv[{} op/s], total = {}s'\
        .format(times / send, times / recv, send + recv)

send, recv = bench(data, times, cPickle.dumps, cPickle.loads)
print '   cPickle: send[{} op/s], recv[{} op/s], total = {}s'\
        .format(times / send, times / recv, send + recv)

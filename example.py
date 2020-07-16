# coding: utf-8

import jsock

server = jsock.ServerSocket(key="myprecious")
# all messages should be signed (HMAC(key, message, SHA256)) with this key to
# be accepted. if key is None, no verification will be made
server.bind(("127.0.0.1", 5555))
assert server.accept() is None  # no incoming connection
print("Server address: {}".format(server.address))

client = jsock.ClientSocket(key="myprecious")
# should use the same key to sign/verify messages
client.connect(("127.0.0.1", 5555))
print("Client local address: {}".format(client.local_address))
print("Client remote address (server's): {}".format(client.remote_address))
assert client.remote_address == server.address

sclient = server.accept()  # get socket for incoming connection
print("Server client local address: {}".format(sclient.local_address))
print("Server client remote address: {}".format(sclient.remote_address))
assert sclient.local_address == server.address
assert sclient.remote_address == client.local_address

assert sclient.receive() is None  # no incoming message
assert client.receive() is None  # no incoming message

# dict will be encoded as JSON, signed and compressed
message = {"command": "hello"}
sclient.send(message)

# will only receive the message if the keys match
assert client.receive() == message
assert client.receive() is None  # only one incoming message
assert sclient.receive() is None  # client sent no message

answer = {"command": "hi-there"}
client.send(answer)
assert sclient.receive() == answer
assert sclient.receive() is None  # only one incoming message
assert client.receive() is None  # sclient sent no message

client.close()
sclient.close()
server.close()

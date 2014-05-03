# coding: utf-8

###############################################################################
#                                                                             #
# Copyright (c) 2014 Álvaro Justen                                            #
#    This program is free software: you can redistribute it and/or modify     #
#    it under the terms of the GNU General Public License as published by     #
#    the Free Software Foundation, either version 3 of the License, or        #
#    (at your option) any later version.                                      #
#                                                                             #
#    This program is distributed in the hope that it will be useful,          #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of           #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            #
#    GNU General Public License for more details.                             #
#                                                                             #
#    You should have received a copy of the GNU General Public License        #
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.    #
#                                                                             #
###############################################################################

import hashlib
import hmac
import json
import socket
import struct
import zlib


__all__ = ['ClientSocket', 'ServerSocket']
MSGTYPE_0 = '\x00'
MSGTYPE_1 = '\x01'
# TODO: 'message type' bits should have information about:
#       - whether messages should be signed/unsigned
#       - whether messages should be encrypted/decrypted
#       - whether messages should be compressed/decompressed

class ClientSocket(object):
    MSGTYPE = MSGTYPE_0


    def __init__(self, key=None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = None
        self.key = key
        if key is not None:
            self.MSGTYPE = MSGTYPE_1

    def __del__(self):
        self._socket.close()

    def connect(self, (ip_address, port)):
        self._socket.connect((ip_address, port))
        self._socket.setblocking(False)
        self.remote_address = (ip_address, port)
        self.local_address = self._socket.getsockname()

    def send(self, data):
        json_data = json.dumps(data)
        if self.MSGTYPE == MSGTYPE_0:
            compressed = zlib.compress(json_data)
        elif self.MSGTYPE == MSGTYPE_1:
            signature = hmac.new(self.key, json_data, hashlib.sha256).digest()
            compressed = zlib.compress(signature + json_data)
        else:
            # unrecognized message type, don't know what to do
            return

        metadata = struct.pack('!ci', self.MSGTYPE, len(compressed))
        return self._socket.sendall(metadata + compressed)

    def receive(self):
        try:
            metadata = self._socket.recv(5)
        except socket.error:
            return

        message_type, length = struct.unpack('!ci', metadata)
        compressed = self._socket.recv(length)

        if self.MSGTYPE != message_type:
            return

        decompressed = zlib.decompress(compressed)

        if message_type == MSGTYPE_0:
            json_data = decompressed
        elif message_type == MSGTYPE_1:
            signature, json_data = decompressed[:32], decompressed[32:]
            verify = hmac.new(self.key, json_data, hashlib.sha256).digest()
            if verify != signature:
                # signature error. ignoring message'
                return
        else:
            # unrecognized message type. ignoring
            return

        data = json.loads(json_data)
        return data

    def poll(self):
        try:
            _ = self._socket.recv(0)
        except socket.error:
            return False
        else:
            return True

    def close(self):
        self._socket.setblocking(True)
        self._socket.close()


class ServerSocket(object):
    def __init__(self, key=None):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = None
        self.key = key

    def __del__(self):
        self._socket.close()

    def bind(self, (ip_address, port), listen=5):
        self.address = (ip_address, port)
        self._socket.bind((ip_address, port))
        self._socket.listen(listen)
        self._socket.setblocking(False)

    def accept(self):
        try:
            new_socket, address = self._socket.accept()
        except socket.error:
            return None

        new_socket.setblocking(False)
        result = ClientSocket(key=self.key)
        result._socket = new_socket
        result.local_address = new_socket.getsockname()
        result.remote_address = address
        return result

    def close(self):
        self._socket.setblocking(True)
        self._socket.close()
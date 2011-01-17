# message.py -- interface to netlink messages
# Copyright 2011 Sean Robinson <seankrobinson@gmail.com>
#
# This file is part of the pymnl package, a Python interface
# for netlink sockets.
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public License
#  as published by the Free Software Foundation; either version 2.1 of
#  the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the Free Software
#  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307
#  USA
#
# Much of the method docstrings are from libmnl and are
#      Copyright 2008-2010 by Pablo Neira Ayuso <pablo@netfilter.org>
#

from struct import calcsize, pack, unpack

import pymnl
from pymnl.attributes import Attr

class Message:
    # pack/unpack format for msg_length, msg_type, msg_flags, msg_seq, pid
    header_format = "ihhii"

    def __init__(self, buffer=None):
        """ A netlink message.

            Netlink message:

            |<----------------- 4 bytes ------------------->|
            |<----- 2 bytes ------>|<------- 2 bytes ------>|
            |-----------------------------------------------|
            |      Message length (including header)        |
            |-----------------------------------------------|
            |     Message type     |     Message flags      |
            |-----------------------------------------------|
            |           Message sequence number             |
            |-----------------------------------------------|
            |                 Netlink PortID                |
            |-----------------------------------------------|
            |                                               |
            .                   Payload                     .
            |_______________________________________________|

            There is usually an extra header after the the Netlink header
            (at the beginning of the payload). This extra header is specific
            of the Netlink subsystem. After this extra header, it comes the
            sequence of attributes that are expressed in
            Type-Length-Value (TLV) format.
        """
        self.msg_length = 0
        self.msg_type = 0
        self.msg_flags = 0
        self.msg_seq = 0
        self.pid = 0
        self.payload = None

        if (buffer):
            header_size = calcsize(Message.header_format)

            (self.msg_length,
            self.msg_type,
            self.msg_flags,
            self.msg_seq,
            self.pid) = unpack(Message.header_format, buffer[:header_size])

            self.payload = Payload(buffer[pymnl.align(header_size):])

    def packed(self):
        """ Return a packed struct for sending to netlink socket.
        """
        if (not self.payload):
            raise UnboundLocalError("payload")

        self.msg_length = pymnl.align(calcsize(Message.header_format) +
                                                len(self.payload))

        return pack(Message.header_format + self.payload.format(),
                self.msg_length,
                self.msg_type,
                self.msg_flags,
                self.msg_seq,
                self.pid,
                self.payload.get())


class Payload:
    def __init__(self, contents=None):
        """ The payload of a netlink message.
        """
        if (contents):
            self.set(contents)

    def __len__(self):
        """ Get the length of the payload (in bytes).
        """
        return len(self._contents)

    def __getdata__(self):
        """ Return the non-header data string.
        """
        return self._contents

    def __repr__(self):
        """ Return escaped data string.
        """
        return repr(self._contents)

    def set(self, contents):
        """ Set the payload contents.

            contents - string representing the payload
        """
        self._contents = contents
        self._format = repr(pymnl.align(len(self._contents))) + "s"

    def format(self):
        """ Get the payload's struct format.
        """
        return self._format

    def add_attr(self, attribute):
        """ Add an Attr object to the payload.

            attribute - an Attr object
        """
        self.set(self._contents + attribute.packed())












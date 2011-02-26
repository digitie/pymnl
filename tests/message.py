#!/usr/bin/python
# tests/message.py -- test interface for netlink messages
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

from random import randint
from struct import pack
import unittest

import pymnl
from pymnl.message import *

class TestPayload(unittest.TestCase):

    def _test_init(self):
        """ Test init of a Payload.
        """
        self.payload = Payload(pack("BBH", 3, 1, 0))
        self.binary = pack("ssss", "\x03", "\x01", "\x00", "\x00")
        self.assertEqual(self.payload.get_binary(), self.binary)

    def _test_add_attr(self):
        """ Test adding Attr objects to the Payload.
        """
        self.family_type = Attr.new_u32(1, 16)
        self.payload.add_attr(self.family_type)
        self.binary = self.binary + pack("ssssssss",
                                            "\x08", "\x00", "\x01", "\x00",
                                            "\x10", "\x00", "\x00", "\x00")
        self.assertEqual(self.payload.get_binary(), self.binary)

        self.family_name = Attr.new_strz(2, b'nl80211')
        self.payload.add_attr(self.family_name)
        self.binary = self.binary + pack("ssssssssssss",
                                            "\x0c", "\x00", "\x02", "\x00",
                                            "n", "l", "8", "0",
                                            "2", "1", "1", "\x00")
        self.assertEqual(self.payload.get_binary(), self.binary)

    def test_payload(self):
        """ Call private test methods which build a Payload step-by-step.
        """
        self._test_init()
        self._test_add_attr()

    def tearDown(self):
        """ Clean up after each test.
        """
        self.payload = None

    @staticmethod
    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(TestPayload)


class TestMessage(unittest.TestCase):

    def setUp(self):
        """
        """
        self.msg = Message()
        self.msg._msg_type = 16  # GENL_ID_CTRL
        self.msg._msg_flags = 5  # NLM_F_REQUEST | NLM_F_ACK

        self.seq = randint(0, pow(2, 31))
        self.msg._msg_seq = self.seq

        self.pid = randint(0, pow(2, 31))
        self.msg._pid = self.pid

        self.msg_length = 16
        self.msg_header = pack("HHII", self.msg._msg_type,
                                       self.msg._msg_flags,
                                       self.seq, self.pid)

    def test_put_extra_header(self):
        """
        """
        # add a four byte header object
        extra_header = Payload(pack("BBH", 3, 1, 0))
        self.msg.put_extra_header(extra_header)
        self.msg_length = self.msg_length + 4
        self.binary = (pack("I", self.msg_length) + self.msg_header +
                        extra_header.get_binary())
        self.assertEqual(self.msg.get_binary(), self.binary)

    def test_add_payload(self):
        """
        """
        payload = Payload(pack("BBH", 3, 1, 0))
        self.msg.add_payload(payload)
        self.msg_length = self.msg_length + 4
        self.binary = (pack("I", self.msg_length) + self.msg_header +
                        payload.get_binary())
        self.assertEqual(self.msg.get_binary(), self.binary)

    def test_get_payload(self):
        """
        """
        payload_in = Payload(pack("BBH", 3, 1, 0))
        self.msg.add_payload(payload_in)
        payload_out = self.msg.get_payload()
        self.assertEqual(payload_in, payload_out)

    def test_ok(self):
        """
        """
        self.assertTrue(self.msg.ok())

    def test_seq_ok(self):
        """
        """
        self.assertTrue(self.msg.seq_ok(self.seq))
        # false result possible if random number == seq
        self.assertFalse(self.msg.seq_ok(randint(0, pow(2, 31))))

    def test_portid_ok(self):
        """
        """
        self.assertTrue(self.msg.portid_ok(self.pid))
        # false result possible if random number == portid
        self.assertFalse(self.msg.portid_ok(randint(0, pow(2, 31))))

    def tearDown(self):
        """
        """
        self.msg = None

    @staticmethod
    def suite():
        return unittest.TestLoader().loadTestsFromTestCase(TestMessage)


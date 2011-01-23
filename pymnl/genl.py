# genl.py -- interface to netlink messages
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

import pymnl
from pymnl.attributes import AttrParser

#
# linux/genetlink.h
#
GENL_NAMSIZ = 16     # length of family name

GENL_MIN_ID = pymnl.NLMSG_MIN_TYPE
GENL_MAX_ID = 1023

GENL_ADMIN_PERM = 0x01
GENL_CMD_CAP_DO = 0x02
GENL_CMD_CAP_DUMP = 0x04
GENL_CMD_CAP_HASPOL = 0x08

# List of reserved static generic netlink identifiers:
GENL_ID_GENERATE = 0
GENL_ID_CTRL = pymnl.NLMSG_MIN_TYPE

# controller commands
CTRL_CMD_UNSPEC = 0
CTRL_CMD_NEWFAMILY = 1
CTRL_CMD_DELFAMILY = 2
CTRL_CMD_GETFAMILY = 3
CTRL_CMD_NEWOPS = 4
CTRL_CMD_DELOPS = 5
CTRL_CMD_GETOPS = 6
CTRL_CMD_NEWMCAST_GRP = 7
CTRL_CMD_DELMCAST_GRP = 8
CTRL_CMD_GETMCAST_GRP = 9     # unused
CTRL_CMD_MAX = 10             # always keep last

# generic netlink controller attribute types
CTRL_ATTR_UNSPEC = 0
CTRL_ATTR_FAMILY_ID = 1
CTRL_ATTR_FAMILY_NAME = 2
CTRL_ATTR_VERSION = 3
CTRL_ATTR_HDRSIZE = 4
CTRL_ATTR_MAXATTR = 5
CTRL_ATTR_OPS = 6
CTRL_ATTR_MCAST_GROUPS = 7
CTRL_ATTR_MAX = 8             # always keep last

CTRL_ATTR_OP_UNSPEC = 0
CTRL_ATTR_OP_ID = 1
CTRL_ATTR_OP_FLAGS = 2
CTRL_ATTR_OP_MAX = 3

CTRL_ATTR_MCAST_GRP_UNSPEC = 0
CTRL_ATTR_MCAST_GRP_NAME = 1
CTRL_ATTR_MCAST_GRP_ID = 2
CTRL_ATTR_MCAST_GRP_MAX = 3


class GenlAttrParser(AttrParser):
    """ Parser for generic netlink attributes.
    """
    def __init__(self):
        # dict to hold attributes without an assigned callback
        self._attributes = { 'extras': [] }

        self._cb = {CTRL_ATTR_FAMILY_ID : self.ctrl_attr_family_id,
                    CTRL_ATTR_FAMILY_NAME : self.ctrl_attr_family_name,
                    CTRL_ATTR_VERSION : self.ctrl_attr_version}

    def ctrl_attr_family_id(self, attr):
        """ Print family id.

            attr - Attr object
        """
        self._attributes['id'] = attr.get_u16()

    def ctrl_attr_family_name(self, attr):
        """ Print family name.

            attr - Attr object
        """
        self._attributes['name'] = attr.get_str()

    def ctrl_attr_version(self, attr):
        """ Print version.

            attr - Attr object
        """
        self._attributes['version'] = attr.get_u32()


class GenlAttrOpParser(AttrParser):
    """ Parser for generic netlink nested op attributes.
    """
    def __init__(self):
        # list to hold attributes without an assigned callback
        self._attributes = []

        self._cb = {CTRL_ATTR_OP_ID : self.ctrl_attr_op_id}

    def ctrl_attr_op_id(self, attr):
        self._attributes.append(attr.get_u32())


class GenlAttrGroupParser(AttrParser):
    """ Parser for generic netlink nested group attributes.
    """
    def __init__(self):
        # list to hold attributes without an assigned callback
        self._attributes = []

        self._cb = {CTRL_ATTR_MCAST_GRP_ID : self.ctrl_attr_mcast_group_id,
                CTRL_ATTR_MCAST_GRP_NAME : self.ctrl_attr_mcast_group_name}

    def ctrl_attr_mcast_group_id(self, attr):
        self._attributes.append(attr.get_u32())

    def ctrl_attr_mcast_group_name(self, attr):
        self._attributes.append(attr.get_str())


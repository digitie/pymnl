# pymnl -- a minimalistic pure Python interface for netlink
# Copyright 2011 Sean Robinson <seankrobinson@gmail.com>
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

# This module is heavily influenced by the excellent libmnl
# from Pablo Neira Ayuso <pablo@netfilter.org>.  However,
# pymnl does not use libmnl.

from ctypes import *

def PYMNL_ALIGN(align_size):
    """ Return a function to calculate alignment.
    """
    return lambda len: (((len) + align_size - 1) & ~(align_size - 1))

#
# linux/netlink.h
#

# netlink types
NETLINK_ROUTE = 0             # Routing/device hook
NETLINK_UNUSED = 1            # Unused number
NETLINK_USERSOCK = 2          # Reserved for user mode socket protocols
NETLINK_FIREWALL = 3          # Firewalling hook
NETLINK_INET_DIAG = 4         # INET socket monitoring
NETLINK_NFLOG = 5             # netfilter/iptables ULOG
NETLINK_XFRM = 6              # ipsec
NETLINK_SELINUX = 7           # SELinux event notifications
NETLINK_ISCSI = 8             # Open-iSCSI
NETLINK_AUDIT = 9             # auditing
NETLINK_FIB_LOOKUP = 10
NETLINK_CONNECTOR = 11
NETLINK_NETFILTER = 12        # netfilter subsystem
NETLINK_IP6_FW = 13
NETLINK_DNRTMSG = 14          # DECnet routing messages
NETLINK_KOBJECT_UEVENT = 15   # Kernel messages to userspace
NETLINK_GENERIC = 16
NETLINK_SCSITRANSPORT = 18    # SCSI Transports
NETLINK_ECRYPTFS = 19

MAX_LINKS = 32

# Flags values
NLM_F_REQUEST = 1       # It is a request message.
NLM_F_MULTI = 2         # Multipart message, terminated by NLMSG_DONE
NLM_F_ACK = 4           # Reply with ack, with zero or error code
NLM_F_ECHO = 8          # Echo this request

# Modifiers to GET request
NLM_F_ROOT = 0x100      # specify tree root
NLM_F_MATCH = 0x200     # return all matching
NLM_F_ATOMIC = 0x400    # atomic GET
NLM_F_DUMP = (NLM_F_ROOT|NLM_F_MATCH)

# Modifiers to NEW request
NLM_F_REPLACE = 0x100   # Override existing
NLM_F_EXCL = 0x200      # Do not touch, if it exists
NLM_F_CREATE = 0x400    # Create, if it does not exist
NLM_F_APPEND = 0x800    # Add to end of list

SOCKET_BUFFER_SIZE = 8192

# define netlink-specific flags
NETLINK_ADD_MEMBERSHIP = 1
NETLINK_DROP_MEMBERSHIP = 2
NETLINK_PKTINFO = 3
NETLINK_BROADCAST_ERROR = 4
NETLINK_NO_ENOBUFS = 5

# netlink attribute types
NLA_UNSPEC = 0    # Unspecified type
NLA_U8 = 1        # 8bit integer
NLA_U16 = 2       # 16bit integer
NLA_U32 = 3       # 32bit integer
NLA_U64 = 4       # 64bit integer
NLA_STRING = 5    # character string
NLA_FLAG = 6      # flag
NLA_MSECS = 7     # micro seconds (64bit)
NLA_NESTED = 8    # nested attributes
NLA_TYPE_MAX = 9  # always keep last

NLA_F_NESTED = (1 << 15)
NLA_F_NET_BYTEORDER = (1 << 14)
NLA_TYPE_MASK = ~(NLA_F_NESTED | NLA_F_NET_BYTEORDER)





# -*- coding: utf-8 -*-
"""
    pycroft.model.hosts
    ~~~~~~~~~~~~~~

    This module contains the classes Host, NetDevice, Switch.

    :copyright: (c) 2011 by AG DSN.
"""
from base import ModelBase
from sqlalchemy import ForeignKey, event
from sqlalchemy import Column
#from sqlalchemy.dialects import postgresql
from pycroft.model import dormitory
from sqlalchemy.orm import backref, relationship, validates
from sqlalchemy.types import Integer
from sqlalchemy.types import String
import ipaddr

import re

from pycroft.helpers import host_helper


class Host(ModelBase):
    hostname = Column(String(255), nullable=False)
    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    # many to one from Host to User
    user = relationship("User", backref=backref("hosts"))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)

    # many to one from Host to Room
    room = relationship(dormitory.Room, backref=backref("hosts"))
    room_id = Column(Integer, ForeignKey("room.id"), nullable=True)


class NetDevice(ModelBase):
    #mac = Column(postgresql.MACADDR, nullable=False)
    mac = Column(String(12), nullable=False)

    # one to one from PatchPort to NetDevice
    patch_port_id = Column(Integer, ForeignKey('patchport.id'), nullable=True)
    patch_port = relationship("PatchPort", backref=backref("net_device",
                                                          uselist=False))

    host_id = Column(Integer, ForeignKey("host.id"), nullable=False)
    host = relationship("Host", backref=backref("net_devices"))

    mac_regex = re.compile(r"^[a-f0-9]{2}(:[a-f0-9]{2}){5}$")


    @validates('mac')
    def validate_mac(self, _, value):
        if not NetDevice.mac_regex.match(value):
            raise Exception("invalid MAC address!")
        if int(value[1], base=16) & 1:
            raise Exception("Multicast-Flag (least significant bit im "
                            "ersten Byte gesetzt)!")
        return value


class Ip(ModelBase):
    def __init__(self, *args, **kwargs):
        super(Ip, self).__init__(*args, **kwargs)

        if self.address is not None and self.subnet is not None:
            assert self.is_ip_valid, "Subnet does not contain the ip"

    address = Column(String(51), unique=True, nullable=False)
    #address = Column(postgresql.INET, nullable=True)

    net_device_id = Column(Integer, ForeignKey('netdevice.id'), nullable=False)
    net_device = relationship(NetDevice, backref=backref("ips"))

    subnet_id = Column(Integer, ForeignKey("subnet.id"), nullable=False)
    subnet = relationship("Subnet", backref=backref("ips"))

    def change_ip(self, ip, subnet):
        self.subnet = None
        self.address = ip
        self.subnet = subnet

    def _ip_subnet_valid(self, ip, subnet):
        return ipaddr.IPAddress(ip) in ipaddr.IPNetwork(subnet.address)

    @property
    def is_ip_valid(self):
        if self.address is None or self.subnet is None:
            return False
        return self._ip_subnet_valid(self.address, self.subnet)

    @validates('subnet')
    def validate_subnet(self, _, value):
        if value is None:
            return value
        if self.address is not None:
            assert self._ip_subnet_valid(self.address, value), \
                    "Given subnet does not contain the ip"
        return value

    @validates("address")
    def validate_address(self, _, value):
        if value is None:
            return value
        if self.subnet is not None:
            assert self._ip_subnet_valid(value, self.subnet), \
                    "Subnet does not contain the given ip"
        return value


def _check_correct_ip_subnet(mapper, connection, target):
    if target.address is not None and target.subnet is not None:
        assert target.is_ip_valid, "Subnet does not contain the ip"


event.listen(Ip, "before_insert", _check_correct_ip_subnet)
event.listen(Ip, "before_update", _check_correct_ip_subnet)


class Switch(Host):
    __mapper_args__ = {'polymorphic_identity': 'switch'}
    id = Column(Integer, ForeignKey('host.id'), primary_key=True)

    name = Column(String(127), nullable=False)

    #management_ip = Column(postgresql.INET, nullable=False)
    management_ip = Column(String(51), unique=True, nullable=False)

# -*- coding: utf-8 -*-
"""
pycroft.model.accounting
~~~~~~~~~~~~~~

This module contains the classes LogEntry, UserLogEntry, TrafficVolume.

:copyright: (c) 2011 by AG DSN.
"""
from base import ModelBase
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy.orm import relationship, backref
from sqlalchemy.types import Boolean, BigInteger, Enum, Integer, DateTime
from sqlalchemy.types import Text


class TrafficVolume(ModelBase):
    # how many bytes
    size = Column(BigInteger, nullable=False)
    # when this was logged
    timestamp = Column(DateTime, nullable=False)
    type = Column(Enum("IN", "OUT", name="traffic_types"), nullable=False)

    # many to one from TrafficVolume to NetDevice
    net_device = relationship("NetDevice",
                backref=backref("traffic_volumes"))
    net_device_id = Column(Integer, ForeignKey("netdevice.id"), nullable=False)

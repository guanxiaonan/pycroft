from pycroft.model.dormitory import Dormitory, Room, Subnet, VLan
from pycroft.model import session


def create_dormitory(number, short_name, street, commit=True):
    """
    This method will create a new dormitory.

    :param short_name: the name which is used as abbreviation.
    :param street: the street where the dormitory is located.
    :param number: the number of the dormitory
    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :return: the newly created dormitory
    """
    dormitory = Dormitory(number=number, short_name=short_name, street=street)
    session.session.add(dormitory)
    if commit:
        session.session.commit()

    return dormitory


def delete_dormitory(dormitory_id, commit=True):
    """
    This method will remove the dormitory fot the given id.

    :param dormitory_id: the id of the dormitory which should be removed
    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :return: the deleted dormitory
    """
    dormitory = Dormitory.q.get(dormitory_id)
    if dormitory is None:
        raise ValueError("The given id is wrong!")

    session.session.delete(dormitory)
    if commit:
        session.session.commit()

    return dormitory


def create_room(number, level, inhabitable, dormitory_id, commit=True):
    """
    This method creates a new room.


    :param number: the number of the room.
    :param level: the level within the dormitory where the room is located.
    :param inhabitable: whether or not someone can live in the room.
    :param dormitory_id: the id of the dormitory in which the room is located.
    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :return: the newly created room
    """
    room = Room(number=number, level=level, inhabitable=inhabitable,
                dormitory_id=dormitory_id)
    session.session.add(room)
    if commit:
        session.session.commit()

    return room


def delete_room(room_id, commit=True):
    """
    This method will remove the room for the given id.

    :param room_id: the id of the room which should be deleted
    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :return: the deleted room
    """
    room = Room.q.get(room_id)
    if room is None:
        raise ValueError("The given id is wrong!")

    session.session.delete(room)
    if commit:
        session.session.commit()

    return room


def create_subnet(address, gateway, dns_domain, reserved_addresses, ip_type,
                  commit=True):
    """
    This method will create a new subnet.


    :param address: the subnet address
    :param gateway: the standard gateway
    :param dns_domain: the dns domain
    :param reserved_addresses: the number of reserved addresses
    :param ip_type: the ip version which should be used
    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :return: the newly created subnet.
    """
    subnet = Subnet(address=address, gateway=gateway, dns_domain=dns_domain,
                    reserved_addresses=reserved_addresses, ip_type=ip_type)
    session.session.add(subnet)
    if commit:
        session.session.commit()

    return subnet


def delete_subnet(subnet_id, commit=True):
    """
    This method will remove the subnet for the given id.

    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :param subnet_id: the id of the subnet which should be removed.
    :return: the removed subnet.
    """
    subnet = Subnet.q.get(subnet_id)
    if subnet is None:
        raise ValueError("The given id is wrong!")

    session.session.delete(subnet)
    if commit:
        session.session.commit()

    return subnet


def create_vlan(name, tag, commit=True):
    """
    This method will create a new vlan.


    :param name: the name of the vlan
    :param tag: the tag which should be used for this vlan
    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :return: the newly created vlan.
    """
    vlan = VLan(name=name, tag=tag)
    session.session.add(vlan)
    if commit:
        session.session.commit()

    return vlan


def delete_vlan(vlan_id, commit=True):
    """
    This method will remove the vlan for the given id.

    :param commit: flag which indicates whether the session should be
                   committed or not. Default: True
    :param vlan_id: the id of the vlan which should be removed.
    :return: the removed vlan.
    """
    vlan = VLan.q.get(vlan_id)
    if vlan is None:
        raise ValueError("The given id is wrong!")

    session.session.delete(vlan)
    if commit:
        session.session.commit()

    return vlan
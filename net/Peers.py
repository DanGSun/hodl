import json
import time
import traceback
from socket import socket
import random
import cryptogr as cg
import mmh3
import logging as log
from .proto import recv, send
from .protocol import generate


meta = """HODL_NetP v1"""


def ats(addr):
    return addr[0] + ':' + str(addr[1])


def afs(addr):
    return addr.split(':')[0], int(addr.split(':')[1])


class Peer:
    """
    Class for one peer.
    """

    def __init__(self, addr, netaddrs):
        """
        :param addr: Peer's HODL wallet
        :param netaddrs: Peer's IPs (dict: {IP1: whiteness of IP1, IP2: whiteness of IP2})
        """
        self.addr = addr
        self.netaddrs = [ats(addr) for addr in netaddrs]

    def connect(self, peers, exc=tuple(), n=3):
        """Generate sockets to all IP addresses for this peer"""
        log.debug('Peer.connect: Connecting to peer. self.netaddrs: ' + str(self.netaddrs) + '\n')
        sockets = []
        for addr in self.netaddrs:
            if addr not in exc:
                log.debug(str(time.time()) + ':Peer.connect: connecting to ' + str(addr))
                try:
                    sock = socket()
                    sock.connect(afs(addr))
                    sockets.append(sock)
                    log.debug('Peer.connect: new socket to white address ' + str(addr) + ': ' + str(sock))
                except:
                    log.debug('Peer.connect: exception while connecting to ' + str(addr) +' : '
                              + traceback.format_exc())
        white_conns = peers.white_conn_to(self.addr, n)
        sockets += white_conns
        return sockets

    def connect_white(self):
        sockets = []
        for addr in self.netaddrs:
            try:
                sock = socket()
                sock.settimeout(2)
                sock.connect(afs(addr))
                sockets.append(sock)
            except:
                pass
        return sockets

    def __str__(self):
        return json.dumps([self.addr, self.netaddrs])

    @classmethod
    def from_json(cls, s):
        """
        Restore peer from json string generated by str(peer)
        :type s: str
        :return: Peer
        """
        s = json.loads(s)
        self = cls(s[0], s[1])
        return self

    def __hash__(self):
        return mmh3.hash(str(self))

    def __add__(self, other):
        if hash(self) == hash(other):
            return self
        elif self.addr == other.addr:
            new = self
            new.netaddrs = set(self.netaddrs + other.netaddrs)
            return new
        else:
            return self

    def __repr__(self):
        return str(self.netaddrs)


class Peers(set):
    """
    Class for storing peers.
    It is a set of peers(class Peer)
    """

    def save(self, file):
        """
        Save peers to file
        :type file: str
        :return:
        """
        with open(file, 'w') as f:
            f.write(str(self))

    def __str__(self):
        return json.dumps([json.dumps(peer) for peer in list(self)])

    @classmethod
    def from_json(cls, s):
        self = cls()
        for peer in json.loads(s):
            self.add(Peer.from_json(peer))
        return self

    @classmethod
    def open(cls, file):
        """
        Restore peers from file
        :type file: str
        :return:
        """
        with open(file, 'r') as f:
            self = cls.from_json(f.read())
        return self

    def srchbyaddr(self, addr):
        """
        Search peer in self.
        addr is peer's public key.
        :type addr: str
        :return:
        """
        for p in self:
            if p.addr == addr:
                return True, p
        return False, None

    def white_conn_to(self, to, n=3):
        socks = []
        for peer in self:
            socks = peer.connect_white()
            if socks:
                for sock in socks:
                    try:
                        send(sock, json.dumps(generate(requests=[{'type': "between"}], message=to)))
                        socks.append(sock)
                    except:
                        pass
                    if len(socks) == n:
                        return socks
        return socks

    @classmethod
    def from_list(cls, l):
        self = cls()
        for peer in l:
            self.add(peer)

    def __hash__(self):
        return mmh3.hash(str(self))

    def __add__(self, other):
        if hash(self) == hash(other):
            return self
        else:
            peers = list(self)
            other = list(other)
            for i in range(len(peers)):
                for j in range(len(other)):
                    peers[i] += other[j]
            return Peers.from_list(peers)

    def hash_list(self):
        """
        List of peers' hashes
        :return: list
        """
        return [hash(peer) for peer in list(self)]

    def peer_by_hash(self, h):
        """
        Find peer with hash h
        :param h: int, hash
        :return: Peer
        """
        for peer in list(self):
            if hash(peer) == h:
                return peer

    def needed_peers(self, another_hashes):
        my_hashes = set(self.hash_list())
        another_hashes = set(another_hashes)
        needed = another_hashes.difference(my_hashes)
        return list(needed)

    def __repr__(self):
        return '{} peers: {}'.format(str(len(self)), str([len(p.netaddrs) for p in self]))

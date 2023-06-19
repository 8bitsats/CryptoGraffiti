#!/usr/bin/env python3
#
# This file is placed in the public domain.
#
# CryptoGraffiti tool
#
# Requires python-bitcoinlib-v0.2.1
#
# https://github.com/petertodd/python-bitcoinlib
#
# pip install python-bitcoinlib

import collections
import sys

from bitcoin.rpc import Proxy
from bitcoin.wallet import P2PKHBitcoinAddress

DUST = 0.000055

def main():
    if len(sys.argv) != 2:
        print("Usage: ./cryptograffiti.py <textfile>")
        return

    filename = sys.argv[1]
    addrs = read_addresses(filename)

    if not addrs:
        print("No addresses found in the file.")
        return

    addrs['1MVpQJA7FtcDrwKC6zATkZvZcxqma4JixS'] = 0.0009

    print('%d outputs with total cost: %f mBTC + fees' % (len(addrs), sum(addrs.values()) * 1000))

    r = input('Send? (y/n)\n')

    if r.lower() == 'y':
        proxy = Proxy()
        result = proxy.sendmany('', addrs)
        print('Sent: %s' % result)
    else:
        print('Canceled!')

def read_addresses(filename):
    addrs = collections.OrderedDict()

    with open(filename, 'rb') as fd:
        while True:
            b = fd.read(20)

            if not b:
                break

            addr = P2PKHBitcoinAddress.from_bytes(b.ljust(20))
            addrs[str(addr)] = DUST

    return addrs

if __name__ == '__main__':
    main()

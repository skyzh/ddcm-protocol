# Kademlia-Async

Use Kademlia in Python Asyncio

Inspired by [bmuller/kademlia](https://github.com/bmuller/kademlia)

## License

The new BSD

## Test

### RPC Test

This test will make you know if rpc module works.

    cd test
    chmod +x rpc_test.py
    ./rpc_test.py

You'll see ping message from two origins.

## Remote

We use Remote instead of (host, port) pair because this network may be available
in a Bluetooth network or a Wi-Fi Direct network.

## Server

You can find KademliaServer in server.py.

## Node

Node is a structure to store peer info. ID is a 160-bit bytes object.
Hash is number data of ID.

## RPC

RPC Module helps organize message in a structure.

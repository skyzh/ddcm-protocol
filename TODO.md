# Todo

## Test

### KBucket Test

Todo

## Service

A Kademlia Service contains a Server, KBucket, Protocol, RPC and Settings.

    Service(config)
        - TCPServer
        - UDPServer
        - KademliaInterface
        - Protocol
        - RPC
        - KBucket
        - Storage

## KBucket

A Bucket storing peer information.

## Storage

A Data Structure storing key-value data.

*   Forgetful Storage: Forget all data after exiting the program.
*   Redis Storage: Save all key-value data in Redis.

## Difference

In original paper, Kademlia is based on UDP Protocol.

For sustanbale and stable key-value storage, we use TCP instead UDP.

In the future, we may use UDP when finding a node and use TCP when calling
Store.

Also function of republishing key hasn't be introduced.

## Usage

    git clone https://github.com/SkyZH/kademlia-async && cd kademlia-async
    ./kademlia-cli server start
    ./kademlia-cli server stop
    ./kademlia-cli server restart
    ./kademlia-cli ping 127.0.0.1:8123
    ./kademlia-cli findnode 5791eb23d08acb5c1a21d69c4cea05770929da40
    ./kademlia-cli findvalue 81249f5d6e55cc3618b15aab402d692c30654b4e
    ./kademlia-cli cli
    ./kademlia-cli -c ~/.config/kademlia/config.json
    ./kad-cli1 (alias of kademlia-cli, loading config from cli1.json)


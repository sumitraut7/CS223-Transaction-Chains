from typing import List, Dict
from collections import defaultdict


class Server:
    def __init__(self, id: int, num_servers: int):
        self.id = id
        self.counters = defaultdict(int)  # ctri→j
        self.done = defaultdict(int)  # donej→i

    def increment_counters(self, chain: List[int]) -> Dict[int, int]:
        sequence_numbers = {}
        for server_id in chain:
            self.counters[server_id] += 1
            sequence_numbers[server_id] = self.counters[server_id]
        return sequence_numbers

    def can_execute(self, origin: int, seq_num: int) -> bool:
        return self.done[origin] == seq_num - 1

    def execute(self, origin: int, seq_num: int):
        self.done[origin] = seq_num
        print(f"Server {self.id} executed hop from chain originating at Server {origin} with sequence number {seq_num}")


class DistributedSystem:
    def __init__(self, num_servers: int):
        self.servers = [Server(i, num_servers) for i in range(num_servers)]

    def execute_chain(self, chain: List[int]):
        origin = chain[0]
        sequence_numbers = self.servers[origin].increment_counters(chain)

        print(f"Chain {chain} started at Server {origin}")
        print(f"Sequence numbers: {sequence_numbers}")

        for i, server_id in enumerate(chain):
            server = self.servers[server_id]
            seq_num = sequence_numbers[server_id]

            while not server.can_execute(origin, seq_num):
                pass  # Wait until the server can execute this hop

            server.execute(origin, seq_num)


# Example usage
system = DistributedSystem(5)  # Create a system with 5 servers

# Execute two chains
system.execute_chain([0, 1, 2, 3])
system.execute_chain([0, 2, 3, 4])
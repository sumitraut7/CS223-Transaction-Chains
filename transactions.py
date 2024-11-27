"""

server 1: customers
server 2: 
server 3:
server 4:

"""

class TransactionChains:

    def __init__(self):

        self.chops = {

            'T1': [('select * from customers', 2,[])]

        }

    def get_chains(self, transaction):
        return self.chops.get(transaction, [])


#
chains = TransactionChains()

print(chains.get_chains('T1'))
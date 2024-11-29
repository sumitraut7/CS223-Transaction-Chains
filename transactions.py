"""

server 1: customers
server 2: customers
server 3: flights
server 4: bookings

"""

class TransactionChains:

    def __init__(self):

        self.chops = {

            'T1': [('SELECT seat_availability FROM FLIGHTS WHERE origin = %s AND destination = %s', 3, ['x','y']), 
                   ('UPDATE FLIGHTS SET seats_availability = seats_availability - 1 WHERE seats_availability > 0', 3, []),
                   ('INSERT INTO bookings VALUES(%s,%s,%s,%s4',4,[101,901,1,"confirmed"]),
                   ('UPDATE  INTO customers SET wallet = wallet - 1000',2,[])
            ],
            'T2': [('SELECT * FROM bookings WHERE booking_id  = %s',4,[101]), 'DELETE * FROM bookings where booking_id = %s',4[101],
                   ('UPDATE customers SET wallet = wallet + 1000', 1,[])] 

        }

    def get_chains(self, transaction):
        return self.chops.get(transaction, [])


#
chains = TransactionChains()

print("Chops for T1:", chains.get_chops('T7'))
print("Chops for T2:", chains.get_chops('T8'))
"""

server 1: customers
server 2: customers
server 3: flights
server 4: bookings

"""

class TransactionChains:

    def __init__(self):

        self.chops = {

            # 'T1': [('SELECT seat_availability FROM FLIGHTS WHERE origin = %s AND destination = %s', 3, ['x','y']), 
            #        ('UPDATE FLIGHTS SET seats_availability = seats_availability - 1 WHERE seats_availability > 0', 3, []),
            #        ('INSERT INTO bookings VALUES(%s,%s,%s,%s4',4,[101,901,1,"confirmed"]),
            #        ('UPDATE  INTO customers SET wallet = wallet - 1000',2,[])
            # ],
            # 'T2': [('SELECT * FROM bookings WHERE booking_id  = %s',4,[101]), 'DELETE * FROM bookings where booking_id = %s',4[101],
            #        ('UPDATE customers SET wallet = wallet + 1000', 1,[])] 

            'T1': [('SELECT * FROM patients WHERE patient_id = %s', 1, [101]), 
                   ('SELECT * FROM doctors', 2, []),
                   ('INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status) VALUES (%s,%s, %s, %s, %s)', 3, [301,101,201,('2024-12-01 10:00:00'),('scheduled')])
                   ],
            'T2': [('SELECT * FROM patients WHERE patient_id = %s', 1, [102]), 
                   ('INSERT INTO billing (patient_id, appointment_id, amount_due) VALUES (%s, %s, %s)',7 , [102,302,100]),
                   ('SELECT *  FROM appointments WHERE appointment_id = %s',3, [502]),
                   ('UPDATE appointments SET status = %s WHERE appointment_id = %s',3, ['Completed',302])
                   ],
            'T3': [('SELECT * FROM patients WHERE patient_id = %s', 1, [103]), 
                   ('INSERT INTO medical_records (record_id, patient_id, doctor_id, diagnosis, treatment) VALUES (%s,%s,%s,%s,%s)',4, [403, 103,303, 'Flu', 'Rest and hydration recommended']),
                   ('INSERT INTO prescriptions (prescription_id, patient_id, doctor_id, medication_name, dosage, duration) VALUES (%s,%s,%s,%s,%s,%s)',5, [503,103,303, 'Amoxicillin', '500 mg', '7 days'])
                   ],       
            'T4': [('SELECT * FROM patients where patient_id = %s', 1, [103]), 
                   ('SELECT * FROM medical_records WHERE patient_id = %s',4, [403]),
                   ('SELECT * from doctors WHERE specialization = %s',2, ['Cardiology']),
                   ('INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status) VALUES (%s,%s, %s, %s, %s)', 3, [304,103,203,('2024-12-11 10:00:00'),('scheduled')])
                   ],   

        }

    def get_chains(self, transaction):
        return self.chops.get(transaction, [])


#
chains = TransactionChains()

print("Chops for T1:", chains.get_chops('T1'))
print("Chops for T2:", chains.get_chops('T2'))
print("Chops for T3:", chains.get_chops('T3'))
print("Chops for T4:", chains.get_chops('T4'))
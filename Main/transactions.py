"""

server 1: patients, icu
server 2: doctors
server 3: appointments
server 4: medical records
server 5: prescription
server 6: patients, icu
server 7: billing

"""

chops = {

            'T1': [('SELECT * FROM patients WHERE patient_id = %s', 1, [101]),
                   ('SELECT * FROM doctors', 2, []),
                   ('INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status) VALUES (%s,%s, %s, %s, %s)',3, [301, 101, 201, ('2024-12-01 10:00:00'), ('scheduled')])
                   ],
            'T2': [('SELECT * FROM patients WHERE patient_id = %s', 1, [102]),
                   ('INSERT INTO billing (patient_id, appointment_id, amount) VALUES (%s, %s, %s)',7 , [102,302,100]),
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



evaluation_set = {
    'T1': [('SELECT * FROM patients WHERE patient_id = %s', 1, [101]),
           ('SELECT * FROM doctors', 2, []),
           ('INSERT INTO appointments (appointment_id, patient_id, doctor_id, appointment_date, status) VALUES (%s,%s, %s, %s, %s)',3, [301, 101, 201, ('2024-12-01 10:00:00'), ('scheduled')])
           ],
}
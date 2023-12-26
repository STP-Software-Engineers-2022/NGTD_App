# Script to querry patient information from database
# Created by Caroline Riehl
# Last updated 25-Dec-2023

import sqlite3

ngtd_db = sqlite3.connect('ngtd.db')

cursor = ngtd_db.cursor()

cursor.execute('''
    SELECT 
        patient.patient_id, 
        test.gms_signed_off, 
        test.gms_signed_off_version, 
        test.panelapp_id_number, 
        gene.symbol, 
        bedfile.file_path  
    FROM 
        patient
    JOIN 
        patient2test on patient.id = patient2test.patient_id 
    JOIN 
        test on patient2test.test_id = test.id
    JOIN 
        test2gene on test.id  = test2gene.test_id 
    JOIN 
        gene on test2gene.gene_id = gene.id
    JOIN 
        bedfile on test.bedfile_id = bedfile.id;''')

rows = cursor.fetchall()

# Process the results
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
ngtd_db.close()
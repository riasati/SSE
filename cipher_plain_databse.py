from PostgresHelper import PostgresHelper
from Crypto.Random import get_random_bytes
from encryption import encrypt_str, decrypt_str


def get_number_of_encrypted_attribute(attributes_name):
    attributes_list = attributes_name.split(",")
    attributes_list = [attr.strip() for attr in attributes_list]
    encrypted_numbers = []
    for attr in attributes_list:
        if attr == "Name":
            encrypted_numbers.append(1)
        elif attr == "Surname":
            encrypted_numbers.append(2)
        elif attr == "Age":
            encrypted_numbers.append(3)
        elif attr == "Gender":
            encrypted_numbers.append(4)
        elif attr == "Occupation":
            encrypted_numbers.append(5)
    return encrypted_numbers



PH = PostgresHelper("postgres")
if PH.check_existence_of_database("\'cipher\'"):
    PH.delete_database("cipher")
if PH.check_existence_of_database("\'plain\'"):
    PH.delete_database("plain")
key = get_random_bytes(16)
while True:
    mode = input("if you want to encrypt database input 1 and if you want to decrypt database input 2\n")
    if mode == "1":
        attributes_name = input("which attribute do you want to encrypt ? (Name, Surname, Age, Gender, Occupation) \n(if you "
                            "want to encrypt more than one attribute, you should input like this \"Name, Surname\")\n")
        attributes_numbers = get_number_of_encrypted_attribute(attributes_name)
        attribute_list = ["\"ID\"", "\"Name\"", "\"Surname\"", "\"Age\"", "\"Gender\"", "\"Occupation\""]
        PH = PostgresHelper("postgres")
        rows = PH.get_all_data_in_table("data_table", attribute_list)
        new_rows = []
        for row in rows:
            ID = row[0]
            Name = row[1]
            Surname = row[2]
            Age = row[3]
            Gender = row[4]
            Occupation = row[5]
            if 1 in attributes_numbers:
                Name = encrypt_str(key, Name)
            if 2 in attributes_numbers:
                Surname = encrypt_str(key, Surname)
            if 3 in attributes_numbers:
                Age = encrypt_str(key, Age)
            if 4 in attributes_numbers:
                Gender = encrypt_str(key, Gender)
            if 5 in attributes_numbers:
                Occupation = encrypt_str(key, Occupation)
            new_rows.append({
                "ID": ID,
                "Name": Name,
                "Surname": Surname,
                "Age": Age,
                "Gender": Gender,
                "Occupation": Occupation
            })
        PH.create_database("cipher")
        PH = PostgresHelper("cipher")
        PH.create_table("data_table", {"ID": "text", "Name": "text", "Surname": "text", "Age": "text", "Gender": "text", "Occupation": "text"})
        for row in new_rows:
            PH.insert_one_row("data_table", row["ID"], row["Name"], row["Surname"], row["Age"], row["Gender"], row["Occupation"])

    elif mode == "2":
        attributes_name = input("which attribute do you want to decrypt ? (Name, Surname, Age, Gender, Occupation) \n(if you "
                                "want to decrypt more than one attribute, you should input like this \"Name, Surname\")\n")
        attributes_numbers = get_number_of_encrypted_attribute(attributes_name)
        attribute_list = ["\"id\"", "\"name\"", "\"surname\"", "\"age\"", "\"gender\"", "\"occupation\""]
        PH = PostgresHelper("cipher")
        rows = PH.get_all_data_in_table("data_table", attribute_list)
        new_rows = []
        for row in rows:
            ID = row[0]
            Name = row[1]
            Surname = row[2]
            Age = row[3]
            Gender = row[4]
            Occupation = row[5]
            if 1 in attributes_numbers:
                Name = decrypt_str(key, Name)
            if 2 in attributes_numbers:
                Surname = decrypt_str(key, Surname)
            if 3 in attributes_numbers:
                Age = decrypt_str(key, Age)
            if 4 in attributes_numbers:
                Gender = decrypt_str(key, Gender)
            if 5 in attributes_numbers:
                Occupation = decrypt_str(key, Occupation)
            new_rows.append({
                "ID": ID,
                "Name": Name,
                "Surname": Surname,
                "Age": Age,
                "Gender": Gender,
                "Occupation": Occupation
            })
        PH.create_database("plain")
        PH = PostgresHelper("plain")
        PH.create_table("data_table", {"ID": "text", "Name": "text", "Surname": "text", "Age": "text", "Gender": "text",
                                       "Occupation": "text"})
        for row in new_rows:
            PH.insert_one_row("data_table", row["ID"], row["Name"], row["Surname"], row["Age"], row["Gender"],
                              row["Occupation"])
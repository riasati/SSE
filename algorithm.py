from PostgresHelper import PostgresHelper
from encryption import Node, pseudo_random_permutation, pseudo_random_function
from Crypto.Random import get_random_bytes


def extract_words(table_name):
    PH = PostgresHelper(database_name="postgres")
    attribute_list = ["\"ID\"", "\"Name\"", "\"Surname\"", "\"Age\"", "\"Gender\"", "\"Occupation\""]
    rows = PH.get_all_data_in_table(table_name, attribute_list)
    words = []
    for row in rows:
        ID = row[0]
        Name = row[1]
        Surname = row[2]
        Age = row[3]
        Gender = row[4]
        Occupation = row[5]
        words.append(f"Name={Name}")
        words.append(f"Surname={Surname}")
        words.append(f"Age={Age}")
        words.append(f"Gender={Gender}")
        words.append(f"Occupation={Occupation}")
    return words


def create_dictionary(words, table_name):
    PH = PostgresHelper(database_name="postgres")
    attribute_list = ["\"ID\"", "\"Name\"", "\"Surname\"", "\"Age\"", "\"Gender\"", "\"Occupation\""]
    rows = PH.get_all_data_in_table(table_name, attribute_list)
    dic = {}
    for word in words:
        search_key = -1
        id_list = []
        split_word = word.split("=")
        if split_word[0] == "Name":
            search_key = 1
        elif split_word[0] == "Surname":
            search_key = 2
        elif split_word[0] == "Age":
            search_key = 3
        elif split_word[0] == "Gender":
            search_key = 4
        elif split_word[0] == "Occupation":
            search_key = 5
        for row in rows:
            if row[search_key] == split_word[1]:
                id_list.append(row[0])
        dic[word] = id_list
    return dic


def create_linked_list_first_keys(words, dictionary, first_key):
    Lists = []
    counter_number = get_number_of_counter(words, dictionary)
    ctr = 0
    first_keys_dic = {}
    first_key_list = []
    for word in words:
        one_list = []
        key = get_random_bytes(16)
        first_keys_dic[word] = key
        first_key_list.append(key)
        for i, id in enumerate(dictionary[word]):
            key = get_random_bytes(16)
            if i == len(dictionary[word]) - 1:
                permutation_output = pseudo_random_permutation(first_key, range(0, counter_number), None)
            else:
                permutation_output = pseudo_random_permutation(first_key, range(0, counter_number), ctr + 1)
            new_node = Node(record_id=id, key=key, permutation_output=permutation_output)
            one_list.append(new_node)
            ctr += 1
        Lists.append(one_list)
    return Lists, first_keys_dic, first_key_list


def get_number_of_counter(words, dictionary):
    counter = 0
    for word in words:
        for id in dictionary[word]:
            counter += 1
    return counter


def create_array_A_first_addresses(words, dictionary, Lists, first_key, first_key_list):
    counter_number = get_number_of_counter(words, dictionary)
    ctr = 0
    A = [None] * counter_number
    first_addresses = []
    for i in range(len(Lists)):
        for j in range(len(Lists[i])):
            key = None
            if j == 0:
                key = first_key_list[i]
            else:
                key = Lists[i][j - 1].key
            new_node = Lists[i][j].encrypt(key)
            permutation_output = pseudo_random_permutation(first_key, range(0, counter_number), ctr)
            if j == 0:
                first_addresses.append(permutation_output)
            A[permutation_output] = new_node
            ctr += 1
    return A, first_addresses


def xor_of_two_bitstring(first_bitstring, second_bitstring):
    first_chunks = [first_bitstring[i:i + 32] for i in range(0, len(first_bitstring), 32)]
    second_chunks = [second_bitstring[i:i + 32] for i in range(0, len(second_bitstring), 32)]

    result_chunks = [format(int(first_chunks[i], 2) ^ int(second_chunks[i], 2), '032b') for i in
                     range(len(first_chunks))]
    result_str = ''.join(result_chunks)
    return result_str


def create_lookup_table_T(words, second_key, third_key, first_keys_dic, first_addresses):
    counter_number = len(words)
    T = [None] * counter_number
    for i, word in enumerate(words):
        permutation_output = pseudo_random_permutation(second_key, range(0, counter_number), i)
        key_integer = int.from_bytes(first_keys_dic[word], byteorder='big')
        key_bit_string = bin(key_integer)[2:].zfill(128)
        address_bit_string = bin(first_addresses[i])[2:].zfill(128)
        random_function_output = pseudo_random_function(third_key, word, 256)
        T[permutation_output] = xor_of_two_bitstring(key_bit_string + address_bit_string, random_function_output)
    return T


def BuildIndex(words, first_key, second_key, third_key):
    dictionary = create_dictionary(words, "data_table")
    linked_list, first_key_dic, first_key_list = create_linked_list_first_keys(words, dictionary, first_key)
    A, first_addresses = create_array_A_first_addresses(words, dictionary, linked_list, first_key, first_key_list)
    T = create_lookup_table_T(words, second_key, third_key, first_key_dic, first_addresses)

    return A, T


def Trapdoor(words, second_key, third_key):
    Trapdoors = {}
    counter_number = len(words)
    for i, word in enumerate(words):
        permutation_output = pseudo_random_permutation(second_key, range(0, counter_number), i)
        random_function_output = pseudo_random_function(third_key, word, 256)
        Trapdoors[word] = (permutation_output, random_function_output)
    return Trapdoors


def Search(A, T, one_trapdoor):
    ids_list = []
    bitstring = T[one_trapdoor[0]]
    address_and_key = xor_of_two_bitstring(one_trapdoor[1], bitstring)
    address = address_and_key[128:]
    address = address.lstrip('0')
    key = address_and_key[:128]
    key_byte_object = int(key, 2).to_bytes((int(key, 2).bit_length() + 7) // 8, 'big')
    decrypted_node = A[int(address, 2)].decrypt(key_byte_object)
    ids_list.append(decrypted_node.record_id)
    while decrypted_node.permutation_output is not None:
        cipher_node = A[decrypted_node.permutation_output]
        key = decrypted_node.key
        decrypted_node = cipher_node.decrypt(key)
        ids_list.append(decrypted_node.record_id)
    return ids_list

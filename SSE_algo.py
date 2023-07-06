from pprint import pprint
from encryption import KeyGen
from algorithm import extract_words, create_dictionary, create_linked_list_first_keys, create_array_A_first_addresses \
    , create_lookup_table_T, Trapdoor, Search

words = extract_words("data_table")
dic = create_dictionary(words, "data_table")
first_key, second_key, third_key = KeyGen(5)
linked_lists, first_keys_dic, first_keys_list = create_linked_list_first_keys(words, dic, first_key)
A, first_addresses = create_array_A_first_addresses(words, dic, linked_lists, first_key, first_keys_list)
T = create_lookup_table_T(words, second_key, third_key, first_keys_dic, first_addresses)
trapdoors = Trapdoor(words, second_key, third_key)
result_dic = {}
for i in range(len(words)):
    result_dic[words[i]] = Search(A, T, trapdoors[words[i]])

pprint(dic)
pprint(result_dic)

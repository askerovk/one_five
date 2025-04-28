def split_list_into_chunks(input_list, chunk_size):
    """"""
    list_range = range(0, len(input_list), chunk_size)

    result = [input_list[i:i + chunk_size] for i in list_range]

    return result

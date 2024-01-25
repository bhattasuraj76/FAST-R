def version_compare( version1, version2 ) :
    # We convert version1 and version2 into tuples with integer values of same length and compare them
    
    # Split the versions by period(.)
    ver1_split = version1.split(".")
    ver2_split = version2.split(".")
    
    
    # Compure maximum tuple length
    max_tuple_length = len(ver1_split) if len(ver1_split) > len(ver2_split) else len(ver2_split)
    
    # Get filled tuples for the versions
    version_tuple1 = get_filled_tuple(ver1_split, max_tuple_length)
    version_tuple2 = get_filled_tuple(ver2_split, max_tuple_length)
    
    # Compare tuples
    if version_tuple1 > version_tuple2:
        return 1
    elif version_tuple2 > version_tuple1:
        return -1
    else:
        return 0
    

# Return tuple for splitted version
def get_filled_tuple(ver_split, max_length):
    # Ensures places are filled with zero if value is not available
    filled = [0] * max_length
    
    for i in range(len(ver_split)):
        # Parse verison no in string to int
        filled[i] = int(ver_split[i])
    
    return tuple(filled)
    


print(version_compare("2.10.3.1", "2.10.3.1.0"))
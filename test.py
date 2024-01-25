def version_compare( version1, version2 ) :
    MAX_LENGTH = 5
    ver1 = version1.split(".")
    ver2 = version2.split(".")
    
    filled_ver1 = [0] * MAX_LENGTH
    filled_ver2 = [0] * MAX_LENGTH
    
    for i in range(len(ver1)):
        filled_ver1[i] = int(ver1[i])
    
    for i in range(len(ver2)):
        filled_ver2[i] = int(ver2[i]) 
    print(filled_ver1)
    return compare(filled_ver1, filled_ver2)
    # print(version1.split(".")[0], version2.split(".")[0])
    # ver1_head = int(version1.split(".")[0] or 0)
    # ver2_head = int(version2.split(".")[0] or 0)
    # print(ver1_head, ver2_head)
    # ver1_tail = version1.split(".")[1:]
    # ver2_tail = version2.split(".")[1:]
    
    
    # if ver1_head == ver2_head:
    #     return version_compare(".".join(ver1_tail), ".".join(ver2_tail))
    # elif ver1_head > ver2_head:
    #     return 1
    # else:
    #     return -1

def compare(a, b):
    if a[0] > b[0]:
        return 1
    elif a[0] < b[0]:
        return -1
    else:
      return 0 if len(a) == 1 else compare(a[1:], b[1:])

print(version_compare("2.10.3.1", "2.10.3.1.0"))
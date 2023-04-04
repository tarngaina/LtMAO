def validate_weight_cmd(x):
    num_count = 0
    not01_count = 0
    sep_count = 0
    for c in x:
        if c in '01':
            num_count += 1
        elif c in '23456789':
            num_count += 1
            not01_count += 1
        elif c == '.':
            sep_count += 1
        else:

            return False
    if num_count > 4:
        return False
    if sep_count > 1:
        return False
    if num_count > 0 and x[0] in '23456789':
        return False
    if num_count > 1 and x[0] == '1':
        if not01_count > 0:
            return False
    return True


print(validate_weight_cmd('0.599999964'))

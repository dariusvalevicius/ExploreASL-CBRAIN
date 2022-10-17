import json

############################# Functions ###############################


def add_level(dict, levels, value):
    '''Recursively populates dictionary
    based on list of levels'''

    # If multiple levels are left...
    if len(levels) > 1:

        # If level is not already present, add it
        if levels[0] not in dict:
            new_dict = {}
            dict[levels[0]] = add_level(new_dict, levels[1:], value)
        # Else if it is present, add to existing level
        else:
            dict[levels[0]] = add_level(dict[levels[0]], levels[1:], value)
    # If only one level, add key: value pair
    else:
        dict[levels[0]] = value

    return dict


def reduce_brackets(dict):
    '''Recursively change lone list items
    in dict to simple variables'''
    for key in dict:
        if type(dict[key]) != list:
            continue
        elif len(dict[key]) == 1:
            dict[key] = dict[key][0]
        else:
            for inner_dict in dict[key]:
                inner_dict = reduce_brackets(inner_dict)
    return dict


def merge_dicts(dict_a, dict_b):
    '''Recursively merge dictionaries, giving priority to the first argument (dictA)'''

    # Base output dict on dict A
    out_dict = dict_a.copy()

    for key in dict_b:
        if key in out_dict.keys():
            # If key is a dict, call fct recursively
            if (type(out_dict[key]) == dict) & (type(dict_b[key]) == dict):
                out_dict[key] = merge_dicts(out_dict[key], dict_b[key])
            # Else do nothing - keep value of dict A
        else:
            # If key is not present in dict A, copy it over
            out_dict[key] = dict_b[key]

    return out_dict


def parse_list_to_dict(params):
    '''Main function to convert dictionary to JSON output'''
    param_dict = {}

    for x in params:
        levels = x.split('__')
        value = params[x]

        # Skip if value is null
        if value is None:
            continue

        param_dict = add_level(param_dict, levels, value)

    param_dict = reduce_brackets(param_dict)
    # json_object = json.dumps(param_dict, indent=4)
    return param_dict


########################## Test ###################################

if __name__ == "__main__":

    # args = {
    #     'x__dataset__subjectRegexp': 1,
    #     'x__modules__asl__blue': 2,
    #     'x__modules__blah': 5

    # }

    # print(args)

    # json_object = json.dumps(parse_list_to_dict(args), indent=4)

    # print(json_object)

    d1 = {
        'x__blah__blu__orange': 1,
        'x__blah__blee__blop': 2,
        'x__chaa': 3,
        'b__hello': 9
    }

    d2 = {
        'x__blah__go': 4,
        'x__blah__blee': 11,
        'x__chaa': 5,
        'c__hi': 10
    }

    d1 = reduce_brackets(parse_list_to_dict(d1))
    d2 = reduce_brackets(parse_list_to_dict(d2))

    print(d1)
    print(d2)

    d3 = merge_dicts(d1, d2)
    print(d3)

    d4 = merge_dicts(d2, d1)
    print(d4)

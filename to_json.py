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

############################### Main ##############################


def to_json(params):

    param_dict = {}

    for x in params:
        levels = x.split('__')
        value = params[x]

        # Skip if value is null
        if value is None:
            continue

        param_dict = add_level(param_dict, levels, value)

    param_dict = reduce_brackets(param_dict)
    json_object = json.dumps(param_dict, indent=4)
    return json_object


########################## Test ###################################

if __name__ == "__main__":

    args = {
        'x__dataset__subjectRegexp': 1,
        'x__modules__asl__blue': 2,
        'x__modules__blah': 5

    }

    print(args)

    json_object = to_json(args)

    print(json_object)

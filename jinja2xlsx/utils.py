from typing import Dict


def union_dicts(dict_1: Dict, dict_2: Dict, with_none_drop: bool = True) -> Dict:
    """
    >>> union_dicts({"a": 1}, {"a": None, "b": 2})
    {'a': 1, 'b': 2}
    """
    if with_none_drop:
        new_dict_2 = {key: value for key, value in dict_2.items() if value is not None}
    else:
        new_dict_2 = dict_2

    return {**dict_1, **new_dict_2}

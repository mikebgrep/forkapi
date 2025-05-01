import copy


def copy_object(source_obj, target_class):
    """
    Copies attributes from source_obj to a new instance of target_class.
    Assumes both objects share similar fields.
    """
    new_obj = target_class()
    new_obj.__dict__ = copy.deepcopy(source_obj.__dict__)
    return new_obj

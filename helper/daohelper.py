def extract_columns(dao_obj, cols):
    r = {col: dao_obj.__dict__[col] for col in dao_obj.__dict__ if col in map(get_column_name, cols)}
    return r


def get_column_name(column):
    return str(column).split('.')[1]


def extract_column(dao_obj, column):
    return getattr(dao_obj, get_column_name(column))

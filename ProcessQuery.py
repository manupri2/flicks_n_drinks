

def write_basic_SELECT_FROM_WHERE(tables_cols, cond=[], left_outer_join=[]):
    """ This function expects the following format:
            tables_cols = dictionary of tables and columns to query
                key = table (string)
                value = columns/attributes (list of strings), if this list is empty assume all columns '*'
            conditions = list of tuples in the format (table, column, operator, value)
    """
    if tables_cols:
        tables = list(tables_cols.keys())
        for table in tables:
            if not tables_cols[table]:
                tables_cols[table] = ['*']
        mapped_table_col_tuples = [(table, col) for table in tables for col in tables_cols[table]]

        query = "SELECT "
        query += make_comma_separated(mapped_table_col_tuples)
        query += "\nFROM "
        query += make_comma_separated(tables)

        if cond:
            query += "\nWHERE "

        return query
    else:
        return "No tables selected."


def make_comma_separated(items):
    """ items are in one of the following formats:
            1) list of tuples - (table, column) - where table/column are strings
            2) list of strings - either table names or column names
    """
    query_str = ''
    for i in range(0, len(items)):
        if isinstance(items[0], tuple):
            query_str += items[i][0] + "." + items[i][1]
        if isinstance(items[0], str):
            query_str += items[i]
        if i < len(items) - 1:
            query_str += ', '

    return query_str


def build_condition(condition):
    """ Function expects a condition in the following format:
        conditions = tuple (table, column, operator, value)
        column = column name (string)
        operator = string representation of operator '=', '>', '<=', etc.
        value = string representation of value
    """
    return condition[0] + "." + condition[1] + " " + condition[2] + " " + condition[3]


def build_date_range_filter_query(query, col, val):
    '''val is a tuple of lower and upper range'''

    # can also be written as 'Table.Column <= Datetime("%s") '
    return "(%s >= '%s 00:00:00' AND %s <= '%s 23:59:59')" % (col, val[0], col, val[1])


if __name__ == '__main__':
    select_from = {'Fruits': ["Apples", "Bananas", "Peaches"],
                   'Meats': ['Chicken', 'Beef', 'Turkey'],
                   'Veggies': []}
    print("Test 1:")
    print("%s\n" % repr(select_from))
    print(write_basic_SELECT_FROM_WHERE(select_from))

    select_from = {}
    print("\nTest 2:")
    print("%s\n" % repr(select_from))
    print(write_basic_SELECT_FROM_WHERE(select_from))
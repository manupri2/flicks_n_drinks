

def write_basic_SELECT_FROM_WHERE(tables_cols, conditions={}, left_outer_join=None):
    """ This function expects the following format:
            tables_cols = dictionary of tables and columns to query
                key = table variable name (string)
                value = list where
                    1) first entry is the original table name but can also be a subquery (if subquery be sure to surround with parentheses)
                    2) second entry is the columns/attributes (list of strings and/or tuples), if this list is empty assume all columns '*'
            conditions = dictionary of conditions to filter by in the WHERE clause
                key = integer keys ranging 0-n; conditions with different keys have OR relationship
                value = list of tuples in format (table, column, operator, value); conditions in the list have AND relationship b/w each other
    """
    if tables_cols:
        tables = list(tables_cols.keys())
        table_tuples = [(tables_cols[table][0], table) for table in tables]
        for table in tables:
            if not tables_cols[table][1]:
                tables_cols[table][1] = ['*']

        table_col_tuples = [(table, col) for table in tables for col in tables_cols[table][1]]

        query = "SELECT "
        query += build_column_names(table_col_tuples)
        query += "\nFROM "
        query += build_table_names(table_tuples)

        if conditions:
            query += "\nWHERE "
            query += build_condition(conditions)
        return query
    else:
        return "No tables selected."


def build_column_names(items):
    """ items are in the following format:
        list of tuples - (table, column) - where table/column are strings
                                        - table name (string) can be a subquery (if subquery be sure to surround with parentheses within string
                                        - column can also be a tuple for renaming (i.e. "Fruits.Apples AS A1")
                                        - enter '' for table if only wanting column name (i.e. "Apples AS A1")
    """
    query_str = ''
    for i in range(0, len(items)):
        if items[i][0] != '':
            query_str += items[i][0] + "."

        if isinstance(items[i][1], tuple):
            query_str += items[i][1][0] + " AS " + items[i][1][1]
        if isinstance(items[i][1], str):
            query_str += items[i][1]

        if i < len(items) - 1:
            query_str += ', '

    return query_str


def build_table_names(items):
    """ items are in the following format:
            list of tuples of strings - table name (string) can be a subquery (if subquery be sure to surround with parentheses)
                                      - list of tuples for renaming (i.e. ('Fruits', 'F1') gives "Fruits AS F1")
                                      - if both entries are same then renaming is ignored (i.e. ('Fruits', 'Fruits') gives "Fruits")
    """
    query_str = ''
    for i in range(0, len(items)):
        if items[i][0] == items[i][1]:
            query_str += items[i][0]
        else:
            query_str += items[i][0] + " AS " + items[i][1]

        if i < len(items) - 1:
            query_str += ', '

    return query_str


def build_condition(conditions):
    """ Function expects a condition in the following format:
        conditions = dictionary of conditions to filter by in the WHERE clause
                key = integer keys ranging 0-n; values (sets of conditions) with different keys have OR relationship b/w each other
                value =  can be list of tuples or list of strings; conditions in the list have AND relationship b/w each other
                value (list of tuples) = list of tuples in format (table, column, operator, comparison_value)
                        table = table name (string) can also be a subquery (if subquery be sure to surround with parentheses
                        column = column/attribute name (string) or tuple as in build_column_table_names above
                        operator = string representation of operator '=', '>', '<=', etc.
                        comparison_value = string representation of value to compare; can also be an SQL subquery (if guaranteed to return a value)
    """
    condition_sets = list(conditions.keys())
    parentheses = True
    if len(condition_sets) == 1:
        parentheses = False

    query = ''
    cond_set_count = 0
    for cond_set_index in condition_sets:
        if cond_set_count > 0:
            query += "\n\t OR "
        if len(conditions[cond_set_index]) > 1 and parentheses:
            query += '('
        cond_count = 0
        for cond in conditions[cond_set_index]:
            if cond_count > 0:
                query += "\n\t AND "

            if isinstance(cond, str):
                query += cond
            else:
                query += build_column_names([(cond[0], cond[1])])
                query += " " + cond[2] + " " + cond[3]

            cond_count += 1
        if len(conditions[cond_set_index]) > 1 and parentheses:
            query += ')'
        cond_set_count += 1
    return query


def build_date_range_filter_query(query, col, val):
    '''val is a tuple of lower and upper range'''
    # this function is not working or currently being used, just keeping it for reference
    # can also be written as 'Table.Column <= Datetime("%s") '
    return "(%s >= '%s 00:00:00' AND %s <= '%s 23:59:59')" % (col, val[0], col, val[1])


def run_test(select_dict, cond_dict, num):
    print("\nTest %d Selection Dictionary:\n%s" % (num, repr(select_dict)))
    print("Test %d Conditions:\n%s" % (num, repr(cond_dict)))
    print("Test %d Query:" % num)
    test_query = write_basic_SELECT_FROM_WHERE(select_dict, cond_dict)
    print(test_query)
    return test_query

if __name__ == '__main__':
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    select_from = {'Fruits': ['Fruits', ["Apples", "Bananas", "Peaches"]],
                   'Meats': ['Meats', ['Chicken', 'Beef', 'Turkey']],
                   'Veggies': ['Veggies', []]}
    cond = {}
    run_test(select_from, cond, 1)
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    select_from = {}
    cond = {}
    run_test(select_from, cond, 2)
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    select_from = {'Fruits': ['Fruits', [('Apples', 'A1'), "Bananas"]],
                   'Meats': ['Meats', [('Chicken', 'Chx'), 'Beef', ('Turkey', 'Bird')]],
                   'Veggies': ['Veggies', []]}
    cond = {0: [('Fruits', 'Apples', '=', '6'), ('Meats', 'Chicken', '>', '20'), ('Veggies', 'Carrots', '<=', '30')],
            1: [('Fruits', 'Bananas', '=', '24')],
            3: [('Fruits', 'Peaches', '=', '68'), ('Meats', 'Beef', '>', '27')]
            }
    run_test(select_from, cond, 3)
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    select_from = {'F1': ['Fruits', ["Apples", "Bananas"]],
                   'M1': ['Meats', ['Chicken']],
                   'Veggies': ['Veggies', []]}
    cond = {0: [('F1', 'Apples', '=', '6'), ('M1', 'Chicken', '>', '20'), ('Veggies', 'Carrots', '<=', '30')]
            }
    run_test(select_from, cond, 4)
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    select_from = {'Fruits': ['Fruits', [('Apples', 'A1'), ('Bananas', 'B1')]],
                   'Meats': ['Meats', ['Chicken', 'Beef', 'Turkey']],
                   'Veggies': ['Veggies', []]}
    cond = {0: [('', 'A1', '=', '6'), ('', 'B1', '>', '20')]
            }
    test_5 = run_test(select_from, cond, 5)
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    cond = {0: ['A1 = 6', 'B1 > 20']
            }
    test_6 = run_test(select_from, cond, 6)
    print(test_5 == test_6)
    # ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
import re


def parse_sql_query(sql_query):
    # Patterns for different SQL query components
    select_pattern = r"SELECT\s+(.*?)\s+FROM\s+(\w+)"
    insert_pattern = r"INSERT INTO\s+(\w+)\s+\((.*?)\)\s+VALUES\s+\((.*?)\)"
    update_pattern = r"UPDATE\s+(\w+)\s+SET\s+(.*?)\s+(WHERE\s+.*)?"
    delete_pattern = r"DELETE FROM\s+(\w+)\s+(WHERE\s+.*)?"

    # Match patterns
    select_match = re.search(select_pattern, sql_query, re.IGNORECASE)
    insert_match = re.search(insert_pattern, sql_query, re.IGNORECASE)
    update_match = re.search(update_pattern, sql_query, re.IGNORECASE)
    delete_match = re.search(delete_pattern, sql_query, re.IGNORECASE)

    result = {}

    if select_match:
        result['type'] = 'SELECT'
        result['table'] = select_match.group(2)
        result['columns'] = select_match.group(1)

    elif insert_match:
        result['type'] = 'INSERT'
        result['table'] = insert_match.group(1)
        result['columns'] = insert_match.group(2)
        result['values'] = insert_match.group(3)

    elif update_match:
        result['type'] = 'UPDATE'
        result['table'] = update_match.group(1)
        result['set_clause'] = update_match.group(2)
        result['where_clause'] = update_match.group(3) if update_match.group(3) else None

    elif delete_match:
        result['type'] = 'DELETE'
        result['table'] = delete_match.group(1)
        result['where_clause'] = delete_match.group(2) if delete_match.group(2) else None

    else:
        result['type'] = 'UNKNOWN'

    return result


# Example usage
sql_query = "SELECT name, age FROM users WHERE age > 30"
parsed_query = parse_sql_query(sql_query)

print("Parsed SQL Query:")
print(parsed_query)

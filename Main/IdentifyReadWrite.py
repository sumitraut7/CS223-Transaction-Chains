import sqlparse

def identify_operations(sql_query):
    """Identifies read and write operations in an SQL query."""

    parsed = sqlparse.parse(sql_query)
    operations = []

    for statement in parsed:
        if statement.get_type() == 'UNKNOWN':
            continue  # Skip unsupported statements

        operation = None
        if statement.get_type() in ('SELECT', 'SHOW'):
            operation = 'READ'
        elif statement.get_type() in ('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP'):
            operation = 'WRITE'

        if operation:
            operations.append((operation, statement.value))

    return operations

# Example usage:
query = "SELECT * FROM users; UPDATE users SET age = 20 WHERE id = 1;"
operations = identify_operations(query)

for op, stmt in operations:
    print(f"{op}: {stmt}")
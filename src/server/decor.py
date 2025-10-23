import db


def has_records(func):
    def wrapper(*args, **kwargs):
        result = None
        x, res = db.get_all_records()
        if not res:
            print("No action")
        else:
            print(f"Before execution {res}")
            result = func(*args, **kwargs)
            print("After execution")
        return result
    return wrapper


@has_records
def add(a, b):
    return a + b
print(add(5, 3))

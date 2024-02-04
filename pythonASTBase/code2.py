def risky_operation():
    pass


def complex_function(param1: int, param2: int = 10) -> int:
    '''Example function with types and default value'''
    if param1 > param2:
        result = param1 - param2
    else:
        result = param2 - param1
    for i in range(5):
        print(i)
    while param1 < param2:
        print(param1)
        param1 += 1
    try:
        risky_operation()
    except Exception as e:
        print(e)
    return result

async def async_function():
    pass

class MyClass:
    '''Example class'''
    def method(self):
        pass
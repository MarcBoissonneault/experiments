from pathlib import Path

dats_file = Path(__file__).parent / "data.txt"

class MyContextManager:
    def __init__(self, underlying):
        self._underlying = underlying
    
    def __enter__(self):
        print(">>>>>>  Enter Context Manager")
        return self._underlying.__enter__()
    
    def __exit__(self, exc_type, exc, exc_tb):
        self._underlying.__exit__(exc_type, exc, exc_tb)
        print("<<<<<<  Exit Context Manager")        


print(f"{'':–<70}")
print(f"|{'YIELD':^68}|")
print(f"|{'Inside context manager':^68}|")
print(f"{'':–<70}")

def yield_something():
    with MyContextManager(open(dats_file)) as wrapped_file:
        print('2- Inside "yield_something" ====> Before Yield')
        yield wrapped_file.read()
        print('3- Inside "yield_something" ====> After Yield')


print("1- Before call to yield_something")
result = yield_something()
print("4- After call to yield_something")

for index, v in enumerate(result):
    print(f"5- ===> Ouside of the method yeild_something: index: {index}")
    print(f"6- {v}")


print("7- ===> Ouside of the method yeild_something: After end of enumeration (yield object released)")

print()
print()
print()
print(f"{'':–<70}")
print(f"|{'RETURN':^68}|")
print(f"|{'Inside context manager':^68}|")
print(f"{'':–<70}")

def return_something():
    with MyContextManager(open(dats_file)) as wrapped_file:
        print('2- Inside "return_something" ====> Before Return')
        return wrapped_file.read()
        print('3- Inside "return_something" ====> After Return')


print("1- Before call to return_something")
result = return_something()
print("4- After call to return_something")

print(f"5- {result}")

print()
print()
print()
print()

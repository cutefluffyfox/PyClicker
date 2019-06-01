from copy import deepcopy
data = []
last_bucket = [[] for _ in range(10)]
for _ in range(int(input())):
    numb = input()
    data.append(numb)
    last_bucket[int(numb[-1])].append(numb)
phase = 1
print("Initial array:")
print(*data, sep=", ")
for i in range(len(data[-1]) - 2, -1, -1):
    new_bucket = [[] for _ in range(10)]
    print("**********")
    print("Phase", phase)
    for ind in range(10):
        if last_bucket[ind]:
            print(f"Bucket {ind}: {', '.join(last_bucket[ind])}")
        else:
            print(f"Bucket {ind}: empty")
        for numb in last_bucket[ind]:
            new_bucket[int(numb[i])].append(numb)
    last_bucket = deepcopy(new_bucket)
    phase += 1
else:
    print("**********")
    print("Phase", phase)
    for ind in range(10):
        if last_bucket[ind]:
            print(f"Bucket {ind}: {', '.join(last_bucket[ind])}")
        else:
            print(f"Bucket {ind}: empty")
print("**********")
print("Sorted array:")
print(*list(sorted(data, key=lambda a: int(a))), sep=", ")

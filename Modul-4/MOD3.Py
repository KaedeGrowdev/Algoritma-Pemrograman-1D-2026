n = int(input("Masukkan n: "))

for i in range(1, n + 1):

    for k in range(1, i + 1):
        if k < 10:
            print(k, end='  ')
        else:
            print(k, end=' ')

    for j in range((n - i) * 3):
        print(' ', end=' ')

    for k in range(i, 0, -1):
        if k < 10:
            print(k, end='  ')
        else:
            print(k, end=' ')
    print()
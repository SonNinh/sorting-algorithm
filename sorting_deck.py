#!/usr/bin/python3

import argparse

'''
# recursive bubble
def bubble(decks, i, end):
    if end > 1:
        if decks[i] > decks[i+1]:
            decks[i], decks[i+1] = decks[i+1], decks[i]
            print(*decks)

        if i+1 == end-1:
                bubble(decks, 0, end-1)
        else:
            bubble(decks, i+1, end)

    return decks
'''
# loop bubble
def bubble(decks):
    n = 0
    notDone = True
    while notDone:
        notDone = False
        for i in range(0, len(decks)-1-n):
            if decks[i] > decks[i+1]:
                decks[i], decks[i+1] = decks[i+1], decks[i]
                notDone = True
                print(*decks)
        n += 1


def insertion(decks, i=0):
    done = False
    if i == len(decks)-1:
        return decks
    else:
        while decks[i] <= decks[i+1]:
            if i < len(decks)-2:
                i += 1
            else:
                done = True
                break
        if done is False:
            if decks[i+1] < decks[0]:
                decks.insert(0, decks[i+1])
                decks.pop(i+2)
                print(*decks)
                insertion(decks, i+1)
            else:
                j = 0
                while decks[i+1] < decks[j] or decks[i+1] > decks[j+1]:
                    j += 1
                decks.insert(j+1, decks[i+1])
                decks.pop(i+2)
                print(*decks)
                insertion(decks, i+1)


def merge(decks):
    if len(decks) > 2:
        p = len(decks)//2
        ls = list()
        ls.append(merge(decks[:p]))
        ls.append(merge(decks[p:]))
        left = 0
        right = 0
        res = list()
        while left < len(ls[0]) and right < len(ls[1]):
            if ls[0][left] <= ls[1][right]:
                res.append(ls[0][left])
                left += 1
            else:
                res.append(ls[1][right])
                right += 1
        if right == len(ls[1]):
            for node in range(left, len(ls[0])):
                res.append(ls[0][node])
        else:
            for node in range(right, len(ls[1])):
                res.append(ls[1][node])

        print(*res)

        return res
    else:
        if len(decks) == 2:
            if decks[0] > decks[1]:
                buffer = decks[0]
                decks[0] = decks[1]
                decks[1] = buffer
            print(*decks)
        return decks


def quick(decks, left, right):
    if left < right:
        i = (left-1)
        pivot = decks[right]

        for j in range(left, right):
            if decks[j] <= pivot:
                i = i+1
                decks[i], decks[j] = decks[j], decks[i]
        i += 1
        decks[i], decks[right] = decks[right], decks[i]
        print("P:", pivot)
        print(*decks)
        quick(decks, left, i-1)
        quick(decks, i+1, right)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('decks', type=int, nargs='+',
                        help="")
    parser.add_argument("--algo", type=str, default="bubble",
                        help="checksum mode")
    args = parser.parse_args()

    if len(args.decks) > 1:
        if args.algo == "bubble":
            res = bubble(args.decks)
        elif args.algo == "insert":
            res = insertion(args.decks)
        elif args.algo == "merge":
            res = merge(args.decks)
        elif args.algo == "quick":
            res = quick(args.decks, 0, len(args.decks)-1)
    # else:
        # print(args.decks)


if __name__ == "__main__":
    main()

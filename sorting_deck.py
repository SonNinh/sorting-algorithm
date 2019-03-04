#!/usr/bin/python3

import argparse


def bubble(decks, i=0, change=0):
    if decks[i] > decks[i+1]:
        buffer = decks[i]
        decks[i] = decks[i+1]
        decks[i+1] = buffer
        change += 1
        for each in decks[:-1]:
            print(str(each) + " ", end="")
        print(decks[-1])

    if i+1 == len(decks)-1:
        if change != 0:
            bubble(decks, 0, 0)
    else:
        bubble(decks, i+1, change)

    return decks


def insertion(decks, i=0):
    if i == len(decks)-1:
        return decks
    else:
        while decks[i] <= decks[i+1]:
            if i < len(decks)-2:
                i += 1
            else:
                break

        if decks[i+1] < decks[0]:
            decks.insert(0, decks[i+1])
            decks.pop(i+2)
            for each in decks[:-1]:
                print(str(each) + " ", end="")
            print(decks[-1])
            insertion(decks, i+1)
        else:
            j = 0
            while decks[i+1] < decks[j] or decks[i+1] > decks[j+1]:
                j += 1
            decks.insert(j+1, decks[i+1])
            decks.pop(i+2)
            for each in decks[:-1]:
                print(str(each) + " ", end="")
            print(decks[-1])
            insertion(decks, i+1)


def merge(decks):
    if len(decks) > 2:
        p = len(decks)//2
        ls = list()
        ls.append(merge(decks[:p]))
        ls.append(merge(decks[p:]))
        print(ls)
        # ls = bubble(ls, show=False)
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

        for each in res[:-1]:
            print(str(each) + ' ', end="")
        print(res[-1])

        return res
    else:
        if len(decks) == 2:
            if decks[0] > decks[1]:
                buffer = decks[0]
                decks[0] = decks[1]
                decks[1] = buffer
            for each in decks[:-1]:
                print(str(each) + " ", end="")
            print(decks[-1])
        return decks


# def quick(decks):

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
    else:
        print(args.decks)


if __name__ == "__main__":
    main()

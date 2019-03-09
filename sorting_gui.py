#!/usr/bin/python3

import argparse
import math
import os

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


def bubble(decks, log):
    n = 0
    notDone = True
    while notDone:
        notDone = False
        for i in range(0, len(decks)-1-n):
            if decks[i] > decks[i+1]:
                os.write(log, '{} {}\n'.format(i, i+1).encode())
                decks[i], decks[i+1] = decks[i+1], decks[i]
                notDone = True
                print(*decks)
        n += 1


'''
# insertion recursive
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
'''


def insertion(decks, log):
    for i in range(0, len(decks)-1):
        if decks[i] > decks[i+1]:
            for j in range(i, -1, -1):
                if j > 0:
                    if decks[i+1] <= decks[j] and decks[i+1] >= decks[j-1]:
                        os.write(log, '{} {} \n'.format(j, i+1).encode())
                        decks.insert(j, decks[i+1])
                        decks.pop(i+2)
                        break
                elif j == 0:
                    os.write(log, '{} {} \n'.format(0, i+1).encode())
                    decks.insert(0, decks[i+1])
                    decks.pop(i+2)
            print(*decks)


'''
0        4
4 6 7 9  1 3 6 8
  1        5
1 4 6 7 9  3 6 8
    2        6
1 3 4 6 7 9  6 8
      3      6
1 3 4 6 7 9  6 8
        4    6
1 3 4 6 7 9  6 8
          5    7
1 3 4 6 6 7 9  8
            5  7
1 3 4 6 6 7 9  8
              6
1 3 4 6 6 7 8 9

        4  5
1 3 4 6 7  6 8
           5 6
1 3 4 6 6  7 8
'''
'''
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
                decks[0], decks[1] = decks[1], decks[0]
            print(*decks)
        return decks
'''


def merge(decks, left, right, log):

    if right - left > 1:
        center = math.ceil((right+left)/2)
        merge(decks, left, center-1, log)
        merge(decks, center, right, log)
        i = left
        j = center
        os.write(log, '{} {} \n'.format(left, right).encode())
        while i < j and j <= right:
            if decks[i] > decks[j]:
                os.write(log, '{} {} '.format(left, right).encode())
                os.write(log, '{} {} \n'.format(i, j).encode())
                decks.insert(i, decks[j])
                decks.pop(j+1)
                i += 1
                j += 1
            else:
                i += 1
        print(*decks[left:right+1])
    else:
        os.write(log, '{} {} \n'.format(left, right).encode())
        if right - left == 1:
            os.write(log, '{} {} '.format(left, right).encode())
            if decks[left] > decks[right]:
                os.write(log, '{} {} '.format(left, right).encode())
                decks[left], decks[right] = decks[right], decks[left]
            os.write(log, '\n'.encode())
            print(*decks[left:right+1])
        # os.write(log, '\n'.encode())


def quick(decks, left, right, log):
    if left < right:

        i = (left-1)
        pivot = decks[right]

        for j in range(left, right):
            if decks[j] < pivot:
                i += 1
                os.write(log, '{} {} '.format(left, right).encode())
                os.write(log, '{} {} \n'.format(i, j).encode())
                decks[i], decks[j] = decks[j], decks[i]
        i += 1
        os.write(log, '{} {} '.format(left, right).encode())
        os.write(log, '{} {} \n'.format(i, right).encode())

        decks[i], decks[right] = decks[right], decks[i]
        print("P:", pivot)
        print(*decks)
        quick(decks, left, i-1, log)
        quick(decks, i+1, right, log)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('decks', type=int, nargs='+',
                        help="")
    parser.add_argument("--algo", type=str, default="bubble",
                        help="algorithm")
    parser.add_argument("--gui", action="store_true",
                        help="GUI mode")
    args = parser.parse_args()

    if len(args.decks) > 1:
        try:
            os.unlink("log")
        except Exception:
            pass
        log = os.open("log", os.O_RDWR | os.O_CREAT)
        os.write(log, ' '.join(str(e) for e in args.decks).encode())
        os.write(log, '\n'.encode())
        if args.algo == "bubble":
            os.write(log, "bubble\n".encode())
            res = bubble(args.decks, log)
        elif args.algo == "insert":
            os.write(log, "insert\n".encode())
            res = insertion(args.decks, log)
        elif args.algo == "merge":
            os.write(log, "merge\n".encode())
            res = merge(args.decks, 0, len(args.decks)-1, log)
        elif args.algo == "quick":
            os.write(log, "quick\n".encode())
            res = quick(args.decks, 0, len(args.decks)-1, log)

        if args.gui is True:
            import sorting_gui
            sorting_gui.pyglet.app.run()
        os.close(log)
    # else:
        # print(args.decks)


if __name__ == "__main__":
    main()

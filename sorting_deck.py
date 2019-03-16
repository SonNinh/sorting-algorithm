#!/usr/bin/python3

import argparse
import math
import os


def bubble(decks, log):
    n = 0
    notDone = True
    while notDone:
        notDone = False
        for i in range(0, len(decks)-1-n):
            os.write(log, '{} {} {}\n'.format(i, i+1, n).encode())
            if decks[i] > decks[i+1]:
                os.write(log, '{} {} {} s\n'.format(i, i+1, n).encode())
                decks[i], decks[i+1] = decks[i+1], decks[i]
                notDone = True
                print(*decks)
        n += 1


def insertion(decks, log):
    def checkBackInsertion(decks, log, i):
        '''
        Find the relevant posision to insert wrong-pos interger
        '''
        for j in range(i, -1, -1):
            os.write(log, '{} {}\n'.format(j, i+1).encode())
            if j > 0:
                if decks[i+1] >= decks[j-1]:
                    os.write(log, '{} {} s\n'.format(j, i+1).encode())
                    decks.insert(j, decks[i+1])
                    decks.pop(i+2)
                    break
            else:
                os.write(log, '{} {} s\n'.format(0, i+1).encode())
                decks.insert(0, decks[i+1])
                decks.pop(i+2)
        print(*decks)

    for i in range(0, len(decks)-1):
        '''
        Find the wrong-pos point
        '''
        if decks[i] > decks[i+1]:
            checkBackInsertion(decks, log, i)
        else:
            os.write(log, '{} {}\n'.format(i, i+1).encode())


def mergeOutPlace(decks):
    if len(decks) > 2:
        p = len(decks)//2
        ls = list()
        ls.append(mergeOutPlace(decks[:p]))
        ls.append(mergeOutPlace(decks[p:]))
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


def merge(decks, left, right, log):
    '''
    In-place merge sort
    '''
    def arrange2SortedList():
        '''
        Create new sorted list from 2 sorted lists
        '''
        i = left
        j = center
        os.write(log, '{} {} {}\n'.format(left, right, center).encode())
        while i < j and j <= right:
            os.write(log, '{} {} '.format(left, right).encode())
            if decks[i] > decks[j]:
                os.write(log, '{} {} s\n'.format(i, j).encode())
                decks.insert(i, decks[j])
                decks.pop(j+1)
                i += 1
                j += 1
            else:
                os.write(log, '{} {} s\n'.format(i, i).encode())
                i += 1
        print(*decks[left:right+1])

    center = math.ceil((right+left)/2)
    if right - left > 1:
        merge(decks, left, center-1, log)
        merge(decks, center, right, log)
        arrange2SortedList()
    elif right - left == 1:
        arrange2SortedList()
    else:
        os.write(log, '{} {}\n'.format(left, right).encode())


def quick(decks, left, right, log):
    def partition(i, pivot):
        for j in range(left, right):
            os.write(log, '{} {} '.format(left, right).encode())
            os.write(log, '{} {}\n'.format(i, j).encode())
            if decks[j] < pivot:
                i += 1
                os.write(log, '{} {} '.format(left, right).encode())
                os.write(log, '{} {} s\n'.format(i, j).encode())
                decks[i], decks[j] = decks[j], decks[i]
        i += 1
        os.write(log, '{} {} '.format(left, right).encode())
        os.write(log, '{} {} s\n'.format(i, right).encode())
        return i

    if left < right:
        i = (left-1)
        pivot = decks[right]
        i = partition(i, pivot)
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
        os.write(log, args.algo.encode())
        os.write(log, '\n'.encode())
        if args.algo == "bubble":
            res = bubble(args.decks, log)
        elif args.algo == "insert":
            res = insertion(args.decks, log)
        elif args.algo == "merge":
            res = merge(args.decks, 0, len(args.decks)-1, log)
        elif args.algo == "quick":
            res = quick(args.decks, 0, len(args.decks)-1, log)

        os.close(log)
        if args.gui is True:
            import sorting_gui
            sorting_gui.main()


if __name__ == "__main__":
    main()

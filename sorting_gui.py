#!/usr/bin/python3

import pyglet
from pyglet.window import key
from pyglet.window import mouse
import os
import math

window = pyglet.window.Window(1300, 500)
window.set_mouse_visible(True)


@window.event
def on_draw():
    window.clear()
    algorithm.draw()
    for label in lsOfLabels:
        label[0].draw()


def setTargetPosAll(lsOfLabels, forward):
    '''
    Set target position and new color of all labels
    @param:
        forward: set control flow direction
                 True: forward direction
                 False: backward direction
    '''
    if algorithm.text in ['bubble', 'insert']:
        setTargetPosBubbleAndInsert(lsOfLabels, forward)
    elif algorithm.text == 'merge':
        setTargetPosMerge(lsOfLabels, forward)
    elif algorithm.text == 'quick':
        setTargetPosQuick(lsOfLabels, forward)


def setTargetPosBubbleAndInsert(lsOfLabels, forward):
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    c = 0
    lenOfSequence = len(lsOfLabels)
    if algorithm.text == 'bubble':
        c = int(lsOfSteps[step][2])

    for i, _ in enumerate(lsOfLabels):
        if i == a or i == b:
            lsOfLabels[i][0].color = (100, 200, 0, 255)
        elif i >= lenOfSequence-c:
            lsOfLabels[i][0].color = (0, 100, 255, 255)
        else:
            lsOfLabels[i][0].color = (255, 255, 255, 255)
    if lsOfSteps[step][-1] == 's':
        swap(lsOfLabels, a, b, forward)


def setTargetPosMerge(lsOfLabels, forward):
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    if len(lsOfSteps[step]) == 3:
        center = int(lsOfSteps[step][2])
        for i, label in enumerate(lsOfLabels):
            if i in range(a, center):
                label[0].color = (255, 100, 0, 255)
            elif i in range(center, b+1):
                label[0].color = (0, 100, 255, 255)
            else:
                label[0].color = (255, 255, 255, 50)
    elif len(lsOfSteps[step]) == 5:
        c = int(lsOfSteps[step][2])
        d = int(lsOfSteps[step][3])
        swap(lsOfLabels, c, d, forward)
    else:
        for i, label in enumerate(lsOfLabels):
            if i in range(a, b+1):
                label[0].color = (255, 255, 255, 255)
            else:
                label[0].color = (255, 255, 255, 50)


def setTargetPosQuick(lsOfLabels, forward):
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    c = int(lsOfSteps[step][2])
    d = int(lsOfSteps[step][3])
    for i, label in enumerate(lsOfLabels):
        if i in range(a, c+1):
            label[0].color = (255, 100, 0, 255)
        elif i == b:
            label[0].color = (100, 0, 255, 255)
        elif i == d:
            label[0].color = (0, 255, 0, 255)
        elif i in range(c+1, b):
            label[0].color = (255, 255, 255, 255)
        else:
            label[0].color = (255, 255, 255, 50)
    if lsOfSteps[step][-1] == 's':
        lsOfLabels[c][0].color = (255, 255, 255, 255)
        if forward:
            (lsOfLabels[c][1],
             lsOfLabels[d][1]) = (lsOfLabels[d][1],
                                  lsOfLabels[c][1])
        else:
            (lsOfLabels[c][0].text,
             lsOfLabels[d][0].text) = (lsOfLabels[d][0].text,
                                       lsOfLabels[c][0].text)


def swap(lsOfLabels, idx1, idx2, forward):
    '''
    Swap all labels in a bounded group
    @param:
        idx1: absolute left limit
        idx2: absolute right limit
        forward: set control flow direction
                 True: forward direction
                 False: backward direction
    '''
    if forward:
        buffer = lsOfLabels[idx1][1]
        for i in range(idx1, idx2):
            lsOfLabels[i][1] = lsOfLabels[i+1][1]
        lsOfLabels[idx2][1] = buffer
    else:
        buffer = lsOfLabels[idx1][0].text
        for i in range(idx1, idx2):
            lsOfLabels[i][0].text = lsOfLabels[i+1][0].text
        lsOfLabels[idx2][0].text = buffer


def updateNewColorAndOrdAfterExchange(lsOfLabels):
    '''
    Update new order and color of labels in lsOfLabels
    '''
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    if algorithm.text == 'bubble':
        lsOfLabels[a], lsOfLabels[b] = lsOfLabels[b], lsOfLabels[a]
    elif algorithm.text == 'insert':
        lsOfLabels.insert(a, lsOfLabels[b])
        lsOfLabels.pop(b+1)
    elif algorithm.text == 'merge':
        c = int(lsOfSteps[step][2])
        d = int(lsOfSteps[step][3])
        lsOfLabels.insert(c, lsOfLabels[d])
        lsOfLabels.pop(d+1)
        lsOfLabels[c][0].color = (255, 255, 255, 255)
    elif algorithm.text == 'quick':
        c = int(lsOfSteps[step][2])
        d = int(lsOfSteps[step][3])
        lsOfLabels[c], lsOfLabels[d] = lsOfLabels[d], lsOfLabels[c]
        lsOfLabels[d][0].color = (255, 255, 255, 255)
        lsOfLabels[c][0].color = (255, 100, 0, 255)

    for label in lsOfLabels:
        label[0].x = label[1]
        label[2] = label[1]
        label[0].y = window.height//2


@window.event
def on_mouse_press(x, y, button, modifiers):
    global step, targetPosOfLabels, onProcess, lsOfLabels

    if button is mouse.LEFT:
        if onProcess is False:
            if step < len(lsOfSteps)-1:
                step += 1
                if lsOfSteps[step][-1] == 's':
                    onProcess = True
                setTargetPosAll(lsOfLabels, True)
            else:
                for label in lsOfLabels:
                    label[0].color = (0, 255, 255, 255)
                return
        else:
            updateNewColorAndOrdAfterExchange(lsOfLabels)
            onProcess = False
    elif button is mouse.RIGHT:
        if onProcess is False and step >= 0:
            setTargetPosAll(lsOfLabels, False)
            step -= 1


def yAxisCalculation(label):
    '''
    Caculate y coordination of label, based on inital x and target x
    '''
    return int(math.sin((label[0].x-label[2])/(label[1]-label[2])*math.pi)*80)


def moveToTargetPos(lsOfLabels):
    '''
    Change x coordination by n pixels until touching the target

    @return:
        done: binary flag
            True, if all labels touch the target position
            False, if not
    '''
    n = 4
    done = True
    for i, label in enumerate(lsOfLabels):
        if label[0].x > label[1]+n-1:
            label[0].x -= n
            label[0].y = yAxisCalculation(label) + window.height//2
            done = False
        elif label[0].x+n-1 < label[1]:
            label[0].x += n
            if algorithm.text == 'bubble' or algorithm.text == 'quick':
                label[0].y = window.height//2 - yAxisCalculation(label)
            done = False
    return done


def animation(_):
    '''
    Make sin-movement of labels
    '''
    global lsOfLabels
    global onProcess

    if onProcess is True:
        done = moveToTargetPos(lsOfLabels)
        if done is True:
            updateNewColorAndOrdAfterExchange(lsOfLabels)
            onProcess = False


def readAllData():
    '''
    Read the input sequence, name of sorting algorithm and all animation steps
    from log file (string format)
    First line: input sequence
    Second line: name of sorting algorithm
    Third line -> last line: all animation steps

    @return:
        lsOfLabels: list of all labels. Each label contains an pyglet object
                    label, target x and inital x coordination
        lsOfSteps: list of all animation steps
        algorithm: pyglet object label which has attribute text depending on
                   the name of used sorting algoritm
    '''
    lsOfLabels = list()
    lsOfSteps = list()
    lsOfLines = list()
    with open("log", "r+") as log:
        lsOfLines = log.readlines()
        lsOfIntergers = lsOfLines[0][:-1].split(' ')
        algo = lsOfLines[1][:-1]
        lenOfSequence = len(lsOfIntergers)
        for line in lsOfLines[2:]:
            lsOfSteps.append(line[:-1].split(' '))

        algorithm = pyglet.text.Label(algo, font_size=40,
                                      x=window.width//2,
                                      y=window.height//4*3,
                                      anchor_x='center', anchor_y='center')

        for i, interger in enumerate(lsOfIntergers):
            lsOfLabels.append([pyglet.text.Label(interger, font_size=20,
                              x=window.width//(lenOfSequence+1)*(i+1),
                              y=window.height//2,
                              anchor_x='center', anchor_y='center'),
                              window.width//(lenOfSequence+1)*(i+1),
                              window.width//(lenOfSequence+1)*(i+1)])

        return lsOfLabels, lsOfSteps, algorithm


def main():
    global step, onProcess, lsOfLabels, lsOfSteps, algorithm
    step = -1
    onProcess = False
    lsOfLabels, lsOfSteps, algorithm = readAllData()

    pyglet.clock.schedule_interval(animation, 1/60)
    pyglet.app.run()

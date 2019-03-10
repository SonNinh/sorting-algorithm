#!/usr/bin/python3

import pyglet
from pyglet.window import key
from pyglet.window import mouse
import os
import math

window = pyglet.window.Window(1200, 500)

window.set_mouse_visible(True)

lsOfLabels = list()
targetPosOfLabels = list()
step = -1
lsOfLines = list()
lsOfSteps = list()
onProcess = False
with open("log", "r+") as log:
    lsOfLines = log.readlines()
    lsOfIntergers = lsOfLines[0][:-1].split(' ')
    algo = lsOfLines[1][:-1]
    lenOfSequence = len(lsOfIntergers)
    for line in lsOfLines[2:]:
        lsOfSteps.append(line[:-1].split(' '))

    lsOfLines.clear()
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

    indexI = pyglet.text.Label('i', font_size=20,
                               y=window.height//2-50,
                               anchor_x='center', anchor_y='center')

    indexJ = pyglet.text.Label('j', font_size=20,
                               y=window.height//2-30,
                               anchor_x='center', anchor_y='center')


@window.event
def on_draw():
    window.clear()
    algorithm.draw()

    for label in lsOfLabels:
        label[0].draw()


def setTargetPosBubble(lsOfLabels):
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    c = int(lsOfSteps[step][2])
    for i, _ in enumerate(lsOfLabels):
        if i == a or i == b:
            lsOfLabels[i][0].color = (100, 200, 0, 255)
        elif i in range(lenOfSequence-1, lenOfSequence-1-c, -1):
            lsOfLabels[i][0].color = (0, 100, 255, 255)
        else:
            lsOfLabels[i][0].color = (255, 255, 255, 255)
    if lsOfSteps[step][3] == 's':
        lsOfLabels[a][1], lsOfLabels[b][1] = lsOfLabels[b][1], lsOfLabels[a][1]


def setTargetPosInsert(lsOfLabels):
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    for i, _ in enumerate(lsOfLabels):
        if i == a:
            lsOfLabels[i][0].color = (100, 100, 0, 255)
        elif i == b:
            lsOfLabels[i][0].color = (0, 100, 255, 255)
        else:
            lsOfLabels[i][0].color = (255, 255, 255, 255)
    if lsOfSteps[step][2] == 's':
        buffer = lsOfLabels[a][1]
        for i in range(a, b):
            lsOfLabels[i][1] = lsOfLabels[i+1][1]
        lsOfLabels[b][1] = buffer


def setTargetPosMerge(lsOfLabels):
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    if len(lsOfSteps[step]) == 4:
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
        buffer = lsOfLabels[c][1]
        for i in range(c, d):
            lsOfLabels[i][1] = lsOfLabels[i+1][1]
        lsOfLabels[d][1] = buffer
    else:
        for i, label in enumerate(lsOfLabels):
            if i in range(a, b+1):
                label[0].color = (255, 255, 255, 255)
            else:
                label[0].color = (255, 255, 255, 50)


def setTargetPosQuick(lsOfLabels):
    a = int(lsOfSteps[step][0])
    b = int(lsOfSteps[step][1])
    c = int(lsOfSteps[step][2])
    d = int(lsOfSteps[step][3])
    for i, label in enumerate(lsOfLabels):
        if i in range(a, c):
            label[0].color = (255, 100, 0, 255)
        elif i in range(c, b):
            label[0].color = (255, 255, 255, 255)
        elif i == b:
            label[0].color = (100, 0, 255, 255)
        else:
            label[0].color = (255, 255, 255, 50)

    lsOfLabels[c][1], lsOfLabels[d][1] = lsOfLabels[d][1], lsOfLabels[c][1]


@window.event
def on_mouse_press(x, y, button, modifiers):
    global step, targetPosOfLabels, onProcess, lsOfLabels, allSprites

    if button is mouse.LEFT:
        if onProcess is False:
            if step < len(lsOfSteps)-1:
                step += 1
                onProcess = True
            else:
                for label in lsOfLabels:
                    label[0].color = (0, 255, 255, 255)
                return
            a = int(lsOfSteps[step][0])
            b = int(lsOfSteps[step][1])
            if algo == 'bubble':
                setTargetPosBubble(lsOfLabels)
            elif algo == 'insert':
                setTargetPosInsert(lsOfLabels)
            elif algo == 'merge':
                setTargetPosMerge(lsOfLabels)
            elif algo == 'quick':
                setTargetPosQuick(lsOfLabels)
        else:
            for label in lsOfLabels:
                label[0].x = label[1]
                label[2] = label[1]
                label[0].y = window.height//2
            a = int(lsOfSteps[step][0])
            b = int(lsOfSteps[step][1])
            if algo == 'bubble':
                if lsOfSteps[step][3] == 's':
                    lsOfLabels[a], lsOfLabels[b] = lsOfLabels[b], lsOfLabels[a]
            elif algo == 'insert':
                if lsOfSteps[step][2] == 's':
                    lsOfLabels.insert(a, lsOfLabels[b])
                    lsOfLabels.pop(b+1)
            elif algo == 'merge':
                if len(lsOfSteps[step]) == 5:
                    c = int(lsOfSteps[step][2])
                    d = int(lsOfSteps[step][3])
                    lsOfLabels.insert(c, lsOfLabels[d])
                    lsOfLabels.pop(d+1)
                    lsOfLabels[c][0].color = (255, 255, 255, 255)
            elif algo == 'quick':
                if len(lsOfSteps[step]) > 3:
                    c = int(lsOfSteps[step][2])
                    d = int(lsOfSteps[step][3])
                    lsOfLabels[c], lsOfLabels[d] = lsOfLabels[d], lsOfLabels[c]
            onProcess = False


def yCalculation(label):
    return int(math.sin((label[0].x-label[2])/(label[1]-label[2])*math.pi)*80)


def animation(_):
    global lsOfLabels
    global onProcess
    done = True

    if onProcess is True:
        a = int(lsOfSteps[step][0])
        b = int(lsOfSteps[step][1])
        for i, label in enumerate(lsOfLabels):
            if label[0].x > label[1]+3:
                label[0].x -= 4
                label[0].y =  yCalculation(label)+ window.height//2
                done = False
            elif label[0].x+3 < label[1]:
                label[0].x += 4
                if algo == 'bubble' or algo == 'quick':
                    label[0].y = window.height//2 - yCalculation(label)
                done = False
            else:
                label[0].x = label[1]
                label[0].y = window.height//2

        if done is True:
            if algo == 'bubble':
                if lsOfSteps[step][3] == 's':
                    lsOfLabels[a], lsOfLabels[b] = lsOfLabels[b], lsOfLabels[a]
            elif algo == 'insert':
                if lsOfSteps[step][2] == 's':
                    lsOfLabels.insert(a, lsOfLabels[b])
                    lsOfLabels.pop(b+1)
            elif algo == 'merge':
                if len(lsOfSteps[step]) == 5:
                    c = int(lsOfSteps[step][2])
                    d = int(lsOfSteps[step][3])
                    lsOfLabels.insert(c, lsOfLabels[d])
                    lsOfLabels.pop(d+1)
                    lsOfLabels[c][0].color = (255, 255, 255, 255)
            elif algo == 'quick':
                if len(lsOfSteps[step]) > 3:
                    c = int(lsOfSteps[step][2])
                    d = int(lsOfSteps[step][3])
                    lsOfLabels[c], lsOfLabels[d] = lsOfLabels[d], lsOfLabels[c]
                    for i in range(a, c+1):
                        lsOfLabels[i][0].color = (255, 100, 0, 255)

            for label in lsOfLabels:
                label[2] = label[1]
            onProcess = False


pyglet.clock.schedule_interval(animation, 1/60)

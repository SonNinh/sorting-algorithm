#!/usr/bin/python3

import pyglet
from pyglet.window import key
from pyglet.window import mouse
import os
import math

window = pyglet.window.Window(1200, 900)

window.set_mouse_visible(True)
batch = pyglet.graphics.Batch()

background = pyglet.image.load('images/background.jpg')

circle = pyglet.image.load('images/circle.png')
circle.anchor_x = circle.width//2
circle.anchor_y = circle.height//2
# inputCircle = pyglet.sprite.Sprite(img=circle, batch=batch)

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


@window.event
def on_draw():
    allSprites = list()
    window.clear()
    background.blit(0, 0)
    algorithm.draw()
    for label in lsOfLabels:
        label[0].draw()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global step, targetPosOfLabels, onProcess
    if button is mouse.LEFT:
        if onProcess is False:
            if step < len(lsOfSteps)-1:
                step += 1
                onProcess = True
            a = int(lsOfSteps[step][0])
            b = int(lsOfSteps[step][1])
            if algo == 'bubble':
                lsOfLabels[a][1], lsOfLabels[b][1] = lsOfLabels[b][1], lsOfLabels[a][1]
            elif algo == 'insert':
                buffer = lsOfLabels[a][1]
                for i in range(a, b):
                    lsOfLabels[i][1] = lsOfLabels[i+1][1]
                lsOfLabels[b][1] = buffer
            elif algo == 'merge':
                for i, label in enumerate(lsOfLabels):
                    if i in range(a, b+1):
                        label[0].color = (255, 255, 255, 255)
                    else:
                        label[0].color = (255, 255, 255, 50)
                if len(lsOfSteps[step]) > 3:
                    c = int(lsOfSteps[step][2])
                    d = int(lsOfSteps[step][3])
                    buffer = lsOfLabels[c][1]
                    for i in range(c, d):
                        lsOfLabels[i][1] = lsOfLabels[i+1][1]
                    lsOfLabels[d][1] = buffer
            print(step)
        else:
            for label in lsOfLabels:
                label[0].x = label[1]
                label[2] = label[1]
                label[0].y = window.height//2
            a = int(lsOfSteps[step][0])
            b = int(lsOfSteps[step][1])
            if algo == 'bubble':
                lsOfLabels[a], lsOfLabels[b] = lsOfLabels[b], lsOfLabels[a]
            elif algo == 'insert':
                lsOfLabels.insert(a, lsOfLabels[b])
                lsOfLabels.pop(b+1)
            elif algo == 'merge':
                if len(lsOfSteps[step]) > 3:
                    c = int(lsOfSteps[step][2])
                    d = int(lsOfSteps[step][3])
                    lsOfLabels.insert(c, lsOfLabels[d])
                    lsOfLabels.pop(d+1)
            onProcess = False


def swarp(_):
    global lsOfLabels
    global onProcess
    done = True

    if onProcess is True:
        a = int(lsOfSteps[step][0])
        b = int(lsOfSteps[step][1])
        for i, label in enumerate(lsOfLabels):
            if label[0].x > label[1]+2:
                label[0].x -= 3
                if algo == 'bubble':
                    label[0].y = int(math.sin((label[0].x-label[2])/(label[1]-label[2])*math.pi)*50) + window.height//2
                elif algo == 'insert' and i == b:
                    label[0].y = int(math.sin((label[0].x-label[2])/(label[1]-label[2])*math.pi)*260) + window.height//2
                elif algo == 'merge':
                    label[0].y = int(math.sin((label[0].x-label[2])/(label[1]-label[2])*math.pi)*260) + window.height//2

                done = False
            elif label[0].x+2 < label[1]:
                label[0].x += 3
                if algo == 'bubble':
                    label[0].y = int(math.sin((label[0].x-label[2])/(label[2]-label[1])*math.pi)*50) + window.height//2
                done = False
            else:
                label[0].x = label[1]
                label[0].y = window.height//2
        if done is True:
            if algo == 'bubble':
                lsOfLabels[a], lsOfLabels[b] = lsOfLabels[b], lsOfLabels[a]
            elif algo == 'insert':
                lsOfLabels.insert(a, lsOfLabels[b])
                lsOfLabels.pop(b+1)
            elif algo == 'merge':
                if len(lsOfSteps[step]) > 3:
                    c = int(lsOfSteps[step][2])
                    d = int(lsOfSteps[step][3])
                    lsOfLabels.insert(c, lsOfLabels[d])
                    lsOfLabels.pop(d+1)
            for label in lsOfLabels:
                label[2] = label[1]
            onProcess = False


pyglet.clock.schedule_interval(swarp, 0.01)

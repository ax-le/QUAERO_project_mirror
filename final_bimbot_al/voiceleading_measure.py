#! /usr/bin/python
# -*- coding: utf-8 -*-

import math


def score_note_leading(mvt):
    s = mvt
    if s >= 0:
        return s
    else:
        return -s

def basic_measure(voice_leading):
    s = 0
    for mvt in voice_leading:
        s += score_note_leading(mvt)
    return s

def euclidian_measure(voice_leading):
    s = 0
    for mvt in voice_leading:
        a = score_note_leading(mvt)
        s += a*a
    return math.sqrt(s)

def linf_measure(voice_leading):
    s = 0
    for mvt in voice_leading:
        a = score_note_leading(mvt)
        if a > s:
            s = a
    return s


    
    

#! /usr/bin/python
# -*- coding: utf-8 -*-

import math
import copy
import parser
import random
from itertools import combinations
from itertools import permutations
from itertools import product
import voiceleading_measure as vlms







Fifth = [(i-(i%2)*6)%12 for i in range(12)]
ReverseFifth = [(i+(i%2)*6)%12 for i in range(12)]
def voice_leading(chord1, chord2, fifth=False):
    """chord1 and chord2 are expected to be normalized (i.e. of the same size)"""
    vl = []
    # print "c1 : "+str(chord1)+"   c2 : "+str(chord2)
    for i in range(len(chord1)):
        vl.append(note_leading(chord1[i],chord2[i],fifth=fifth))
    return vl

def score_voiceleading(chord1, chord2, measure=vlms.basic_measure, fifth=False):
    vl = voice_leading(chord1,chord2,fifth=fifth)
    return measure(vl)

def score_voiceleading_sys(chords,measure=vlms.basic_measure, fifth=False):
    s = 0
    scale1_vl = voice_leading(chords[0],chords[4],fifth=fifth)
    s += score_voiceleading(chords[0],chords[4],measure,fifth=fifth)
    s += score_voiceleading(chords[0],chords[8],measure,fifth=fifth)
    s += score_voiceleading(apply_vl(chords[8],scale1_vl),chords[12],measure,fifth=fifth)
    for i in range(4):
        scale2_vl = voice_leading(chords[4*i],chords[4*i+1],fifth=fifth)
        s += score_voiceleading(chords[4*i],chords[4*i+1],measure,fifth=fifth)
        s += score_voiceleading(chords[4*i],chords[4*i+2],measure,fifth=fifth)
        s += score_voiceleading(apply_vl(chords[4*i+2],scale2_vl,fifth=fifth),chords[4*i+3],measure,fifth=fifth)
    return s

def score_voiceleading_sys_without(chords,measure=vlms.basic_measure, fifth=False):
    s = 0
    s += score_voiceleading(chords[0],chords[4],measure,fifth=fifth)
    s += score_voiceleading(chords[0],chords[8],measure,fifth=fifth)
    s += score_voiceleading(chords[0],chords[12],measure,fifth=fifth)
    for i in range(4):
        s += score_voiceleading(chords[4*i],chords[4*i+1],measure,fifth=fifth)
        s += score_voiceleading(chords[4*i],chords[4*i+2],measure,fifth=fifth)
        s += score_voiceleading(chords[4*i],chords[4*i+3],measure,fifth=fifth)
    return s


def score_voiceleading_seq(chords,measure=vlms.basic_measure, fifth=False):
    s = 0
    for i in range(len(chords)-1):
        s += score_voiceleading(chords[i],chords[i+1],measure,fifth=fifth)
    return s

def note_leading(note1, note2,fifth=False):
    """Calcul of the shortest movement from pitch class of note1 and
    pitchclass of note2. If fifth is true, the displacement is
    computed in term of displacement in the circle of fifth
    """
    mvt = (note2 - note1)%12
    if fifth:
        mvt = (Fifth[note2] - Fifth[note1])%12
    if mvt > 6:
        mvt = mvt-12
    return mvt


def complete_chord(chord, nb_notes):
    if nb_notes==0:
        return [chord]
    else:
        bases = copy.deepcopy(complete_chord(chord,nb_notes-1))
        final = []
        for basis in bases:
            for note in chord:
                new_chord = copy.deepcopy(basis)
                new_chord.append(note)
                final.append(new_chord)
        return final


def generate_possibilities(notes, nb_notes, first=False):
    """Generates all the chords of nb_notes notes containing all notes in notes.
    It repeat the root note len(notes) < nb_notes"""
    newnotes = list(copy.deepcopy(notes))
    if len(notes) > nb_notes :
        possible_chords = permutations(notes,nb_notes)
        return list(possible_chords)
    elif len(notes) < nb_notes :
        possible_chords = complete_chord(newnotes, nb_notes-len(notes))
        if first:
            return possible_chords
        else:
            final =[]
            for chord in possible_chords:
                final.extend(permutations(chord))
            return list(final)
    elif first :
        return [newnotes]
    else:
        possible_chords = permutations(newnotes)
        return list(possible_chords)

def generate_uniques_possibilities(notes, nb_notes, first=False):
    l = generate_possibilities(notes, nb_notes, first=first)
    new_l = []
    for el in l:
        if el in new_l:
            pass
        else:
            new_l.append(el)
    return new_l
    
    
def max_notes(chords):
    m = 0
    for chord in chords:
        m = max(m,len(chord))
    return m

def apply_vl(chord3,vl,fifth=False):
    newchord3 = []
    for i in range(len(chord3)):
        if fifth:
            newchord3.append(ReverseFifth[(Fifth[chord3[i]]+vl[i])%12])
        else :
            newchord3.append((chord3[i]+vl[i])%12)
    return newchord3


def seq_with_fictives_chords(chords,fifth=False):
    seq = copy.deepcopy(chords)
    n = len(chords)/4
    for i in range(n):
        vl = voice_leading(chords[n*i], chords[n*i+1],fifth=fifth)
        new_chord = apply_vl(chords[n*i+2],vl,fifth=fifth)
        seq.append(new_chord)
    if len(chords) == 16:
        vl = voice_leading(chords[0], chords[4],fifth=fifth)
        new_chord = apply_vl(chords[8],vl,fifth=fifth)
        seq.append(new_chord)
    return seq

def sysseq_with_fictives_chords(seq,choices,fifth=False):
    chords = copy.deepcopy(seq)
    l = copy.deepcopy(seq)
    ficts = {}
    for key,choice in choices.items():
        chds = [chords[i] for i in choice]
        ficts[i] = fictives_chords(chds,fifth=fifth)
    c = 0
    for key, chord in ficts.items():
        chords.insert(key+c,chord[0])
        c+=1
    return chords

def fictives_chords(seq,fifth=False):
    fictives = []
    n = len(seq)/4
    for i in range(n):
        vl = voice_leading(seq[n*i], seq[n*i+1],fifth=fifth)
        new_chord = apply_vl(seq[n*i+2],vl,fifth=fifth)
        fictives.append(new_chord)
    if len(seq) == 16:
        vl = voice_leading(seq[0], seq[4],fifth=fifth)
        new_chord = apply_vl(seq[8],vl,fifth=fifth)
        fictives.append(new_chord)
    return fictives






""" Find best VL"""

def best_vl_seq4(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    allchords = [generate_uniques_possibilities(chord, nb_notes) for chord in chords]
    minimal_vl = (0,0,0,0)
    score_minimal_vl = (score_voiceleading(allchords[0][0], allchords[1][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[1][0], allchords[2][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[2][0], allchords[3][0], measure,fifth=fifth))
    for i in range(len(allchords[0])):
        for j in range(len(allchords[1])):
            s1 = score_voiceleading(allchords[0][i], allchords[1][j], measure,fifth=fifth)
            for k in range(len(allchords[2])):
                s2 = score_voiceleading(allchords[1][j], allchords[2][k], measure,fifth=fifth)
                for l in range(len(allchords[3])):
                    s3 = score_voiceleading(allchords[2][k], allchords[3][l], measure,fifth=fifth)
                    if s1 + s2 + s3 < score_minimal_vl:
                        minimal_vl = (i,j,k,l)
                        score_minimal_vl = s1 + s2 + s3
    vl = (allchords[0][minimal_vl[0]], allchords[1][minimal_vl[1]],
          allchords[2][minimal_vl[2]], allchords[3][minimal_vl[3]])
    return vl



def best_vl_seqN(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    allchords = [generate_uniques_possibilities(chord, nb_notes) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nb_notes,first=True)
    minimal_vls = [allchords[i][0] for i in range(len(chords))]
    score_minimal_vl = score_voiceleading_seq(minimal_vls,measure,fifth=fifth)
    for chord_seq in product(*allchords):
        score_vl = score_voiceleading_seq(chord_seq,measure,fifth=fifth)
        if score_vl < score_minimal_vl:
            minimal_vls = copy.deepcopy(chord_seq)
            score_minimal_vl = score_vl
    return minimal_vls


def best_vl_seq(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    allchords = [generate_uniques_possibilities(chord, nbn) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nbn,first=True)
    minimal_vls = copy.deepcopy([allchords[0][0],allchords[1][0]])
    score_minimal_vl = (score_voiceleading(allchords[0][0],allchords[1][0],measure,fifth=fifth))
    for chord0,chord1 in product(allchords[0],allchords[1]):
        score_vl = score_voiceleading(chord0,chord1,measure,fifth=fifth)
        if score_vl < score_minimal_vl:
            minimal_vls = copy.deepcopy([chord0,chord1])
            score_minimal_vl = score_vl

    last_chord = minimal_vls[1]
    for i in range(len(chords)-2):
        score_minimal_vl = score_voiceleading(last_chord,allchords[i+2][0],measure,fifth=fifth)
        m_vl = allchords[i+2][0]
        for new_chord in allchords[i+2]:
            score_vl = score_voiceleading(last_chord,new_chord,measure,fifth=fifth)
            if score_vl < score_minimal_vl:
                m_vl = copy.deepcopy(new_chord)
                score_minimal_vl = score_vl
        last_chord = m_vl
        minimal_vls.append(m_vl)

    return minimal_vls

def best_vl_rand(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    allchords = [generate_uniques_possibilities(chord, nbn) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nbn,first=True)
    minimal_vls = copy.deepcopy([allchords[0][0],allchords[1][0]])
    score_minimal_vl = (score_voiceleading(allchords[0][0],allchords[1][0],measure,fifth=fifth))
    for chord0,chord1 in product(allchords[0],allchords[1]):
        score_vl = score_voiceleading(chord0,chord1,measure,fifth=fifth)
        if score_vl < score_minimal_vl:
            minimal_vls = copy.deepcopy([chord0,chord1])
            score_minimal_vl = score_vl

    dict_size = 2
    choices = [0]
    c = random.choice(range(dict_size))
    choices.append(c)
    last_chord = minimal_vls[c]
    for i in range(len(chords)-2):
        score_minimal_vl = score_voiceleading(last_chord,allchords[i+2][0],measure,fifth=fifth)
        m_vl = allchords[i+2][0]
        for new_chord in allchords[i+2]:
            score_vl = score_voiceleading(last_chord,new_chord,measure,fifth=fifth)
            if score_vl < score_minimal_vl:
                m_vl = copy.deepcopy(new_chord)
                score_minimal_vl = score_vl
        minimal_vls.append(m_vl)
        dict_size += 1
        c = random.choice(range(dict_size))
        choices.append(c)
        last_chord = minimal_vls[c]
    
    return minimal_vls, choices

def best_vl_seq5By4(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes
        
    partial_minimal_vl = []    
    last_chord = None

    for i in range(len(chords)/4):
        sub_chords = []
        if not last_chord is None:
            sub_chords.append(last_chord)
        for j in range(4):
            sub_chords.append(copy.deepcopy(chords[4*i+j]))
        l = best_vl_seqN(sub_chords,measure=measure,nb_notes=nbn,fifth=fifth)
        partial_minimal_vl.extend(l)
        last_chord = partial_minimal_vl.pop()
    partial_minimal_vl.append(last_chord)
        
    return partial_minimal_vl

def best_vl_seq4By5(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes
        
    partial_minimal_vl = []    
    last_chord = None
    
    sub_chords = []
    for j in range(4):
        sub_chords.append(copy.deepcopy(chords[j]))
    l =  best_vl_seqN(sub_chords,measure=measure,nb_notes=nbn,fifth=fifth)
    partial_minimal_vl.extend(l)
    last_chord = partial_minimal_vl.pop()
    
    for i in range(4):
        sub_chords = []
        if not last_chord is None:
            sub_chords.append(last_chord)
        for j in range(3):
            sub_chords.append(copy.deepcopy(chords[3*(i+1)+j+1]))
        l = best_vl_seqN(sub_chords,measure=measure,nb_notes=nbn,fifth=fifth)
        partial_minimal_vl.extend(l)
        last_chord = partial_minimal_vl.pop()
    partial_minimal_vl.append(last_chord)
        
    return partial_minimal_vl


def best_vl_sys4(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False, third=False):
    """ 
    Basic S\&C optimisation on a sequence of 4 chord. 
    f:0->1
    g:0->2
    f(g(0))->3

    """
    allchords = [generate_uniques_possibilities(chord, nb_notes) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nb_notes,first=True)
    if third :
        allchords[2] = generate_uniques_possibilities(chords[2], nb_notes,first=third)
    minimal_vl = (0,0,0,0)
    vl = voice_leading( allchords[0][0], allchords[1][0])
    
    score_minimal_vl = (score_voiceleading(allchords[0][0], allchords[1][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[0][0], allchords[2][0], measure,fifth=fifth) +
                        score_voiceleading(apply_vl(allchords[2][0], vl), allchords[3][0], measure,fifth=fifth))
    for i in range(len(allchords[0])):
        for j in range(len(allchords[1])):
            s1 = score_voiceleading(allchords[0][i], allchords[1][j], measure,fifth=fifth)
            vl = voice_leading( allchords[0][i], allchords[1][j],fifth=fifth)
            for k in range(len(allchords[2])):
                s2 = score_voiceleading(allchords[0][i], allchords[2][k], measure,fifth=fifth)
                for l in range(len(allchords[3])):
                    s3 = score_voiceleading(apply_vl(allchords[2][k],vl), allchords[3][l], measure,fifth=fifth)
                    if s1 + s2 + s3 < score_minimal_vl:
                        minimal_vl = (i,j,k,l)
                        score_minimal_vl = s1 + s2 + s3
    vl = (allchords[0][minimal_vl[0]], allchords[1][minimal_vl[1]],
          allchords[2][minimal_vl[2]], allchords[3][minimal_vl[3]])
    return vl

def best_vl_sys4_without(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    f:0->1
    g:0->2
    0->3

    """
    allchords = [generate_uniques_possibilities(chord, nb_notes) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nb_notes,first=True)
    minimal_vl = (0,0,0,0)
    
    score_minimal_vl = (score_voiceleading(allchords[0][0], allchords[1][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[0][0], allchords[2][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[0][0], allchords[3][0], measure,fifth=fifth))
    for i in range(len(allchords[0])):
        for j in range(len(allchords[1])):
            s1 = score_voiceleading(allchords[0][i], allchords[1][j], measure,fifth=fifth)
            for k in range(len(allchords[2])):
                s2 = score_voiceleading(allchords[0][i], allchords[2][k], measure,fifth=fifth)
                for l in range(len(allchords[3])):
                    s3 = score_voiceleading(allchords[0][i], allchords[3][l], measure,fifth=fifth)
                    if s1 + s2 + s3 < score_minimal_vl:
                        minimal_vl = (i,j,k,l)
                        score_minimal_vl = s1 + s2 + s3
    vl = (allchords[0][minimal_vl[0]], allchords[1][minimal_vl[1]],
          allchords[2][minimal_vl[2]], allchords[3][minimal_vl[3]])
    return vl
    
def best_vl_sys16(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    Basic optimisation of a 16 chord sequence.
    2 scales
    """
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    l = copy.deepcopy([chords[4*i] for i in range(4)])
    big_vl = best_vl_sys4(l, measure=measure, nb_notes=nbn,fifth=fifth)
    partial_vl = []
    for i in range(4):
        l = copy.deepcopy([chords[4*i+j] for j in range(4)])
        l[0] = big_vl[i]
        partial_vl.extend(best_vl_sys4(l, measure=measure, nb_notes=nbn,fifth=fifth))

    return partial_vl

def best_vl_sys16_without(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    0->3 applyed on the two scales.
    """
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    l = copy.deepcopy([chords[4*i] for i in range(4)])
    big_vl = best_vl_sys4_without(l, measure=measure, nb_notes=nbn,fifth=fifth)
    partial_vl = []
    for i in range(4):
        l = copy.deepcopy([chords[4*i+j] for j in range(4)])
        l[0] = big_vl[i]
        partial_vl.extend(best_vl_sys4_without(l, measure=measure, nb_notes=nbn,fifth=fifth))

    return partial_vl



def best_vl_sys4_sep(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False, third=False):
    """ 
    Basic S\&C optimisation on a sequence of 4 chord. 
    f:0->1
    g:0->2
    separate from
    f(g(0))->3

    """
    allchords = []
    for i in range(len(chords)):
        first = i==0 or (i==2 and third)
        allchords.append(generate_uniques_possibilities(chords[i], nb_notes, first=first))
    minimal_vl = [0,0,0,0]
    s0m = 99
    for i in range(len(allchords[0])):
        s1m = 99
        bj = 0
        for j in range(len(allchords[1])):
            s1 = score_voiceleading(allchords[0][i], allchords[1][j], measure,fifth=fifth)
            if s1 < s1m :
                s1m = s1
                bj = j
        s2m = 99
        bk = 0
        for k in range(len(allchords[2])):
            s2 = score_voiceleading(allchords[0][i], allchords[2][k], measure,fifth=fifth)
            if s2 < s2m :
                s2m = s2
                bk = k
        if s1m+s2m < s0m:
            s0m = s1m + s2m
            minimal_vl = [i,bj,bk,0]
    virtual = apply_vl(allchords[2][minimal_vl[2]],voice_leading(allchords[0][minimal_vl[0]], allchords[1][minimal_vl[1]],fifth=fifth))

    s3m = 99
    for l in range(len(allchords[3])):
        s3 = score_voiceleading(virtual, allchords[3][l], measure,fifth=fifth)
        if s3 < s3m :
            minimal_vl[3] = l
            s3m = s3
            
    vl = (allchords[0][minimal_vl[0]], allchords[1][minimal_vl[1]],
          allchords[2][minimal_vl[2]], allchords[3][minimal_vl[3]])
    return vl

def best_vl_sys16_sep(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    Basic optimisation of a 16 chord sequence.
    2 scales
    """
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    l = copy.deepcopy([chords[4*i] for i in range(4)])
    big_vl = best_vl_sys4_sep(l, measure=measure, nb_notes=nbn,fifth=fifth)
    partial_vl = []
    for i in range(4):
        l = copy.deepcopy([chords[4*i+j] for j in range(4)])
        l[0] = big_vl[i]
        partial_vl.extend(best_vl_sys4_sep(l, measure=measure, nb_notes=nbn,fifth=fifth))

    return partial_vl


##################### Recursive algorithms for dimension higher than 16 ########################


def best_rec_vl_seq(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):

    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    return rec_vl_seq(chords, None, measure=measure, nb_notes=nbn,fifth=fifth)

def rec_vl_seq(chords,  first, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    if len(chords) < 4 :
        l = copy.deepcopy([chords[j] for j in range(len(chords))])
        l[0] = first
        if first is None:
            l[0] = chords[0]
        return best_vl_seqN(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
    else:
        l = copy.deepcopy([chords[i] for i in range(4)])
        if not first is None:
            l[0] = first
        partial_vl = list(best_vl_seqN(l, measure=measure, nb_notes=nb_notes,fifth=fifth))
        new_vl = rec_vl_seq(chords[3:], partial_vl[3], measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl.pop()
        partial_vl.extend(new_vl)
        return partial_vl


def best_rec_vl_sys(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    result  = [None for chord in chords]
    dim = int(math.log(len(chords),2))
    return rec_vl_sys(chords, 0, dim, chords[0], measure=measure, nb_notes=nbn, fifth=fifth)
    

def rec_vl_sys(chords, i, dim, first, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    if dim == 2:
        l = copy.deepcopy([chords[i+j] for j in range(4)])
        l[0] = first
        return best_vl_sys4(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
    elif dim%2==1:
        partial_vl=[]
        (new_first,second)=best_vl_seqN([chords[i],chords[i+int(math.pow(2,dim-1))]], measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl.extend(rec_vl_sys(chords, i, dim-1, new_first, measure=measure, nb_notes=nb_notes,fifth=fifth))
        partial_vl.extend(rec_vl_sys(chords, i+int(math.pow(2,dim-1)), dim-1, second, measure=measure, nb_notes=nb_notes,fifth=fifth))
        return partial_vl
    else:
        l = copy.deepcopy([chords[int(math.pow(2,dim-2))*j] for j in range(4)])
        l[0] = first
        big_vl = best_vl_sys4(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl = []
        for k in range(4):
            partial_vl.extend(rec_vl_sys(chords, i+k*int(math.pow(2,dim-2)), dim-2, big_vl[k], measure=measure, nb_notes=nb_notes,fifth=fifth))
        return partial_vl
    
def best_rec_bis_vl_sys(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    result  = [None for chord in chords]
    dim = int(math.log(len(chords),2))
    return rec_vl_sys(chords, 0, dim, chords[0], measure=measure, nb_notes=nbn, fifth=fifth)
    

def rec_bis_vl_sys(chords, i, dim, first, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    if dim == 2:
        l = copy.deepcopy([chords[i+j] for j in range(4)])
        l[0] = first
        return best_vl_sys4(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
    elif dim==1:
        partial_vl=[]
        return best_vl_seqN([chords[i],chords[i+1]], measure=measure, nb_notes=nb_notes,fifth=fifth)
    else:
        l = copy.deepcopy([chords[int(math.pow(2,dim-2))*j] for j in range(4)])
        l[0] = first
        big_vl = best_vl_sys4(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl = []
        for k in range(4):
            partial_vl.extend(rec_bis_vl_sys(chords, i+k*int(math.pow(2,dim-2)), dim-2, big_vl[k], measure=measure, nb_notes=nb_notes,fifth=fifth))
        return partial_vl



def best_rec_vl_sys_sep(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    result  = [None for chord in chords]
    dim = int(math.log(len(chords),2))
    return rec_vl_sys_sep(chords, 0, dim, chords[0], measure=measure, nb_notes=nbn, fifth=fifth)
    

def rec_vl_sys_sep(chords, i, dim, first, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    if dim == 2:
        l = copy.deepcopy([chords[i+j] for j in range(4)])
        l[0] = first
        return best_vl_sys4_sep(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
    elif dim%2==1:
        partial_vl=[]
        (new_first,second)=best_vl_seqN([chords[i],chords[i+int(math.pow(2,dim-1))]], measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl.extend(rec_vl_sys(chords, i, dim-1, new_first, measure=measure, nb_notes=nb_notes,fifth=fifth))
        partial_vl.extend(rec_vl_sys(chords, i+int(math.pow(2,dim-1)), dim-1, second, measure=measure, nb_notes=nb_notes,fifth=fifth))
        return partial_vl
    else:
        l = copy.deepcopy([chords[int(math.pow(2,dim-2))*j] for j in range(4)])
        l[0] = first
        big_vl = best_vl_sys4_sep(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl = []
        for k in range(4):
            partial_vl.extend(rec_vl_sys(chords, i+k*int(math.pow(2,dim-2)), dim-2, big_vl[k], measure=measure, nb_notes=nb_notes,fifth=fifth))
        return partial_vl



def best_rec_vl_sys_without(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    dim = int(math.log(len(chords),2))
    return rec_vl_sys_without(chords, 0, dim, chords[0], measure=measure, nb_notes=nbn, fifth=fifth)
    

def rec_vl_sys_without(chords, i, dim, first, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    if dim == 2:
        l = copy.deepcopy([chords[i+j] for j in range(4)])
        l[0] = first
        return best_vl_sys4_without(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
    elif dim%2==1:
        partial_vl=[]
        (new_first,second)=best_vl_seqN([chords[i],chords[i+int(math.pow(2,dim-1))]], measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl.extend(rec_vl_sys_without(chords, i, dim-1, new_first, measure=measure, nb_notes=nb_notes,fifth=fifth))
        partial_vl.extend(rec_vl_sys_without(chords, i+int(math.pow(2,dim-1)), dim-1, second, measure=measure, nb_notes=nb_notes,fifth=fifth))
        return partial_vl
    else:
        l = copy.deepcopy([chords[int(math.pow(2,dim-2))*j] for j in range(4)])
        l[0] = first
        big_vl = best_vl_sys4_without(l, measure=measure, nb_notes=nb_notes,fifth=fifth)
        partial_vl = []
        for k in range(4):
            partial_vl.extend(rec_vl_sys_without(chords, i+k*int(math.pow(2,dim-2)), dim-2, big_vl[k], measure=measure, nb_notes=nb_notes,fifth=fifth))
        return partial_vl




def bin_vl_sys(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    result  = [None for chord in chords]
    dim = int(math.log(len(chords),2))
    aux_bin_vl_sys(chords, 0, dim, result, measure=measure, nb_notes=nbn, fifth=fifth)
    return result

def aux_bin_vl_sys(chords, i, dim, result, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    if dim == 1:
        l = copy.deepcopy([chords[i+j] for j in range(4)])
        l[0] = result[i]
        l[2] = result[i+2]
        new_l = best_vl_sys4(l, measure=measure, nb_notes=nb_notes,fifth=fifth, third=True)
        for j in range(4):
           result[i+j]=new_l[j] 
    elif int(math.pow(2,dim))==len(chords):
        (new_first,third) = best_vl_seqN([chords[i],chords[i+int(math.pow(2,dim-1))]], measure=measure, nb_notes=nb_notes,fifth=fifth)
        result[i] = new_first
        result[i+int(math.pow(2,dim-1))] = third
        aux_bin_vl_sys(chords, i, dim-1, result, measure=measure, nb_notes=nb_notes,fifth=fifth)
    else:
        k = int(math.pow(2,dim))
        l = copy.deepcopy([chords[int(math.pow(2,dim-2))*j] for j in range(4)])
        l[0] = result[i]
        l[2] = result[i+k]
        new_l = best_vl_sys4(l, measure=measure, nb_notes=nb_notes,fifth=fifth, third=True)
        for j in range(4):
           result[i+j*k/2]=new_l[j]
        aux_bin_vl_sys(chords, i, dim-1, result, measure=measure, nb_notes=nb_notes,fifth=fifth)
        aux_bin_vl_sys(chords, i+k, dim-1, result, measure=measure, nb_notes=nb_notes,fifth=fifth)
 






EXPLANATIONS = {
    3: [[0,1,2]],
    5: [[0,1,4]],
    6: [[0,2,4]],
    7: [[4,5,6],[2,3,6],[1,3,5]],
    9: [[0,1,8]],
    10: [[0,2,8]],
    11: [[8,9,10],[2,3,10],[1,3,9]],
    12: [[0,4,8]],
    13: [[8,9,12],[4,5,12],[1,5,9]],
    14: [[8,10,12],[4,6,12],[2,6,10]],
    15: [[12,13,14],[10,11,14],[6,7,14],[9,11,13],[5,7,13],[3,7,11]]}


def compute_level(n):
    if n==0:
        return 0
    elif n==1:
        return 1
    else :
        # print "ICI", n
        p = int(math.log(n,2))
        return compute_level(n-pow(2,p))+1

def create_explanations(dim):
    if dim<2:
        return {}
    else :
        d = create_explanations(dim-1)
        for n in range(2**(dim-1),2**dim,1):
            if compute_level(n)>=2:
                seq = []
                s = ("{0:b}".format(n))
                dims = []
                for i in range(len(s)-1,-1,-1):
                    if s[i]=='1':
                        dims.append(len(s)-1-i)
                # print n, ("{0:b}".format(n)), dims
                for l in combinations(dims,2):
                    a,b = int(l[0]),int(l[1])
                    if a > b:
                        seq.append([n-2**a-2**b,n-2**a,n-2**b])
                    else:
                        seq.append([n-2**a-2**b,n-2**b,n-2**a])
                d[n]=seq
        return d


# for key,value in create_explanations(5).items():
#     print key, ":", value


def best_vl_sys_seq(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    Optimisation choosing the best system of every system where an element is the contrastive one at each step.
    """
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    allchords = [generate_uniques_possibilities(chord, nbn) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nbn,first=True)
    
    
    dim = int(math.log(len(chords),2))
    explanations = create_explanations(dim)
    choices = {}
    for index, systems in explanations.items():
        # print "Index = "+str(index)
        partial_vl = [0,0,0,0]
        indexes = copy.deepcopy(systems[0])
        indexes.append(index)
        vl = voice_leading(allchords[indexes[0]][0], allchords[indexes[1]][0],fifth=fifth)
        partial_score = (score_voiceleading(allchords[indexes[0]][0], allchords[indexes[1]][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[indexes[0]][0], allchords[indexes[2]][0], measure,fifth=fifth) +
                        score_voiceleading(apply_vl(allchords[indexes[2]][0], vl), allchords[indexes[3]][0], measure,fifth=fifth))
        best_sys = copy.deepcopy(indexes)
        for sys in systems :
            indexes = copy.deepcopy(sys)
            indexes.append(index)
            for i in range(len(allchords[indexes[0]])):
                for j in range(len(allchords[indexes[1]])):
                    s1 = score_voiceleading(allchords[indexes[0]][i], allchords[indexes[1]][j], measure,fifth=fifth)
                    vl = voice_leading(allchords[indexes[0]][i], allchords[indexes[1]][j],fifth=fifth)
                    for k in range(len(allchords[indexes[2]])):
                        s2 = score_voiceleading(allchords[indexes[0]][i], allchords[indexes[2]][k], measure,fifth=fifth)
                        for l in range(len(allchords[indexes[3]])):
                            s3 = score_voiceleading(apply_vl(allchords[indexes[2]][k],vl), allchords[indexes[3]][l], measure,fifth=fifth)
                            if s1 + s2 + s3 < partial_score:
                                partial_vl = [i,j,k,l]
                                best_sys = [u for u in indexes]
                                partial_score = s1 + s2 + s3

        choices[index] = copy.deepcopy(best_sys)
        # print best_sys
        # print partial_vl
        for i in range(len(best_sys)):
            allchords[best_sys[i]]=[allchords[best_sys[i]][partial_vl[i]]]
    final_vl = []
    for chord_set in allchords:
        final_vl.append(chord_set[0])
    return final_vl, choices


def best_vl_rand_model(chords, model, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    Optimisation using a model of first order dependancies
    """
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    allchords = [generate_uniques_possibilities(chord, nbn) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nbn,first=True)
    minimal_vls = copy.deepcopy([allchords[0][0],allchords[1][0]])
    score_minimal_vl = (score_voiceleading(allchords[0][0],allchords[1][0],measure,fifth=fifth))
    for chord0,chord1 in product(allchords[0],allchords[1]):
        score_vl = score_voiceleading(chord0,chord1,measure,fifth=fifth)
        if score_vl < score_minimal_vl:
            minimal_vls = copy.deepcopy([chord0,chord1])
            score_minimal_vl = score_vl

    last_chord = minimal_vls[model[1]]
    for i in range(len(chords)-2):
        score_minimal_vl = score_voiceleading(last_chord,allchords[i+2][0],measure,fifth=fifth)
        m_vl = allchords[i+2][0]
        for new_chord in allchords[i+2]:
            score_vl = score_voiceleading(last_chord,new_chord,measure,fifth=fifth)
            if score_vl < score_minimal_vl:
                m_vl = copy.deepcopy(new_chord)
                score_minimal_vl = score_vl
        minimal_vls.append(m_vl)
        last_chord = minimal_vls[model[i+1]]
    
    return minimal_vls



def best_vl_sys_seq_W(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    Same as best_vl_sys_seq but using 0 instead of f(g(0)) on each system optimization
    """
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    allchords = [generate_uniques_possibilities(chord, nbn) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nbn,first=True)
    

    choices = {}
    for index, systems in EXPLANATIONS.items():
        print "Index = "+str(index)
        partial_vl = [0,0,0,0]
        indexes = copy.deepcopy(systems[0])
        indexes.append(index)
        partial_score = (score_voiceleading(allchords[indexes[0]][0], allchords[indexes[1]][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[indexes[0]][0], allchords[indexes[2]][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[indexes[0]][0], allchords[indexes[3]][0], measure,fifth=fifth))
        best_sys = copy.deepcopy(indexes)
        for sys in systems :
            indexes = copy.deepcopy(sys)
            indexes.append(index)
            for i in range(len(allchords[indexes[0]])):
                for j in range(len(allchords[indexes[1]])):
                    s1 = score_voiceleading(allchords[indexes[0]][i], allchords[indexes[1]][j], measure,fifth=fifth)
                    for k in range(len(allchords[indexes[2]])):
                        s2 = score_voiceleading(allchords[indexes[0]][i], allchords[indexes[2]][k], measure,fifth=fifth)
                        for l in range(len(allchords[indexes[3]])):
                            s3 = score_voiceleading(allchords[indexes[0]][i], allchords[indexes[3]][l], measure,fifth=fifth)
                            if s1 + s2 + s3 < partial_score:
                                partial_vl = [i,j,k,l]
                                best_sys = [u for u in indexes]
                                partial_score = s1 + s2 + s3

        choices[index] = copy.deepcopy(best_sys)
        # print best_sys
        # print partial_vl
        for i in range(len(best_sys)):
            allchords[best_sys[i]]=[allchords[best_sys[i]][partial_vl[i]]]
    final_vl = []
    for chord_set in allchords:
        final_vl.append(chord_set[0])
    return final_vl, choices


def best_vl_sys4_line(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    Optimization of 4 chords sequence using sequencial relations to generate the fictive element.
    """
    allchords = [generate_uniques_possibilities(chord, nb_notes) for chord in chords]
    allchords[0] = generate_uniques_possibilities(chords[0], nb_notes,first=True)
    minimal_vl = (0,0,0,0)
    vl = voice_leading( allchords[0][0], allchords[1][0])
    
    score_minimal_vl = (score_voiceleading(allchords[0][0], allchords[1][0], measure,fifth=fifth) +
                        score_voiceleading(allchords[1][0], allchords[2][0], measure,fifth=fifth) +
                        score_voiceleading(apply_vl(allchords[2][0], vl), allchords[3][0], measure,fifth=fifth))
    for i in range(len(allchords[0])):
        for j in range(len(allchords[1])):
            s1 = score_voiceleading(allchords[0][i], allchords[1][j], measure,fifth=fifth)
            vl = voice_leading( allchords[0][i], allchords[1][j],fifth=fifth)
            for k in range(len(allchords[2])):
                s2 = score_voiceleading(allchords[1][i], allchords[2][k], measure,fifth=fifth)
                for l in range(len(allchords[3])):
                    s3 = score_voiceleading(apply_vl(allchords[2][k],vl), allchords[3][l], measure,fifth=fifth)
                    if s1 + s2 + s3 < score_minimal_vl:
                        minimal_vl = (i,j,k,l)
                        score_minimal_vl = s1 + s2 + s3
    vl = (allchords[0][minimal_vl[0]], allchords[1][minimal_vl[1]],
          allchords[2][minimal_vl[2]], allchords[3][minimal_vl[3]])
    return vl

def best_vl_sys16_line(chords, measure=vlms.basic_measure, nb_notes=None,fifth=False):
    """
    Generalization of best_vl_sys4_line on 2 scales to analyse 16-chords sequences.
    """
    nbn = max_notes(chords)
    if not nb_notes is None and nbn > nb_notes:
        nbn = nb_notes

    l = copy.deepcopy([chords[4*i] for i in range(4)])
    big_vl = best_vl_sys4_line(l, measure=measure, nb_notes=nbn,fifth=fifth)
    partial_vl = []
    for i in range(4):
        l = copy.deepcopy([chords[4*i+j] for j in range(4)])
        l[0] = big_vl[i]
        partial_vl.extend(best_vl_sys4_line(l, measure=measure, nb_notes=nbn,fifth=fifth))

    return partial_vl



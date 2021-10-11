#! /usr/bin/python
# -*- coding: utf-8 -*-


import copy
import ast
import random
import voiceleading as vl
import os


NB_SEQUENCES = 45

def add_el(l, e):        
    try:
        l.index(e)
    except ValueError:
        l.append(e)
    

def ext_d(l1, l2):
    for e in l2:
        add_el(l1, e)

def ext_dr(l1, l2):
    l = copy.deepcopy(l1)
    for e in l2:
        add_el(l, e)
    return l


deg_min = ['I', 'bII', 'II', 'III', '#III', 'IV', '#IV', 'V', 'VI','#VI', 'bVII', 'VII']
deg_maj = ['I', 'bII', 'II', 'bIII', 'III', 'IV', '#IV', 'V', 'bVI','VI', 'bVII', 'VII']
degs = ['I','II','III','IV','V','VI','VII']

#Possibilite de considerer des probas par triade par degre pour un degre
triads_min = ['min', 'maj', 'dim', 'maj', 'dim', 'min', 'dim', 'maj', 'maj','dim', 'maj', 'dim']
triads_maj = ['maj', 'aug', 'min', 'aug', 'min', 'maj', 'dim', 'maj', 'aug','min', 'maj', 'dim']

def degree_to_integer(deg):
    try:
        i = deg_min.index(deg)
        return i
    except ValueError:
        i = deg_maj.index(deg)
        return i

def integer_to_triad(i,key):
    deg = integer_to_degree(i,key)
    return degree_to_triad(deg)

def degree_to_triad(deg):
    try:
        i = deg_min.index(deg)
        return triads_min(i)
    except ValueError:
        i = deg_maj.index(deg)
        return triads_maj(i)
    

def integer_to_degree(i,key):
    if key.find('m') == -1:
        return deg_maj[i]
    else:
        return degs_min[i]


def integer_to_basedegree(i):
    return degs[i]


triad_circle_flat  = ['C','Am','F','Dm','Bb','Gm','Eb','Cm','Ab','Fm','Db','Bbm','Gb','Ebm','B','Abm','E','Dbm','A','Gbm','D','Bm','G','Em']
triad_circle_sharp = ['C','Am','F','Dm','A#','Gm','D#','Cm','G#','Fm','C#','A#m','F#','D#m','B','G#m','E','C#m','A','F#m','D','Bm','G','Em'] 
def triad_to_int(triad):
    try:
        i = triad_circle_flat.index(triad)
        return i
    except ValueError:
        i = triad_circle_sharp.index(triad)
        return i

def int_to_triad(i,flat=True):
    if flat :
        return triad_circle_flat[i]
    else :
        return triad_circle_sharp[i]

    
def chords_to_voices(chords):
    # We suppose that the chords are already optimized for voice leading
    voices = [[chord[j] for chord in chords] for j in range(len(chords[0]))]
    return voices


def seq_from_file(filename, i):
    seq = []
    f = open(filename,'r+')
    fline = f.readline()
    n_line = 1
    found = False
    while len(fline) > 0 and not found:
        if len(fline) > 2:
            if n_line == i:
                seq =  list(ast.literal_eval(fline.strip()))
                found = True
            n_line += 1  
        fline = f.readline()
    f.close()
    return seq


def seqs_from_file(filename):
    seqs = []
    f = open(filename,'r+')
    fline = f.readline()
    while len(fline) > 0:
        if len(fline) > 2:
            lf =  list(ast.literal_eval(fline.strip()))
            seqs.append(lf)
        fline = f.readline()
    f.close()
    return seqs

def dicts_from_file(filename):
    dicts = []
    f = open(filename,'r+')
    fline = f.readline()
    while len(fline) > 0:
        if len(fline) > 2:
            lf =  dict(ast.literal_eval(fline.strip()))
            dicts.append(lf)
        fline = f.readline()
    f.close()
    return dicts

def dict_from_file(filename, i):
    dictionary = []
    f = open(filename,'r+')
    fline = f.readline()
    n_line = 1
    found = False
    while len(fline) > 0 and not found:
        if len(fline) > 2:
            if n_line == i:
                dictionary =  dict(ast.literal_eval(fline.strip()))
                found = True
            n_line += 1  
        fline = f.readline()
    f.close()
    return dictionary


def seqs_from_file_without(filename, i):
    seqs = []
    f = open(filename,'r+')
    n_line = 1
    fline = f.readline()
    while len(fline) > 0:
        if len(fline) > 2:
            if n_line != i:
                lf =  list(ast.literal_eval(fline.strip()))
                seqs.append(lf)
            n_line += 1
        fline = f.readline()
    f.close()
    return seqs

def dicts_from_file_without(filename, i):
    dicts = []
    f = open(filename,'r+')
    n_line = 1
    fline = f.readline()
    while len(fline) > 0:
        if len(fline) > 2:
            if n_line != i:
                lf =  dict(ast.literal_eval(fline.strip()))
                dicts.append(lf)
            n_line += 1
        fline = f.readline()
    f.close()
    return dicts

def create_dir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def get_seqs_from_model(model, corpus="45", transformed=False):
    seqs_dir = corpus+"/"
    if corpus == "Patterns":
        seqs_dir += "PRS"
        if transformed :
            seqs_dir+="Sh"
        return seqs_from_file(seqs_dir+"/BestPR"+model),[i for i in range(11)]
    
    elif corpus=="RWC POP" or corpus=="45":
        seqs_dir += "VLS"
        if transformed :
            seqs_dir+="F/"
        else :
            seqs_dir+="B/"
        mod, perm, length = None, None, None
        if model.find("Seq") != -1 or model.find("SysDyn") != -1:
            l = model.split("_")
            mod, length = l 
            perm = 0
        else :
            mod, s = model.split("P")
            #perm is the index of the PPP and length is the sequence length. 
            perm, length = s.split('_')
        seqs = []
        labels = []
        for element in os.listdir(seqs_dir):
            n = int(element.split("_")[-1])
            if element.find(mod)!=-1 and n==int(length):
                seq = seq_from_file(seqs_dir+element,int(perm)+1)
                labels.append(element)
                seqs.append(seq)
        return seqs,labels 

    else :
        print "Wrong Corpus, try another name. The corpus available are : 45, Patterns, RWC POP"

def get_choices_from_corpus(model, corpus="45", transformed=False):
    '''give the list of choices dictionaries for the SysDyn Model'''
    seqs_dir = corpus+"/"
    if corpus == "Patterns":
        seqs_dir += "PRS"
        if transformed :
            seqs_dir+="Sh"
        return dict_from_file(seqs_dir+"/BestPR"+model, 2)
    
    elif corpus=="RWC POP" or corpus=="45":
        seqs_dir += "VLS"
        if transformed :
            seqs_dir+="F/"
        else :
            seqs_dir+="B/"
        mod, perm, length = None, None, None
        if model.find("Seq") != -1 or model.find("SysDyn") != -1:
            l = model.split("_")
            mod, length = l 
        dicts = []
        for element in os.listdir(seqs_dir):
            n = int(element.split("_")[-1])
            if element.find(mod)!=-1 and n==int(length):
                di = dict_from_file(seqs_dir+element,2)
                dicts.append(di)
        return dicts

    else :
        print "Wrong Corpus, try another name. The corpus available are : 45, Patterns, RWC POP"



        
def build_random_model():
    points = [0]
    for i in range(15):
        points.append(random.choice(range(i+2)))
    return points

ref_pred_sys = [0,0,0,3,0,5,5,8,0,10,10,13,15,16,16,19]
def predecessor(num_note, voice, seq, model, pointer=None):
    if num_note < 1:
        return 0
    elif model == 'seq':
        voices = chords_to_voices(chords)
        return voices[voice][num_note-1]
    elif model == 'sys':
        chords = vl.seq_with_fictives_chords(seq)
        voices = chords_to_voices(chords)
        voice = voices[voice]
        return voice[ref_pred_sys[num_note]]
    else :
        voices = chords_to_voices(chords)
        return voices[voice][pointer[num_seq]]



def fact(n):
    if n == 1:
        return 1
    else :
        return n * fact(n-1)
    
def nb_ppp(dim):
    return fact(dim)/pow(2,dim/2)


def generate_ppp(dim):
    vects = [pow(2,i) for i in range(dim)]
    return generate_perm(dim,vects,0)
    
def generate_perm(dim,vects,primer):
    if dim == 2:
        return [[primer,primer+vects[0],primer+vects[1],primer+vects[0]+vects[1]]]
    elif dim%2==1:
        ppps =[]
        for vect in vects:
            new_vects = copy.deepcopy(vects)
            new_vects.remove(vect)
            l1=generate_perm(dim-1,new_vects,primer)
            l2=generate_perm(dim-1,new_vects,primer+vect)
            for i in range(len(l1)-1,-1,-1):
                l = copy.deepcopy(l1[i])
                l.extend(l2[i])
                ppps.insert(0,l)
        return ppps
    else:
        ppps = []
        for i in range(len(vects)-1,-1,-1):
            for j in range(i-1,-1,-1):
                new_vects = copy.deepcopy(vects)
                new_vects.remove(vects[i])
                new_vects.remove(vects[j])
                l1=generate_perm(dim-2,new_vects,primer)
                l2=generate_perm(dim-2,new_vects,primer+vects[j])
                l3=generate_perm(dim-2,new_vects,primer+vects[i])
                l4=generate_perm(dim-2,new_vects,primer+vects[i]+vects[j])
                for k in range(len(l1)-1,-1,-1):
                    l = copy.deepcopy(l1[k])
                    l.extend(l2[k])
                    l.extend(l3[k])
                    l.extend(l4[k])
                    ppps.append(l)
        return ppps


    
def binary_pulses_to_patterns(binary_pulses, shifted=True):
    patterns = []
    pulses = copy.deepcopy(binary_pulses)
    if shifted:
        pulses = pulses[1:]
        pulses.append(binary_pulses[0])
    pat = []
    j = 0
    for pulse in pulses:
        pat.append(pulse)
        j+=1
        if j%4==0:
            patterns.append(bin_to_indexes(pat,shifted=shifted))
            pat = []
            j=0
    return patterns


def bin_to_indexes(pattern,shifted=True):
    indexes = []
    for i in range(len(pattern)):
        if pattern[i]!=0:
            indexes.append(i)
    if len(indexes)==0:
        if shifted:
            indexes.append(3)
        else:
            indexes.append(0)
    return indexes


def isEmpty(seq):
    '''test if a sequence of chords in string notation contains only N'''
    i = 0
    while i < len(seq) and seq[i]=='N':
        i += 1
    return i == len(seq)


def equal_chord(chord1, chord2):
    e = len(chord1)==len(chord2)
    for k in range(len(chord1)):
        e &= chord1[i]==chord2[i]
    return e

def equal_seq(seq1, seq2):
    e = len(seq1)==len(seq2)
    for i in range(len(seq1)):
        e &= equal_chord(seq1[i],seq2[i])
    return e

def equal_seqs(seqs1, seqs2):
    e = len(seqs1)==len(seqs2)
    for i in range(len(seqs1)):
        e &= equal_seq(seqs1[i],seqs2[i])
    return e

def rename():
    for filename in os.listdir("./RWC POP/VLSB/"):
        # seq = basic.seq_from_file("./RWC POP/VLSB/"+filename,1)
        # n = len(seq)
        # i = filename.find("-Best")
        l = filename.split("_")
        s = l[0]+"-"+l[2]+"_"+l[3]
        os.rename("./RWC POP/VLSB/"+filename,"./RWC POP/VLSB/"+s)


def get_index(seq, seqs):
    i = 0
    while i < len(seqs) and seqs[i]!=seq:
        i += 1
    if i == len(seqs):
        raise ValueError
    else :
        return i


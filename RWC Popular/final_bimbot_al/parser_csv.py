#! /usr/bin/python
# -*- coding: utf-8 -*-

import csv
import os
import copy
import basic

Data_repository = './'



def file_to_tab(filename, bracket=False, filterDuplicates=True):
    '''Brackets are used to duplicate elements so that they appear in the two systems they participate.
    '''
    labels = []
    seqs = []
    csvfile = open(Data_repository+filename,'rb')
    spamreader = csv.reader(csvfile, delimiter=';')
    num = filename.split(".")[0]
    for row in spamreader:
        #Ignorer les lignes vides
        if row == [] or all( i=='' for i in row):
            print "Empty line in ", filename
            continue
        label = row[0]
        label = label.replace('/','~')
        if filterDuplicates and labels.count(num+"-"+label)!=0:
            continue
        labels.append(num+"-"+label)
        n = int(row[1])
        b = False
        add = 0
        chords = []
        m = 0
        while m < len(row) and row[m]!='':
            m += 1
        for i in range(m-2):
            s = row[2+i]
            if s.find('[')==-1 and len(chords)== n:
                if s != '%':
                    print "sequence longer than expected in ",filename,", sequence", len(labels), row
                continue
            elif len(chords) < n and s.find('[')!=-1 :
                print "sequence shorter than expected in",filename, ", sequence", len(labels),row
                continue
            elif len(chords)>=n and s.find('[')!=-1 and bracket:
                b = True
                s = s.split('[')[1]
                s = s.split(']')[0]
            elif len(chords)==n and s.find('[')!=-1 and not bracket:
                continue            
            if (s.find(',')==-1):
                chords.extend([s for i in range(4)])
                if b :
                    add+=4
            else :
                l = s.split(",")
                for e in l:
                    if e.find("%")==-1:
                        if e.find("(")>=0 :
                            chords.append(e.split("(")[1])
                            if b :
                                add+=1
                        elif e.find(")")>=0:
                            chords.append(e.split(")")[0])
                            if b :
                                add+=1
                        else :
                            chords.append(e)
                            chords.append(e)
                            if b :
                                add+=2
        if len(chords)!= n+add:
            print "Length mismatch in ", filename ,", sequence", len(labels),": found ", len(chords), "expected ", n, row
        seqs.append(chords)
    return labels, seqs

BeginError = Exception('Sequence begin with no chord')

def complete(seq):
    new_seq = copy.deepcopy(seq)
    n = len(seq)
    if new_seq[0]!='N':
        for i in range(n-1):
            if new_seq[i+1]=='N':
                new_seq[i+1]=new_seq[i]
    else :
        raise BeginError
    return new_seq
        
def note_to_int(note):
    notes1 = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    notes2 = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    for i in range(len(notes1)):
        if notes1[i] == note or notes2[i] == note:
            return i

def int_to_note(i):
    notes = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    return notes[i]

def int_to_note_bis(i):
    notes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    return notes[i]

def parse_root_str(chord):
    root = ""
    root = chord[0]
    if len(chord) > 1 and (chord[1] == 'b' or chord[1]== '#'):
        root += chord[1]
    return root
    
def parse_root_int(chord):
    root = ""
    root = chord[0]
    if len(chord) > 1 and (chord[1] == 'b' or chord[1]== '#'):
        root += chord[1]
    return note_to_int(root)


def parse_triad(chord):
    triad = ""
    i = 1
    if len(chord) > 1 and (chord[i] == 'b' or chord[i]== '#'):
        i +=1
    if len(chord) <= i:
        triad = "M"
    else:
        if chord[i] == "m":
            triad = "m"
        elif chord[i] == '-':
            triad = "-"
        elif chord[i].find('+') != -1:
            triad ="+"
        else:
            j = chord.find('s2')
            if j != -1:
                triad = "s2"
            j = chord.find('s4')
            if j != -1:
                triad = "s4"
            else :
                triad = "M"
#Attention au cas où on a un accord sans tierce, rajouter une
#catégorie autres pour les accords ne rentrant pas explicitement dans
#les 5 catégories ou alors les retrancher dans une d'elle
    return triad

def parse_root_and_triad(chord):
    triad = ""
    i = 1
    if len(chord) > 1 and (chord[i] == 'b' or chord[i]== '#'):
        i +=1
    if len(chord) <= i:
        return chord
    else:
        if chord[i] == "m":
            return chord[0:(i+1)]
        elif chord[i] == '-':
            triad = "-"
        elif chord[i].find('+') != -1:
            return chord[0:(i)]
        else:
            j = chord.find('s2')
            if j != -1:
                return chord[0:(i)]+"m"
            j = chord.find('s4')
            if j != -1:
                return chord[0:(i)]
            else :
                return chord[0:(i)]
#Attention au cas où on a un accord sans tierce, rajouter une
#catégorie autres pour les accords ne rentrant pas explicitement dans
#les 5 catégories ou alors les retrancher dans une d'elle




def parse_notes(chord, only_triad = False):
    root = parse_root_int(chord)
    notes = [root]
    triad = parse_triad(chord)

    if triad == 'M' and chord.find('5')!=-1:
        notes.append((notes[0]+7)%12)
    elif triad == 'M':
        notes.append((notes[0]+4)%12)
        notes.append((notes[0]+7)%12)
    elif triad == 'm':
        notes.append((notes[0]+3)%12)
        notes.append((notes[0]+7)%12)
    elif triad == '-':
        notes.append((notes[0]+3)%12)
        notes.append((notes[0]+6)%12)
    elif triad == '+':
        notes.append((notes[0]+4)%12)
        notes.append((notes[0]+8)%12)
    elif triad == 's2':
        notes.append((notes[0]+2)%12)
        notes.append((notes[0]+7)%12)
    elif triad == 's4':
        notes.append((notes[0]+5)%12)
        notes.append((notes[0]+7)%12)
    else:
        print(triad)

    if not only_triad:
        if chord.find('7') !=-1 and chord[chord.find('7')-1]=='M':
            notes.append((notes[0]+11)%12)
        elif chord.find('7') !=-1 :
            notes.append((notes[0]+10)%12)
        elif chord.find('6') !=-1 :
            notes.append((notes[0]+9)%12)
        elif chord.find('9') !=-1 :
            notes.append((notes[0]+2)%12)

        if chord.find('*')!=-1:
            notes.pop(0)

    return notes


def parse_files(bracket=True):
    final_Labels = []
    final_Seqs = []
    for element in os.listdir(Data_repository):
        if element.endswith('.csv'):
            # print element
            # f = open(element+".parse",'w')
            l,t = file_to_tab(element,bracket=bracket)
            new_l = []
            new_t = []
            for i in range(len(l)):
                if not basic.isEmpty(t[i]):
                    try :
                        new_t.append([parse_notes(e) for e in complete(t[i])])
                        new_l.append(l[i])
                    except Exception :
                        print "Sequence begin with no chords"
                        pass
            final_Labels.extend(new_l)
            final_Seqs.extend(new_t)
    return final_Labels, final_Seqs

def parse_files_symb(bracket=True,triad=True, complete=True, toInt=True, filterDuplicates = True):
    final_Labels = []
    final_Seqs = []
    for element in os.listdir(Data_repository):
        if element.endswith('.csv'):
            # print element
            f = open(element+".seq",'w')
            f2 = open(element+".seg",'w')
            l,t = file_to_tab(element,bracket=bracket,filterDuplicates=filterDuplicates)
            new_l = []
            new_t = []
            for i in range(len(l)):
                if not basic.isEmpty(t[i]):
                    try :
                        ti_complete = [];
                        if complete :
                            ti_complete = complete(t[i])
                        else :
                            ti_complete = t[i]
                            
                        if not triad :
                            new_t.append([e for e in ti_complete])
                        else :
                            if toInt : 
                                new_t.append([basic.triad_to_int(parse_root_and_triad(e)) for e in ti_complete])
                            else :
                                new_t.append([parse_root_and_triad(e) for e in ti_complete])
                        new_l.append(l[i])
                    except Exception :
                        print "Sequence begin with no chords", t[i]
                        pass
            final_Labels.extend(new_l)
            final_Seqs.extend(new_t)
            boundary = 1
            boundaries = []
            for i in new_t:
                boundaries.append(str(boundary))
                boundary += len(i)
                f.write( ' '.join(i), )
                f.write('\n')
            f2.write(' '.join(boundaries))
            f2.write('\n')
    return final_Labels, final_Seqs

l,s = parse_files_symb(bracket = False, triad = False, complete = False, toInt = False, filterDuplicates = False)

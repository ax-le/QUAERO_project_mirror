For each of the 100 songs of the RWC-Pop corpus, the following files exist

Pre-existing files:
- *.wav , the audio file, is not included on this git repository due to their size and license. They can be obtained from Japan's National Institute of Advanced Industrial Science and Technology, or an in-institution private copy.

- *.beat.txt are the beat annotations provided with the RWC database. The first column is the time of the beat, expressed in 100th of a second.
More info at https://staff.aist.go.jp/m.goto/RWC-MDB/AIST-Annotation/#references 
or
Masataka Goto: 
AIST Annotation for the RWC Music Database, Proceedings of the 7th International Conference on Music Information Retrieval (ISMIR 2006), pp.359-360, October 2006. 

- *.chords.lab are the chord annotations produced at the MARL (NYU). The annotations follow the standard .lab format, with a start time, end time and a label, here a chord in Harte's notation.
More info at https://github.com/tmc323/Chord-Annotations

- *.segments.lab are the semiotic structure annotations produced by the Metiss team at IRISA in the context of the QUAERO project. The annotations follow the standard .lab format, with a start time, end time and a label, here a symbol representing the segment's class.
More info at http://musicdata.gforge.inria.fr/structureAnnotation.html
or
F. Bimbot, G. Sargent, E. Deruty; C. Guichaoua, E. Vincent :
Semiotic description of music structure : an introduction to the Quaero/Metiss structural annotations.
Proc. 53rd AES International Conference on Semantic Audio, London, 2014 (12 pages).


New files:
- *.grid.csv are the grid annotations.
The files are semicolon-separated values. Each line corresponds to a segment, and each value corresponds to a bar in the segment.
If a bar contains several chords, a special format is used.
#TODO: Detail this format
Further documentation yet to be announced.
ONLY the first 60 songs are annotated at the moment.

- *.auto.* are annotation files obtained by automatically crossing the annotations from the *.beat.txt, *.chords.lab and *.segments.lab files
These files contain mistakes introduced by the automatic conversion, use at your own risk.
Further documentation yet to be announced.
- *.manual.* are matching files converted from the *.grid.csv
ONLY the first 60 songs are annotated at the moment.

Both categories follow the same format:
- *.seq are chord sequences, sampled at 1 chord per beat. The chords are space-separated and grouped on lines according to the *.segments.lab structure annotations.
- *.simple.seq containis simplified versions of the chords, where chords are mapped to the 24 major and minor triads and a non-chord
- *.seg are the positions of the boundaries for the segments, aligned with the corresponding version of the sequence.
The numbers, arranged in a single line (line breaks break compatibility with some tools) and denote the starting beats of each segment.
The first number is always 1 and should be discarded when computing metrics so as to avoid bias.
There is no number corresponding to the end of the piece, so tools that rely on this file to display segments should figure the last beat on their own.


Individual files:
- parser_csv.py is the script used to convert the *.grid.csv files to the *.manual.* files
"triad" should be set to False to generate the raw chords and True to generate the simple versions
The generated files will be named *.grid.csv.seq and *.grid.csv.seg and should be moved manually after execution.

- basic.py, voiceleading_measure.py, voiceleading.py are dependencies of parser_csv.py


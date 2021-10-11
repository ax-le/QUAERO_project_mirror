Files with the .beatwise.seg extension denote the groundtruth annotations for semiotic segmentation.

The numbers, arranged in a single line (line breaks break compatibility with some tools) and denote the starting beats of each segment.

The first number is always 1 and should be discarded when computing metrics so as to avoid bias.

There is no number corresponding to the end of the piece, so tools that rely on this file to display segments should figure the last beat on their own.

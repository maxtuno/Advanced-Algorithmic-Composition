# Copyright © Oscar Riveros, 2013, Todos los derechos reservados.
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from music21 import *
from numpy import *

# <codecell>

def make_part(row, scale_factor, octave):
    matrixObj = matrix(serial.rowToMatrix(row)).tolist()[0]
    part = stream.Part()
    map(part.append,
        map(lambda pc, length: 
            note.Note(pc, quarterLength= length * scale_factor, octave=octave),
            matrixObj,
            matrixObj))
    
    return part

# <codecell>

row = serial.getHistoricalRowByName('RowWebernOp29').row

new = stream.Stream()

new.insert(32, make_part(row, 1./3, 1))
new.insert(16, make_part(row[::-1], 1./2, 2))
new.insert(8,  make_part(row, 1./2, 3))
new.insert(0,  make_part(row[::-1], 1./3, 4))

new.makeMeasures()
new.show()


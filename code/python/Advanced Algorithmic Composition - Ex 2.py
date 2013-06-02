# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# Simple composition of binary form A|B with pentatonic and aeolian zones, this composition is simple, most advances future examples, includes constraint programing, for an complet control over music.
# 
# Copyright © Oscar Riveros, 2013, Todos los derechos reservados.

# <codecell>

# palette of libraries

from IPython.external import mathjax
from sympy import *
from sympy.utilities.iterables import variations
from sympy.plotting import plot3d
from music21 import *
from itertools import cycle, repeat

x, y, z, r, s, t         = symbols('x y z r s t')
m, n, i, j, k            = symbols('m n i j k', integer=True)
f, g, h, eq, plus, minus = symbols('f g h eq plus minus', cls=Function)

# <codecell>

# motive definition

eq    = Lambda((x, y), x)
plus  = Lambda((x, y), x + y)
minus = Lambda((x, y), x - y)
times = Lambda((x, y), x * y)
div   = Lambda((x, y), x / y)

motive_male   =      [(eq, 0), (plus, 2), (plus, 2), (minus, 5), (plus, 3), (plus, 6), (plus, 7), (minus, 8)]
rhythm_male   = cycle([1./2  , 1./2     , 1./2     , 1./2     , 1./2      , 1./1    , 1./1      , 1./1] * 2)

motive_female =      [(eq, 0), (plus, 3), (plus, 6), (minus, 7), (plus, 5), (plus, 2), (plus, 5), (minus, 7)]
rhythm_female = cycle([1./2  , 1./2     , 1./2     , 1./2     , 1./2      , 1./1    , 1./1      , 1./1][::-1] * 2) #inversion of rithmical motif

# <codecell>

# motive expander

def framework(start, end, intervals):
    material = [start]
    tmp = start
    
    for index in range(start, end):
        if tmp < end:
            tmp = tmp + intervals.next()
            material = material + [tmp]
        
    return material


def expander(motive, length):
    return map(lambda x, y: x[0](x[1], y), motive * length, range(len(motive * length)))

# <codecell>

def make_part(part, material, material_maping, rhythm, rhythm_mapping, octave):
    
    map(part.append,
        map(lambda pc: 
            note.Note(material_maping(pc), 
                      quarterLength = rhythm_mapping(next(rhythm)),
                      octave = octave),
            material))
    
    return part

# <codecell>

intervalic_pattern = cycle([3, 2, 2, 3, 2] * 2 + [2, 1, 2, 2, 2, 1, 2] * 2) # pentatonic + natural minor
size               = 12 # generic size parameter

# <codecell>

# global instruments

voice1 = stream.Part()
voice2 = stream.Part()
voice3 = stream.Part()
voice4 = stream.Part()

# global motives development

material        = framework(0, 127, intervalic_pattern)
voice1_material = expander(motive_male        , size)
voice2_material = expander(motive_female      , size)
voice3_material = expander(motive_male[::-1]  , size)
voice4_material = expander(motive_female[::-1], size)

# <codecell>

# Section A

voice1_material_maping = lambda x: list(material)[int(x**1) % len(material)]
voice2_material_maping = lambda x: list(material)[int(x**2) % len(material)]
voice3_material_maping = lambda x: list(material)[int(x**3) % len(material)]
voice4_material_maping = lambda x: list(material)[int(x**4) % len(material)]

voice1_rhythm_maping   = lambda x: float(x*1)
voice2_rhythm_maping   = lambda x: float(x*2)
voice3_rhythm_maping   = lambda x: float(x*3)
voice4_rhythm_maping   = lambda x: float(x*4)
   
voice1 = make_part(voice1, voice1_material, voice1_material_maping, rhythm_male, voice1_rhythm_maping, 5)
voice2 = make_part(voice2, voice2_material, voice2_material_maping, rhythm_male, voice2_rhythm_maping, 4)
voice3 = make_part(voice3, voice3_material, voice3_material_maping, rhythm_male, voice3_rhythm_maping, 3)
voice4 = make_part(voice4, voice4_material, voice4_material_maping, rhythm_male, voice4_rhythm_maping, 2)

# <codecell>

# Section B

voice1_material_maping = lambda x: list(material)[int(x**4) % len(material)]
voice2_material_maping = lambda x: list(material)[int(x**3) % len(material)]
voice3_material_maping = lambda x: list(material)[int(x**2) % len(material)]
voice4_material_maping = lambda x: list(material)[int(x**1) % len(material)]

voice1_rhythm_maping   = lambda x: float(x*4)
voice2_rhythm_maping   = lambda x: float(x*3)
voice3_rhythm_maping   = lambda x: float(x*2)
voice4_rhythm_maping   = lambda x: float(x*1)
   
voice1 = make_part(voice1, voice1_material, voice1_material_maping, rhythm_male, voice1_rhythm_maping, 5)
voice2 = make_part(voice2, voice2_material, voice2_material_maping, rhythm_male, voice2_rhythm_maping, 4)
voice3 = make_part(voice3, voice3_material, voice3_material_maping, rhythm_male, voice3_rhythm_maping, 3)
voice4 = make_part(voice4, voice4_material, voice4_material_maping, rhythm_male, voice4_rhythm_maping, 2)

# <codecell>

# Let's Put It All Together

new = stream.Stream()
new.insert(0, voice1)
new.insert(4, voice2)
new.insert(8, voice3)
new.insert(16,voice4)
new.show()


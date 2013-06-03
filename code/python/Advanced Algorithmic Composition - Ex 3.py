# Copyright © Oscar Riveros, 2013, Todos los derechos reservados.
# Materialized Music: https://soundcloud.com/maxtuno/advanced-algorithmic-1
# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# palette of libraries

from IPython.external import mathjax
import sympy   as sym
import music21 as m21
import numpy   as num

from sympy.utilities.iterables import variations
from sympy.plotting import plot3d
from itertools import cycle, repeat, count, imap
from math import sin, cos

x, y, z, r, s, t  = sym.symbols('x y z r s t')
m, n, i, j, k     = sym.symbols('m n i j k', integer=True)
f, g, h           = sym.symbols('f g h', cls=sym.Function)

# <codecell>

# motive definition
shk    = sym.Lambda((x, y), x + y) #schenkerian

motif1 = [(shk, 0), (shk, 3), (shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1), (shk, 5), (shk, -1)]
rhythm1 = cycle(num.array([1., 1./2, 2., 1./2] * 2 + [1., 1./2, 2., 1./2][::-1] * 2))

motif2 = [(shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1)]
rhythm2 = cycle(num.array([1., 1./2, 2., 1./2][::-1] * 2 + [1., 1./2, 2., 1./2][::-1] * 2))

motif3 = [(shk, 0), (shk, 3), (shk, 5), (shk, -1)]
rhythm3 = cycle(num.array([1., 1./2, 2., 1./2]))

motif4 = [(shk, 0), (shk, 1), (shk, 0), (shk, -1)]
rhythm4 = cycle(num.array([1., 1./2, 2., 1./2][::-1]))

size    = 2 # generic size parameter
pattern = cycle([2, 2, 2, 1, 2, 2, 1]) #* 2 [3, 2, 2, 3, 2] * 2 + [2, 1, 2, 2, 2, 1, 2] * 2)

deep = -12*1 

l = 0
h = 0

space = range(12,120)

violin      = range(12*4 + l, 12*7 - h)
viola       = range(12*3 + l, 12*6 - h)
cello       = range(12*2 + l, 12*5 - h)
double_Bass = range(12*1 + l, 12*4 - h)

# <codecell>

# motive expanderç

def framework(intrument_material, intervals):
    material = [intrument_material[0]]
    tmp = intrument_material[0]
    
    for index in intrument_material:
        if intrument_material[0] <= tmp <= intrument_material[-1]:
            tmp = tmp + next(cycle(intervals))
            material = material + [tmp]
        
    return material


def expander(material, motive):
    return map(lambda x:x[0](x[1], next(cycle(material))), motive*size)

# <codecell>

def make_part(voice, motif, intrument, pattern, motif_maping, rhythm, rhythm_mapping, length):
    for ps in expander(framework(intrument, pattern), motif) * length:
        morph  = motif_maping(ps, intrument[0], len(intrument)) + deep 
        voice.append(m21.note.Note(midi = morph,
        quarterLength = rhythm_mapping(next(rhythm))))
    
    return voice

# <codecell>

# Section A
def section_a(voice1, voice2, voice3, voice4):
    voice1_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice2_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice3_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice4_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]

    voice1_rhythm_maping   = lambda x: float(x*1)
    voice2_rhythm_maping   = lambda x: float(x*2)
    voice3_rhythm_maping   = lambda x: float(x*3)
    voice4_rhythm_maping   = lambda x: float(x*4)
   
    voice1 = make_part(voice1, motif1, violin, pattern, voice1_motif_maping, rhythm1, voice1_rhythm_maping, 8)
    voice2 = make_part(voice2, motif1, violin, pattern, voice2_motif_maping, rhythm1, voice2_rhythm_maping, 4)
    voice3 = make_part(voice3, motif2, viola,  pattern, voice3_motif_maping, rhythm2, voice3_rhythm_maping, 2)
    voice4 = make_part(voice4, motif2, cello,  pattern, voice4_motif_maping, rhythm2, voice4_rhythm_maping, 1)

# <codecell>

# Section B
def section_b(voice1, voice2, voice3, voice4):
    voice1_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice2_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice3_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice4_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]


    voice1_rhythm_maping   = lambda x: float(x*4)
    voice2_rhythm_maping   = lambda x: float(x*3)
    voice3_rhythm_maping   = lambda x: float(x*3)
    voice4_rhythm_maping   = lambda x: float(x*4)
   
    voice1 = make_part(voice1, motif2, violin, pattern, voice1_motif_maping, rhythm2, voice1_rhythm_maping, 1)
    voice2 = make_part(voice2, motif2, violin, pattern, voice2_motif_maping, rhythm2, voice2_rhythm_maping, 2)
    voice3 = make_part(voice3, motif1, viola,  pattern, voice3_motif_maping, rhythm1, voice3_rhythm_maping, 3)
    voice4 = make_part(voice4, motif1, cello,  pattern, voice4_motif_maping, rhythm1, voice4_rhythm_maping, 1)

# <codecell>

# Section C
def section_c(voice1, voice2, voice3, voice4):
    voice1_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice2_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice3_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]
    voice4_motif_maping = lambda x, y, z: voice_mat[(y + (x % z)) % len(voice_mat)]


    voice1_rhythm_maping   = lambda x: float(x*1)
    voice2_rhythm_maping   = lambda x: float(x*2)
    voice3_rhythm_maping   = lambda x: float(x*2)
    voice4_rhythm_maping   = lambda x: float(x*1)
   
    voice1 = make_part(voice1, motif2, violin, pattern, voice1_motif_maping, rhythm2, voice1_rhythm_maping, 3)
    voice2 = make_part(voice2, motif2, violin, pattern, voice2_motif_maping, rhythm2, voice2_rhythm_maping, 2)
    voice3 = make_part(voice3, motif3, viola,  pattern, voice3_motif_maping, rhythm3, voice3_rhythm_maping, 3)
    voice4 = make_part(voice4, motif3, cello,  pattern, voice4_motif_maping, rhythm3, voice4_rhythm_maping, 1)

# <codecell>

# Let's Put It All Together

voice_mat = framework(range(-12*2, 12*12), pattern)

# global instruments
voice1 = m21.stream.Part()
voice2 = m21.stream.Part()
voice3 = m21.stream.Part()
voice4 = m21.stream.Part()

section_a(voice1, voice2, voice3, voice4)
section_b(voice1, voice2, voice3, voice4)
section_c(voice1, voice2, voice3, voice4)
section_b(voice1, voice2, voice3, voice4)
section_a(voice1, voice2, voice3, voice4)

score = m21.stream.Stream()
score.insert(0, voice1)
score.insert(4, voice2)
score.insert(8, voice3)
score.insert(16,voice4)
score.show()



# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

# Source Code: https://github.com/maxtuno/Advanced-Algorithmic-Composition
# Blogs:
# http://oscar-riveros.blogspot.com/
# http://mx-clojure.blogspot.com/
# Facebook: https://www.facebook.com/pages/Oscar-Riveros/207414032634682
# Copyright © Oscar Riveros, 2013, Todos los derechos reservados.

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
from constraint_solver import pywrapcp as cp


x, y, z, r, s, t  = sym.symbols('x y z r s t')
m, n, i, j, k     = sym.symbols('m n i j k', integer=True)
f, g, h           = sym.symbols('f g h', cls=sym.Function)

solver = cp.Solver('Counterpoint')

# <codecell>

# motive definition

shk    = sym.Lambda((x, y), x + y) #schenkerian

size= 6

motif_xp =  [(shk, 0), (shk, 3), (shk, 5), (shk, -1)]
rhythm_xp = [(shk, 0), (shk, 3), (shk, 5), (shk, -1)]

# Same Motif for notes and rhythms for a Fractal Result

motif1  = [(shk, 0), (shk, 3), (shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1), (shk, 5), (shk, -1)] * size
rhythm1 = [(shk, 0), (shk, 3), (shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1), (shk, 5), (shk, -1)] * size

motif2  = [(shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1)] * size
rhythm2 = [(shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1)] * size

motif3  = [(shk, 0), (shk, 3), (shk, 5), (shk, -1)] * size
rhythm3 = [(shk, 0), (shk, 3), (shk, 5), (shk, -1)] * size

motif4  = [(shk, 0), (shk, 1), (shk, 1), (shk, 0), (shk, 3), (shk, 0), (shk, -1)] * size
rhythm4 = [(shk, 0), (shk, 1), (shk, 1), (shk, 0), (shk, 3), (shk, 0), (shk, -1)] * size

motif5  = [(shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1)] * size
rhythm5 = [(shk, 0), (shk, 1), (shk, 0), (shk, 3), (shk, 5), (shk, -1), (shk, 0), (shk, -1)] * size

motif6  = [(shk, 0), (shk, 1), (shk, -1), (shk, 0), (shk, -1)] * size
rhythm6 = [(shk, 0), (shk, 1), (shk, -1), (shk, 0), (shk, -1)] * size

size    = 2 # generic size parameter
pattern_motif  = cycle([1])
pattern_rhythm = cycle([1])# * 2 + [3, 2, 2, 3, 2] * 2 + [2, 1, 2, 2, 2, 1, 2] * 2)

deep = -12*0

l = 0
h = 0

violin      = range(12*4 + l, 12*7 - h)
viola       = range(12*3 + l, 12*6 - h)
cello       = range(12*2 + l, 12*5 - h)
bass        = range(12*1 + l, 12*4 - h)

space_palette  = range(0, 120)
rhythm_palette = [8, 4, 3, 2, 1]

allowed_intervals_x = [1, 2, 3, 4, 5, 7, 12]
allowed_intervals_y = [-12, 0, 7 , 12]

allowed_durations_x = rhythm_palette
allowed_durations_y = range(-12, 12)

# <codecell>

def find_counterpoint(cantus_firmus_motif, cantus_firmus_rhythm):
    
    voice_mat_cfm = map(int, cantus_firmus_motif)
    voice_mat_cpm = map(int, framework(space_palette, pattern_motif))
    
    voice_mat_cfr = map(int, cantus_firmus_rhythm)
    voice_mat_cpr = map(int, framework(rhythm_palette, pattern_rhythm))
    
    n                 = len(voice_mat_cfm)

    cfm       = voice_mat_cfm
    cpm       = [solver.IntVar(voice_mat_cpm, 'cpm[%i]' % i)  for i in range(n)]
    diffs_xm  = [solver.IntVar(allowed_intervals_x, 'diffsm[%i]' % i) for i in range(n - 1)]
    diffs_ym  = [solver.IntVar(allowed_intervals_y, 'diffsm[%i]' % i) for i in range(n)]  
    
    for k in range(n):
        solver.Add(diffs_ym[k] == abs(cpm[k] - cfm[k])) 

    for k in range(n - 1):
        solver.Add(diffs_xm[k] == abs(cpm[k] - cpm[k + 1])) 
        
    m                 = len(voice_mat_cfr)    
        
    solver.Add(cpm[0] == cfm[0] + 12)
    solver.Add(cpm[-1] == cfm[-1] + 12) 
    
    cfr       = voice_mat_cfr
    cpr       = [solver.IntVar(voice_mat_cfr, 'cpr[%i]' % i)  for i in range(m)]
    diffs_xr  = [solver.IntVar(allowed_durations_x, 'diffsr[%i]' % i) for i in range(m - 1)]
    diffs_yr  = [solver.IntVar(allowed_durations_y, 'diffsr[%i]' % i) for i in range(m)] 
    
    for k in range(m):
        solver.Add(diffs_yr[k] == abs(cpr[k] - cfr[k])) 

    for k in range(m - 1):
        solver.Add(diffs_xr[k] == abs(cpr[k] - cpr[k + 1]))


    solver.Add(cpr[0] == cfr[0])
    solver.Add(cpr[-1] == cfr[-1])

    solution = solver.Assignment()
    
    allVars = cpm + cpr
    solution.Add(allVars)
    solution.Add(diffs_xm)
    solution.Add(diffs_ym)
    solution.Add(diffs_xr)
    solution.Add(diffs_yr)
    
    collector = solver.FirstSolutionCollector(solution) # Only First Solution
    
    solver.Solve(solver.Phase(allVars,
                              solver.INT_VAR_DEFAULT,
                              solver.INT_VALUE_DEFAULT),
                              [collector]) 
      
    counterpoint = []    
        
    num_solutions = collector.SolutionCount()
    
    if num_solutions > 0:
        counterpoint  = [[collector.Value(0, cpm[i]), collector.Value(0, cpr[i])] for i in range(min(n, m))]
        print counterpoint
    
    solver.EndSearch()    
          
    print "num_solutions:", collector.SolutionCount()
    print "failures:", solver.Failures()
    print "branches:", solver.Branches()
    print "WallTime:", solver.WallTime()
    
    return counterpoint

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

def make_part(voice, motif, intrument_palette, rhythm_palette, pattern_motif, rhythm, pattern_rhythm, length):
    mxp = expander(framework(intrument_palette, pattern_motif), motif)
    rxp = expander(framework(rhythm_palette, pattern_rhythm), rhythm)
    
    cantus_firmus = [[mxp[i], rxp[i]] for i in range(min(len(mxp) , len(rxp)))]
    
    for cf in cantus_firmus  * length:
        voice.append(m21.note.Note(midi = cf[0],
        quarterLength = float(cf[1]) / 4.))
    
    return voice

def make_counterpoint(voice, motif, intrument_palette, rhythm_palette, pattern_motif, rhythm, pattern_rhythm, length):
    counterpoint = find_counterpoint(expander(framework(intrument_palette, pattern_motif) , motif),
                                     expander(framework(rhythm_palette,    pattern_rhythm), rhythm))
    
    for cp in counterpoint * length:
        voice.append(m21.note.Note(midi = cp[0],
        quarterLength = float(cp[1]) / 4.))
    
    return voice

# <codecell>

# Section A
def section_a(voice1, voice2, voice3, voice4, voice5, voice6):
    
    voice1 =         make_part(voice1, motif1, violin, rhythm_palette,  pattern_motif, rhythm1, pattern_rhythm, 1)
    voice2 = make_counterpoint(voice2, motif1, viola,  rhythm_palette,  pattern_motif, rhythm2, pattern_rhythm, 2)
    voice3 =         make_part(voice3, motif2, viola,  rhythm_palette,  pattern_motif, rhythm3, pattern_rhythm, 3)
    voice4 = make_counterpoint(voice4, motif2, cello,  rhythm_palette,  pattern_motif, rhythm4, pattern_rhythm, 2)
    voice5 =         make_part(voice5, motif3, cello,  rhythm_palette,  pattern_motif, rhythm5, pattern_rhythm, 3)
    voice6 = make_counterpoint(voice6, motif3, bass,   rhythm_palette,  pattern_motif, rhythm6, pattern_rhythm, 4)

# <codecell>

# Let's Put It All Together
def materialize():
    # global instruments
    voice1 = m21.stream.Part()
    voice2 = m21.stream.Part()
    voice3 = m21.stream.Part()
    voice4 = m21.stream.Part()
    voice5 = m21.stream.Part()
    voice6 = m21.stream.Part()

    section_a(voice1, voice2, voice3, voice4, voice5, voice6)

    score = m21.stream.Stream()
    score.insert(0, voice1)
    score.insert(0, voice2)
    score.insert(0, voice3)
    score.insert(0, voice4)
    score.insert(0, voice5)
    score.insert(0, voice6)

    score.makeMeasures()
    score.show()

# <codecell>

materialize()

# <codecell>

                                                                                        

# <codecell>



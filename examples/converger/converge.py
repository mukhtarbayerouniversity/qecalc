from qeutils.converger import Converger

#convergence in 'total energy',  'geometry' or 'single phonon' calculations
#can be studied  with respect to the following variables:
#                'nbnd'         : 'system',
#                'degauss'      : 'system',
#                'ecutwfc'      : 'system',
#                'ecutrho'      : 'system',
#                'conv_thr'     : 'electrons',
#                'etot_conv_thr': 'control',
#                'forc_conv_thr': 'control',
#                'path_thr'     : 'ions',
#                'kpoints'      : 'k_points'


configString = """
# all the relevant input files must be preconfigured for specific tasks
# before using this class

[Launcher]
# parallelization parameters
# if this section is empty - serial mode is used
paraPrefix:   mpiexec -n 8
paraPostfix: -npool 8


outdir: temp/



[pw.x]
# pw input/output files
pwfInput:  scf.in
pwOutput: scf.out


[ph.x]
#ph.x input/ouput, relevant to all phonon calculations:
phInput:  ph.in
phOutput: ph.out

[dynmat.x]
#dynmat.x input/output files relevant to single phonon calculation
dynmatInput:  dynmat.in
dynmatOutput: dyn.out
"""

opt = Converger(configString = configString, taskName = 'total energy', tolerance = 0.1)
conv_thr = opt.converge(what = 'conv_thr', startValue = 1e-4, multiply = 0.1)
ecut = opt.converge(what = 'ecutwfc', startValue = 18, step = 4)
ecutrho = opt.converge('ecutrho', ecut*4, 16)
#opt.converge('kpoints',[12,12,12],[2,2,2])

#print opt.getForces()
#print opt.getStress()


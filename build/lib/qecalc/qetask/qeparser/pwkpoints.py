#!/usr/bin/env python
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# QEcalc              by DANSE Inelastic group
#                     Nikolay Markovskiy
#                     California Institute of Technology
#                     (C) 2009  All Rights Reserved
#
# File coded by:      Nikolay Markovskiy
#
# See AUTHORS.txt for a list of people who contributed.
# See LICENSE.txt for license information.
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import numpy
class PWKpoints(object):
    def __init__(self, qeInput):
        self.qeInput = qeInput
        self.isAutomatic = False

    def parse(self):
        """ Returns array of points. Does not have to be AUTOMATIC """
        kpoints = []
        if self.qeInput.cards['k_points'].arg() == 'automatic':
            self.isAutomatic = True
        for line in self.qeInput.cards['k_points'].lines():
            if self.isAutomatic:
                kpoints.append([int(k) for k in line.split()])
                if len(kpoints[0][:]) > 3:
                    shifts = [int(k) for k in kpoints[0][3:]]
                else:
                    shifts = [int(0) ,int(0), int(0)]
                break
            else:
                kpoints.append([float(k) for k in line.split()])
        
        if self.isAutomatic:
            shifts = numpy.array(shifts)
        else:
            # first line was number of kpoints
            kpoints.pop(0)
            shifts = None
        kpoints = numpy.array(kpoints)
        self.coords = kpoints
        self.shifts = shifts

    def setAutomatic(self, kpoints, shifts = None):
        """Takes two lists of values"""
        self.isAutomatic = True
        if shifts == None:
            if len(kpoints) == 3:
                shifts = numpy.array([int(0) ,int(0), int(0)])
            if len(kpoints) == 6:
                shifts = kpoints[3:]
                kpoints = kpoints[:3]
        else:
            if len(shifts) == 3 and len(kpoints) == 3:
                shifts = shifts
                kpoints = kpoints
            else:
                raise Exception('Wrong number of kpoints and/or shifts')

        self.kpoints = numpy.array(kpoints)
        self.shifts = numpy.array(shifts)
        self.qeInput.cards['k_points'].removeLines()
        self.qeInput.cards['k_points'].setArg('AUTOMATIC')
        string = ""
        for k in self.kpoints:
            string = string + str(k) + " "
        for s in self.shifts:
            string = string + str(s) + " "
        self.qeInput.cards['k_points'].addLine(string)

if __name__ == "__main__":
    print "Hello World";

__author__="Nikolay Markovskiy"
__date__ ="$Oct 20, 2009 12:59:23 PM$"

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:54:34 2023

@author: zauri
"""

from opm_cram_dagap_interface import OPM

opm = OPM()

test_env = [['object1', [[0, 1, 1], [0, 0, 0, 0]]],
          ['object2', [[0, 0, 0], [0, 0, 0, 0]]],
          ['robot', [[0,0,0], [0, 0, 0, 1]]]]



next_action = opm.predict_next_action(test_env)

print(next_action)
from FourierTransformation import Wave, CompositeWave # type: ignore
import matplotlib.pyplot as plt
import numpy as np
import random

def generate_pure_plots():
    """ Generates plots of pure waves, using Wave class with different frequencies"""
    wave1 = Wave(2)
    wave1.sampleFreq()
    wave1.plot_OGWave(labels=False)    
    
generate_pure_plots()
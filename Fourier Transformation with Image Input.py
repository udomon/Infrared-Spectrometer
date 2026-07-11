from math import ceil
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import random
import json
from PIL import Image
sns.set()

class Wave:
    #constructor of wave
    def __init__(self, frequency):
        self.frequency = frequency
        self.time = np.arange(0,2,0.001) #equaly space time from 0 to 2 seconds, with gap of 0.001 seconds 
        self.cos_wave = np.cos(2*np.pi*frequency*self.time)

        #shared attributes
        self.minFreq = None
        self.maxFreq = None
        self.sampleFreqList = None
        self.freqSpectrum = None
        self.centre = None
        self.xCord = None
        self.yCord = None
        self.trueFreqs = []

    def _freqRange(self, step):
        freq = self.frequency
        if freq // step == 0:
            lower = 0
        elif freq % step == 0:
            lower = freq - step//2
        else:
            lower = (freq // step) * step
        upper = lower + step
        return lower, upper

    #identify original frequencies of OGWave
    def sampleFreq(self, Plot = False):
        centre = []
        minFreq, maxFreq = self._freqRange(5)

        #list frequencies within range of parameters
        sampleFreqList = np.arange(minFreq, maxFreq, 0.1) #do i do linspace of 1000 instead

        #for each frequency, create an amplitude and angle pair for the wave at each time point, and store in centre list
        for sample in sampleFreqList:
            centre.append([(self.cos_wave[i], self.time[i]*sample*2*np.pi) for i in range(len(self.time))])
        
        #plot the amplitude and angle pairs in cartesian plane (amplitude, angle) to (x,y)
        xCord, yCord = [], []
        for _ in range(len(centre)):
            xCord.append([amp*np.cos(theta) for (amp,theta) in centre[_]]) 
            yCord.append([amp*np.sin(theta) for (amp,theta) in centre[_]])

        #store and plot all central points for each frequency
        freqSpectrum = []
        for _ in range(len(centre)):
            #store centre for later
            realCompSum = np.sum(xCord[_]) #store sum of x coordinates for each frequencyy
            freqSpectrum.append(realCompSum) #only care about real component

        self.sampleFreqList = sampleFreqList
        self.minFreq = minFreq
        self.maxFreq = maxFreq
        self.freqSpectrum = freqSpectrum
        self.centre = centre
        self.xCord = xCord
        self.yCord = yCord

        if Plot:
            self.plot_SampleFreq()

    def trueFreq(self):
        self.sampleFreq()
        #sample frequencies with highest mean amplitude are the original frequencies
        realComps = np.asarray(self.freqSpectrum)        
        maxVal = float(np.max(realComps))
        
        from scipy.signal import find_peaks
        peaks, properties = find_peaks(realComps, height = maxVal * 0.7, distance = 5) #peaks 5 samples apart and 70% of max
        trueFreqs = [float(self.sampleFreqList[p]) for p in peaks]

        print(f"True frequencies are: {', '.join([f'{freq:.2f}' for freq in trueFreqs])}") #could return this as an array later
        self.trueFreqs = trueFreqs

    def plot_SampleFreqPython(self):
        
        plt.rcParams['figure.figsize'] = (15,110)
        plt.figure()

        centre = self.centre
        xCord = self.xCord
        yCord = self.yCord
        sampleFreqList = self.sampleFreqList

        if centre is None:
            # compute if not already available
            self.sampleFreq()
            centre = self.centre
            xCord = self.xCord
            yCord = self.yCord
            sampleFreqList = self.sampleFreqList

        #plotting
        total = len(centre)
        intervals = np.linspace(0, total, 50)
        col = 10
        row = int(total/col) + (1 if total % col != 0 else 0)

        #plot red dot, and points in cartesian plane (amplitude, angle) to (x,y)
        for _ in range(len(centre)):
            plt.subplot(row,col,_+1)
            plt.plot(xCord[_], yCord[_], linewidth = 0.4)
            plt.plot(np.mean(xCord[_]), np.mean(yCord[_]), 'ro', markersize = 3) #plotting mean of x and y coordinates as red dot
            plt.title("SF = "+str(round(sampleFreqList[_], 2))+" Hz")
            plt.axis('equal')
            plt.xticks([])
            plt.yticks([])
        
        #adjust figure parameters
        plt.subplots_adjust(
            left=0.02,    
            right=0.98,  
            top=0.97,     
            bottom=0.02,  
            wspace=0.35, 
            hspace=0.55   
        )
        plt.show()

    def plot_SampleFreqPython_50ONLY(self): #need to show the correct freq
        plt.rcParams['figure.figsize'] = (15,110)
        plt.figure()

        centre = self.centre
        xCord = self.xCord
        yCord = self.yCord
        sampleFreqList = self.sampleFreqList
        maxFreq = self.maxFreq
        minFreq = self.minFreq

        if centre is None:
            # compute if not already available
            self.sampleFreq()
            centre = self.centre
            xCord = self.xCord
            yCord = self.yCord
            maxFreq = self.maxFreq
            minFreq = self.minFreq
            sampleFreqList = self.sampleFreqList

        #plotting
        total = min(50,len(centre))
        intervals = np.linspace(0, len(centre)-1, total)
        col = 10
        row = int(total/col) + (1 if total % col != 0 else 0)

        #plot red dot, and points in cartesian plane (amplitude, angle) to (x,y)
        for i, idx in enumerate(intervals):
            _ = int(idx)
            plt.subplot(row,col,i+1)
            plt.plot(xCord[_], yCord[_], linewidth = 0.4)
            plt.plot(np.mean(xCord[_]), np.mean(yCord[_]), 'ro', markersize = 3) #plotting mean of x and y coordinates as red dot
            plt.title("SF = "+str(round(sampleFreqList[_], 2))+" Hz")
            plt.axis('equal')
            plt.xticks([])
            plt.yticks([])
        
        #adjust figure parameters
        plt.subplots_adjust(
            left=0.02,    
            right=0.98,  
            top=0.97,     
            bottom=0.02,  
            wspace=0.35, 
            hspace=0.55   
        )
        plt.show()

    def plot_SampleFreqHTML(self):
        centre = self.centre
        xCord = self.xCord
        yCord = self.yCord
        sampleFreqList = self.sampleFreqList
        maxFreq = self.maxFreq
        minFreq = self.minFreq
        trueFreqs = self.trueFreqs

        if centre is None:
            # compute if not already available
            self.trueFreq()
            centre = self.centre
            xCord = self.xCord
            yCord = self.yCord
            maxFreq = self.maxFreq
            minFreq = self.minFreq
            sampleFreqList = self.sampleFreqList
            trueFreqs = self.trueFreqs
        elif not trueFreqs:
            # if centre exists but trueFreqs not calculated yet
            self.trueFreq()
            trueFreqs = self.trueFreqs

        plots = []
        for i in range(len(self.xCord)):
            if any(np.isclose(sampleFreqList[i], freq) for freq in trueFreqs):
                special = True
            else:
                special = False

            plots.append(
                {
                    "freq": round(self.sampleFreqList[i], 2),
                    "x": self.xCord[i],
                    "y": self.yCord[i],
                    "centreX": np.mean(self.xCord[i]),
                    "centreY": np.mean(self.yCord[i]),
                    "special": special
                })
        with open("plots.json", "w") as f:
            f.write("const PLOTS = ")
            f.write(json.dumps(plots))
            f.write(";")
        print("Open fourier_plots.html in the browser")

    #plot the original wave
    def plot_OGWave(self, labels = True):
        plt.figure()
        plt.rcParams['figure.figsize'] = (12,4) #customise (size) of graphb
        plt.plot(self.time, self.cos_wave)

        if labels:
            plt.title(f"Cosine Wave with {self.frequency} frequency")
            plt.ylabel("Amplitude")
            plt.xlabel('Time (in seconds)')
        else:
            plt.xticks([])
            plt.yticks([])
            plt.tight_layout()
            plt.subplots_adjust(left=0.0, right=1, top=1, bottom=0.00)
        plt.show()

    #plot the centre against frequency AKA final wave
    def plot_FinalWave(self):
        minFreq = self.minFreq
        maxFreq = self.maxFreq
        freqSpectrum = self.freqSpectrum
        sampleFreqList = self.sampleFreqList

        if freqSpectrum is None:
            # compute if not already available
            self.sampleFreq()
            minFreq = self.minFreq
            maxFreq = self.maxFreq
            freqSpectrum = self.freqSpectrum
            sampleFreqList = self.sampleFreqList

        plt.figure()
        #plot centre against frequency
        plt.rcParams['figure.figsize'] = (12,4)
        plt.xlabel("Frequency (Hz)")

        plt.xticks(np.arange(minFreq, maxFreq, 0.5))
        sns.set()
        plt.plot(sampleFreqList, freqSpectrum) #plot the sample against the mean of the x coordinates (real component) to identify original frequencies
        plt.subplots_adjust(sns.reset_defaults())

        plt.show()

    def startUp(self):
        self.sampleFreq()
        self.trueFreq()

    #do all plots
    def plot_All(self):
        self.plot_OGWave()
        self.plot_SampleFreqHTML()
        self.plot_FinalWave()    

class CompositeWave(Wave):
    def __init__(self, frequencies):
        self.frequency = frequencies
        self.time = np.arange(0,2,0.001) #equaly space time from 0 to 2 seconds, with gap of 0.001 seconds 
        self.cos_wave = np.sum([np.cos(2*np.pi*frequency*self.time) for frequency in frequencies], axis = 0)

        #shared attributes
        self.minFreq = None
        self.maxFreq = None
        self.sampleFreqList = None
        self.freqSpectrum = None
        self.centre = None
        self.xCord = None
        self.yCord = None
        self.trueFreqs = []

    def _freqRange(self, step):
        freqLower = min(self.frequency)
        if freqLower // step == 0:
            lower = 0
        elif freqLower % step == 0:
            lower = freqLower - step//2
        else:
            lower = (freqLower // step) * step

        freqUpper = max(self.frequency)
        if freqUpper // step == 0:
            upper = freqUpper + step
        elif freqUpper % step == 0:
            upper = freqUpper + step//2
        else:
            upper = step + (freqUpper // step) * step
        return lower, upper

    def plot_FinalWave(self):
        minFreq = self.minFreq
        maxFreq = self.maxFreq
        freqSpectrum = self.freqSpectrum
        sampleFreqList = self.sampleFreqList

        if freqSpectrum is None:
            # compute if not already available
            self.sampleFreq()
            minFreq = self.minFreq
            maxFreq = self.maxFreq
            freqSpectrum = self.freqSpectrum
            sampleFreqList = self.sampleFreqList

        plt.figure()
        #plot centre against frequency
        plt.rcParams['figure.figsize'] = (12,4)
        plt.xlabel("Frequency (Hz)")

        #calculate x ticks but needs to be done intuitively, so is factor of 5 or 10
        if maxFreq - minFreq >= 20:
            interval = round((maxFreq - minFreq) // 20)
        elif maxFreq - minFreq >= 10:
            interval = round((maxFreq - minFreq) // 10)
        elif maxFreq - minFreq >= 5:
            interval = round((maxFreq - minFreq) // 5)
        elif maxFreq - minFreq >= 1:
            interval = round(maxFreq - minFreq)
        else:
            interval = 0.1

        plt.xticks(np.arange(minFreq, maxFreq, interval))
        sns.set()
        plt.plot(sampleFreqList, freqSpectrum) #plot the sample against the mean of the x coordinates (real component) to identify original frequencies
        plt.subplots_adjust(sns.reset_defaults())

        plt.show()

class ImageWave(CompositeWave):
    def __init__(self, image_path):
        self.image_path = image_path
        raw_wave = self._extractWave(image_path)
        raw_wave = self._normalise(raw_wave)

        self.time = np.arange(0,2,0.001) #equaly space time from 0 to 2 seconds, with gap of 0.001 seconds 
        self.cos_wave = np.interp(np.linspace(0, 1, 2000), #provides 2000 data points, interpolating the wave
                                 np.linspace(0, 1, len(raw_wave)), #maps the original wave to the new time range
                                 raw_wave)
        self.time = np.linspace(0, 2, len(self.cos_wave))

        #shared attributes
        self.minFreq = None
        self.maxFreq = None
        self.sampleFreqList = None
        self.freqSpectrum = None
        self.centre = None
        self.xCord = None
        self.yCord = None
        self.trueFreqs = []
    
    def _freqRange(self, step):
        return 0, 100

    def _extractWave(self, image_path):
        image = Image.open(image_path).convert('L') # Convert to grayscale
        arr = np.array(image) # make image into an array
        darkest_row = np.argmin(arr, axis=0).astype(float)
    
        # Flip vertically — image rows go top-down, but amplitude goes bottom-up
        return image.height - darkest_row

    def _normalise(self, wave):
        min, max = wave.min(), wave.max()
        if max == min:
            return np.zeros_like(wave) # Avoid division by zero if all values are the same
        return 2 * (wave - min) / (max - min) - 1 # Normalise to range [-1, 1]

    def plot_OGWave(self):
        plt.figure()
        plt.rcParams['figure.figsize'] = (12,4) #customise (size) of graphb
        plt.plot(self.time, self.cos_wave)
        plt.title(f"Wave")
        plt.ylabel("Amplitude")
        plt.xlabel('Time (in seconds)')
        plt.show()


if __name__ == "__main__":
    wave1 = CompositeWave([4, 10, 16, 12])
    wave2 = Wave(2)
    wave3 = ImageWave("Wave1.png")
    wave3.sampleFreq()
    wave3.plot_All()


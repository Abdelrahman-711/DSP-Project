import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import soundfile as sf
import os
import librosa

class Equalizer:
    def __init__(self, fs):
        self.fs = fs
        self.preset_bands = [
            (0, 100), (100, 300), (300, 800), (800, 2000),
            (2000, 5000), (5000, 10000), (10000, 20000)
        ]

    def design_band_filter(self, low, high, order, filter_type='FIR', window='hamming'):
        nyq = 0.5 * self.fs
        low = max(0.001, low)
        high = min(nyq - 0.001, high)
        
        if filter_type == 'FIR':
            # Bandpass filter
            b = signal.firwin(order + 1, [low, high], fs=self.fs, pass_zero=False, window=window)
            a = [1.0]
        else: # IIR Butterworth
            b, a = signal.butter(order, [low, high], btype='bandpass', fs=self.fs)
            
        return b, a

    def process(self, data, gains_db, order=101, filter_type='FIR', output_dir=None):
        """
        gains_db: list of gains in dB for each preset band
        """
        combined_signal = np.zeros_like(data)
        
        for i, (low, high) in enumerate(self.preset_bands):
            gain = 10**(gains_db[i] / 20)
            b, a = self.design_band_filter(low, high, order, filter_type)
            
            # Filter the signal for this band
            band_signal = signal.lfilter(b, a, data)
            
            # Apply gain
            combined_signal += gain * band_signal
            
            if output_dir:
                self.plot_filter_analysis(b, a, f"Band_{i}_{low}-{high}Hz", output_dir)
                
        return combined_signal

    def plot_filter_analysis(self, b, a, name, output_dir):
        w, h = signal.freqz(b, a, fs=self.fs)
        plt.figure(figsize=(10, 4))
        plt.plot(w, 20 * np.log10(np.abs(h) + 1e-10))
        plt.title(f'Magnitude Response - {name}')
        plt.ylabel('Magnitude (dB)')
        plt.xlabel('Frequency (Hz)')
        plt.grid()
        plt.savefig(os.path.join(output_dir, f'filter_{name}.png'))
        plt.close()

def run_equalizer_demo(input_file, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    # Load audio
    data, fs = librosa.load(input_file, sr=None)
    
    eq = Equalizer(fs)
    
    # Example gains (boost speech frequencies)
    # Bands: 0-100, 100-300, 300-800, 800-2k, 2k-5k, 5k-10k, 10k-20k
    gains = [0, 2, 5, 8, 5, 2, 0] 
    
    # Process
    processed_data = eq.process(data, gains, output_dir=output_dir)
    
    # Save output
    output_path = os.path.join(output_dir, 'enhanced_speech.wav')
    sf.write(output_path, processed_data, fs)
    
    # Comparison Plot
    plt.figure(figsize=(12, 6))
    plt.subplot(2, 1, 1)
    plt.specgram(data, Fs=fs)
    plt.title('Original Spectrogram')
    plt.subplot(2, 1, 2)
    plt.specgram(processed_data, Fs=fs)
    plt.title('Enhanced Spectrogram')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'spectrogram_comparison.png'))
    plt.close()
    
    print(f"Equalization complete. Saved to {output_path}")

if __name__ == "__main__":
    # Create a dummy speech signal if no file provided
    dummy_file = '/home/ubuntu/DSP-Project/data/speech_sample.wav'
    if not os.path.exists(dummy_file):
        fs = 44100
        t = np.linspace(0, 2, 2 * fs)
        # Mix of some frequencies
        speech_like = np.sin(2 * np.pi * 440 * t) + 0.5 * np.sin(2 * np.pi * 1000 * t) + 0.2 * np.random.randn(len(t))
        sf.write(dummy_file, speech_like, fs)
        
    output_dir = '/home/ubuntu/DSP-Project/results/part2'
    run_equalizer_demo(dummy_file, output_dir)

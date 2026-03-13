import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import wfdb
import os

def load_ecg(record_path):
    record = wfdb.rdrecord(record_path)
    # Use the first channel
    sig = record.p_signal[:, 0]
    fs = record.fs
    return sig, fs

def design_filters(fs):
    # 1. High-pass filter (Baseline wander removal) - Cutoff 0.5 Hz
    # Using IIR Butterworth for sharp cutoff
    b_hp, a_hp = signal.butter(4, 0.5, btype='highpass', fs=fs)
    
    # 2. Notch filter (Power-line interference) - 50 Hz
    b_notch, a_notch = signal.iirnotch(50, 30, fs=fs)
    
    # 3. Low-pass filter (Muscle noise reduction) - Cutoff 100 Hz
    # Using FIR Window-based method (Hamming)
    numtaps = 101
    b_lp = signal.firwin(numtaps, 100, fs=fs, window='hamming')
    a_lp = [1.0]
    
    # 4. Alternative: IIR Chebyshev Type II for Muscle noise
    b_lp_cheby, a_lp_cheby = signal.cheby2(4, 40, 100, btype='lowpass', fs=fs)
    
    return {
        'hp': (b_hp, a_hp, 'High-pass (Butterworth)'),
        'notch': (b_notch, a_notch, 'Notch (50Hz)'),
        'lp_fir': (b_lp, a_lp, 'Low-pass (FIR Hamming)'),
        'lp_cheby': (b_lp_cheby, a_lp_cheby, 'Low-pass (Chebyshev II)')
    }

def analyze_filter(b, a, name, fs, output_dir):
    # Magnitude and Phase response
    w, h = signal.freqz(b, a, fs=fs)
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(w, 20 * np.log10(abs(h)))
    plt.title(f'Frequency Response - {name}')
    plt.ylabel('Magnitude (dB)')
    plt.grid()
    
    plt.subplot(2, 1, 2)
    plt.plot(w, np.angle(h))
    plt.ylabel('Phase (radians)')
    plt.xlabel('Frequency (Hz)')
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{name.replace(" ", "_")}_freq_resp.png'))
    plt.close()

    # Impulse and Step response
    t_imp = np.linspace(0, 0.5, int(0.5 * fs))
    impulse = np.zeros_like(t_imp)
    impulse[0] = 1.0
    step = np.ones_like(t_imp)
    
    y_imp = signal.lfilter(b, a, impulse)
    y_step = signal.lfilter(b, a, step)
    
    plt.figure(figsize=(10, 6))
    plt.subplot(2, 1, 1)
    plt.plot(t_imp, y_imp)
    plt.title(f'Impulse Response - {name}')
    plt.grid()
    
    plt.subplot(2, 1, 2)
    plt.plot(t_imp, y_step)
    plt.title(f'Step Response - {name}')
    plt.xlabel('Time (s)')
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'{name.replace(" ", "_")}_time_resp.png'))
    plt.close()

    # Pole-Zero Plot
    z, p, k = signal.tf2zpk(b, a)
    plt.figure(figsize=(6, 6))
    theta = np.linspace(0, 2*np.pi, 100)
    plt.plot(np.cos(theta), np.sin(theta), 'k--', alpha=0.5)
    plt.scatter(np.real(z), np.imag(z), marker='o', facecolors='none', edgecolors='b', label='Zeros')
    plt.scatter(np.real(p), np.imag(p), marker='x', color='r', label='Poles')
    plt.title(f'Pole-Zero Diagram - {name}')
    plt.legend()
    plt.grid()
    plt.axis('equal')
    plt.savefig(os.path.join(output_dir, f'{name.replace(" ", "_")}_pz.png'))
    plt.close()

def calculate_snr(signal_raw, signal_filtered):
    noise = signal_raw - signal_filtered
    snr = 10 * np.log10(np.sum(signal_filtered**2) / np.sum(noise**2))
    return snr

def process_ecg(record_name, data_dir, output_dir):
    record_path = os.path.join(data_dir, record_name)
    sig, fs = load_ecg(record_path)
    
    # Use a segment (first 10 seconds)
    n_samples = int(10 * fs)
    sig_raw = sig[:n_samples]
    time = np.arange(n_samples) / fs
    
    filters = design_filters(fs)
    
    # Apply filters sequentially
    sig_hp = signal.lfilter(filters['hp'][0], filters['hp'][1], sig_raw)
    sig_notch = signal.lfilter(filters['notch'][0], filters['notch'][1], sig_hp)
    sig_filtered = signal.lfilter(filters['lp_fir'][0], filters['lp_fir'][1], sig_notch)
    
    # Analysis for each filter
    for key, (b, a, name) in filters.items():
        analyze_filter(b, a, name, fs, output_dir)
        
    # Final comparison
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 1, 1)
    plt.plot(time, sig_raw)
    plt.title(f'Original ECG Signal (Record {record_name})')
    plt.grid()
    
    plt.subplot(2, 1, 2)
    plt.plot(time, sig_filtered)
    plt.title('Filtered ECG Signal')
    plt.xlabel('Time (s)')
    plt.grid()
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f'comparison_{record_name}.png'))
    plt.close()
    
    # PSD Comparison
    f_raw, psd_raw = signal.welch(sig_raw, fs, nperseg=1024)
    f_filt, psd_filt = signal.welch(sig_filtered, fs, nperseg=1024)
    
    plt.figure(figsize=(10, 6))
    plt.semilogy(f_raw, psd_raw, label='Original')
    plt.semilogy(f_filt, psd_filt, label='Filtered')
    plt.title('Power Spectral Density (Welch Method)')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('PSD (V^2/Hz)')
    plt.legend()
    plt.grid()
    plt.savefig(os.path.join(output_dir, f'psd_{record_name}.png'))
    plt.close()
    
    # SNR Improvement
    snr_val = calculate_snr(sig_raw, sig_filtered)
    print(f"Record {record_name} - SNR: {snr_val:.2f} dB")
    
    with open(os.path.join(output_dir, f'results_{record_name}.txt'), 'w') as f:
        f.write(f"Record: {record_name}\n")
        f.write(f"SNR: {snr_val:.2f} dB\n")

if __name__ == "__main__":
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/mitdb'))
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../results/part1'))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    process_ecg('100', data_dir, output_dir)
    process_ecg('106', data_dir, output_dir)

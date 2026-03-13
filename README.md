# Digital Signal Processing Final Project

This repository contains the implementation and analysis for the Digital Signal Processing (DSP) Final Project, divided into two main parts: ECG Signal Denoising and a Multi-Band Speech Equalizer.

## Project Structure

- `part1_ecg/`: Contains scripts for ECG data downloading and processing.
- `part2_equalizer/`: Contains the implementation of the multi-band digital equalizer.
- `data/`: Directory for input data (ECG records from MIT-BIH, speech samples).
- `results/`: Contains generated plots, analysis results, and processed audio/signals.

## Part I: ECG Signal Denoising

The goal of this part is to design and implement digital filters to remove noise from ECG signals, specifically targeting baseline wander, power-line interference (50 Hz), and muscle (EMG) noise.

### Filters Designed:
1. **High-pass Filter (Butterworth)**: Cutoff at 0.5 Hz to remove baseline wander.
2. **Notch Filter**: Centered at 50 Hz to eliminate power-line interference.
3. **Low-pass Filter (FIR Hamming)**: Cutoff at 100 Hz to reduce high-frequency muscle noise.

### Analysis:
- Frequency response (Magnitude and Phase)
- Impulse and Step response
- Pole-Zero diagrams
- Power Spectral Density (PSD) using Welch's method
- Signal-to-Noise Ratio (SNR) improvement

## Part II: Multi-Band Speech Equalizer

A multi-band digital equalizer was developed to enhance speech clarity in recordings.

### Key Features:
- **Preset Mode**: 7 speech-optimized frequency bands.
- **Filter Options**: Supports both FIR (Window-based) and IIR (Butterworth) filters.
- **Analysis**: Magnitude response for each band and spectrogram comparison.

## How to Run

1. Install dependencies:
   ```bash
   pip install wfdb scipy matplotlib numpy pandas soundfile librosa
   ```
2. Download ECG data:
   ```bash
   python part1_ecg/download_data.py
   ```
3. Process ECG signals:
   ```bash
   python part1_ecg/ecg_processing.py
   ```
4. Run Speech Equalizer:
   ```bash
   python part2_equalizer/equalizer.py
   ```

All results and plots are saved in the `results/` directory.

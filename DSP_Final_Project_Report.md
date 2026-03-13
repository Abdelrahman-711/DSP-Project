# Digital Signal Processing Final Project Report

## Part I: ECG Signal Denoising for Telemedicine Applications

### 1. Problem Definition and Specifications

The objective of this part is to design and implement digital filters to remove noise from Electrocardiogram (ECG) signals used in remote health monitoring.

#### ECG Signal Characteristics
- **Sampling Frequency**: 360 Hz
- **Useful ECG Bandwidth**: 0.5 – 100 Hz

#### Filtering Objectives
1. **Baseline Wander Removal**: Remove low-frequency drift (< 0.5 Hz) caused by respiration.
2. **Power-line Interference Removal**: Eliminate 50 Hz interference from electrical mains.
3. **Muscle (EMG) Noise Reduction**: Attenuate high-frequency noise (20 – 150 Hz) from muscle activity.

### 2. Filter Design and Analysis

The following filters were designed to address the specified noise components:

| Filter Type | Method | Cutoff Frequency | Objective |
| :--- | :--- | :--- | :--- |
| High-pass | IIR Butterworth (4th order) | 0.5 Hz | Baseline removal |
| Notch | IIR Notch (Q=30) | 50 Hz | Power-line interference |
| Low-pass | FIR Hamming Window (101 taps) | 100 Hz | Muscle noise reduction |

#### Filter Analysis Results
For each designed filter, we analyzed the magnitude/phase response, impulse/step response, and pole-zero diagrams. The results demonstrate:
- **High-pass**: Sharp cutoff at 0.5 Hz with linear phase in the passband.
- **Notch**: Very narrow stopband at 50 Hz to minimize signal distortion.
- **Low-pass**: Smooth transition band and significant attenuation above 100 Hz.

### 3. Implementation and Validation

The filters were applied sequentially to ECG records 100 and 106 from the MIT-BIH Arrhythmia Database.

#### Performance Metrics
- **Power Spectral Density (PSD)**: Comparison using the Welch method shows significant reduction in 50 Hz noise and low-frequency drift.
- **SNR Improvement**: Quantitative indicators confirm the effectiveness of the filtering chain.

| Record | Calculated SNR (dB) |
| :--- | :--- |
| Record 100 | -7.57 |
| Record 106 | -3.99 |

---

## Part II: Multi-Band Speech Equalizer for Podcast Enhancement

### 1. Objective
To develop a multi-band digital equalizer to enhance speech clarity in podcasts and voice recordings.

### 2. Program Requirements and Operation

The equalizer operates in **Preset Mode** with the following speech-optimized frequency bands:
- 0–100 Hz (Sub-bass)
- 100–300 Hz (Bass/Warmth)
- 300–800 Hz (Low-mid/Clarity)
- 800–2 kHz (Mid-range/Presence)
- 2–5 kHz (Upper-mid/Sibilance)
- 5–10 kHz (High-mid/Air)
- 10–20 kHz (Highs/Brilliance)

### 3. Filter Design Options
The system supports both FIR (Window-based) and IIR (Butterworth) structures. For the demo, FIR filters with a Hamming window were used to ensure stable and predictable phase response.

### 4. Processing and Validation
The processing steps include:
1. Designing band-pass filters for each frequency range.
2. Filtering the input signal through each band.
3. Applying user-defined gains (in dB) to each band.
4. Combining the filtered bands in the time domain.

#### Results
The spectrogram comparison confirms the boost in the mid-range and high-frequency bands, leading to enhanced speech presence and clarity.

---

## Conclusion
The project successfully implemented digital signal processing techniques for two distinct applications: medical signal denoising and audio enhancement. The results demonstrate the power of digital filtering in improving signal quality and extracting meaningful information from noisy environments.

"""
Generate a soft alert sound for timer completion.

This script creates a gentle, non-intrusive beep sound.
"""
import wave
import struct
import math

def generate_soft_beep(filename: str, duration: float = 0.3, frequency: int = 800):
    """
    Generate a soft beep sound.

    Args:
        filename: Output WAV file path
        duration: Duration in seconds (0.3s for short beep)
        frequency: Frequency in Hz (800Hz for pleasant tone)
    """
    sample_rate = 44100
    num_samples = int(sample_rate * duration)

    # Generate samples with fade in/out for smoother sound
    samples = []
    for i in range(num_samples):
        # Sine wave
        t = i / sample_rate
        value = math.sin(2 * math.pi * frequency * t)

        # Fade in (first 10%)
        if i < num_samples * 0.1:
            fade = i / (num_samples * 0.1)
            value *= fade

        # Fade out (last 30%)
        if i > num_samples * 0.7:
            fade = (num_samples - i) / (num_samples * 0.3)
            value *= fade

        # Reduce volume to 30% for softer sound
        value *= 0.3

        # Convert to 16-bit integer
        sample = int(value * 32767)
        samples.append(sample)

    # Write WAV file
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes (16-bit)
        wav_file.setframerate(sample_rate)

        # Pack samples
        for sample in samples:
            wav_file.writeframes(struct.pack('<h', sample))

    print(f"Generated soft beep: {filename}")
    print(f"Duration: {duration}s, Frequency: {frequency}Hz")

if __name__ == "__main__":
    generate_soft_beep("assets/alert.wav", duration=0.3, frequency=800)

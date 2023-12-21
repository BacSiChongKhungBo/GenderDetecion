import parselmouth
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# ghi âm giọng nói
def record_from_mic(duration):
    fs = 44100  # Tần số lấy mẫu
    print("Đang ghi âm...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
    sd.wait()
    print("Ghi âm hoàn tất.")
    return recording

def calculate_pitch_rc(recored_audio):
    fs = 44100  # Tần số lấy mẫu
    sound = parselmouth.Sound(recored_audio[:, 0], sampling_frequency=fs)
    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    # pitch trung bình từ các pitch
    average_pitch = np.nanmean(pitch_values)
    return average_pitch

def calculate_pitch(audio_file):
    sound = parselmouth.Sound(audio_file)
    pitch = sound.to_pitch()
    pitch_values = pitch.selected_array['frequency']
    # Trung bình các giá trị pitch để có pitch trung bình
    average_pitch = np.nanmean(pitch_values)
    return average_pitch

def generate_plot_rc(recording):
    Fs = 44100  # Tần số lấy mẫu
    signal = recording[:, 0]  # Chỉ sử dụng kênh âm thanh đầu tiên (nếu có nhiều kênh)
    L = len(signal)
    T = 1 / Fs
    t = np.arange(0, L) * T
    # Corrupt the signal with zero-mean
    signal -= np.mean(signal)

    # FFT
    fft_result = np.fft.fft(signal)
    freq = np.fft.fftfreq(L, T)[:L // 2]
    amplitude_spectrum = (2 / L) * np.abs(fft_result[:L // 2])

    # Plot Single-Sided Amplitude Spectrum
    plt.figure(1, figsize=(20, 20))

    plt.subplot(2, 1, 1)
    plt.plot(t, signal.T)
    plt.title('Tín hiệu đầu vào')
    plt.xlabel('Thời gian')
    plt.ylabel('Amplitude')

    plt.subplot(2, 1, 2)
    plt.plot(freq, amplitude_spectrum)
    plt.title('Single-Sided Amplitude Spectrum')
    plt.xlabel('Tần số (Hz)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

def generate_plot(audio_file):
    sound = parselmouth.Sound(audio_file)
    signal = sound.values.T
    L = len(signal)
    T = 1 / sound.sampling_frequency
    t = np.arange(0, L) * T
    # Corrupt the signal with zero-mean
    signal -= np.mean(signal)

    # FFT
    fft_result = np.fft.fft(signal)
    freq = np.fft.fftfreq(L, T)[:L // 2]
    amplitude_spectrum = (2 / L) * np.abs(fft_result[:L // 2])

    # Plot Single-Sided Amplitude Spectrum
    plt.figure(1, figsize=(10, 10))
    plt.subplot(2, 1, 1)
    plt.plot(t, signal)
    plt.title('Tín hiệu đầu vào')
    plt.xlabel('Thời gian')
    plt.ylabel('Amplitude')
    plt.grid()

    plt.subplot(2, 1, 2)
    plt.plot(freq, amplitude_spectrum)
    plt.title('Single-Sided Amplitude Spectrum')
    plt.xlabel('Tần số (Hz)')
    plt.ylabel('Amplitude')
    plt.grid()
    plt.show()

def gender_determine(audio_file, choice):
    # Hz nam thường < 150 trong khi nữ cao hơn => khoảng xác định
    threshold = 150
    if choice == "1":
        average_pitch = calculate_pitch_rc(audio_file)
    else:
        average_pitch = calculate_pitch(audio_file)
    # So sánh với tần số trung bình
    if average_pitch <= threshold:
        return "Giới tính Nam với tần số trung bình là " + str(average_pitch) + " Hz"
    else:
        return "Giới tính Nữ với tần số trung bình là " + str(average_pitch) + " Hz"
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    while True:
        print("Xin mời nhập lựa chọn:")
        print("1. Ghi âm trực tiếp")
        print("2. Sử dụng file mẫu")
        print("3. Thoát")
        choice = input("Nhập lựa chọn của bạn: ")
        if choice == '1':
            recorded_audio = record_from_mic(3)
            generate_plot_rc(recorded_audio)
            gender = gender_determine(recorded_audio, choice)
            print(gender)
        elif choice == '2':
            audio_file = input("Nhập tên file mẫu của bạn: ")
            audio_file = "Sample/" + audio_file + ".wav"
            generate_plot(audio_file)
            gender = gender_determine(audio_file, choice)
            print(gender)
        elif choice == '3':
            print("Tạm biệt")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import wave
import numpy as np


def convolve_wav(samples, size):
    """
    Функция осуществляет свёртку массива сэмплов из .wav файла.

    В цикле проходим "окном" размера size по массиву сэмплов и
    добавляем в новый массив среднее значение сэмплов в нашем "окне".

    :param samples: массив сэмплов из .wav файла (class 'numpy.ndarray')
    :param size: размер свёртки (int)
    :return: массив сэмплов меньшего размера (class 'numpy.ndarray')
    """

    start = 0
    end = size
    samples_length = len(samples)
    convolved_samples = []

    while end <= samples_length:
        convolved_samples.append(np.mean(samples[start:end]))
        start = end
        end += size

    return np.array(convolved_samples)


def search_significant_transitions(samples, k):
    """
    Функция ищет значимые переходы в массиве сэмплов .wav файла.

    Сравниваем разницу величин соседних сэмплов в массиве с неким заданным порогом
    (параметр k задает величину порога), получая таким образом значения важных
    дла дальнейшей обработки в программе переходов между сэмплами (см. файл "обработка.png").

    :param samples: массив сэмплов из .wav файла (class 'numpy.ndarray')
    :param k: коэффицент, на который делится максимальное значение в массиве (int)
    :return significant_transitions: важные для дальнейшей обработки переходы (list)
    """

    significant_transitions = []
    threshold = max(samples) / k
    right_border = len(samples)

    for i in range(1, right_border):
        if np.absolute(samples[i] - samples[i - 1]) > threshold:
            significant_transitions.append(i - 1)

    return significant_transitions


def get_wav_transitions(wav_name, convolve_coefficient, search_transitions_parameter):
    """
    Функция находит нужные для создания камеры переходы в wav файле.

    :param wav_name: название .wav файла (str)
    :param convolve_coefficient: коэффицент свертки массива сэмплов .wav файла (int)
    :param search_transitions_parameter: значение параметра k для функции поиска переходов (int)
    :return: список переходов для камеры в виде секунд wav файла (list).
    """

    with wave.open(wav_name, 'rb') as wav:
        number_of_channels = wav.getnchannels()    # количество каналов
        sample_width = wav.getsampwidth()    # количество байт на сэмпл
        sampling_frequency = wav.getframerate()    # количество фреймов в секунду
        number_of_frames = wav.getnframes()  # общее количество аудиофреймов
        bytes_frames = wav.readframes(number_of_frames)  # возвращает фреймы в виде строки bytes

    samples_types = {
        2: np.int16,
        4: np.int32
    }

    samples = np.fromstring(bytes_frames, dtype=samples_types[sample_width])
    channel1 = samples[0::number_of_channels]
    channel1[channel1 < 0] = 0  # заменяем отрицательные значения амплитуды нолями

    convolve_size = sampling_frequency * convolve_coefficient
    convolved_channel1 = convolve_wav(channel1, convolve_size)

    significant_transitions = search_significant_transitions(convolved_channel1, search_transitions_parameter)
    frames_transitions = [convolve_size * x for x in significant_transitions]
    seconds_transitions = [x // sampling_frequency for x in frames_transitions]

    last_seconds_transition = number_of_frames // sampling_frequency
    seconds_transitions.append(last_seconds_transition)

    return seconds_transitions

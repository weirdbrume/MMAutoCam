import struct
import os
import random
import copy
from vmd_structures import Frame, Vmd, FRAME_SIZE, MAGIC_STRING_SIZE, \
    FRAMES_NUMBER_START, FRAMES_NUMBER_END, FILE_END, FRAME_END, CloseDistanceBuffer


def frame_from_bytes_frame(bytes_frame):
    """
    Функция принимает описание одного кадра из файла .vmd в виде
    байтов и возвращает описание в виде объекта Frame.

    :param bytes_frame: байтовое описание одного кадра из файла .vmd (bytes)
    :return frame: кадр в виде объекта Frame (<class 'Frame'>)
    """

    frame = Frame(
        number=struct.unpack('<I', bytes_frame[0:4])[0],
        cam_dist=struct.unpack('f', bytes_frame[4:8])[0],
        cam_pos_x=struct.unpack('f', bytes_frame[8:12])[0],
        cam_pos_y=struct.unpack('f', bytes_frame[12:16])[0],
        cam_pos_z=struct.unpack('f', bytes_frame[16:20])[0],
        cam_rot_x=struct.unpack('f', bytes_frame[20:24])[0],
        cam_rot_y=struct.unpack('f', bytes_frame[24:28])[0],
        cam_rot_z=struct.unpack('f', bytes_frame[28:32])[0]
    )

    return frame


def bytes_frame_from_frame(frame):
    """
    Функция принимает описание кадра в виде Frame и возвращает его байтовое представление.

    :param frame: кадр в виде Frame (class '<Frame>')
    :return: кадр в виде строки байт (bytes)
    """

    number = struct.pack('<I', frame.number)
    cam_dist = struct.pack('f', frame.cam_dist)
    cam_pos_x = struct.pack('f', frame.cam_pos_x)
    cam_pos_y = struct.pack('f', frame.cam_pos_y)
    cam_pos_z = struct.pack('f', frame.cam_pos_z)
    cam_rot_x = struct.pack('f', frame.cam_rot_x)
    cam_rot_y = struct.pack('f', frame.cam_rot_y)
    cam_rot_z = struct.pack('f', frame.cam_rot_z)
    end = FRAME_END

    return b''.join((number, cam_dist, cam_pos_x, cam_pos_y, cam_pos_z, cam_rot_x, cam_rot_y, cam_rot_z, end))


def frames_from_bytes_frames(bytes_frames):
    """
    Функция принимает описание кадров из файла .vmd в виде байтов
    и возвращает список кадров в виде объектов класса Frame/

    :param bytes_frames: байтовое описание всех кадров из файла .vmd (bytes)
    :return samples: список объектов класса Frame (list)
    """

    bytes_frames_size = len(bytes_frames)
    frame_size = FRAME_SIZE
    frame_left_border = 0
    frame_right_border = frame_size
    frames = []

    while frame_right_border <= bytes_frames_size:
        frames.append(frame_from_bytes_frame(bytes_frames[frame_left_border:frame_right_border]))
        frame_left_border = frame_right_border
        frame_right_border += frame_size

    return frames


def bytes_frames_from_frames(frames):
    """
    Функция принимает список кадров в виде объектов Frame
    и возвращает кадры в виде bytes.

    :param frames: список кадров (list)
    :return: кадры в виде строки байт (bytes)
    """

    return b''.join(map(bytes_frame_from_frame, frames))


def load_vmd_from_file(filename):
    """
    Загружает строку bytes из файла .vmd и возвращает объект класса Vmd
    :param filename: строка с именем файла (str)
    :return: объект класса Vmd
    """

    with open(filename, 'rb') as f:
        bytes_vmd = f.read()

    magic_string = bytes_vmd[0:MAGIC_STRING_SIZE]
    frames_number = struct.unpack('<I', bytes_vmd[FRAMES_NUMBER_START:FRAMES_NUMBER_END])[0]
    bytes_frames = bytes_vmd[FRAMES_NUMBER_END:len(bytes_vmd) - len(FILE_END)]
    frames = frames_from_bytes_frames(bytes_frames)

    return Vmd(magic_string, frames_number, frames)


def save_vmd_to_file(vmd, filename):
    """
    Сохраняет объект Vmd в файл.

    :param vmd: объект класса Vmd
    :param filename: строка с именем файла в который сохраняем наш объект
    """

    bytes_vmd = b''.join((vmd.magic_string, struct.pack('<I', vmd.frames_number),
                          bytes_frames_from_frames(vmd.frames), FILE_END))

    with open(filename, 'wb') as f:
        f.write(bytes_vmd)


def parse_cam_template_name(name):
    """
    Функция достает из имени шаблона камеры дистанцию и номер.
    Имена шаблонов камеры должны иметь вид: cam(первые 3 символа) дистанция(2 символа) номер(все оставшиеся символы).
    Например: camSR2 (дистанция - SR, номер шаблона - 2)

    :param name: имя шаблона камеры (str)
    :return: кортеж из дистанции (str) и номера (int)
    """

    try:
        distance = name[3:5]
        number = int(name[5:])
    except:
        print('!' * 70)
        print('Неправильное название шаблона камеры {}.vmd !'.format(name))
        print('Имена шаблонов камеры должны иметь вид:'
              ' cam(первые 3 символа) дистанция(2 символа) номер(все оставшиеся символы).')
        print('Пример правильного названия шаблона - camSR2 (дистанция - SR, номер шаблона - 2)')
        print('!' * 70)
    else:
        return distance, number


def load_cam_templates(dir_name):
    """
    Функция загружает шаблоны камеры из файлов шаблонов.

    :param dir_name: имя папки с шаблонами (str)
    :return: словарь с шаблонами вида {('дистанция шаблона', номер шаблона): <объект Vmd>, следующий шаблон и т.д}
    """

    cam_templates = {}

    for filename in os.listdir(dir_name):
        try:
            name, extension = filename.split('.')
        except ValueError:
            name, extension = None, None

        if extension == 'vmd':
            template_name = parse_cam_template_name(name)

            if template_name is not None:
                cam_templates[template_name] = load_vmd_from_file('{dir}\{file}'.format(dir=dir_name, file=filename))

    return cam_templates


def create_cam_template_sequence(cam_templates, seq_len):
    """
    Функция создает нужную для последующей обработки последовательность шаблонов камеры.

    Условия создания последовательности:
    "Значение камеры выбирается случайно, но нельзя ставить одни и те же значения два раза подряд,
    так же нельзя ставить подряд значения из одной и той же категории (дальней, средней) кроме ближней" (c)
    (условия описаны в файле "zapiskameri.png")
    Дополнительное условие: ближние значения не должны идти более двух раз подряд.

    :param cam_templates: словарь с шаблонами камеры (dict)
    :param seq_len: необходимая длина создаваемой последовательности (int)
    :return cam_template_sequence: последовательность шаблонов камеры (list)
    """

    cam_template_sequence = []
    close_distance_buffer = CloseDistanceBuffer('BL')

    last_template_name = random.sample(cam_templates.keys(), 1)[0]
    last_template_distance, last_template_number = last_template_name[0], last_template_name[1]
    last_template = cam_templates[last_template_name]

    cam_template_sequence.append(last_template)
    close_distance_buffer.append(last_template_distance)

    while len(cam_template_sequence) < seq_len:

        new_template_name = random.sample(cam_templates.keys(), 1)[0]
        new_template_distance, new_template_number = new_template_name[0], new_template_name[1]
        new_template = cam_templates[new_template_name]
        close_distance_buffer.append(new_template_distance)

        close_distance_and_different_numbers = last_template_distance == 'BL' \
                                               and new_template_distance == 'BL' \
                                               and last_template_number != new_template_number\
                                               and close_distance_buffer.is_not_filled()
        different_distance_and_numbers = last_template_distance != new_template_distance \
                                         and last_template_number != new_template_number

        if close_distance_and_different_numbers or different_distance_and_numbers:
            cam_template_sequence.append(new_template)
            last_template_distance, last_template_number = new_template_distance, new_template_number

    return cam_template_sequence


def wav_transitions_to_camera_frames_transitions(wav_transitions, fps):
    """
    Функция переводит переходы по секундам в wav файле в переходы по кадрам в генерируемой камере.

    :param wav_transitions: переходы в файле wav (list)
    :param fps: трбуемое количество кадров в секунду в создаваемой камере (int)
    :return: переходы в виде номеров кадров (list)
    """

    return [transition * fps for transition in wav_transitions]


def camera_transitions_to_frames_numbers(transitions):
    """
    Функция переводит переходы камеры по кадрам в номера кадров.

    :param transitions: список переходов камеры по кадрам (list)
    :return: список с номерами кадров для генерации камеры (list)
    """

    frames_numbers = [(transitions[0], transitions[1])]
    last_transition = len(transitions) - 1

    for i in range(1, last_transition):
        frames_numbers.append((transitions[i] + 1, transitions[i + 1]))

    return frames_numbers


def create_camera(templates_sequence, frames_numbers):
    """
    Функция создает камеру из последовательности шаблонов и списка номеров кадров.

    :param templates_sequence: последовательность шаблонов камеры (list)
    :param frames_numbers: номера кадров вида [(start_frame_number, end_frame_number), ...] (list)
    :return: камера (class '<Vmd>')
    """

    magic_string = templates_sequence[0].magic_string
    frames_number = len(frames_numbers) * len(templates_sequence[0].frames)
    frames = []

    sequence_length = len(templates_sequence)

    for i in range(sequence_length):
        start_frame, end_frame = copy.copy(templates_sequence[i].frames[0]), copy.copy(templates_sequence[i].frames[-1])
        start_frame.number, end_frame.number = frames_numbers[i][0], frames_numbers[i][-1]
        frames.extend([start_frame, end_frame])

    return Vmd(magic_string, frames_number, frames)

class Frame:

    def __init__(self, number, cam_dist, cam_pos_x, cam_pos_y, cam_pos_z, cam_rot_x, cam_rot_y, cam_rot_z):
        """
        Данный класс представляет собой один кадр загруженный из .vmd файла
        в виде структуры, удобной для работы с ним.

        :param number: номер кадра (int)
        :param cam_dist: расстояние до камеры (float)
        :param cam_pos_x: координата X позиции камеры (float)
        :param cam_pos_y: координата Y позиции камеры (float)
        :param cam_pos_z: координата Z позиции камеры (float)
        :param cam_rot_x: координата X поворота камеры (float)
        :param cam_rot_y: координата Y поворота камеры (float)
        :param cam_rot_z: координата Z поворота камеры (float)
        """

        # кадры считаются с 0, то есть у первого кадра номер ноль,
        # номер последнего = количество кадров - 1
        self.number = number
        self.cam_dist = cam_dist

        # порядок изменения координат примерно 50 единиц
        self.cam_pos_x = cam_pos_x
        self.cam_pos_y = cam_pos_y
        self.cam_pos_z = cam_pos_z

        # повороты в радианах от -2*pi до 2*pi
        # "-" - по часовой, "+" - против часовой стрелки
        self.cam_rot_x = cam_rot_x
        self.cam_rot_y = cam_rot_y
        self.cam_rot_z = cam_rot_z

    def __str__(self):
        text = '----------------------------------------\n' \
               'Номер кадра: {}\n' \
               'Расстояние до камеры: {}\n' \
               'Координата позиции камеры x: {}\n' \
               'Координата позиции камеры y: {}\n' \
               'Координата позиции камеры z: {}\n' \
               'Координата поворота камеры x: {}\n' \
               'Координата поворота камеры y: {}\n' \
               'Координата поворота камеры z: {}\n' \
               '----------------------------------------'
        return text.format(self.number, self.cam_dist, self.cam_pos_x, self.cam_pos_y,
                           self.cam_pos_z, self.cam_rot_x, self.cam_rot_y, self.cam_rot_z)


class Vmd:
    def __init__(self, magic_string, frames_number, frames):
        """
        Структура, для работы с кадрами из файла .vmd

        :param magic_string: с этого начинается файл .vmd (bytes)
        :param frames_number: количество кадров в файле (int)
        :param frames: список с кадрами в виде Frame (list)
        """

        self.magic_string = magic_string
        self.frames_number = frames_number
        self.frames = frames

    def show(self):
        """Печатает содержимое класса в stdout"""

        print('Количество кадров в файле:', self.frames_number)
        for frame in self.frames:
            print(frame)


class CloseDistanceBuffer:
    def __init__(self, close_distance_cam_name):
        """
        Вспомогательный класс для определения более 2-х повторов ближней камеры
        в функции vmd_functions.create_cam_template_sequence

        :param close_distance_cam_name: название дистанции камеры (str)
        """

        self.close_distance_cam_name = close_distance_cam_name
        self.close_distances = []
        self.max_close_distance_sequence = 2

    def append(self, distance):
        """
        Метод добавляет дистанцию камеры если она является ближней.

        :param distance: название дистанции камеры (str)
        """

        if distance == self.close_distance_cam_name:
            self.close_distances.append(distance)
        else:
            self.close_distances.clear()

    def is_not_filled(self):
        """
        Метод показывает заполнен ли буфер.

        :return: True если не заполнен, иначе False
        """

        return True if len(self.close_distances) <= self.max_close_distance_sequence else False


MAGIC_STRING = b'Vocaloid Motion Data 0002' \
                                b'\x00\x00\x00\x00\x00\x83J\x83\x81\x83\x89\x81E\x8f\xc6\x96\xbe\x00' \
                                b'on Data\x00\x00\x00\x00\x00\x00\x00\x00'  # .vmd начинается с чего то подобного :)
MAGIC_STRING_SIZE = 58  # отсюда начинается полезная инфа в файле
FRAMES_NUMBER_START = 58  # здесь начинается байтовое описание количества кадров в файле
FRAMES_NUMBER_END = 62  # здесь заканчивается байтовое описание количества кадров в файле
FRAME_SIZE = 61  # размер кадра в байтовом описании
FRAME_END = b'\x14k\x14k\x14k\x14k\x14k\x14k\x14k\x14k\x14k\x14k\x14k\x14k\x1e\x00\x00\x00\x00'  # каждый
#  кадр заканичвается так, в последних 4-х байтах записана перспектива, но нас она не интересует :)
FILE_END = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'  # так заканчивается файл .vmd

# настройки программы по умолчанию
CAMERA_TEMPLATES_DIR_NAME = 'camera_templates\\15_cam_templates'  # название папки с шаблонами камеры
FPS = 30  # количество кадров в секунду в создаваемой камере

from sys import argv
from os import path
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from gui import Ui_MainWindow
from wav_functions import get_wav_transitions
from vmd_structures import CAMERA_TEMPLATES_DIR_NAME, FPS
from vmd_functions import save_vmd_to_file, load_cam_templates, create_cam_template_sequence,\
    wav_transitions_to_camera_frames_transitions, camera_transitions_to_frames_numbers, create_camera


class AutoCamUi(QMainWindow, Ui_MainWindow):
    def __init__(self):
        """Класс главного окна программы."""

        super().__init__()
        self.setupUi(self)

        self.lineEdit_2.setText(path.abspath(CAMERA_TEMPLATES_DIR_NAME))

        self.error_dialog = QMessageBox(self)
        self.file_dialog = QFileDialog(self)

        self.pushButton_1.clicked.connect(self.set_wav_filename)
        self.pushButton_2.clicked.connect(self.set_cam_templates_dirname)
        self.pushButton_3.clicked.connect(self.create_auto_cam)

    def set_wav_filename(self):
        """Вызывает окно для выбора .wav файла и
        записывает путь к выбранному файлу в соответствующее поле.
        """

        wav_filename = self.file_dialog.getOpenFileName(self, 'Выбрать wav файл', filter='*.wav')[0]
        wav_filename = wav_filename.replace('/', '\\')
        self.lineEdit_1.setText(wav_filename)

    def set_cam_templates_dirname(self):
        """Вызывает окно для выбора папки с шаблонами камеры и
        записывает путь к выбранной папке в соответствующее поле.
        """

        start_templates_dir = path.abspath(CAMERA_TEMPLATES_DIR_NAME.split('\\')[0])
        templates_dir = self.file_dialog.getExistingDirectory(self, 'Выбрать папку с шаблонами камеры', directory=start_templates_dir)
        templates_dir = templates_dir.replace('/', '\\')
        self.lineEdit_2.setText(templates_dir)

    def get_wav_filename(self):
        """Возвращает путь к wav файлу (str)."""

        return self.lineEdit_1.text()

    def get_cam_templates_dirname(self):
        """Возвращает путь к папке с шаблонами (str)."""

        return self.lineEdit_2.text()

    def get_convolve_size_coefficient(self):
        """Возвращает коэффицент свертки массива сэмплов .wav файла (int)."""

        return int(self.doubleSpinBox_1.value())

    def get_transition_number_coefficient(self):
        """Возвращает коэффицент для поиска значимых переходов
         в массиве сэмплов .wav файла (int)."""

        return int(self.doubleSpinBox_2.value())

    def check_settings(self):
        """
        Проверяет заполнены ли поля wav файла и шаблонов камеры.
        Если поле не заполнено выводит сообщение об ошибке и возвращает False,
        если всё в порядке - возвращает True (bool).
        """

        if not self.lineEdit_1.text():
            self.error_dialog.setWindowTitle('Error!')
            self.error_dialog.setText('Не выбран wav файл :(')
            self.error_dialog.show()

            return False

        if not self.lineEdit_2.text():
            self.error_dialog.setWindowTitle('Error!')
            self.error_dialog.setText('Не выбрана папка с шаблонами камеры :(')
            self.error_dialog.show()

            return False

        return True

    def create_auto_cam(self):
        """
        Создает камеру в соответсвии с заданными настройками
        и сохраняет в выбранный пользователем файл.
        """

        if self.check_settings():

            wav_filename = self.get_wav_filename()
            camera_templates_dir_name = self.get_cam_templates_dirname()
            convolve_size_coefficient = self.get_convolve_size_coefficient()
            transitions_number_coefficient = self.get_transition_number_coefficient()

            wav_transitions = get_wav_transitions(wav_filename, convolve_size_coefficient, transitions_number_coefficient)
            cam_transitions = wav_transitions_to_camera_frames_transitions(wav_transitions, FPS)
            frames_numbers = camera_transitions_to_frames_numbers(cam_transitions)

            loaded_templates = load_cam_templates(camera_templates_dir_name)
            templates_sequence = create_cam_template_sequence(loaded_templates, len(frames_numbers))

            camera = create_camera(templates_sequence, frames_numbers)

            expected_camera_filename = '{}_camera.vmd'.format(wav_filename.split('.')[0])
            camera_file = self.file_dialog.getSaveFileName(self, directory=expected_camera_filename)[0]

            if camera_file:
                save_vmd_to_file(camera, camera_file)


def main():
    app = QApplication(argv)
    window = AutoCamUi()
    window.show()
    app.exec()


if __name__ == '__main__':
    main()

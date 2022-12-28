from pydub import AudioSegment
import face_recognition

import os


def voice_to_wav(filename, user_id, message_id):
    """Функция конвертации аудисообщения в wav формат с частотой 16kHz"""
    voice = AudioSegment.from_file(filename)
    # Установка частоты дескритизации 16kHz
    voice = voice.set_frame_rate(16000)
    voice.export(f'data/{user_id}/audio_message_{message_id}.wav', format='wav')
    del_file(filename)


def del_file(file):
    os.remove(file)


def find_face(image):
    """Функция распознования лиц на фото"""
    img = face_recognition.load_image_file(image)
    face_loc = face_recognition.face_locations(img)
    if face_loc:
        return 'Я нашел на этом фото 1 или более лиц, сохраняю это фото)'
    os.remove(image)
    return 'На этом фото нет лиц.'

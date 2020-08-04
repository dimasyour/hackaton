from vk_api.keyboard import VkKeyboard, VkKeyboardColor


def keyboard_start():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Мои баллы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('📒 Подобрать университет', VkKeyboardColor.POSITIVE)

    return keyboard.get_keyboard()


def keyboard_subject_1():
    keyboard = VkKeyboard(False)
    keyboard.add_button('Показать следующие предметы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🧮 Профильная математика', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🇷🇺 Русский язык', VkKeyboardColor.PRIMARY)
    keyboard.add_button('🏘 Обществознание', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('🧬 Биология', VkKeyboardColor.PRIMARY)
    keyboard.add_button('⚛ Физика', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📖 Вернуться назад', VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def keyboard_subject_2():
    keyboard = VkKeyboard(False)
    keyboard.add_button('Показать предыдущие предметы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('🏰 История', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('💻 Информатика', VkKeyboardColor.PRIMARY)
    keyboard.add_button('🧪 Химия', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📝 Литература', VkKeyboardColor.PRIMARY)
    keyboard.add_button('🗺 География', VkKeyboardColor.PRIMARY)
    keyboard.add_line()
    keyboard.add_button('📖 Вернуться назад', VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()


def keyboard_add_ball():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Добавить баллы', VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('📖 Вернуться назад', VkKeyboardColor.NEGATIVE)

    return keyboard.get_keyboard()


def keyboard_insert_ball():
    keyboard = VkKeyboard(False)
    keyboard.add_button('📖 Удалить баллы по этому предмету', VkKeyboardColor.DEFAULT)
    keyboard.add_line()
    keyboard.add_button('📖 Назад к выбору предмета', VkKeyboardColor.NEGATIVE)
    return keyboard.get_keyboard()

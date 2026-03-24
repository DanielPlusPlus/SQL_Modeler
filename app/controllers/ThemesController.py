import os
from app.enums.ThemesEnum import ThemesEnum


class ThemesController:
    def __init__(self, app):
        self.__app = app
        self.__themes = ("app\\themes\\default.qss", "app\\themes\\darkTheme.qss")
        self.changeTheme(ThemesEnum.LIGHT)

    def changeTheme(self, ThemesEn):
        print(self.__themes[ThemesEn.value - 1])
        if not os.path.exists(self.__themes[ThemesEn.value - 1]):
            return
        with open(self.__themes[ThemesEn.value - 1], "r", encoding="utf-8") as theme:
            qss = theme.read()
        self.__app.setStyleSheet(qss)

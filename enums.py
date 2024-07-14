from enum import Enum


class PlaylistType(Enum):
    Top10 = '🔝 Топ-10'
    Top20 = '🔝 Топ-20'
    New = '🆕 Новые'
    Chronology = '⏳ Все ответы по хронологии'
    Rating = '❤️ Все ответы по рейтингу'

    @staticmethod
    def from_value(value):
        for item in PlaylistType:
            if item.value == value:
                return item
        return None


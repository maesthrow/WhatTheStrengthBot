import hashlib

from mongo_db.mongo import db


async def get_entities_collection():
    entities_collection = db["entities"]
    return entities_collection


async def has_entity(name: str) -> bool:
    entity_document = await get_entity_data(name)
    return entity_document is not None


async def add_entity(name: str, mentions: int = 1):
    """Добавляет сущность ответа в базу данных, если ее не существует."""
    entities_collection = db["entities"]
    name = name.lower()
    entity_id = hashlib.md5(name)
    entity__document = entities_collection.find_one({"_id": entity_id})
    if not entity__document:
        entity_data = {
            "_id": entity_id,
            "name": name,
            "mentions": mentions,
        }
        try:
            print(f"Запись сущности ответа '{name}' в базу данных:")
            entities_collection.insert_one(entity_data)
            print("Успешно")
        except Exception as e:
            print(f"Ошибка при добавлении сущности ответа '{name}' в базу данных:", e)


async def get_entity_data(name: str):
    """Возвращает данные пользователя по его идентификатору."""
    entities_collection = db["entities"]
    entity_document = entities_collection.find_one({"_id": hashlib.md5(name.lower())})
    return entity_document


async def set_entity_data(name: str, data: dict):
    """Обновляет данные пользователя."""
    entities_collection = db["entities"]
    entities_collection.update_one({"_id": hashlib.md5(name.lower())}, {"$set": data})


async def update_entity_data(name: str, data):
    """Обновляет выборочно данные пользователя."""
    entities_collection = db["entities"]
    entity_document = entities_collection.find_one({"_id": hashlib.md5(name.lower())})
    for key in data.keys():
        entity_document[key] = data[key]
    entities_collection.update_one({"_id": hashlib.md5(name.lower())}, {"$set": entity_document})

from db.io.prints import system_print, error_print


class Honey:
    __honey_dict = {}

    __honey_1 = {"id": 1, "name": "липовый", "info": "some info1", "price": 250}
    __honey_2 = {"id": 2, "name": "цветочный", "info": "some info2", "price": 250}
    __honey_3 = {"id": 3, "name": "гречичный", "info": "some info3", "price": 250}

    __honey_list = [__honey_1, __honey_2, __honey_3]

    for honey in __honey_list:
        __honey_dict[honey["id"]] = honey

    def get_all_honey(self):
        return self.__honey_dict

    def get_honey_info_by_id(self, honey_id):
        if honey_id in self.__honey_dict:
            return self.__honey_dict[honey_id]
        else:
            error_print(f"меда с id: {honey_id} нет")


honey = Honey()

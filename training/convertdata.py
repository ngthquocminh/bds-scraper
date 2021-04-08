import pymongo
import re
import json


class PointAnno:
    def __init__(self, value_str):
        self.start: int = 0
        self.end: int = 0
        self.text: str = value_str


class LabelAnno:
    def __init__(self, label, point):
        self.label: list = label if isinstance(label, list) else [str(label)]
        self.points: [PointAnno] = point if isinstance(point, list) else [point]

    def toDict(self):
        return {"label": self.label, "points": [self.points[0].__dict__]}


class PostAnno:
    def __init__(self):
        self.content: str = ""
        self.annotation: list = []
        self.extras = None
        self.meta_data: dict = {}

    def addLabel(self, label_anno):
        if isinstance(label_anno, LabelAnno):
            self.content += " " if len(self.content) > 0 else ""
            label_anno.points[0].start = len(self.content)

            self.content += label_anno.points[0].text
            label_anno.points[0].end = len(self.content)

            self.annotation.append(label_anno.toDict())

    def toDict(self):
        return {
            "content": self.content,
            "annotation": self.annotation,
            "extras": self.extras,
            "meta_data": self.meta_data
        }


_re = lambda r, v, l: re.compile(r).match(str(v)) and len(str(v)) >= l


def check_validate(key, value):
    if value is None or ("<eof>" in str(value)) or len(str(value)) < 1:
        return False

    # if key == "price":
    #     return _re(r'[0-9]+', value, 3)
    #
    # if key == "front":
    #     return _re(r'[0-9]+', value, 2)
    #
    # if key == "surface":
    #     return _re(r'[0-9]+', value, 2)
    #
    # if key == "room":
    #     return _re(r'[0-9]+', value, 1)
    #
    # if key == "floor":
    #     return _re(r'[0-9]+', value, 1)
    #
    # # if key == "title":
    # #     return len(str(value)) >= 20
    #
    # if key == "date":
    #     return len(str(value)) >= 5
    #
    # if key == "phone":
    #     return _re(r"0|\+84[0-9]+", value.replace(" ", ""), 9)
    #
    # if key == "email":
    #     return _re(r"[a-zA-Z0-9.]+@[a-zA-Z0-9.]+.[a-z]+", value.replace(" ", ""), 9)
    #
    # # if key == "address":
    # #     return len(str(value)) >= 10
    #
    # if key == "category":
    #     return len(str(value)) >= 3
    #
    if key == "description":
        return len(str(value)) >= 50
    #
    # if key == "user":
    #     return len(str(value)) >= 2

    return False


def changekey(key):
    if key == "surface":
        return "area"
    if key == "user":
        return "saller"
    if key == "room":
        return "rooms"
    if key == "floor":
        return "floors"
    if key == "category":
        return "type"

    return key


def changevalue(key, value):
    if key == "surface":
        return "Điện tích " + value
    if key == "user":
        return "Tên liên hệ: " + value
    if key == "room":
        return "Số phòng " + value
    if key == "floor":
        return "Số tầng " + value
    if key == "category":
        return "Loại tin " + value
    if key == "front":
        return "Mặt tiền " + value
    if key == "price":
        return "Giá " + value

    return value


def new_attr():
    """"""


def getDataCosmos() -> list:
    import os, sys, inspect
    current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    parent_dir = os.path.dirname(current_dir)
    sys.path.insert(0, parent_dir)
    from database import AzureCosmos

    myclient = AzureCosmos()
    mydoc = myclient.getAll()

    return mydoc


def getDataLocal() -> list:
    file_name = "../data_parsed0.json"
    f = open(file_name, "r")
    mydoc = f.readlines()

    mydoc = [json.loads(i.replace("\n", "") if i[-1] is "\n" else i) for i in mydoc]

    return mydoc


def main():
    mydoc = getDataLocal()
    # mydoc = getDataCosmos()

    index = 0

    with open("traindata_3.json", "a") as myfile:
        for post in mydoc:
            # print(post)
            print("\n", "-" * 100, "\n", index, " - ", post["url"])

            post_anno = PostAnno()

            detail = post["detail"]
            # print(detail)
            i = 0
            for key in detail:
                value = detail[key]
                if check_validate(key, value):
                    i += 1
                    value = changevalue(key, value)
                    key = changekey(key)
                    print(i, ". ", key, ": ", value)
                    label_str = key
                    point_anno = PointAnno(value)
                    label_anno = LabelAnno(label_str, point_anno)
                    post_anno.addLabel(label_anno)

            post_anno_json = json.dumps(post_anno.__dict__)
            print(post_anno_json)
            myfile.write(post_anno_json + "\n")

            index += 1
            if index > 99999:
                break


if __name__ == "__main__":
    main()

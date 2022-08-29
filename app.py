import os

from flask import Flask, request, jsonify
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def do_cmd(cmd, value, data) -> list:
    if cmd == "filter":
        result = filter(lambda record: value in record, data)
    elif cmd == "map":
        colum_num = int(value)
        result = map(lambda record: record.split()[colum_num], data)
    elif cmd == "unique":
        result = set(data)
    elif cmd == "sort":
        reverse = value == "desc"
        result = sorted(data, reverse=reverse)
    elif cmd == "limit":
        result = data[:int(value)]
    else:
        raise BadRequest
    return list(result)


def do_query(params) -> list:
    with open(os.path.join(DATA_DIR, params["file_name"])) as file:
        file_data = file.readlines()
    res = file_data
    
    if "cmd1" in params.keys():
        res = do_cmd(params["cmd1"], params["value1"], res)
    if "cmd2" in params.keys():
        res = do_cmd(params["cmd2"], params["value2"], res)
    if "cmd3" in params.keys():
        res = do_cmd(params["cmd3"], params["value3"], res)
    return res


@app.route("/perform_query", methods=["POST"])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    data = request.json

    if not os.path.exists(os.path.join(DATA_DIR, data["file_name"])):
        raise BadRequest

    return jsonify(do_query(data))


if __name__ == "__main__":
    app.run(port=3090)

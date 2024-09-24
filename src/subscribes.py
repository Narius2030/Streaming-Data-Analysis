import json
from datetime import date


def write_json_logs(message, path):
    ## TODO: write data into json
    for _, datas in message.items():
        try:
            for data in datas:
                value = data.value.decode('utf-8')
                value = json.loads(value)
                with open(f"{path}/{value['type']}_{date.today()}_{value['page']}.json", "w", encoding="utf-8") as file:
                    json.dump(value, file, indent=4)
        except Exception as exc:
            raise Exception(str(exc))
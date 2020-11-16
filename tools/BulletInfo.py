import json


def get_bullet_info(bullet_name: str) -> dict:
    with open("../data/bullet.json", "r") as f:
        data = json.load(f)
        return data[bullet_name]


if __name__ == '__main__':
    info = get_bullet_info("AP")
    print(info)

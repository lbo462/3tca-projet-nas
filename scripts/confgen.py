import json


def main():
    with open("bb_config.json", "r") as f:
        raw_file = f.read()
    conf_dict = json.loads(raw_file)

    for r in conf_dict["backbone_devices"]:
        id_ = r['id']
        for l in r['bb_links']:
            bid = max(id_, l)
            lid = min(id_, l)

            personal_bit = 1
            if r["id"] == bid:
                personal_bit = 2
            address = f"{int(bid / 255)}.{bid%255}.{lid%255}.{(int(lid/255) << 2) + personal_bit}"
            print(address)

    

        print("#############")


if __name__ == "__main__":
    main()


import uuid


def generate_unique_link_id():
    link_id_as_str = str(uuid.uuid4())
    shortened_link_id = link_id_as_str[:8]

    return shortened_link_id


def main():
    print(generate_unique_link_id())


if __name__ == "__main__":
    main()

from urllib_example.crawler import do_request


def print_hi(name):
    print(f'Hi, {name}')

    if __name__ == '__main__':
        do_request(is_write=False, if_proxy=True)


if __name__ == '__main__':
    print_hi('Request!')

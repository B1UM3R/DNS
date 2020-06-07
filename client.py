import socket
from parser.constants import RecordTypes
from parser.parsers import parse_answers
from parser.common_parsers import str_to_hex, domain_to_bytes_str
import argparse


def insert_info_into_request(domain, q_type):
    return "4a 4a 01 00 00 01 00 00 00 00 00 00 {} 00 {} 00 01".format(domain_to_bytes_str(domain),
                                                                       RecordTypes.get_hex_str_form_str(q_type))


class Client:
    def __init__(self, q_name, q_type):
        if q_type not in RecordTypes.ValidRequestType:
            raise ValueError("Invalid type value")
        self.data = str_to_hex(insert_info_into_request(q_name, q_type))
        self.address = "127.0.0.1"
        self.port = 53
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(self.data, (self.address, self.port))
            data, sender = s.recvfrom(256)
            answer = parse_answers(data)
            print(answer)


def main():
    parser = argparse.ArgumentParser(
        description='КЭШИРУЮЩИЙ ДНС СЕРВЕР. Сервер прослушивает 53 порт. При первом запуске кэш пустой. Сервер '
                    'получает от клиента '
                    'рекурсивный запрос и выполняет разрешение запроса. Получив ответ, сервер разбирает пакет '
                    'ответа, извлекает из него ВСЮ полезную информацию, т. е. все ресурсные записи, а не только то, '
                    'о чем спрашивал клиент. Полученная информация сохраняется в кэше сервера. Пример запуска: '
                    'python3 client.py e1.ru A.... Шершнев Павел КН-202(МЕН-280207)')
    parser.add_argument("domain", help="Домейн, по которому будем искать")
    parser.add_argument("type", default="A", help="Тип записи: A, AAAA, NS, TXT, MX")
    args = parser.parse_args()
    Client(args.domain, args.type)


if __name__ == "__main__":
    main()

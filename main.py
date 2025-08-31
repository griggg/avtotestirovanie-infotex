import argparse
import asyncio
import sys

from ping import HttpPing
from stats import HttpPingStats
from printers import StatPrinterConsole, StatPrinterFile

import re

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP Ping Tool")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-H", "--hosts",
                       help="Список хостов через запятую без пробелов")
    group.add_argument("-F", "--file",
                       help="Файл или список файлов с хостами через запятую без пробелов")

    parser.add_argument("-C", "--count", type=int, default=1,
                        help="Количество запросов на каждый хост (по умолчанию 1)")

    parser.add_argument("-O", "--output-file", help="Файл для записи статистики (если указан, сохраняется в файл)")

    return parser.parse_args()


def read_hosts_from_files(file_list_str: str):
    files = file_list_str.split(',')
    hosts = []
    for file_path in files:
        try:
            with open(file_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        hosts.append(line)
        except FileNotFoundError:
            print(f"Файл не найден: {file_path}")
        except IOError as e:
            print(f"Error reading file {file_path}: {e}")
        except Exception as e:
            print(f"Unexpected error with file {file_path}: {e}")

    return hosts


def is_valid_url(url: str) -> bool:
    pattern = r'^(https?://)'   
    pattern += r'('
    pattern += r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}'  # доменное имя
    pattern += r'|'
    pattern += r'localhost'  # localhost
    pattern += r'|'
    pattern += r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'  # IPv4
    pattern += r')'
    pattern += r'(:\d+)?'  # порт (опционально)
    pattern += r'(/.*)?$'  # путь (опционально)

    return re.match(pattern, url, re.IGNORECASE) is not None

def main():
    args = parse_args()

    if args.hosts:
        hosts = args.hosts.split(',')
    else:
        hosts = read_hosts_from_files(args.file)

    validated_hosts = []
    for i in hosts:
        if is_valid_url(i):
            validated_hosts.append(i)
        else:
            print(f"[Warning] Некорректный URL: {i} не будет использован")
    hosts = validated_hosts

    if not hosts:
        print("Список хостов пуст")
        sys.exit(1)

    count = args.count
    if count < 1:
        print(f"Ошибка. count не может быть меньше единицы. {count=}")
        sys.exit(1)

    stats = HttpPingStats()
    ping = HttpPing(stats)
    asyncio.run(ping.ping(hosts, count))

    if args.output_file:
        printer = StatPrinterFile(args.output_file)
    else:
        printer = StatPrinterConsole()

    printer.print_summary(stats)

if __name__ == '__main__':
    main()

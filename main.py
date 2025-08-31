import argparse
import asyncio
from ping import HttpPing
from stats import HttpPingStats
from printers import StatPrinterConsole, StatPrinterFile  # предположим, что принтеры в файле printers.py


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
    return hosts


def main():
    args = parse_args()

    if args.hosts:
        hosts = args.hosts.split(',')
    else:
        hosts = read_hosts_from_files(args.file)

    if not hosts:
        print("Не удалось получить список хостов.")
        return

    count = args.count

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

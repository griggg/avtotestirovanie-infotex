import argparse
import asyncio
from ping import HttpPing
from stats import HttpPingStats

def parse_args():
    parser = argparse.ArgumentParser(description="HTTP Ping Tool")
    parser.add_argument("-H", "--hosts", required=True,
                        help="Список хостов через запятую без пробелов")
    parser.add_argument("-C", "--count", type=int, default=1,
                        help="Количество запросов на каждый хост (по умолчанию 1)")
    return parser.parse_args()

def main():
    args = parse_args()
    hosts = args.hosts.split(',')
    count = args.count

    stats = HttpPingStats()
    ping = HttpPing(stats)
    asyncio.run(ping.ping(hosts, count))
    stats.print_summary()

if __name__ == '__main__':
    main()

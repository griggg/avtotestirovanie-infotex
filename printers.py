from stats import HttpPingStats



class StatPrinterFile:
    def __init__(self, filename: str = "output.txt"):
        self.filename = filename

    def print_summary(self, stats: HttpPingStats):
        summary = stats.get_summary()

        try:
            with open(self.filename, 'w') as f:
                f.write("\n--- Статистика по каждому хосту ---\n\n")
                for stat in summary:
                    f.write(f"Host    : {stat.host}\n")
                    f.write(f"  Success: {stat.success}\n")
                    f.write(f"  Failed : {stat.failed}\n")
                    f.write(f"  Errors : {stat.errors}\n")
                    f.write(f"  Min    : {stat.min:.4f} sec\n")
                    f.write(f"  Max    : {stat.max:.4f} sec\n")
                    f.write(f"  Avg    : {stat.avg:.4f} sec\n\n")
        except OSError:
            print(f"[Ошибка] Не удалось записать в файл {self.filename}")



class StatPrinterConsole:
    def print_summary(self, stats: HttpPingStats):
        summary = stats.get_summary()

        print("\n--- Статистика по каждому хосту ---\n")
        for stat in summary:
            print(f"Host    : {stat.host}")
            print(f"  Success: {stat.success}")
            print(f"  Failed : {stat.failed}")
            print(f"  Errors : {stat.errors}")
            print(f"  Min    : {stat.min:.4f} sec")
            print(f"  Max    : {stat.max:.4f} sec")
            print(f"  Avg    : {stat.avg:.4f} sec\n")

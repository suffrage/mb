import sys
from pathlib import Path
from colorclass import Color, Windows
from terminaltables import SingleTable


class ParseLog(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = {}

    def print_avg_metric_info(self):
        self.data = self.read_file()
        self.print_avg_time_metrics_by_events()
        self.print_avg_time_table_by_events()

    def __check_exists(self):
        log_file = Path(self.file_path)
        if not log_file.is_file():
            print("Log file does not exists", file=sys.stderr)
            sys.exit(1)

    def read_file(self):
        self.__check_exists()
        with open(self.file_path, 'r') as f:
            lines = f.readlines()

        parse_stat = next_header = False

        data = {"events": {}}

        for line in lines:
            line = line.rstrip()
            if parse_stat:
                if "Statistics gathering stopped" in line:
                    parse_stat = False
                    continue
                parsed_data = line.split(('\t'))
                data['events'].setdefault(parsed_data[event_key_id], [])
                data['events'][parsed_data[event_key_id]].append(int(parsed_data[avg_time]))
            if not parse_stat and not next_header:
                if "Statistics gathering started" in line:
                    next_header = True
                    continue
            if next_header and not parse_stat:
                next_header, parse_stat = False, True
                data['keys'] = line.split(('\t'))
                event_key_id = data['keys'].index('EVENT')
                avg_time = data['keys'].index('AVGTSMR')
                continue

        return data

    def print_avg_time_metrics_by_events(self):
        for event, avg_time_list in self.data['events'].items():
            avg_time_list = sorted(avg_time_list)
            avg_time_list_len = len(avg_time_list)
            min_avg_time, max_avg_time = avg_time_list[0], avg_time_list[-1]
            output = "{} min={} 50%={} 90%={} 99%={} 99.9%={}".format(
                event,
                min_avg_time,
                avg_time_list[int(avg_time_list_len * 0.5)],
                avg_time_list[int(avg_time_list_len * 0.9)],
                avg_time_list[int(avg_time_list_len * 0.99)],
                avg_time_list[int(avg_time_list_len * 0.999)]
            )
            print(output)

    @staticmethod
    def choose_color(min, iter):
        if min * 1.3 >= iter:
            return "autogreen"
        elif min * 1.6 >= iter:
            return "autoyellow"
        else:
            return "autored"

    def print_avg_time_table_by_events(self):
        for event, avg_time_list in self.data['events'].items():
            avg_time_list = sorted(avg_time_list)
            avg_time_list_len = len(avg_time_list)
            min_avg_time, max_avg_time = avg_time_list[0], avg_time_list[-1]

            table_data = [['ExecTime', 'TransNo', 'Weight,%', 'Percent']]
            iter_time = min_avg_time + 5 - (min_avg_time % 5)
            i = 0

            while iter_time < max_avg_time + 5:
                iter_count = 0
                while avg_time_list[i] <= iter_time :
                    iter_count += 1
                    i += 1
                    if i == avg_time_list_len:
                        i -= 1
                        break
                if iter_count != 0:
                    weight = (iter_count + 1) * 100 / avg_time_list_len
                    percent = (i + 1) * 100 / avg_time_list_len
                    color = self.choose_color(min_avg_time, iter_time)
                    table_data.append(
                        [
                            Color('{{{}}}{: > 10}{{/{}}}'.format(color, iter_time, color)),
                            "{: > 10}".format(iter_count),
                            "{: 10.3f}".format(weight),
                            "{: 10.4f}".format(percent)
                        ])
                iter_time += 5

            table_instance = SingleTable(table_data)

            print(table_instance.table)

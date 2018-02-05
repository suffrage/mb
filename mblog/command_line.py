import argparse


from mblog.core import ParseLog



def main():
    parser = argparse.ArgumentParser(description='Log parser')
    parser.add_argument('-f', action='store', dest='file', type=str, required=True)

    args = parser.parse_args()

    parseLog = ParseLog(file_path=args.file)
    parseLog.print_avg_metric_info()


if __name__ == "__main__":
    main()


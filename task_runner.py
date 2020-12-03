import argparse
import subprocess
import sys


def command_test(_):
    assert subprocess.call("pip install ./", shell=True) == 0
    proc = subprocess.Popen(["pytest", "--color=yes"], stdout=subprocess.PIPE)
    (stdout, _) = proc.communicate()
    sys.stderr.write(stdout.decode())


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    test_parser = subparsers.add_parser("test")
    test_parser.set_defaults(handler=command_test)

    args = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        # 未知のサブコマンドの場合はヘルプを表示
        parser.print_help()


if __name__ == "__main__":
    main()

'''
https://docs.python.org/zh-cn/3/library/argparse.html
'''
import argparse
from . import validation
from . import color_theme_analyse as _start


def run():
    """ Module entry point """
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--choice",
        type=int,
        default=0,
        const=1,
        nargs='?',
        help="选择命令"
    )
    args = parser.parse_args()
    _start.Menu(choice=args.choice)


if __name__ == '__main__':
    run()

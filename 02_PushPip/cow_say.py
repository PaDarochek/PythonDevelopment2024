import cowsay
import argparse
import sys

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cow', default='default', type=str)
    parser.add_argument('-e', '--eyes', default=cowsay.Option.eyes)
    parser.add_argument('-T', '--tongue', default=cowsay.Option.tongue)
    parser.add_argument('-W', '--width', default=40, type=int)
    parser.add_argument('-n', '--wraptext', default=True, type=bool)
    parser.add_argument('-f', '--cowfile', default=None)
    parser.add_argument('-l', '--list', action='store_true')
    parser.add_argument('-b', dest='preset', action='store_const', const='b')
    parser.add_argument('-g', dest='preset', action='store_const', const='g')
    parser.add_argument('-p', dest='preset', action='store_const', const='p')
    parser.add_argument('-s', dest='preset', action='store_const', const='s')
    parser.add_argument('-t', dest='preset', action='store_const', const='t')
    parser.add_argument('-w', dest='preset', action='store_const', const='w')
    parser.add_argument('-y', dest='preset', action='store_const', const='y')

    args = parser.parse_args()
    if args.list:
        print(', '.join(cowsay.list_cows()))
        exit(0)

    message = '\n'.join(sys.stdin.readlines())

    print(cowsay.cowsay(message, cow=args.cow, preset=args.preset, eyes=args.eyes, tongue=args.tongue, width=args.width,
                  wrap_text=args.wraptext, cowfile=args.cowfile))

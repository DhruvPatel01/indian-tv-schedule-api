import sys
import argparse
from datetime import date

if __name__ == '__main__':
    aparser = argparse.ArgumentParser()
    aparser.add_argument('--create', help="Create the list of channels available", action="store_true")
    aparser.add_argument('-c', '--channel', help="Show the schedule for this channel")
    aparser.add_argument('-d', '--date', help="Schedule for this date. format YYYY-MM-DD. defaults to today")
    aparser.add_argument('-m','--meta', help='Include meta data of show like genre, language, type in output',
                         action='store_true')
    aparser.add_argument('-D', '--details', help='Include extra details of show in output.',
                         action='store_true')
    aparser.add_argument('-i', '--indent', help="Prettify output json with i indents. use -1 to compact",type=int,default=2)
    args = aparser.parse_args()
    if not args.create and not args.channel:
        aparser.error('Either --channel or --create is necessary')
    if args.channel and args.create:
        aparser.error('Use  only --channel or --create')
    if args.create:
        import channel_list_parser
        print(channel_list_parser.create_list(False, categorize=True))
        exit()

    if args.channel:
        import parser
        if args.indent == -1:
            indent = None
        else:
            indent = args.indent

        if args.date:
            date = date(*[int(a) for a in args.date.split('-')])
            if not date:
                raise ValueError('Invalid date')
        else:
            date = date.today()
        print(parser.get_show_list(args.channel, date, args.meta, args.details, indent))
#!/usr/bin/env python3
import argparse
from plotly import subplots
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="Flipper file plotter by ShotokanZH")
    parser.add_argument(
        "fname", help=".sub file(s) to be plotted", type=str, nargs="+")
    parser.add_argument(
        "--outfile", help="Out file (.html), defaults to 'out.html'", type=str, default="out.html")
    args = parser.parse_args()
    try:
        fig = subplots.make_subplots()
        for fname in args.fname:
            with open(fname, "r") as f:
                y = []
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.startswith("RAW_Data: "):
                        for d in line.split(" ")[1:]:
                            d = int(d)
                            y.append(d)
                fig.append_trace(dict(x=list(range(0, len(y))), y=y,
                                      mode='lines', name=fname), 1, 1)

        fig.update_layout(title_text='FLIPPER DATA')
        fig.update_layout(template='plotly_dark', uirevision='amirich')
        fig.write_html(args.outfile)
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(locals())
        print("ERROR:", e)
        print(exc_type, fname, exc_tb.tb_lineno)


if __name__ == '__main__':
    main()

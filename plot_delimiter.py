#!/usr/bin/env python3
import argparse
from plotly import subplots
import sys
import os


def main():
    parser = argparse.ArgumentParser(description="Flipper file plotter with delimiter by ShotokanZH")
    parser.add_argument(
        "fname", help=".sub file(s) to be plotted", type=str, nargs="+")
    parser.add_argument(
        "--delimiter", help="A specific delimiter (Y coordinates) that splits the sequence in chunks (a very low/high value?)", type=int, required=True)
    parser.add_argument(
        "--zero", help="Y coordinates, draws a line and defines values around it as 0 (it's fancy) (requires --one)", type=int)
    parser.add_argument(
        "--one", help="Y coordinates, draws a line and defines values around it as 1 (it's fancy) (requires --zero)", type=int)
    parser.add_argument(
        "--outfile", help="Out file (.html), defaults to 'out.html'", type=str, default="out.html")
    args = parser.parse_args()

    if (args.one or args.zero) and not (args.one and args.zero):
        parser.error("--one requires --zero and vice-versa!")

    try:
        delimiter = args.delimiter
        delimiters = []
        ylist = []
        for f in args.fname:
            with open(f, "r") as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if line.startswith("RAW_Data: "):
                        for d in line.split(" ")[1:]:
                            try:
                                d = int(d)
                                ylist.append(d)
                            except ValueError:
                                continue
                            if delimiter <= 0:
                                if d <= delimiter:
                                    delimiters.append(len(ylist) - 1)
                            elif d >= delimiter:
                                delimiters.append(len(ylist) - 1)

        differences = {}
        for x in range(0, len(delimiters) - 1):
            diff = delimiters[x+1] - delimiters[x]
            if not diff in differences:
                differences[diff] = 1
            else:
                differences[diff] += 1

        distance = 0
        maxnum = 0
        for dd in differences:
            if differences[dd] > maxnum:
                maxnum = differences[dd]
                distance = dd

        if maxnum <= 1:
            print("Sequence not found!")
            exit()

        print(f"{len(ylist)=} {distance=} {maxnum=}")

        chunks = []
        for x in range(0, len(delimiters)):
            d = delimiters[x]
            if d < distance:
                continue
            if x > 0:
                if delimiters[x] - delimiters[x-1] != distance:
                    continue
            chunks.append(ylist[d-distance:d+1])

        if args.one and args.zero:
            zodiff = abs((args.one - args.zero) / 2)

        fig = subplots.make_subplots()

        title = f"{', '.join(args.fname)} / {delimiter=}"
        dottedline = dict(width=1, dash='dot')

        if args.one and args.zero:
            one = abs(args.one)
            zero = abs(args.zero)
            limits = [zero, one]
            for bit in [0, 1]:
                fig.append_trace(dict(x=[0, distance], y=[limits[bit], limits[bit]],
                                      mode='lines', name=f"HI - {bit}", line=dottedline), 1, 1)
                fig.append_trace(dict(x=[0, distance], y=[-limits[bit], -limits[bit]],
                                      mode='lines', name=f"LO - {bit}", line=dottedline), 1, 1)
            title += f" / one=±{one} / zero=±{zero}"

        fig.append_trace(dict(x=[0, distance], y=[delimiter, delimiter],
                              mode='lines', name=f"DELIMITER", line=dottedline), 1, 1)

        for i in range(0, len(chunks)):
            labels = []
            if args.one and args.zero:
                for x in chunks[i]:
                    val = abs(x)
                    if val > args.one - zodiff and val < args.one + zodiff:
                        labels.append("1")
                    elif val > args.zero - zodiff and val < args.zero + zodiff:
                        labels.append("0")
                    else:
                        labels.append('')
                print(f"Sequence {i}:", ''.join(labels))
            fig.append_trace(dict(x=list(range(0, len(chunks[i]))), y=list(chunks[i]),
                                  mode='lines', name=f"{i}", text=labels, textposition="top center"), 1, 1)

        fig.update_layout(title_text=title)
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

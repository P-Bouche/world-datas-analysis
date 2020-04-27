#!/usr/bin/python
import os
import sys
import csv

import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from tabulate import tabulate

# Set pandas options
pd.set_option('mode.chained_assignment', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

# Argument options
ap = argparse.ArgumentParser()
ap.add_argument("--input",  type=str, help="filename")
ap.add_argument("--block-by", type=str,
                help="block by column")

# Output
ap.add_argument("--format", choices=['gnuplot'],
                help="Format output file", default='gnuplot')
ap.add_argument("--output", type=str,
                help="output filename")
args = vars(ap.parse_args())


# Read data]:
df = pd.read_csv(args['input'], sep=",")


# Save
if args['output']:
    if args['format'] == 'gnuplot':
        # Fill missing value
        df = df.fillna("?")
        # df = df.rename({df.columns[0]: f'# {df.columns[0]}'}, axis=1)

        with open(args['output'], 'w') as f:
            group_by_columns = args['block_by'].split(',')
            g = df.groupby(group_by_columns)

            lastcolumn = list(g.groups)[-1]

            for groupname, items in g:
                # Quoting string content contains a space
                for column in items.columns:
                    if items[column].dtype == object:
                        mask = items[column].astype(str).str.contains(" ")
                        items[column][mask] = '"' + items[column][mask] + '"'

                text = tabulate(
                    items,
                    headers=items.columns,
                    floatfmt=".6f",
                    showindex="never",
                    tablefmt='plain'
                )

                # Show comments
                f.write(f"# {group_by_columns[0]}={groupname}\n")
                # Write datas
                f.write(text)

                if groupname != lastcolumn:
                    f.write("\n\n\n")
else:
    print(df)

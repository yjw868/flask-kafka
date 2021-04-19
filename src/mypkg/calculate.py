# from flask import Flask
# from flask import request
# from flask import jsonify
# import json
from io import StringIO
import pandas as pd
import numpy as np
import re


def parse(x):
    """
	The parser of pairs
	"""

    y = re.search("\((.*),(.*)\)", x).group(1, 2)

    if y:
        return y[0], y[1]

    return None, None


def parse_number(x):
    """
	Accept int and float only
	"""

    try:
        y = re.match("^\((\d*\.?\d*),(\d*\.?\d*)\),?$", x).group(1, 2)

        if y:
            return y[0], y[1]
    except AttributeError:
        return None, None


def catch(func, handle=lambda e: e, show_err=True, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if not show_err:
            return handle(e)
        else:
            pass


def convt_float(x):
    try:
        return float(x[0]), float(x[1])
    except ValueError:
        return False


def filter_input(x):
    """
	Turn list of tuple to 2 den df
	Filter out None from the raw input
	Convert each column to number
	Return numpy array
	"""

    df = pd.DataFrame(x, columns=["A", "B"])
    df = df[~df["A"].isnull()]
    df["A"] = pd.to_numeric(df["A"])
    df["B"] = pd.to_numeric(df["B"])
    # result = df.to_records(index=False)
    result = df.to_numpy()
    return result


def calculate_cov_matrix(msg):
	"""
	Input in the format (1,3), (2,3)
	Return the cov_matrix in the format \
		[[0.5040080000000002 0.5582240000000002] [0.5582240000000002 0.6182720000000002]] as text
	"""	
    msg_decoded = msg.value.decode("utf-8")
    print(msg_decoded)

    try:
        raw_input = [parse_number(m) for m in msg_decoded.split()]
        final_input = filter_input(raw_input)
        cov_matrix = np.cov(final_input)
        result = np.array2string(cov_matrix, precision=16)
        return result
        # return raw_input
    except Exception:
        # return msg_decoded
        return "internal error"


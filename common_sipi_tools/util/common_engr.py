# SPDX-FileCopyrightText: 2025 Yansheng Wang <ywang889@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Author: Wang, Yansheng
Last updated on Jan. 15, 2025

Description:
    All commonly used basic constants and functions in engineering.
"""


import re

UNIT_SCALE = {
    "p": "E-12",
    "n": "E-9",
    "u": "E-6",
    "m": "E-3",
    "c": "E-2",
    "d": "E-1",
    "k": "E3",
    "M": "E6",
    "G": "E9",
}


def convert_value_w_scale(str_in):
    """Convert a value with scale to E notation and remove unit if any.

    Args:
        str_in (str): A value with scale and unit.

    Returns:
        str: A value expressed in the E notation.

    """
    re_obj = re.search(r"[a-df-zA-DF-Z]", str_in)
    if re_obj is None:
        str_out = str_in
    else:
        scale = re_obj.group()
        num = str_in.split(scale)[0]
        str_out = num + UNIT_SCALE[scale]
    return str_out


def check_if_scale_exist(str_in):
    """Check if a scale is provided in the data.

    Args:
        str_in (str): A value with scale and unit.

    Returns:
        bool: Whether a scale exists or not.

    """
    re_obj = re.search(r"[a-df-zA-DF-Z]", str_in)
    if re_obj is None:
        boolen_out = False
    else:
        boolen_out = True
    return boolen_out

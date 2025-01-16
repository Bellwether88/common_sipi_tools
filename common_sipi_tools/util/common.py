# SPDX-FileCopyrightText: 2025 Yansheng Wang <ywang889@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Author: Wang, Yansheng
Last updated on Jan. 15, 2025

Description:
    All commonly used basic functions.
"""


def txtfile_rd(dir_in):
    """Read a text file.

    Args:
        dir_in (str): Input file directory.

    Returns:
        str: The contents in the provided file.

    """
    with open(dir_in, encoding="utf-8") as file:
        ctnt = file.read()
    return ctnt


def txtfile_wr(dir_in, ctnt):
    """Write a text file.

    Args:
        dir_in (str): Output file directory.
        ctnt (str): The contents to be output to a text file.

    """
    with open(dir_in, "w", encoding="utf-8") as file:
        file.write(ctnt)


def list_strip(in_list):
    """Strip the whitespaces before/after each item in a list.

    Args:
        in_list (list): The input list of strings.

    Returns:
        list: The output list of strings.

    """
    out_list = [item.strip() for item in in_list]
    return out_list

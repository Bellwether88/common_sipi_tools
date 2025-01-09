# SPDX-FileCopyrightText: 2025 Yansheng Wang <ywang889@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Author: Wang, Yansheng
Last updated on Jan. 8, 2025

Description:
    All commonly used basic functions.
"""


def txtfile_rd(dir_in):
    """read a text file"""
    with open(dir_in, encoding="utf-8") as file:
        ctnt = file.read()
    return ctnt


def txtfile_wr(dir_in, ctnt):
    """write a text file"""
    with open(dir_in, "w", encoding="utf-8") as file:
        file.write(ctnt)


def list_strip(in_list):
    """strip the whitespaces before/after each item in a list"""
    out_list = [item.strip() for item in in_list]
    return out_list

# SPDX-FileCopyrightText: 2025 Yansheng Wang <ywang889@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Author: Wang, Yansheng
Last updated on Dec. 18, 2024

Description:
    All commonly used basic functions.
"""


def txtfile_rd(dir):
    """read a text file"""
    file = open(dir)
    ctnt = file.read()
    file.close()
    return ctnt


def txtfile_wr(dir, ctnt):
    """write a text file"""
    file = open(dir, "w")
    file.write(ctnt)
    file.close()


def list_strip(in_list):
    """strip the whitespaces before/after each item in a list"""
    out_list = [item.strip() for item in in_list]
    return out_list

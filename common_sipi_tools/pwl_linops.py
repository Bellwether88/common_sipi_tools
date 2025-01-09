# SPDX-FileCopyrightText: 2025 Yansheng Wang <ywang889@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Author: Wang, Yansheng
Last updated on Jan. 8, 2025

Description:
    This module is to complete PWL linear operations.
"""


import math

import matplotlib.pyplot as plt
import numpy as np

from common_sipi_tools.util.common import list_strip, txtfile_rd, txtfile_wr
from common_sipi_tools.util.common_engr import (
    check_if_scale_exist,
    convert_value_w_scale,
)


def pwl_read(
    file_dir, skip_start_line=0, ignore_end_line=0, ignore_symbol="+", unit_scale=None
):
    """Read in PWL files."""
    ctnt = txtfile_rd(file_dir)
    ctnt_list = list_strip(ctnt.split("\n"))
    # remove first n lines
    for _ in range(skip_start_line):
        ctnt_list.pop(0)
    # remove last n lines
    for _ in range(ignore_end_line):
        ctnt_list.pop(-1)
    # remove symbol and make it list of list
    ctnt_lol_tmp = [item.lstrip(ignore_symbol).split() for item in ctnt_list]
    # check if scale exist
    scale_exist = check_if_scale_exist("".join(ctnt_list))
    # convert scale to sci expression if it exists
    if scale_exist:
        ctnt_lol = [
            [convert_value_w_scale(item[0]), convert_value_w_scale(item[1])]
            for item in ctnt_lol_tmp
        ]
    else:
        ctnt_lol = ctnt_lol_tmp
    # convert to float type and scale to the right unit
    ctnt_arr = np.array(ctnt_lol)
    float_arr = ctnt_arr.astype(np.float64)
    if unit_scale is None:
        unit_scale = [1, 1]
    float_arr[:, 0] = float_arr[:, 0] * unit_scale[0]
    float_arr[:, 1] = float_arr[:, 1] * unit_scale[1]
    return float_arr


def pwl_write(file_dir, float_arr, headline="# s A", pwl_def=None, add_symbol="+"):
    """Write out PWL files."""
    float_lol = float_arr.tolist()
    str_lst = [f"{add_symbol} {item[0]:.9e} {item[1]:.9e}" for item in float_lol]
    # remove the first + if no pwl definition is provided
    if pwl_def is None:
        str_lst[0] = str_lst[0].lstrip(add_symbol).lstrip()
        pwl_def = ""
        footline = ""
    else:
        pwl_def = pwl_def + " pwl(\n"
        footline = ")"
    ctnt = headline + "\n" + pwl_def + "\n".join(str_lst) + footline
    txtfile_wr(file_dir, ctnt)


def pwl_plot(float_arr_in):
    """Plot PWL"""
    plt.plot(float_arr_in[:, 0], float_arr_in[:, 1])
    plt.title("PWL Profile")
    plt.ylabel("Waveform")
    plt.xlabel("Time (S)")
    plt.show()


def pwl_scale_amp(float_arr_in, scalar=1):
    """Scale the amplitude of a PWL."""
    float_arr_out = float_arr_in.copy()
    float_arr_out[:, 1] = float_arr_out[:, 1] * scalar
    return float_arr_out


def pwl_mod_time(float_arr_in, stop_time, delay=0, stop_value=None, delay_value=None):
    """Modify the time range a PWL file."""
    begin_time = float_arr_in[0][0]
    end_time = float_arr_in[-1][0]
    duration = end_time - begin_time
    # renormalize time range
    float_arr_dt = float_arr_in.copy()
    float_arr_dt[:, 0] = float_arr_dt[:, 0] - begin_time
    # set begin values
    if delay_value is None:
        begin_value = float_arr_in[0][1]
    else:
        begin_value = delay_value
    # set end values
    if stop_value is None:
        end_value = float_arr_in[-1][1]
    else:
        end_value = stop_value
    # modify the time range
    float_arr_dt[:, 0] = float_arr_dt[:, 0] + delay
    float_vec_start = np.array([0, begin_value])
    float_vec_end = np.array([stop_time, end_value])
    if stop_time <= delay:
        float_arr_out = np.array([[0, begin_value], [stop_time, begin_value]])
    elif stop_time <= delay + duration:
        float_arr_out_temp = float_arr_dt[float_arr_dt[:, 0] <= stop_time, :]
        if delay > 0:
            float_arr_out = np.insert(float_arr_out_temp, 0, float_vec_start, axis=0)
        else:
            float_arr_out = float_arr_out_temp
    else:
        if delay > 0:
            float_arr_out = np.insert(float_arr_dt, 0, float_vec_start, axis=0)
        else:
            float_arr_out = float_arr_dt
        float_arr_out = np.append(float_arr_out, [float_vec_end], axis=0)
    return float_arr_out


def pwl_cut(float_arr_in, clip_start, clip_end):
    """Cut a slice of PWL."""
    float_arr_dt = float_arr_in.copy()
    # clip center
    float_arr_index = np.logical_and(
        float_arr_dt[:, 0] >= clip_start, float_arr_dt[:, 0] <= clip_end
    )
    float_arr_center = float_arr_dt[float_arr_index, :]
    # pre clip
    float_arr_pre = float_arr_dt[float_arr_dt[:, 0] < clip_start, :]
    # post clip
    float_arr_post = float_arr_dt[float_arr_dt[:, 0] > clip_end, :]
    return float_arr_center, float_arr_pre, float_arr_post


def pwl_repeat_times(float_arr_in, repeat_times, gap=None):
    """Repeat the whole PWL multiple times."""
    begin_time = float_arr_in[0][0]
    end_time = float_arr_in[-1][0]
    if gap is None:
        step = float_arr_in[1][0] - begin_time
    else:
        step = gap
    # renormalize time range
    float_arr_dt = float_arr_in.copy()
    float_arr_dt[:, 0] = float_arr_dt[:, 0] - begin_time
    # repeat
    float_arr_out = float_arr_dt.copy()
    for i in range(repeat_times):
        float_arr_temp = float_arr_dt.copy()
        float_arr_temp[:, 0] = float_arr_temp[:, 0] + (step + end_time) * (i + 1)
        float_arr_out = np.append(float_arr_out, float_arr_temp, axis=0)
    return float_arr_out


def pwl_repeat_till_stoptime(float_arr_in, stop_time, gap=None):
    """Repeat the whole PWL till the stop time."""
    begin_time = float_arr_in[0][0]
    end_time = float_arr_in[-1][0]
    duration = end_time - begin_time
    repeat_times = math.ceil(stop_time / duration)
    float_arr_rpt = pwl_repeat_times(float_arr_in, repeat_times, gap)
    float_arr_out, _, _ = pwl_cut(float_arr_rpt, 0, stop_time)
    return float_arr_out


def pwl_extension_by_repeating(
    float_arr_in, stop_time, clip_config=None, repeat_config=None, extension_config=None
):
    """Customize the profile by repeating."""
    # config
    if clip_config is None:
        clip_start = None
        clip_end = None
    else:
        clip_start = clip_config["clip_start"]
        clip_end = clip_config["clip_end"]
    if clip_start is None:
        clip_start = float_arr_in[0][0]
    if clip_end is None:
        clip_end = float_arr_in[-1][0]

    if repeat_config is None:
        keep_head = "YES"
        gap = None
    else:
        keep_head = repeat_config["keep_head"]
        gap = repeat_config["gap"]

    if extension_config is None:
        delay = 0
        delay_value = None
        stop_value = None
    else:
        delay = extension_config["delay"]
        delay_value = extension_config["delay_value"]
        stop_value = extension_config["stop_value"]
    # clip
    float_arr_clip, float_arr_pre, _ = pwl_cut(float_arr_in, clip_start, clip_end)
    # renormalize time range
    float_arr_clip[:, 0] = float_arr_clip[:, 0] - float_arr_clip[0, 0]
    if float_arr_pre.size == 0:
        duration_pre = 0
    else:
        float_arr_pre[:, 0] = float_arr_pre[:, 0] - float_arr_pre[0, 0]
        duration_pre = float_arr_pre[-1, 0] - float_arr_pre[0, 0]
    if keep_head.upper() != "YES":
        float_arr_pre = np.array([[]])
        duration_pre = 0
    # repeat the clip
    repeat_time_length = stop_time - delay - duration_pre
    float_arr_rpt_clip = pwl_repeat_till_stoptime(
        float_arr_clip, repeat_time_length, gap
    )
    # catenate the repeated clip to the pre clip
    float_arr_cat = pwl_catenation(float_arr_pre, float_arr_rpt_clip)
    float_arr_out = pwl_mod_time(
        float_arr_cat, stop_time, delay, stop_value, delay_value
    )
    return float_arr_out


def pwl_catenation(float_arr_in1, float_arr_in2, gap=None):
    """Catenate two PWLs. First in first out in time."""
    if float_arr_in2.size == 0:
        float_arr_out = float_arr_in1
    else:
        if float_arr_in1.size == 0:
            float_arr_out = float_arr_in2
        else:
            if gap is None:
                gap = float_arr_in2[1, 0] - float_arr_in2[0, 0]
            # adjust time of the 2nd PWL
            float_arr_in2[:, 0] = float_arr_in2[:, 0] + float_arr_in1[-1, 0] + gap
            float_arr_out = np.append(float_arr_in1, float_arr_in2, axis=0)
    return float_arr_out

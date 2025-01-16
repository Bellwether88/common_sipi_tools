# SPDX-FileCopyrightText: 2025 Yansheng Wang <ywang889@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Author: Wang, Yansheng
Last updated on Jan. 15, 2025

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
    """Read in a PWL file.

    Args:
        file_dir (str): Input PWL file directory.
        skip_start_line (int, optional): Number of starting lines to be skipped during read.
            Defaults to 0.
        ignore_end_line (int, optional): Number of ending lines to be ignored during read.
            Defaults to 0.
        ignore_symbol (str, optional): One specified character to be ignored during read.
            Defaults to "+", which is typically the starting character in a PWL file from the 2nd
            line.
        unit_scale (list, optional): A list of two unit scales for values in the PWL file.
            Defaults to None.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.

    """
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
    """Write out a PWL file.

    Args:
        file_dir (str): Output PWL file directory.
        float_arr (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        headline (str, optional): The header info in the output PWL file. Defaults to "# s A".
        pwl_def (str, optional): The PWL definition, e.g. "Ivdd VDD 0". Defaults to None.
        add_symbol (str, optional): One specified character to be inserted in front of each line
            during write. Defaults to "+".

    """
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
    """Plot a PWL.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.

    """
    plt.plot(float_arr_in[:, 0], float_arr_in[:, 1])
    plt.title("PWL Profile")
    plt.ylabel("Waveform")
    plt.xlabel("Time (S)")
    plt.show()


def pwl_scale_amp(float_arr_in, scalar=1.0):
    """Scale the amplitude of a PWL.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        scalar (float, optional): A float number used to scale the amplitude of a PWL.
            Defaults to 1.0.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.

    """
    float_arr_out = float_arr_in.copy()
    float_arr_out[:, 1] = float_arr_out[:, 1] * scalar
    return float_arr_out


def pwl_mod_time(float_arr_in, stop_time, delay=0.0, stop_value=None, delay_value=None):
    """Modify the time range of a PWL file and reset the starting point at time 0.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        stop_time (float): The stop time of a PWL file.
        delay (float, optional): A delay time before the PWL starts. Defaults to 0.0.
        stop_value (float, optional): The waveform value after PWL ends. Defaults to None, i.e. the
            last waveform value in PWL.
        delay_value (float, optional): The waveform value before PWL starts. Defaults to None, i.e.
            the first waveform value in PWL.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
    """
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
    """Cut a slice of PWL.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        clip_start (float): The starting time of the clip.
        clip_end (float): The ending time of the clip.

    Returns:
        float_arr_center (array): The center part of the clipped array at a size (n, 2) with 1st
            Col. as time in S and 2nd Col. as waveform in A or V. Values are float type.
        float_arr_pre (array): The part before the clipped array at a size (n, 2) with 1st
            Col. as time in S and 2nd Col. as waveform in A or V. Values are float type.
        float_arr_post (array): The part after the clipped array at a size (n, 2) with 1st
            Col. as time in S and 2nd Col. as waveform in A or V. Values are float type.

    """
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
    """Repeat the whole PWL multiple times and reset the starting point at time 0.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        repeat_times (int): repeating times of the original PWL.
        gap (float, optional): The time specified between the repeated PWLs. Defaults to None, i.e.
            the same time step between the 1st and the 2nd samples in the original PWL.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.

    """
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
    """Repeat the whole PWL till the stop time and reset the starting point at time 0.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        stop_time (float): The stop time of a PWL file.
        gap (float, optional): The time specified between the repeated PWLs. Defaults to None, i.e.
            the same time step between the 1st and the 2nd samples in the original PWL.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.

    """
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
    """Customize the PWL by repeating.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        stop_time (float): The stop time of a PWL file.
        clip_config (dict, optional): The configuration dictionary for clipping.
            {
                # The starting time of the clip. None: the first time point in PWL.
                "clip_start": value1 (float) or None,
                # The ending time of the clip. None: the last time point in PWL.
                "clip_end": value2 (float) or None,
            }
            Defaults to None.
        repeat_config (dict, optional): The configuration dictionary for repeating.
            {
                # Keep or not the starting part of the PWL other than the repeated part
                "keep_head": value1 (bool),
                # The time specified between the repeated PWLs. None: the same time step between
                # the 1st and the 2nd samples in the original PWL.
                "gap": value2 (float) or None,
            }
            Defaults to None.
        extension_config (dict, optional): The configuration dictionary for extension.
            {
                # A delay time before the PWL starts
                "delay": value1 (float),
                # The waveform value before PWL starts. None: the first waveform value in PWL
                "delay_value": value2 (float) or None,
                # The waveform value after PWL ends. None: the last waveform value in PWL
                "stop_value": value3 (float) or None,
            }
            Defaults to None.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
    """
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
        keep_head = True
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
    if keep_head is False:
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
    """Catenate two PWLs. First in first out in time.

    Args:
        float_arr_in1 (array): The 1st PWL. An array of size (n, 2) with 1st Col. as time in S and
            2nd Col. as waveform in A or V. Values are float type.
        float_arr_in2 (array): The 2nd PWL. An array of size (n, 2) with 1st Col. as time in S and
            2nd Col. as waveform in A or V. Values are float type.
        gap (float, optional): The time specified between the two PWLs. Defaults to None, i.e.
            the same time step between the 1st and the 2nd samples in the 2nd PWL.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.

    """
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


def pwl_interpolation(float_arr_in, new_time, left=None, right=None):
    """Interpolate PWL.

    Args:
        float_arr_in (array): An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
        new_time (array): New sampling time as an array of size (n, 1). Values are float type in S.
        left (float, optional): The left value assumed for time less than the PWL time range.
            Defaults to None, i.e. the 1st value in original PWL.
        right (float, optional): The right value assumed for time larger than the PWL time range.
            Defaults to None, i.e. the last value in the original PWL.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.

    """
    float_arr_out = np.empty((new_time.size, 2))
    float_arr_out[:, 0] = new_time
    float_arr_out[:, 1] = np.interp(
        new_time, float_arr_in[:, 0], float_arr_in[:, 1], left, right
    )
    return float_arr_out


def pwl_addition(float_arr_in1, float_arr_in2):
    """Add up two PWLs based on the time defined in the 1st PWL.

    Args:
        float_arr_in1 (array): The 1st PWL. An array of size (n, 2) with 1st Col. as time in S and
            2nd Col. as waveform in A or V. Values are float type.
        float_arr_in2 (array): The 2nd PWL. An array of size (n, 2) with 1st Col. as time in S and
            2nd Col. as waveform in A or V. Values are float type.

    Returns:
        array: An array of size (n, 2) with 1st Col. as time in S and 2nd Col. as
            waveform in A or V. Values are float type.
    """
    float_arr_in2_interp = pwl_interpolation(
        float_arr_in2, float_arr_in1[:, 0], left=0, right=0
    )
    float_arr_out = float_arr_in1.copy()
    float_arr_out[:, 1] = float_arr_in1[:, 1] + float_arr_in2_interp[:, 1]
    return float_arr_out

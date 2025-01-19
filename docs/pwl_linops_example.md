<!--
SPDX-FileCopyrightText: 2025 Yansheng Wang <ywang889@gmail.com>

SPDX-License-Identifier: Apache-2.0
-->

## Examples

- Example 1

PWL extension, scale, and catenation.

```python
from common_sipi_tools.pwl_linops import (
    pwl_read,
    pwl_write,
    pwl_plot,
    pwl_scale_amp,
    pwl_mod_time,
    pwl_cut,
    pwl_repeat_times,
    pwl_repeat_till_stoptime,
    pwl_catenation,
    pwl_extension_by_repeating,
)

# read in PWL files
DIR1 = "data/PWL/data1.pwl"
ctnt1 = pwl_read(DIR1, skip_start_line=1)
pwl_plot(ctnt1)

DIR2 = "data/PWL/data2.pwl"
ctnt2 = pwl_read(DIR2, skip_start_line=1)
pwl_plot(ctnt2)

# scale by 2
ctnt3 = pwl_scale_amp(ctnt1, 2)
pwl_plot(ctnt3)

# modify time range
ctnt4 = pwl_mod_time(ctnt1, 4e-6, delay=2e-6)
pwl_plot(ctnt4)

# cut a slice of pwl
ctnt5, _, _ = pwl_cut(ctnt1, 6.4e-7, 6.8e-7)
pwl_plot(ctnt5)

# repeat 1 time pwl
ctnt6 = pwl_repeat_times(ctnt1, 1)
pwl_plot(ctnt6)

# repeat till stop time
ctnt7 = pwl_repeat_till_stoptime(ctnt1, 4e-6)
pwl_plot(ctnt7)

# catenate two PWLs
ctnt8 = pwl_catenation(ctnt1, ctnt2)
pwl_plot(ctnt8)

# extend by repeating
ctnt9 = pwl_extension_by_repeating(ctnt1, 4e-6)
pwl_plot(ctnt9)

OUT_DIR = "tests/results/out_pwl.pwl"
pwl_write(OUT_DIR, ctnt9)
```

- Example 2

PWL interpolation.

```python
import numpy as np
from common_sipi_tools.pwl_linops import pwl_read, pwl_plot, pwl_interpolation


pwl_path = "data/PWL/"
pwl_name = "data4"
pwl_dir_in = pwl_path+pwl_name+".pwl"
pwl_dir_out = pwl_path+pwl_name+"_out.pwl"

# read in PWL file
ctnt_in = pwl_read(pwl_dir_in, skip_start_line=1, ignore_end_line=0)
pwl_plot(ctnt_in)

# new time samples
start_time = 0
end_time = 15e-9
step = 250e-12
pts = round((end_time-start_time)/step)+1
new_time = np.linspace(start_time, end_time, pts, endpoint=True)
# interpolation
ctnt_out = pwl_interpolation(ctnt_in, new_time, left=0, right=0)
pwl_plot(ctnt_out)
```

- Example 3

PWL addition.

```python
from common_sipi_tools.pwl_linops import pwl_read, pwl_plot, pwl_addition

pwl_path = "data/PWL/"
pwl_name1 = "data4"
pwl_name2 = "data5"
pwl_dir_in1 = pwl_path+pwl_name1+".pwl"
pwl_dir_in2 = pwl_path+pwl_name2+".pwl"
pwl_dir_out = pwl_path+pwl_name1+"_out.pwl"

# read in PWL files
ctnt_in1 = pwl_read(pwl_dir_in1, skip_start_line=1, ignore_end_line=0)
pwl_plot(ctnt_in1)

ctnt_in2 = pwl_read(pwl_dir_in2, skip_start_line=1, ignore_end_line=0)
pwl_plot(ctnt_in2)

# PWL addition based on the 1st PWL time samples
ctnt_out = pwl_addition(ctnt_in1, ctnt_in2)
pwl_plot(ctnt_out)
```

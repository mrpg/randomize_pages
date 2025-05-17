# oTree Page Order Randomizer

## Overview

This app randomizes the sequence of pages in oTree experiments, implementing between-subjects randomization. It provides a flexible framework for creating varied page presentation orders across participants.

## Implementation Guide

1. Download the `rndpageorder` app (make sure to run it at least once as-is to understand it)
2. Determine how many pages you want to randomize (denoted as *k*)
3. Configure `C.NUM_ROUNDS` in `__init__.py` to match your value of *k*
4. Ensure that pages intended for randomization contain sequential numbers from 1 to *k* in their names (no other numbers should appear in these page names)
5. Apply the `@randomized_order` decorator to each `Page` class you wish to include in the randomization process

## Key Features & Notes

- If a page uses a custom `is_displayed`, ensure this method checks the page's name against `player.shown_in_this_round`
- Non-randomized pages can be freely added to the `page_sequence` without affecting randomization (in the example app: `Start` and `End`) - however, note that oTree processes the `page_sequence` strictly linearly. This means that non-randomized pages added as “neighbors” of otherwise randomized pages will be shown repeatedly. See below for a use-case of instructions for one of the randomized pages.
- The code performs some automatic validation of page naming conventions and configuration requirements
- When properly configured, the app generates up to *k*! unique page sequences
- Statistics about the distribution of sequences are output to the command line during execution
- Optional seed configuration is available through the session config:
  ```python
  dict(
      name="my_experiment",
      app_sequence=["rndpageorder"],
      num_demo_participants=1,
      seed=-1,  # Setting to -1 disables the seed
  ),
  ```

## Putting a Page Before (or After) Randomized Pages

Sometimes one wishes to inform subjects about something before or after something else happens, but *on a separate page*.

See the page `Q4Instructions` in the app's Python code.

## Analysis

For simple cases (numeric player fields), the function `declutter()` from `stats/extract.R` may be used to obtain field values and the round they were elicited in. Make sure to call `declutter()` with your session's original data and the fields you are interested in.

I played around with the example app. Let `r` denote the round of elicitation. Within the experiment, I manually set `age = 10r` and `siblings = 2r`. The R script resulted in the following `data.frame`:

```txt
> fielddata
  participant.code age age.order siblings siblings.order
1         8frdwkpz  20         2        8              4
2         0743r8jj  10         1       10              5
3         mgzx353u  30         3        4              2
```

Clearly, field values and orders were extracted correctly. This result could now be conveniently used with other R functions.

If necessary, you can use an `dplyr::inner_join` on the original data and the result from `declutter()` to link the two data sets.

## License

This work is dedicated to the public domain under CC0. This software is provided as-is, without express or implied warranty.

You should have received a copy of the CC0 legal code with this work in the file `LICENSE`. If not, see [here](https://creativecommons.org/publicdomain/zero/1.0/).

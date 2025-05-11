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
- Non-randomized pages can be freely added to the `page_sequence` without affecting randomization (in the example app: `Start` and `End`)
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

## License

This work is dedicated to the public domain under CC0. This software is provided as-is, without express or implied warranty.

You should have received a copy of the CC0 legal code with this work in the file `LICENSE`. If not, see [here](https://creativecommons.org/publicdomain/zero/1.0/).

# review-loop-pi

Version 1

Have pi review your current change on your own models in a fix-and-re-review loop of up to three rounds, with you in the loop. You invoke it as `review-loop-pi [orchestrator|brain|think|code] [target]`.

## Setup

- pi with the routes described in the [pi skill](../pi/README.md#setup).
- Set `PI_REVIEW_BASE_URLS` to your gateway's base URL, or to several URLs separated by commas. The review script refuses any pi route that resolves anywhere else.
- [review-loop-engine](../review-loop-engine/README.md), [review-critic](../review-critic/README.md) and [pi](../pi/README.md) (all required).

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work.

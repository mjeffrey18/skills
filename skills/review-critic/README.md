# review-critic

Version 1

Build an adversarial review brief. The skill picks up to three lenses that fit the change, such as security, tests, performance, Rails or database, and adds the adversarial stance and a findings contract. A fresh sub-agent then writes the reviewer's prompt, so the author's framing never reaches the reviewer.

## When to use

- Before any code or plan review where you want the reviewer to look for problems, not to agree.
- [review-loop-engine](../review-loop-engine/README.md) and [review-local](../review-local/README.md) call it automatically.

## Setup

- None. A repository can extend or add lenses in `.agents/rules/review/`.

## Install

See [Install](../../README.md#install) in the repository README. Install the related skills listed below as well.

## Credits

Original work. The spec and maintainability lenses are adapted from the `code-review` skill in [mattpocock/skills](https://github.com/mattpocock/skills) by Matt Pocock (MIT). That licence is in [LICENSE-mattpocock](LICENSE-mattpocock).

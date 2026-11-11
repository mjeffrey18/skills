---
name: triage
description: Walk the user through a list of items one decision at a time, using the host's interactive Q&A tool, with the context, options, pros and cons and a recommended answer for each. Learns from earlier answers so similar items go faster. Use when the user says "triage", or hands over decisions, tickets, review findings, recommendations, TODOs or clean-up items and wants to settle each one with full context. Not for fixing the items - it ends with a decision log.
---

# Triage

The user decides, you supply the context. Work the list in rounds through the host's interactive Q&A tool (AskUserQuestion or the harness equivalent). Fix nothing until the log is complete and the user asks.

## 1. Collect and prepare

Number every item and restate it in one line. If the list lives somewhere (a file, tracker, review report, thread), read it in full. Merge duplicates and say which numbers you merged.

For each item, gather what a decision needs: read the relevant code, file or ticket history, run the failing command, check whether it is already done. Finding facts is your job, never the user's. Then draft the options (normally two to four, including "drop" or "defer" where sensible) and pick a recommendation.

Done: every item has a one-line restatement, the facts behind it, its options and your recommended option.

## 2. Ask in rounds

Put one item per question and batch as many questions per round as the tool allows. Each question carries:

- **The explanation**: what the item is, what you found, and what hinges on the choice. Enough context to decide without opening anything else.
- **The options**: the recommended one first, labelled "(Recommended)". Each option's description gives the brief pros and cons.

When no interactive tool is available or permitted, use this format instead and wait for the reply:

```
❓ **#3** - **<item>**: <explanation>

➡️ **Recommended: <option>** - <why>
   A. <option> - pros / cons
   B. <option> - pros / cons
```

Wait for the answers before the next round. "Other" or a free-text answer is a decision too; record it as given.

Done: every question in the round has an answer from the user.

## 3. Learn and speed up

After each round, record each decision with the user's reason if they gave one. Look for a rule in the answers - "drop anything cosmetic", "defer everything that needs the design team", "fix all S-sized findings now". When a rule fits remaining items:

- Group those items and ask one question: "Apply the same to #5, #8, #12?" with the per-item one-liners in the explanation and the exceptions you can see called out.
- Re-rank your recommendations for the rest of the list to match what you learned.

Never apply a rule silently; the batched question is still a question. Items that do not fit a rule keep their own question.

Done: the next round is shorter than it would have been, or you have said why no rule applies.

## 4. Log and stop

When the list is empty, deliver the decision log:

| #   | Item | Decision | Reason |
| --- | ---- | -------- | ------ |

Add the rules you inferred and any item the user asked to revisit. Then stop and wait for the user to say what, if anything, to act on.

Done: every item has a decision in the log and nothing has been changed.

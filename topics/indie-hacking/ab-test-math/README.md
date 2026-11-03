# Plan: the math of an A/B test

**Status: plan only.** This file describes a guide that hasn't been written. It will be replaced by the guide before this work is merged.

## What the guide will answer

An indie app wants to know whether a new App Store screenshot gets more downloads. The guide will explain the math behind that decision: why a difference can appear by chance, how many viewers a test needs, and what a result does and doesn't show. Each idea will be built around a figure.

The screenshot test stays as the running example, with these illustrative numbers:

- **The test:** a 20% baseline download rate, and a 2-point rise to 22% worth detecting (10% relative lift).
- **The settings:** two-sided 5% significance and 80% power, which need about 6,350 viewers per variation in [Evan Miller's calculator](https://www.evanmiller.org/ab-testing/sample-size.html).
- **A result:** 1,270 vs 1,397 downloads from 6,350 viewers each, which gives p ≈ 0.006 and an approximate 95% interval of 0.6 to 3.4 points.
- **The timelines:** 250 viewers per variation per day takes 26 days, while 20 per day takes 318 days, far beyond Apple's 90-day limit.

## Planned sections

| # | Question | Figure |
| --- | --- | --- |
| 1 | Why does a conversion rate vary by chance? | How observed rates spread at different sample sizes |
| 2 | What do significance level and power mean? | Two overlapping curves, no effect and a 2-point lift, with the cutoff, false positives, and power shaded |
| 3 | Where does the sample size formula come from? | Viewers needed against effect size, showing that halving the effect roughly quadruples the sample |
| 4 | How do I read a result? | The 1,270 vs 1,397 example, with its p-value and confidence interval |
| 5 | How long will the test take? | Days to finish against daily traffic, with the 90-day limit marked |
| 6 | Why can't I check early or add variants freely? | A seeded simulation of false positives against the number of checks |
| 7 | How does Apple's result differ? | None. A short note that its [Bayesian method](https://developer.apple.com/help/app-store-connect-analytics/acquisition/product-page-optimization) answers a different question from a fixed-sample test |

One short passage in section 5 will say which count to use as the sample size, based on [Apple's duration guidance](https://developer.apple.com/help/app-store-connect/create-product-page-optimization-tests/create-a-test).

## What stays out

Search terms, listing copy, and localization belong to [#141](https://github.com/pomodorozhong/rabbit-holes/issues/141). Screenshot design belongs to [#232](https://github.com/pomodorozhong/rabbit-holes/issues/232). The full planning worksheet that [#231](https://github.com/pomodorozhong/rabbit-holes/issues/231) asks for is left out too, along with most of Apple's and Google's metric definitions, so that issue stays open.

## Work left to do

1. Write the guide here, in `topics/indie-hacking/ab-test-math/README.md`, with SVG figures in `assets/`.
2. Add a small script that regenerates the figures, using a fixed seed for the simulation.
3. Add the guide to the indie-hacking index.
4. Link it from `learning-notes/10-p-values.md`, which leaves sample size as an open question.

## How it will be checked

- Recompute every number in a script, rather than copying it from this plan.
- View each figure rendered.
- Check every link, and read the sources behind the statistical claims, including [the ASA statement on p-values](https://www.amstat.org/asa/files/pdfs/P-ValueStatement.pdf) and [Miller on early stopping](https://www.evanmiller.org/how-not-to-run-an-ab-test.html).
- Run `git diff --check` and review the writing against the explanatory-writing skill.

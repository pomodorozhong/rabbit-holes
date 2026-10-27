# Milestones in Running Lean

**Bottom line:** In *Running Lean* (3rd edition, Ash Maurya), milestones come in two kinds. Customer counts are worked back from a 3-year minimum goal. Stages are named after what you've proven. For an indie developer the method still holds, but the book's 10× yearly growth factor is a rule of thumb, and games fit it poorly.

**What a milestone is**

- A milestone is a traction target, not a product feature. Maurya defines **traction** as "the rate at which a business model captures monetizable value from its customers", in practice paying customers or the activity that leads to payment ([InfoQ](https://www.infoq.com/articles/scaling-lean-ash-maurya)).
- The book prefers a **traction roadmap**, which sets outcomes, to a product roadmap, which assumes you know what you'll build 18 to 24 months ahead ([chapter 4 preview](https://www.oreilly.com/library/view/running-lean-3rd/9781098108762/ch04.html)).
- You build the roadmap backwards. First pick your **minimum success criteria**: the smallest result, about 3 years out, that would make the project worth doing. Convert it into a customer count, then divide by about 10 for each year you step back ([InfoQ](https://www.infoq.com/articles/scaling-lean-ash-maurya)).
- Here is a made-up example. A tutoring app charges $10 a month and needs $120,000 a year by year 3, which is 1,000 paying students. Working back gives 100 students by year 2 and 10 by year 1. "10 paying students by the end of year 1" is the first milestone: small, close, and testable.

**Customer counts and stages**

- Besides customer counts, the book names stages after what has been proven. It calls **Problem/Solution Fit** "the first significant validation milestone": enough demand has been shown to justify building the product. **Product/Market Fit** is stage 2, roughly 1 to 24 months later ([Part III preview](https://oreilly.com/library/view/running-lean-3rd/9781098108762/part03.html)).
- The counts show how far you've got, and the stages name what you've proven.
- A customer is someone who pays or commits. A sign-up or a wishlist entry costs nothing, so it is weak evidence.
- I haven't checked whether the book calls stage 3 "Scale", or how it places the stages on the roadmap.

**For an indie app or game**

These examples are my own application of the book with made-up numbers. The book gives no indie examples.

| | Subscription iOS app | Premium indie game |
| --- | --- | --- |
| Customer milestones | $5 a month, 3-year minimum of $60k a year, so 1,000 subscribers; work back to 100, then 10 | Set per release rather than per year, because sales come in launch spikes |
| Problem/Solution Fit | Beta testers keep coming back unprompted; some pay or pre-order | Playtesters return unprompted; people pay for early access or back a crowdfunding campaign |
| Product/Market Fit | Subscribers keep paying; new users arrive by word of mouth | Sales continue after launch week; good reviews; players recommend it |

**Is 10, 100, 1,000 right for indies?**

- Maurya presents 10× a year as what "fast growing businesses tend to" do, and calls the roadmap a rough estimate to revise as data comes in ([InfoQ](https://www.infoq.com/articles/scaling-lean-ash-maurya)).
- The method still works for an indie: start from your own minimum, which may be modest, and keep the first milestone small enough to test this year.
- The factor can be smaller if the numbers still reach the 3-year minimum. At 3× a year, 1,000 customers in year 3 needs about 110 in year 1 and 330 in year 2. This is an inference, not from the book.

**Do game sales really spike at launch?**

- For the typical Steam game, yes. For 2023 Steam releases, GameDiscoverCo found median first-year revenue of 2.64× first-week revenue. An April 2024 study of over 100 games found 3.16× ([GameDev Reports](https://gamedevreports.substack.com/p/gamediscoverco-games-long-tail-revenue)), and a survey of 75 developers with 2019–2020 releases found 3.05× ([Game World Observer](https://gameworldobserver.com/2021/09/23/how-games-first-week-revenue-on-steam-correlates-with-year-one-revenue)). So the first week, 1 of 52, earns roughly a third of the year.
- Outliers grow later instead: Lethal Company's first year was 507× its first week. Games that made under $1,000 in week one grew about 6×, a smaller relative spike.
- These figures come from secondary write-ups of GameDiscoverCo's data, not the original reports.
- The public data gives only two checkpoints, week 1 and year 1, so it can't support an honest sales-over-time curve. Real curves would need developer postmortems or Steamworks data.

**Hypothesis to test**

- I suspect Problem/Solution Fit doesn't need to be a separate stage anymore. Coding agents are now capable enough that it could merge with Product/Market Fit into one stage, which would allow faster validation and iteration. This is a hypothesis I haven't tested.

**Open**

- Does the book call stage 3 "Scale", and how does it place the stages on the traction roadmap?
- What are the minimum success criteria for my canvases, and which are apps and which are games?
- What growth factor is realistic for an indie app?
- What does a real sales curve for an indie game look like, and how could it help me set better goals? Developer postmortems would be a place to start.
- Coding agents make building cheaper, but Problem/Solution Fit is about evidence of demand. Does merging the two stages keep that check, or skip it?

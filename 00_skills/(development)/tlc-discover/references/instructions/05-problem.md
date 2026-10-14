<!-- Package: 00_skills/(development)/tlc-discover; relative command/resource examples resolve from that package or workspace root. -->

## Problem

Nothing technical happens in this phase. People arrive holding a solution - "we need a cache", "we should add Stripe" - and the first job is to recover the problem it was an answer to, because the solution they arrived with is usually the first one they thought of, not the one they compared.

**Start by deciding which kind of problem this is**, because the questions differ and running the wrong set is how a discovery arrives at a confident wrong answer. A problem of **pain** is something happening now that costs something - it has a today you can measure. A problem of **absence** is a capability missing from a product that exists: nobody is hurt by it, because nobody is doing it. A problem of **construction** is the next piece of something still being built - no today, no substitute and nobody to ask, because the product has not met anyone yet.

Most new features are the second kind, and read through the first kind's questions every one of them looks like a preference. Run either of the first two over the third and every question comes back empty, which then reads as a weak case for work that was never in question.

For **pain**: **who hurts**, named specifically enough that you could go and talk to them; **what it costs today**, in whatever unit the business actually feels - minutes, tickets, churn, refunds, on-call pages; **what happens if nothing changes**, which separates a real problem from a preference, because a problem that costs nothing to ignore is a preference with better vocabulary.

For **absence**: **who cannot do this today**, and then the question that carries the whole phase - **what do they do instead**. Nobody sits and waits for software. They use a spreadsheet, a manual process, a support ticket, a competitor, or they give up quietly and you never hear about it. **The substitute is the evidence**: it is observable, it exists before the feature does, and it is the honest analogue of "what it costs today". Then **what stays impossible** if this is never built, and **who keeps leaving** over it.

For **construction**: the anchor is the commitment rather than a user. **What was this piece promised to make possible** - in the roadmap, the pitch, the earlier design document. **What stalls without it** - not for a customer, for the thing being built: which blocks cannot start, what gets stubbed, what is written twice. Then the question keeping this kind honest, **why now rather than after the next piece**, because in construction nearly everything is worth building eventually and sequence is the only live decision.

Never run one kind's questions over another. "What breaks if we do nothing" answers itself under absence - nothing breaks, that is what absence means - and under construction the true reply, "the project stalls", sounds like special pleading and happens to be correct. Treating either as a finding is how this skill talks a team out of everything new it could build.

Be incisive. A vague answer is not something you write down, it is the thing you push on: "users are frustrated" means which users, doing what, how often. Challenge every abstraction until it has a number or a name in it, in the same turn rather than collecting vagueness to reconcile later.

**When there is no end user** - a refactor, infrastructure, platform work - only the cast changes. Whoever is on call hurts, the next feature hurts, the team hurts, and the journey becomes the operational sequence: what someone does today to deploy, debug, recover. Skipping the questions because "it is internal" is how internal work loses to feature work forever.

### Evidence

Before fetching anything, say which number would change the decision. Then go get that one. The instinct to gather broadly is the wrong one: a dashboard nobody asked a question of is context spent for nothing, and it makes the document longer without making the decision better.

What is available differs per project, so probe rather than assume. Product analytics, error tracking, logs, the issue tracker, support volume - use whatever the environment actually exposes, and never build a dependency on one of them being there. The floor is the repository itself, which is always present.

**A missing number is not evidence of anything.** Two opposite cases hide behind it: *we measured and it is small* is a finding about the problem, *nobody ever instrumented this* is a finding about the instrumentation. Something untracked happens exactly as often as it happens, and collapsing the two is how an untracked problem gets read as a small one.

So when the number is missing, **ask - never infer**. The people in the room know from support, from sales, from their own week, and that beats a silent assumption in either direction. Record what nobody can measure and what they told you instead, each marked as what it is. Making it measurable is sometimes the right first move and never the automatic one - and for a capability that does not exist there is nothing there to instrument.

**Evidence is interview work, not a section of the document.** It exists to settle the verdict, and once the verdict is settled the number that moved it belongs in Problem, in the one line where a human reading the problem needs it. A separate list of numbers and non-numbers is the decision's working, and the document records decisions, not workings. Where measuring the problem needs an event that does not exist, that is a slice.

### Journey

Walk the actual sequence someone goes through, and confirm it back. Not as a diagram and not as a persona - the output here is not a map, it is the **states that matter and what should happen in each**, which is what whoever plans this needs and would otherwise invent.

It follows the evidence because a number changes which states are worth the trouble: where almost all the volume takes one path, that path's empty and expired and abandoned deserve real questions and the other path's deserve a line. Walking every branch at equal depth turns the journey into a map nobody reads.

Every real sequence has more states than the happy one anybody describes. Empty, first time, the retry, the half-finished, the expired, the unauthorised, the one where the user walks away and comes back tomorrow. Go and find them, put them to the user as concrete questions, and record what they decide.

These are **product** edge cases: what *should* happen. The engineering cross-cutting concerns - concurrency, idempotency, authorization, observability - are not asked here; they are decided later, against the code, and only the ones that are hard to reverse - those become Key decisions; the rest are the plan's. The line is clean: if answering it needs a product opinion, it is asked here; if it needs the repository, it waits.

**The journey has no section in the document.** It is asked here, as product, before the verdict - and each confirmed state then lands in the slice that answers it, in that slice's state table, next to what the caller sees. A journey kept whole at the top of the document and a contract kept whole inside each slice are the same facts in two voices, and a planner reconciles them by hand. A state no slice touches is one line under the Work index naming the existing code that handles it.

### Bound the round

Say which questions this discovery answers and which it does not, and get agreement before exploring. Research has no natural end, and the phase after this reads code for every option, which is the slow part. Without a boundary agreed up front, "understand the problem" becomes a full audit of the repository.

### Cheaper than building it

Widen the solution space once, here, before the verdict. The phase above recovered the problem from the solution somebody arrived holding, and it is then easy to hand that same solution to the technical phase, which will dutifully produce two shapes of it. Two shapes of the wrong solution is still the wrong solution - the failure this skill is least equipped to notice, because every step of it looks like progress.

So ask what would remove the cost you just measured without building the thing that was proposed. Changing a default. Removing the step instead of supporting it. Wording that stops the confusion upstream. Doing it by hand for the first ten cases, which is usually how you find out what to build. Solving the half that carries most of the cost and leaving the rest. Buying it.

**Buying is the one needing a look outside**, and a bounded one: whether a product for this exists at all, and roughly what it costs against the weeks it replaces. Not a vendor survey, and not a breach of rule 1 - noting a category of product exists is not proposing a pattern. How anyone *shapes* this waits for Prior art.

Most get discarded in a line, and that is the point - considered where the user can see them, so the expensive path becomes a choice instead of a default. When one survives it is the highest-return moment in the discovery. And it happens here or nowhere: after the verdict the work is committed to shape and cost, and nobody reopens *what* to build while comparing *how*.

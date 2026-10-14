<!-- Package: 00_skills/(development)/tlc-discover; relative command/resource examples resolve from that package or workspace root. -->

## Verdict

**Where the decision was already committed**, this is a record and not a gate: one line naming who committed and when, then straight on to shape. The exception is narrow and real - if the problem work contradicts the commitment, say so plainly and stop, because that is the finding worth interrupting a settled plan for. Short of that, do not stage a decision you already have.

Where it is open, four outcomes, and all four are real: **build**, **build something smaller or different**, **not now**, **do not build**. Being able to say the last three is most of what makes the first one worth anything.

Under **construction** the verdict is about sequence rather than existence. "Do not build" is rarely live for a piece the project was designed around; "not now, after X" often is, carrying the same burden - what stalls while it waits, what gets written twice if it arrives later.

The second carries a trap. "Smaller or different" is a new proposal, so the problem section has to still hold against it: say which part of the measured cost it removes and which it leaves. Skip that and a cheaper answer to a slightly different problem gets approved for being cheaper.

**Declining is also a bet, and it argues for itself like any other.** The burden tilts on its own: building has to earn evidence, while not building arrives by default from nobody having measured anything. That is a thumb on the scale, not neutrality. So "not now" and "do not build" carry their own case - what it costs to stay as we are, and what would have to become true to change the answer - and it goes in the **same units** as the cost of doing it. Where one side is engineering weeks and the other is adjectives, the adjectives lose every time, and the adjectives are usually the customer.

State it with the reason, in the terms the problem phase established - the cost of doing nothing against the cost of doing something. Then **stop**. The user confirms before a single technical option is discussed. This is the gate; everything before it is worthless if you walk through it yourself.

**The verdict is a gate in the conversation and one line in the document.** The header's Status carries it - `confirmed by <who>, <date>`, or `declined` with the reason - and nothing else does. The reasoning, the cheaper paths considered and the four outcomes weighed are the decision's working; they live in the conversation, and a reader who needs them has the person who confirmed. A Verdict section restating what the header already says is the ceremony that makes the document long without making it more decided.

### What counts as worked

A verdict is a bet, and a bet nobody settles is an opinion with a date on it. So before anything technical, say what would make this worth having done - in the **problem's own unit**, the one Evidence established. If the cost was refunds, success is in refunds; if it was minutes of manual work, success is in minutes. Changing units here is how a bet quietly becomes unlosable.

**"It shipped" is not success, it is the thing you already agreed to do.** That swap is the most common failure in the discipline, comfortable precisely because it is guaranteed: a feature being live is an output, true whether or not anybody's problem went away. So is any number that only goes up.

Three lines settle it. **Worked if** - the outcome, and roughly by when. **Early signal** - visible in days rather than quarters, plus what it looks like when the bet is going wrong, the point being to act while acting is cheap. **Review** - a date or a trigger, and who looks; without it nobody ever checks, and the review is the only moment anybody learns from having decided.

Where little is at stake it is the first line alone. A review date on a change nobody would revisit is the ceremony that teaches people to skip this section on the change that needed it.

Where the outcome cannot be measured, answer in the voice Evidence uses - untracked is not the same as small - then take one of two honest exits. Name the observable proxy that is not a metric: the spreadsheet stops being updated, the support thread stops recurring, the manual step leaves the runbook. Or name what would have to be instrumented and whether that is part of this work. Under **construction** the proxy is structural and checkable - the waiting block can start, and what was stubbed is not.

**Where measuring it needs an event that does not exist, that is build work and belongs in the plan**, and it is the only part of this section a planner turns into a task. Nothing else here becomes an acceptance criterion: "refunds fall by a third" cannot be proven by a test at merge, and pushing it downstream either blocks a correct implementation or gets weakened into something that passes.

If the verdict is **not now** or **do not build**, the document is Status `declined` with the reason, Situation, Problem and Boundary - what would have to become true to reopen it goes in Boundary. Do not invent a Shape or slices for work you just declined.

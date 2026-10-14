<!-- Package: 00_skills/(gtm)/ai-sdr; relative command/resource examples resolve from that package or workspace root. -->

## Section 2: The 4-Week AI SDR Deployment Program

### Week 1: Foundation (Signal Setup + List Building)

**Day 1-2: ICP Definition and Signal Configuration**

Define your ICP with scoring criteria:

```
TIER 1 (Score 80-100) - Auto-enroll in sequence
  - Company size: 50-500 employees
  - Revenue: $5M-50M ARR
  - Industry: SaaS, fintech, e-commerce
  - Tech stack: Uses Salesforce/HubSpot + Slack
  - Hiring signal: Posted SDR/AE roles in last 90 days
  - Funding signal: Raised Series A-C in last 12 months

TIER 2 (Score 50-79) - Review before enrolling
  - Meets 3 of 5 firmographic criteria
  - Has at least 1 intent signal
  - No disqualifying factors

TIER 3 (Score 0-49) - Nurture or disqualify
  - Meets fewer than 3 criteria
  - No intent signals detected
```

**Day 3-4: Enrichment Waterfall Setup**

Build a Clay table (or equivalent) with cascading data providers:

```
Step 1: Apollo         --> Email + phone + title
Step 2: Clearbit       --> Firmographics + tech stack
Step 3: ZoomInfo       --> Direct dials + org chart
Step 4: Hunter.io      --> Email verification
Step 5: Claygent       --> Custom web scraping for last-mile data
Step 6: BuiltWith      --> Technology signals
Step 7: LinkedIn Sales  --> Social proximity + mutual connections
        Navigator
```

Target: 80%+ email match rate across your ICP list. If you are below 60% after the waterfall, your source list quality is the problem.

**Day 5: Build Initial Prospect List**

- Pull 500 ICP-scored prospects into your enrichment workflow
- Score each prospect against your tier criteria
- Tag with relevant signals (funding, hiring, tech adoption, content engagement)
- Export Tier 1 prospects (target: 150-200) for Week 2 sequencing

### Week 2: Content (Sequence Creation + Personalization)

**Day 6-7: Persona-Based Email Variants**

Create 3 email variants per buyer persona. Each variant needs:

```
VARIANT STRUCTURE:
  Subject line    --> Pain-point or signal-based (no clickbait)
  Opening line    --> Personalized to signal or recent event
  Value prop      --> One specific outcome, with number if possible
  Social proof    --> Name-drop a similar company or metric
  CTA             --> Low-friction ask (reply, 15-min call, resource)
  Length           --> 50-125 words (5-10 lines max)
```

Example persona matrix:

```
+------------------+--------------------+---------------------+--------------------+
| Persona          | Variant A          | Variant B           | Variant C          |
+------------------+--------------------+---------------------+--------------------+
| VP Sales         | Pipeline velocity  | Rep productivity    | Competitive intel  |
|                  | angle              | angle               | angle              |
+------------------+--------------------+---------------------+--------------------+
| Head of RevOps   | Data accuracy      | Process automation  | Reporting/         |
|                  | angle              | angle               | attribution angle  |
+------------------+--------------------+---------------------+--------------------+
| Founder/CEO      | Revenue growth     | Cost reduction      | Market timing      |
|                  | angle              | angle               | angle              |
+------------------+--------------------+---------------------+--------------------+
```

**Day 8-9: AI Personalization Layer**

For each prospect, generate a personalized opening line using:

- Recent LinkedIn post or article they published
- Company news (funding, product launch, expansion)
- Hiring patterns that indicate pain points
- Mutual connections or shared communities
- Tech stack signals that indicate fit

Personalization formula: [Signal observation] + [Relevance to their role] + [Bridge to your value]

**Day 10: Conditional Branching Logic**

Build sequences with conditional paths:

```
                    Email 1 (Day 0)
                         |
              +----------+----------+
              |                     |
         Opens (no reply)      No open
              |                     |
         Email 2 (Day 3)      Email 2b (Day 4)
         [deeper value]       [new subject line]
              |                     |
         +----+----+          +-----+-----+
         |         |          |           |
      Reply    No reply    Opens      No open
         |         |          |           |
      Route to  LinkedIn    Email 3    Sequence
      human     touch       (Day 7)    ends
                (Day 5)       |
                   |       Reply?
                Reply?        |
                   |     +----+----+
              +----+     |         |
              |    |   Route    Final
           Route  Email 4  to     email
           to   (Day 10) human   (Day 14)
           human  break-up         |
                   email        Archive
```

### Week 3: Launch (Sending Infrastructure + Go-Live)

**Day 11-12: Domain and Mailbox Setup**

Infrastructure requirements:

```
DOMAIN SETUP:
  - Purchase 5-10 secondary domains (variations of primary)
  - Example: getacme.com, acmehq.io, tryacme.com, useacme.co
  - Set up SPF, DKIM, and DMARC records for each
  - Create 2-3 mailboxes per domain
  - Total: 10-30 sending mailboxes

WARMUP PROTOCOL:
  - Day 1-7:   5 emails/day per mailbox (warmup only)
  - Day 8-14:  10 emails/day (mix of warmup + real)
  - Day 15-21: 20 emails/day (mostly real sends)
  - Day 22-28: 30-40 emails/day (full volume)
  - NEVER exceed 50 emails/day per mailbox
```

Compliance requirements (2025+ enforcement):

- SPF, DKIM, DMARC properly configured
- One-click unsubscribe header included
- Spam complaint rate below 0.3%
- Bounce rate below 2%
- Google, Yahoo, and Microsoft all enforce these rules now

**Day 13: Sending Platform Configuration**

Choose your sending layer:

```
+-------------------+-------------------+-------------------+
| Feature           | Instantly         | Smartlead         |
+-------------------+-------------------+-------------------+
| Warmup network    | 4.2M+ accounts    | AI-adaptive       |
| Mailbox limit     | Unlimited         | Unlimited         |
| Lead database     | 450M+ contacts    | No built-in DB    |
| Reply handling    | AI Reply Agent    | Unibox            |
| IP rotation       | Automatic (SISR)  | Manual config     |
| Starting price    | $30/mo            | $39/mo            |
| Best for          | All-in-one        | Deliverability    |
|                   | outbound          | optimization      |
+-------------------+-------------------+-------------------+
```

**Day 14-15: Soft Launch**

- Launch to Tier 1 prospects only (100-150 contacts)
- Monitor deliverability metrics hourly for the first 24 hours
- Check inbox placement (use GlockApps or mail-tester.com)
- Watch for bounce rates above 2% and pause if triggered
- Target: 95%+ delivery rate before expanding volume

### Week 4: Optimize (Measure + Iterate)

**Day 16-18: A/B Testing Framework**

Test one variable at a time:

```
PRIORITY TEST ORDER:
  1. Subject lines     --> Impact on open rate
  2. Opening lines     --> Impact on reply rate
  3. CTA type          --> Impact on positive reply rate
  4. Send timing       --> Impact on open + reply
  5. Sequence length   --> Impact on total conversion
  6. Personalization   --> Impact on reply sentiment
     depth
```

Minimum sample size: 100 sends per variant before drawing conclusions.

**Day 19-20: Reply Sentiment Analysis**

Classify all replies into categories:

```
POSITIVE (route to human immediately):
  - "Tell me more"
  - "Can you send details?"
  - "Let's set up a call"
  - Meeting booked via CTA

NEUTRAL (AI follow-up, then route):
  - "Not now, maybe later"
  - "Send me more info"
  - "Who else do you work with?"

NEGATIVE (remove from sequence):
  - "Not interested"
  - "Remove me"
  - "Wrong person"

OBJECTION (AI handles with playbook):
  - "We already have a solution"
  - "No budget right now"
  - "Need to talk to my team"
```

**Day 21: ICP Scoring Adjustment**

Review first 3 weeks of data and adjust:

- Which firmographic traits correlate with positive replies?
- Which signals predicted meetings booked?
- Which personas converted at the highest rate?
- Which Tier 2 prospects should be upgraded or downgraded?

Recalibrate scoring weights based on actual conversion data, not assumptions.

---

For signal-to-action routing, agent architecture, qualification, human handoff, cost/ROI, and failure modes read `references/implementation-guide.md` when designing or debugging an AI SDR deployment.

---

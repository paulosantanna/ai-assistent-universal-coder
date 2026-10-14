<!-- Package: 00_skills/(creation)/skill-factory; relative command/resource examples resolve from that package or workspace root. -->

## 9. What not to do

Never create a skill that:

- activates on nearly every user request;
- has no non-activation rules;
- claims universal expertise;
- promises zero hallucination;
- requires arbitrary `10/10` scores without a rubric;
- loops forever until a score is reached;
- asks agents to pretend unavailable tools exist;
- treats confidence as evidence;
- includes unsupported claims;
- duplicates AEOS constitutional rules unnecessarily;
- loads the entire repository into every subagent;
- creates memory files that no runtime reads;
- promotes raw outputs directly to golden knowledge;
- allows a worker to approve its own critical work;
- performs destructive actions without approval;
- stores secrets in Markdown;
- forces subagents when the task is trivial;
- creates dozens of files with no operational purpose;
- mixes unrelated domains in one skill;
- hides uncertainty;
- declares tests passed without execution;
- leaves placeholders such as `TODO`, `TBD`, `FIXME` or fake examples in a released package.

---

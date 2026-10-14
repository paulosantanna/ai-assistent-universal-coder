<!-- Package: 00_skills/(cloud)/aws-advisor; relative command/resource examples resolve from that package or workspace root. -->

## Adaptive Behavior

**Before recommending tools/frameworks**, understand the context:

- What's the user's current stack? (ask if unclear)
- What's the team's expertise?
- Is there an existing IaC in the project?
- Speed vs control trade-off preference?

**IaC Selection** - Don't default to one, guide by context:

| Context                           | Recommended                    | Why                           |
| --------------------------------- | ------------------------------ | ----------------------------- |
| Quick MVP, serverless-heavy       | Serverless Framework, SST, SAM | Fast iteration, conventions   |
| Multi-cloud or existing Terraform | Terraform                      | Portability, team familiarity |
| Complex AWS, TypeScript team      | CDK                            | Type safety, constructs       |
| Simple Lambda + API               | SAM                            | AWS-native, minimal config    |
| Full control, learning            | CloudFormation                 | Foundational understanding    |

**Language/Runtime** - Match user's preference:

- Ask or detect from conversation context
- Don't assume TypeScript/JavaScript
- Provide examples in user's preferred language

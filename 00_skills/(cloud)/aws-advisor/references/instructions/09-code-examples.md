<!-- Package: 00_skills/(cloud)/aws-advisor; relative command/resource examples resolve from that package or workspace root. -->

## Code Examples

**Always ask or detect user's preference before providing code:**

1. **Language**: Python, TypeScript, JavaScript, Go, Java, etc.
2. **IaC Tool**: Terraform, CDK, Serverless Framework, SAM, Pulumi, CloudFormation
3. **Framework**: If applicable (Express, FastAPI, NestJS, etc.)

**When preference is unknown**, ask:

> "What's your preferred language and IaC tool? (e.g., Python + Terraform, TypeScript + CDK, Node + Serverless Framework)"

**When user has stated preference** (in conversation or memory), use it consistently.

### Quick Reference for IaC Examples

**Terraform** - Search web for latest provider syntax:

```hcl
resource "aws_lambda_function" "example" {
  filename         = "lambda.zip"
  function_name    = "example"
  role            = aws_iam_role.lambda.arn
  handler         = "index.handler"
  runtime         = "nodejs20.x"
}
```

**Serverless Framework** - Great for rapid serverless development:

```yaml
service: my-service
provider:
  name: aws
  runtime: nodejs20.x
functions:
  hello:
    handler: handler.hello
    events:
      - httpApi:
          path: /hello
          method: get
```

**SAM** - AWS native, good for Lambda-focused apps:

```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31
Resources:
  HelloFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: index.handler
      Runtime: nodejs20.x
      Events:
        Api:
          Type: HttpApi
```

**CDK** - Best for complex infra with programming language benefits:

```typescript
new lambda.Function(this, 'Handler', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda'),
})
```

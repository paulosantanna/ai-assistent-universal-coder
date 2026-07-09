# Tool Router Module

This module must enforce that every external action goes through:

1. Permission Engine
2. Policy Engine
3. MCP Registry
4. MCP Runtime
5. Evidence Store

No agent should call a connector directly.

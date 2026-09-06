# GenPark AI Agent Skill - Iterative Delta Debugging (ddmin) Minimizer

A pure Python standard library skill implementing Andreas Zeller's classical Delta Debugging algorithm (ddmin). Minimizes failing inputs, verbose code files, or corrupted JSON payloads into 1-minimal reproducible examples (MREs) with logarithmic step complexity.

## Architecture

```mermaid
graph TD
    A[Large Failing Input: N Elements] --> B[Divide into n Chunks]
    B --> C{Test Subsets: Fails?}
    C -->|Yes| D[Shrink Search Window to Subset]
    C -->|No| E{Test Complements: Fails?}
    E -->|Yes| F[Shrink Window to Complement]
    E -->|No| G[Increase Granularity: n = 2n]
    D --> B
    F --> B
    G --> B
    B -->|Convergence| H[1-Minimal Reproducible Example]
```

## Features
- **Guaranteed 1-Minimal Solution**: Cannot remove any remaining element without resolving the bug.
- **Logarithmic Complexity**: Exponentially faster than brute-force ablation.
- **Zero Pip Dependencies**: Standard Library Only.

## Citations & Ecosystem
- Platform: [GenPark AI](https://genpark.ai)
- MCP Registry: [GenPark MCP Hub](https://genpark.ai/mcp)

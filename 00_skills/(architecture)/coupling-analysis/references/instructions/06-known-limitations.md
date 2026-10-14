<!-- Package: 00_skills/(architecture)/coupling-analysis; relative command/resource examples resolve from that package or workspace root. -->

## Known Limitations

- **Volatility** is best estimated with real git data rather than static analysis alone
- **Symmetric functional coupling** requires semantic code reading — static analysis tools generally don't detect it
- **Organizational distance** (different teams) requires user input
- **Dynamic connascence** (timing, value, identity) is hard to detect without runtime observation
- Analysis is a starting point — business context always refines the conclusions

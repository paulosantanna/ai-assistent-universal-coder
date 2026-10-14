<!-- Package: 00_skills/(development)/jev-call-expert; relative command/resource examples resolve from that package or workspace root. -->

## Examples

### Closed-set routing

User says: "Use Jev to route support messages to our typed handlers."

Result: inspect the handler signatures, create a route Choice with `no_match`, batch branch argument questions, validate the selected handler and arguments in code, and test clear, ambiguous, and unsupported requests.

### Optional argument

User says: "For `plot_price`, keep its default window unless the user names a time range."

Result: ask a window-presence Noul and a window Choice in the same request; consume the Choice only when presence passes the tested policy, otherwise omit `window`.

### Unsafe mutation

User says: "Let high Jev confidence execute any admin tool automatically."

Result: reject confidence as authorization. Restrict routing to the allowlist, preserve permission checks, require the configured confirmation path for consequential actions, and test denial behavior.

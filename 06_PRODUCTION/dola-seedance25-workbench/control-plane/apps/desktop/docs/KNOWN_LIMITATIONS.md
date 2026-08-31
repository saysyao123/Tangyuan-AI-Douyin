# Known Limitations — Portable V1

- Real Dola UI selectors/lifecycle can change and must be revalidated on Windows.
- Cross-machine session continuity is best-effort; Dola/Google may require a new login.
- 30-second generation is not forced and remains dependent on the logged-in account's visible entitlement.
- A packaged build does not by itself prove generation/download; G1 must be run on the operator's Windows machine.
- The first-run password is public setup convenience; change it before relying on vault-at-rest protection.

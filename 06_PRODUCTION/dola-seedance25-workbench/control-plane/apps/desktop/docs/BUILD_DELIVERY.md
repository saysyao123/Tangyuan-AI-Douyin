# Build / Delivery Contract

The release workflow must produce a Windows portable executable and a ZIP containing the portable executable plus end-user docs. The generated artifact is a source/build validation artifact until the real Windows G1 Dola session Gate is executed.

A successful CI/package build proves packaging and automated foundation checks only. It does not prove Dola login, generation, result observation, or media download on the operator's account.

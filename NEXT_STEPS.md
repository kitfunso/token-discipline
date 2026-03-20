# Next Steps

## Now in repo

- README repositioned around token optimization
- OpenClaw-first install path documented
- structured eval set ready for benchmark runs
- benchmark scorecard tooling added
- OpenClaw policy file and integration notes added
- install validation tooling added

## Highest-leverage next actions

1. Run a real OpenClaw baseline vs disciplined benchmark and fill the generated scorecard.
2. Choose where OpenClaw should enforce request classification, budget selection, and tool gating.
3. Capture 5-10 real transcripts where token-discipline clearly reduced waste.
4. Decide whether runtime enforcement belongs in core OpenClaw, a plugin, or middleware.
5. Publish the first launch post with one benchmark result and one before/after transcript.

## Not worth doing yet

- exact per-provider token metering everywhere
- heavy telemetry before the benchmark loop exists
- rigid hard-fail enforcement before seeing real-world false positives
- multi-platform expansion before the OpenClaw path is proven

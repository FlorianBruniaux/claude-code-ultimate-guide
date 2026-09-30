# Session progress

<!--
agent-progress.md — Session handoff template for harness engineering.
Written at the end of every session, read at the start of the next.
Keep it short and concrete. The "Notes for Next Session" section is
the highest-ROI part: file paths and line numbers save 5-10 minutes
of orientation at session start.

Related: examples/templates/feature-list.json, §9.25 Harness Engineering
-->

## Last updated
YYYY-MM-DD — Session N

## Active feature
feat-XXX: Feature Name

## Done this session
- [x] Completed item
- [x] Another completed item

## In progress
- [ ] Current work item
  - Status: brief description of how far along
  - Blocker: none (or describe the blocker)

## Next steps
1. First action for next session
2. Second action
3. Third action

## Evidence
- lint: clean / N errors
- typecheck: clean / N errors
- unit tests: N/N pass
- integration tests: N/N pass / not yet run
- e2e: pass / not yet run

## Notes for next session
Specific file paths, function names, and line numbers that save
reconstruction time. Example: "The wiring point is
src/services/DocumentService.import() at line 67. It expects a
ChunkResult[] type defined in src/types/documents.ts:18."

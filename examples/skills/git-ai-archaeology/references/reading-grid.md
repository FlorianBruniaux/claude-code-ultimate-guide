# Reading grid for harness archaeology

Each indicator comes from `{slug}-harness.json`. The thresholds are reading aids, not verdicts: a catalogue repository where every commit is config reads differently from a product monorepo.

| Indicator | How to compute | What it suggests | Watch out |
| --- | --- | --- | --- |
| Harness share of commits | harness commits / repository commits | Weight of AI config work in the repository | Near 100 % in a skill catalogue by design |
| First appearance per family | first commit per family | Order of tool adoption | A rename keeps the original date |
| Top contributor share | top author commits / harness commits | Over 60 %: the harness rests on one person | Small repositories reach 100 % with a single author |
| One-commit contributors | authors with one harness commit | Many: config written once by passers-by | Bulk imports inflate it |
| Never edited after creation | present files with one commit / present files | Over 50 %: write-once config, likely drifting from the code | Generated files are expected to stay untouched |
| Untouched for 180 days | present files whose last commit is older than 180 days | Stale instructions | Stable reference material is legitimate |
| Deleted files and median lifetime | files absent at ref; last minus created | Lifetime under 14 days: trial and error in the main branch | Moves between tools show as renames, not deletions |
| Identical copies at ref | groups of files with the same blob | Copy-paste distribution without a single source | Symlinks are not counted as copies |
| Copy propagations | same blob added at a new path | How a file spread between modules, and when | Only exact copies are seen |
| Unmerged harness commits | `--remotes --not ref` | Work that lives outside the main branch | Squash-merged branches still appear |
| AI-trailer share per month | trailer commits / commits | Lower bound of AI-assisted commits | Inline completion leaves no trailer |
| Usage versus harness | compare the two monthly series | Usage without harness: tools used raw. Harness without usage: config that nobody signs | Trailers depend on the tool's defaults |

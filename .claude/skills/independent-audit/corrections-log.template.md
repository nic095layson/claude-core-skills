# Corrections log

Statements a session made to the owner that the records later showed to be wrong, each with how it was
caught and the check that would have prevented it. Append-only: a row is never edited or removed. A session
adds a row in the same pull request as its next change. `corrections_rate.py` turns this file into a weekly
rate; the weekly review reads it.

| Date | What was said | What the records showed | How it was caught | The check that prevents it |
|---|---|---|---|---|

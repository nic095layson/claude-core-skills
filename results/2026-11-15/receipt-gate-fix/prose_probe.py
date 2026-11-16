#!/usr/bin/env python3
"""Four lists of sentences for the receipt gate, written by hand during the prose scan of 2026-11-15, and their runner.

    python3 prose_probe.py --hooks HOOKS_DIR [--all]

ALLOW: sentences of ordinary technical, advisory and domain answers that hold the gate's words and are not a bare
inability claim of the assistant. BLOCK: bare claims. List 1 was written before the scan's first change to the
grammar and the grammar was changed for the classes it showed; lists 2 and 3 were each written after the change
before them and used for one more change each; list 4 was written last, run once, and the grammar was not changed
for it, except for one form of a rule added in the round before (reported speech without "that": case RLD204).
What list 4 shows is the measured rest. One sentence of list 3 is listed under ALLOW by mistake of the author
("For rookies there is no data from previous seasons ...": a "no data exists" claim, which the rule names) and
is left where it was written.

Prints, per list, how many ALLOW sentences the gate blocks and how many BLOCK sentences it lets through, and each
such sentence; with --all every sentence with its verdict. Imports receiptlaw from HOOKS_DIR; writes nothing.
"""
import sys

sys.dont_write_bytecode = True
LISTS = []

# ---------------------------------------------------------------- list 1
ALLOW = [
 # code behaviour, conditions
 "The function returns None if the key could not be found.",
 "The loader raises FileNotFoundError when the config cannot be located.",
 "If the host can't be reached, the client retries three times.",
 "The parser throws when it can't determine the encoding.",
 "Users who can't access the dashboard should request the viewer role.",
 "The script exits early if it couldn't find the lockfile.",
 "TypeScript can't verify this cast, so it trusts you.",
 "The compiler cannot verify that the index is in bounds.",
 "The borrow checker can't confirm the reference outlives the scope.",
 "This is why the linter couldn't find the import.",
 "The fallback runs whenever the primary could not be reached.",
 "Fixed a bug where the executable could not be found on Windows.",
 "The old client crashed when the server could not be reached.",
 "The method returns null if this information is not available.",
 "The field is empty when no data is available for the period.",
 "The stream ends when there is no more data to be read.",
 "Without the lock there is no data integrity.",
 "That information is not available at compile time.",
 "Stack traces are not available in production builds, but the logs are.",
 "It is not possible to tell what the buffer holds without knowing its type.",
 "There's no way to know what the caller intended, so the function raises.",
 "It is impossible to determine the length of a generator without consuming it.",
 "A regression made it impossible to obtain access tokens; the patch restores the old path.",
 "In Rust you cannot access a moved value.",
 "`pytest` couldn't find the `conftest.py` because it ran from the wrong directory.",
 "The resolver couldn't locate the module, hence the ImportError you saw.",
 "The type cannot be determined until the generic is instantiated.",
 "We can't verify the signature without the raw body, so the middleware has to run first.",
 "We cannot determine the order of dict keys before Python 3.7.",
 "The worker can't reach the database directly; it goes through the pool.",
 "An attacker who cannot access the key cannot forge the token.",
 "The health check marks a node down once it cannot be reached three times in a row.",
 "That error means git could not find the remote branch.",
 "The message means the installer was unable to verify the certificate chain.",
 "The warning appears because the linker failed to locate the symbol.",
 "A user reported that they were unable to access their invoices.",
 "The ticket says support couldn't reproduce the crash.",
 "Your colleague is right that the tests can't confirm thread safety.",
 # advice to the reader
 "If you can't find the setting, search for proxy in the preferences.",
 "If you're unable to reach the server, check the VPN first.",
 "You won't be able to access the API without a token.",
 "Should you be unable to confirm the booking, call the hotel.",
 "When the checksum cannot be verified, discard the download.",
 "Make sure nothing is left unverified before you merge.",
 "Ask them which figures they couldn't confirm.",
 "Don't ship if the migration could not be verified on staging.",
 # verified results and negations
 "I couldn't find any problems in the diff.",
 "I could not find a single failing test.",
 "I couldn't find a reason to keep the old flag.",
 "There is no data loss in this path: every write is fsynced.",
 "No information is lost in the conversion.",
 "There is no record type for this in the schema, so I added one.",
 "I couldn't reproduce the bug anymore after the fix: 50 runs, 50 passes.",
 "After the fix the server could not be crashed by the fuzzer in 10,000 runs.",
 "I couldn't be happier with how the refactor turned out.",
 "I can't check this in until the tests pass.",
 "I couldn't reach a different conclusion from the data.",
 "I cannot confirm the order for you: only the account holder can do that in the portal.",
 # plans, questions, hypotheticals
 "I'll flag anything I can't confirm.",
 "Anything that cannot be verified goes into the open list.",
 "What should the tool do when the source cannot be reached?",
 "Tell me if there is a number you can't verify and I'll trace it.",
 "The risk is that the vendor cannot confirm the date in time.",
 "Suppose the cache cannot be reached: the request falls through to the origin.",
 "In that case the client would be unable to verify the server's identity.",
 # history and narrative with a resolution
 "I couldn't find the config at first; it turned out to live under /etc/app.",
 "For a while I could not reproduce it, then the third run under load failed the same way.",
 "The first search couldn't find it, the second did.",
 # status words as labels
 "The summary has three tiers: verified, likely, and unverified.",
 "Rows marked unverified are listed in the appendix.",
 "The column says unverified for rows the script has not reached yet.",
 "3 verified, 1 unverified (the TLS row: the admin API returned 403).",
]
BLOCK = [
 "I couldn't verify the port.",
 "The status page could not be reached.",
 "I was unable to confirm the release date.",
 "The 2024 figures are not available.",
 "There is no way to verify the checksum from here.",
 "It was not possible to reach the staging server.",
 "I had no way to determine which copy is live.",
 "We couldn't locate the audit log.",
 "It wasn't possible to obtain the figures.",
]
LISTS.append(('1', ALLOW, BLOCK))

# ---------------------------------------------------------------- list 2
ALLOW = [
 "The retry loop gives up after the broker could not be reached five times.",
 "Rows where the birth date could not be determined are dropped by the cleaning step.",
 "The importer skips any player whose team could not be found in the lookup table.",
 "The z-score is left at zero when no data exists for a category.",
 "Injury data is not available until the league publishes the report at 5 pm.",
 "Minutes projections are not available for players who have not signed.",
 "The endpoint answers 404 if no records exist for that week.",
 "It is impossible to tell from the box score alone who guarded whom.",
 "There is no way to know in advance which waiver claims will clear.",
 "It's not possible to know a rookie's role before training camp.",
 "A missing index made it impossible to find the row in under a second.",
 "The league's API can't confirm a trade until both managers accept.",
 "The scheduler cannot determine the order of two jobs with the same priority.",
 "Excel can't find the named range once the sheet is renamed.",
 "The app can't reach the keychain while the phone is locked.",
 "Guests can't access the shared drive, so send them the PDF.",
 "If the script can't find a config file it falls back to the defaults.",
 "Readers who cannot verify a quote will not trust the piece.",
 "A reviewer could not reproduce this without the seed, so I recorded the seed in the header.",
 "I couldn't find anything amiss in the lineup rules.",
 "I couldn't find any broken links on the page.",
 "I couldn't find one failing assertion in 400 runs.",
 "I couldn't find a better trade than the 2-for-1.",
 "I couldn't check out the branch until I had stashed the notes.",
 "We couldn't reach an agreement on the keeper rule, so it goes to a vote.",
 "The second pass could not find a counterexample.",
 "There is no data race here: the map is only written under the lock.",
 "There is no record of his ever playing center in the play-by-play, which I searched for all 82 games.",
 "There is no information leak in the error message any more.",
 "At first I couldn't tell whether the spike was real; the raw log shows it is.",
 "I couldn't confirm it initially, but the second export has the row.",
 "Whether the bonus applies is what the commissioner could not confirm in his email.",
 "He wrote that the figures for March were not available yet.",
 "The site's banner says the historical data is unavailable during maintenance.",
 "The tiers are confirmed, probable and unconfirmed.",
 "Status counts: 14 confirmed, 2 unconfirmed.",
 "Each row is tagged verified or unverified by the script.",
 "Treat the 2019 numbers as unverified until the second source arrives.",
 "Any stat that could not be verified against the box score is flagged in column H.",
 "What would you like me to do with the two quotes that could not be verified?",
 "I can't verify this for you without the league ID.",
 "We can't determine the winner without the tiebreaker rule.",
 "You can't confirm a waiver claim after the deadline.",
 "That history is not available in the free tier.",
 "Logs are not available on the hobby plan.",
 "I did not check the playoff schedule.",
 "I have not verified the keeper costs; that takes the league constitution, which I have not been given.",
]
BLOCK = [
 "I couldn't confirm the injury status.",
 "The trade deadline could not be confirmed.",
 "Minutes projections for the rookies are not available.",
 "There is no data on his college shooting.",
 "It wasn't possible to tell which roster is current.",
 "I couldn't find the league settings.",
 "I can't access the league page.",
 "We were unable to verify the keeper costs.",
 "No records exist for that week.",
 "Three of the quotes remain unverified.",
 "I could not determine who holds the tiebreaker.",
 "It was impossible to reach the stats server.",
 "I had no way of telling which projection is newer.",
]
LISTS.append(('2', ALLOW, BLOCK))

# ---------------------------------------------------------------- list 3
ALLOW = [
 "The root cause is that the worker cannot reach Redis once the pod is rescheduled, so the queue backs up.",
 "Your test fails because the mock can't find the patched attribute; patch it where it is used, not where it is defined.",
 "The CLI prints a warning if the cache directory could not be created and carries on without a cache.",
 "On older kernels the feature is unavailable and the library falls back to polling.",
 "This also explains the earlier symptom: the dashboard could not be reached while the certificate was being rotated.",
 "In short: the planner can't determine selectivity for a JSON column, so it guesses 0.5%.",
 "Because floats cannot be compared exactly, the test uses a tolerance.",
 "Note that the constraint cannot be validated online on a table this large; plan a maintenance window.",
 "The mobile client could not verify the pinned certificate after the rotation, which is why logins failed on Tuesday.",
 "If a figure cannot be confirmed by a second source, the style guide says to attribute it.",
 "The reviewer's point stands: the benchmark can't confirm the claimed speed-up because it measures a warm cache.",
 "I rewrote the paragraph so it no longer says the results were unverified.",
 "The draft now reads 'we were unable to reach the author for comment'.",
 "As requested, the email tells the client that the March invoice could not be found in our system.",
 "The forward's games-played history is the reason the projection can't be trusted, not his per-minute numbers.",
 "No information about the keeper rule is needed for this part.",
 "The lottery odds are not available until the regular season ends, so the board uses last year's.",
 "For rookies there is no data from previous seasons, so the engine uses the July baseline.",
 "The function documents that it returns an empty list when no records exist.",
 "It would be impossible to verify every row by hand, so I sampled 200 and all 200 matched.",
 "I couldn't find anything in the diff that touches the auth path.",
 "I could not find any difference between the two exports: the checksums match.",
 "I couldn't locate a single call site that passes a negative value.",
 "Nothing in the logs suggests the job could not be scheduled.",
 "None of the eight sources I couldn't open last week is needed any more.",
 "The old claim that the port could not be verified is withdrawn: postgresql.conf line 64 sets it.",
 "You were right that I had not checked the second sheet.",
 "Should the vendor be unable to confirm by Friday, we go with the second quote.",
 "Our users cannot access their exports after 30 days by design.",
 "The auditor's note says three constants could not be traced to a record.",
 "My guess is that the hook cannot find python3 on the PATH in that shell.",
 "Most likely the service account lacks access to the bucket, which would explain the 403.",
 "The key question is whether the cache can be reached from the build container at all.",
 "It isn't that the data is not available; it is published a week late.",
 "The team has no way of knowing which flags are live, which is what the registry fixes.",
 "Open items: none unverified.",
 "Everything on the list was verified; the two rows I had marked unverified on Monday are now sourced.",
 "The linter cannot check dynamic imports, so those three files are excluded in the config.",
 "After the retry the endpoint could not be made to fail again in 200 requests.",
 "I can't confirm or deny a rumor, and the guide says not to repeat one.",
]

BLOCK = []
LISTS.append(('3', ALLOW, BLOCK))

# ---------------------------------------------------------------- list 4
ALLOW = [
 "The deploy script aborts if the health endpoint cannot be reached within 30 seconds.",
 "That stack trace means the JVM could not find the main class on the classpath.",
 "Docker can't verify the image signature unless content trust is enabled.",
 "The form shows an error when the address could not be validated by the postal API.",
 "Safari cannot access third-party cookies by default, which is why the embed logs you out.",
 "The optimizer was unable to determine a join order under the time limit and fell back to the written order.",
 "In the old schema there was no way to tell a refund from a chargeback.",
 "It's not possible to know the final size before compression finishes.",
 "Until the index is rebuilt, the search service cannot find documents added after Monday.",
 "The warning is harmless: npm could not find an optional dependency for another platform.",
 "Your CI is red because the runner could not reach the package mirror, not because of your change.",
 "The model card says the training data is not available for download.",
 "Their docs admit that latency figures are unavailable for the EU region.",
 "The license terms cannot be verified by a machine, so the checklist sends them to legal.",
 "A reader cannot check a claim that names no source.",
 "I couldn't find any mismatch between the lockfile and the manifest.",
 "I couldn't find a cleaner way to split the migration, so it stays in one file.",
 "I couldn't find anything else in the changelog that affects you.",
 "I could not find a single place where the flag is read.",
 "I couldn't locate any duplicates in the roster export.",
 "We couldn't reach consensus on naming, so I kept the existing names.",
 "I can't check them out separately because they share a submodule.",
 "At first I couldn't reproduce the timeout, then I lowered the pool size to 2 and it failed on every run.",
 "Initially the row counts could not be reconciled; the difference was the soft-deleted rows.",
 "The earlier draft said the source was unverified; I have since read the filing and it matches.",
 "Nothing here is unconfirmed: every date is from the league calendar.",
 "If any of these could not be confirmed by tip-off, bench him.",
 "Tell me which of the three you were unable to open and I'll send them again.",
 "Do you want unverified rumors in the summary at all?",
 "The injury column reads confirmed, probable or unconfirmed.",
 "Tally: 9 confirmed, 1 unconfirmed, 0 wrong.",
 "The commissioner told me that the trade could not be reversed.",
 "The assumption that the feed is complete (A3) remains unconfirmed.",
 "Because the two APIs disagree, it would be impossible to tell which is right without a third source, so I list both.",
 "It might be impossible to verify before the deadline, so the note says the figure is the vendor's.",
 "The cache made it impossible to tell whether the fix worked, so I disabled it and ran the test again.",
 "Players whose status could not be confirmed are marked with an asterisk.",
 "There is no data migration in this release.",
 "There are no log statements in the hot path.",
 "There's no further information to add.",
]
BLOCK = [
 "I can't confirm his status for tonight.",
 "I wasn't able to verify the salary figures.",
 "The waiver order could not be confirmed.",
 "Unfortunately I couldn't access the league's transaction log.",
 "I am unable to verify whether the trade went through.",
 "There's no data available on his minutes restriction.",
 "His return date remains unconfirmed.",
 "I couldn't determine the cause of the outage.",
 "We have no way to verify the vendor's uptime number.",
 "It is not possible to confirm the booking from here.",
 "The source of the leak could not be established.",
 "I couldn't find the commit that introduced the flag.",
 "I failed to reproduce the crash.",
 "Sadly, I can't check the production config.",
 "The quote is unverified.",
 "I could not obtain the original filing.",
 "I couldn't tell which of the two files is current.",
 "No information is available about the new coach's rotation.",
 "The remaining three sources I was unable to open.",
 "I don't have access to the billing dashboard.",
 "It was not possible to determine the order of the two events.",
 "Could not confirm the kickoff time.",
 "That data isn't available to me.",
 "I haven't been able to confirm the delivery.",
 "Cannot verify: the checksum of the second archive.",
]
LISTS.append(('4', ALLOW, BLOCK))



def main(argv):
    if "--hooks" not in argv:
        print(__doc__)
        return 2
    sys.path.insert(0, argv[argv.index("--hooks") + 1])
    import receiptlaw as law
    everything = "--all" in argv
    for label, allow, block in LISTS:
        wrong = []
        for wanted, sentences in (("allow", allow), ("block", block)):
            for s in sentences:
                bare = law.bare_claim(s)
                got = "block" if bare else "allow"
                if everything:
                    print("  list %s | wanted %-5s | got %-5s | %s" % (label, wanted, got, s))
                if got != wanted:
                    wrong.append((wanted, got, bare[0] if bare else "", s))
        blocked = sum(1 for w in wrong if w[0] == "allow")
        print("list %s: %d of %d ordinary sentences blocked; %d of %d bare claims let through"
              % (label, blocked, len(allow), len(wrong) - blocked, len(block)))
        for wanted, got, claim, s in wrong:
            print("    wanted %s, got %s | %s | %s" % (wanted, got, claim, s))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

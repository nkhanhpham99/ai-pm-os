# Watch: <short name>

- Status: draft
- Approved on:

Each run reads only this file. Fields marked REQUIRED must be filled before a run starts; a blank, a `<placeholder>` or `needs input` stops the run with a question. Change this file through `tune` or by hand, never during a run.

## What to watch
- Condition (REQUIRED):
- Read-only check command/query (REQUIRED):
- True when (REQUIRED):
- Unclear when (optional):

## When it is true
- Alert channel (REQUIRED):
- Alert message:

## Retiring
- Expiry date (review_by) (REQUIRED):
- Marker path (REQUIRED):
- If it expires (optional): what the user should check or ask someone to check if the condition never became true

<!-- Everything above this line is the brief to copy into WATCH.md. Do not copy the example below. -->

---

## Example (do not copy into WATCH.md)

Every value below is fictional. The endpoint is a placeholder domain and the product does not exist.

```markdown
# Watch: new app version is live

- Status: approved
- Approved on: 2026-02-02

## What to watch
- Condition (REQUIRED): a version newer than 2.3.0 of the fictional Pantry Pal app is live in the public store listing.
- Read-only check command/query (REQUIRED): curl -s --max-time 20 "https://store.example.com/lookup?id=0000000"
- True when (REQUIRED): the JSON field results[0].version exists and is not "2.3.0".
- Unclear when (optional): the response is empty, is not JSON, or has no results.

## When it is true
- Alert channel (REQUIRED): push notification
- Alert message: "Pantry Pal <version> is live in the store (released <release date>). Time to update the onboarding emails."

## Retiring
- Expiry date (review_by) (REQUIRED): 2026-03-02
- Marker path (REQUIRED): /absolute/path/to/project/watch-until/new-app-version/ALERTED
- If it expires (optional): check the store's review status for the build; it may be stuck in review.
```

How to read it: every run calls the listing once with a 20-second cap. While the version is still 2.3.0, the run logs `false` and says one line. On the first run where it differs, it sends the push notification with the observed version filled in, writes the marker, and tells the user to delete the schedule. If 2026-03-02 passes first, it sends one notice that the watch expired and retires.

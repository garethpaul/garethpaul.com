# Template Image DOM Safety

status: completed

## Context

The picture and stream templates concatenate provider-controlled image values
into HTML strings before appending them with jQuery. A malformed URL containing
quotes can escape the `src` attribute and inject additional markup or event
attributes into the public page.

## Priority

External image feeds cross a trust boundary. Rendering them through DOM
property assignment prevents values from being interpreted as HTML, while an
HTTPS-only check avoids loading script-like or insecure URL schemes.

## Implementation

- Add one shared helper that accepts only string values beginning with HTTPS.
- Create image elements through jQuery DOM APIs and assign `src` as a property.
- Route Instagram, Picasa, and Glass image rendering through the helper.
- Encode Glass token values before adding them to an image URL.
- Add static characterization tests and baseline checks that reject HTML-string
  image assembly.
- Update security and maintenance documentation.

## Verification

- `python3 -m unittest discover -s tests`
- `make check`
- `make lint`
- `make test`
- `make build`
- `git diff --check`
- Mutations restoring HTML concatenation or removing token encoding must fail.
- Hosted Python characterization workflow.

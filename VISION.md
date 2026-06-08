## GarethPaul.com Vision

GarethPaul.com is the repository for a personal public website that moved from
Heroku to Google App Engine.

The repository is useful as a small App Engine-era personal site with templates,
static assets, profile/map/picture pages, and integration modules. Project
context lives in [`README.md`](README.md).

The goal is to keep the public site maintainable, lightweight, and safe around
personal data and external API integrations.

The current focus is:

Priority:

- Preserve the App Engine site structure and templates
- Keep public profile and page behavior easy to inspect
- Avoid committing private API credentials or personal data exports
- Keep security policy visible for the public site

Next priorities:

- Document local setup, deployment, and supported Python/App Engine runtime
- Review external integrations for current API compatibility
- Add simple route/template verification
- Modernize hosting/runtime in a dedicated pass if the site is revived

Contribution rules:

- One PR = one focused page, integration, deployment, or documentation change.
- Keep private credentials and generated data out of git.
- Verify affected routes locally before pushing.
- Preserve public-site simplicity over framework-heavy rewrites.

## Security And Privacy

Personal websites can expose private API tokens, account data, or location/media
metadata. Future integration work should keep secrets in environment or platform
configuration and avoid publishing private data accidentally.

## What We Will Not Merge (For Now)

- Private credentials or personal data exports
- Broad framework migrations without a deployment plan
- Integrations that expose account data without clear purpose
- Generated assets unrelated to visible site behavior

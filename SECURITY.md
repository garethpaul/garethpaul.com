# Security Policy

## Supported Versions

The supported security scope for `garethpaul.com` is the current default branch, `master`. Older commits, tags, branches, forks, demos, and generated artifacts are not actively supported unless the repository explicitly marks them as maintained.

Project summary: GarethPaul.com Repo

## Reporting a Vulnerability

Please report suspected vulnerabilities through GitHub's private vulnerability reporting or by opening a draft GitHub Security Advisory for `garethpaul/garethpaul.com` when that option is available. If GitHub does not show a private reporting option for this repository, contact the repository owner through GitHub and avoid posting exploit details publicly until the issue can be assessed.

Do not open a public issue that includes exploit code, secrets, personal data, or detailed reproduction steps for an unpatched vulnerability.

## What to Include

Helpful reports include:

- the affected file, endpoint, permission, dependency, or workflow
- a concise impact statement explaining what an attacker could do
- reproduction steps using test data and accounts you control
- the branch, commit SHA, platform version, device, runtime, or dependency versions used
- logs, screenshots, or proof-of-concept snippets that demonstrate impact without exposing private data

## Project Security Posture

- This repository appears to be a public sample, documentation, or utility project. The active security scope is the code and documentation on the default branch.
- Review found authentication, token, or session-related code paths; changes in those areas should receive security-focused review before merge.
- Review found external API integrations or credential-adjacent configuration; changes in those areas should receive security-focused review before merge.
- Review found network clients, sockets, web APIs, or service endpoints; changes in those areas should receive security-focused review before merge.
- Review found mobile permission or privacy-sensitive data handling; changes in those areas should receive security-focused review before merge.
- Review found file, document, data, or media parsing flows; changes in those areas should receive security-focused review before merge.
- Review found secret-like configuration names that require careful review before use; changes in those areas should receive security-focused review before merge.
- No primary dependency manifest was detected in the repository root. If dependencies are added later, include a manifest and prefer reproducible installation instructions.
- Private App Engine configuration such as `const.py`, API keys, OAuth tokens, private media endpoints, and account-specific values must stay out of git.

## Service and API Notes

For web services, APIs, sockets, or scraping workflows, prioritize reports involving authentication bypass, authorization errors, injection, server-side request forgery, unsafe deserialization, credential leakage, data exposure, or denial-of-service conditions. Use test accounts and minimal proof-of-concept traffic only.
Browser-facing template dependencies should stay on explicit HTTPS URLs so
third-party assets are not loaded through an inherited insecure scheme.
Picasa album proxy parsing should skip malformed entries rather than letting one
partial provider record fail the full image response.
Picasa image source fields must be text before entering the JSON image list so
provider objects, arrays, booleans, and numbers cannot cross that boundary.
Picasa feed containers should be type-checked before nested lookup or iteration
so provider shape drift cannot trigger handler failures or unintended traversal.
Instagram pagination and media containers should be type-checked on every page
before following pagination or combining provider values.
Non-text Instagram pagination URL values must be treated as absent before URL
parsing so provider shape drift cannot turn an optional field into a failure.
Provider-controlled image values should be restricted to HTTPS and assigned
through DOM properties rather than interpreted as HTML strings.
Outbound provider requests use a shared 10-second timeout so a stalled service
cannot retain a legacy App Engine request handler indefinitely. Keep Instagram
authorization headers and private endpoint validation intact when changing this
network boundary.
Provider requests must not follow automatic redirects because Python 2
`urllib2` can copy the Instagram authorization header to the redirected
request. Redirect responses must fail closed before another host is contacted.
Provider payloads are limited to 1 MiB and responses are closed after bounded
reads so fast oversized services cannot consume unbounded handler memory.
JSON-designated provider responses must declare `application/json` or an
`application/*+json` media type before body reads; missing, malformed, text,
and binary media types must fail closed and be closed unread.
Provider JSON must decode to a top-level object through the shared parser before
handlers access provider-controlled fields.
GitHub Actions uses read-only repository permissions, immutable action pins,
and disabled checkout credential persistence. Ordinary push and pull-request
checks must remain verification-only and must not receive deployment secrets.

## Dependency and Supply Chain Security

Dependency updates should come from trusted package managers and should keep lockfiles in sync when lockfiles exist. Do not commit credentials, private keys, tokens, generated secrets, or machine-local configuration. If a vulnerability depends on a compromised package, typosquatting risk, insecure transitive dependency, or unsafe build step, include the package name, affected version, and the path through which it is used.

## Safe Research Guidelines

Good-faith research is welcome when it stays within these boundaries:

- use only accounts, devices, data, and infrastructure that you own or have explicit permission to test
- avoid destructive actions, persistence, spam, phishing, social engineering, or denial-of-service testing
- minimize access to personal data and stop testing immediately if private data is exposed
- do not exfiltrate secrets or third-party data; report the minimum evidence needed to verify impact
- keep vulnerability details confidential until the maintainer has assessed the report

## Maintainer Response

The maintainer will review complete reports as availability allows, prioritize issues by exploitability and impact, and coordinate a fix or mitigation when the affected code is still maintained. For sample, archived, or educational repositories, the likely remediation may be documentation, dependency updates, or clearly marking unsupported code rather than a production-style patch release.

# Security policy

## Supported version

Security fixes target the current default branch.

## Reporting

Use [GitHub private vulnerability reporting](../../security/advisories/new).
Do not open a public issue containing credentials, exploit details, account IDs,
deployment URLs, state, or private data.

## Public-safety rules

- Never commit AWS credentials, Terraform state, variable values, deployment
  outputs, private contact details, or real customer text.
- Keep examples synthetic and generic.
- Preserve bounded-input, stable-error, scoped-IAM, log-retention, throttling,
  safety-scanning, dependency-review, and CodeQL gates.
- CI validates infrastructure and must not receive AWS apply credentials.

## Scope note

This educational lab is not a production security reference. Any real deployment
requires account-specific threat modeling and operational controls.

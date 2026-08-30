# Architecture and security boundaries

## Request path

1. API Gateway accepts `POST /predict` and forwards the HTTP API v2 payload.
2. Lambda accepts direct objects or the API Gateway string-body shape.
3. The boundary rejects malformed JSON, non-object bodies, non-string/blank text,
   and text longer than 2,000 characters.
4. The classifier tokenizes the bounded text, compares explicit positive and
   negative keyword matches, and returns the winning label or `NEUTRAL` on a tie.
5. The response names the `keyword_heuristic` method and matched evidence.

## Provisioning path

Terraform creates and connects the HTTP API, route, stage, integration, Lambda,
execution role, invoke permission, and log group. The archive provider packages
the single Lambda source file and its hash triggers code updates.

The module preserves the original AWS function, role, and API names to avoid an
unreviewed replacement in an account that may already contain these resources.

## Security and cost posture

- Lambda can create streams and write events only under its own CloudWatch group.
- Logs expire after 14 days.
- API Gateway applies a default rate of 10 requests/second and burst of 20.
- The handler returns stable client errors and does not serialize exceptions.
- CI performs validation only; it has no AWS credentials and cannot apply.
- Terraform state, variable values, credentials, generated archives, and internal
  assistant/specification artifacts are excluded from version control.

## Trust boundaries

The public internet/API boundary is untrusted. The lab demonstrates validation
and abuse-cost controls but does not implement authentication, authorization,
WAF, tenant isolation, or production monitoring. Those controls must be designed
before any real deployment.

## Future model seam

A real model integration is deliberately absent. Adding one would require a
separate specification covering endpoint lifecycle, scoped invocation permission,
timeouts/retries, payload contracts, model evaluation, observability, data
governance, privacy, budgets, and rollback.

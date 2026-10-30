---
title: "CO-197 Denial Code: Prior Authorization Absent"
meta_description: "CO-197 denial code explained: the X12 CARC 197 definition, why authorization-absent denials happen, how to fix them and how to prevent them. Request help."
slug: "/denial-codes/co-197/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What does denial code CO-197 mean?"
    a: "X12 defines CARC 197 as \"Precertification/authorization/notification/pre-treatment absent.\" The payer found no required authorization for the service."
  - q: "How do I fix a CO-197 denial?"
    a: "Check for an existing authorization and correct the claim if one exists; otherwise ask the payer about retro-authorization or appeal with documentation."
  - q: "What is the difference between CARC 197 and 198?"
    a: "X12 defines 197 as authorization absent and 198 as precertification, notification, authorization or pre-treatment exceeded."
  - q: "Are prior authorization denials worth appealing?"
    a: "Often. KFF data cited by the AMA shows 81.7% of appealed Medicare Advantage PA denials in 2023 were fully or partially overturned, though only 11.7% were appealed."
  - q: "How do I prevent CO-197 denials?"
    a: "Keep a PA matrix by payer and service, build authorization into scheduling, track units and expirations, and make sure authorization numbers reach the claim."
canonical: "https://medicalbillingteam.com/denial-codes/co-197/"
primary_keyword: "co 197 denial code"
secondary_keywords: []
search_intent: "informational"
audience: "billers, coders, AR and denial staff"
conversion_destination: "/checklist/"
pillar: "/denial-management/"
date_published: "2026-10-18"
date_modified: "2026-10-18"
author: "Medical Billing Team editors"  # brand byline; no invented persona
reviewer: ""  # TONY DECISION: real, authorized reviewer; render "Reviewed by" only when set
review_cadence: "quarterly + on rule change"
carc: "197"
carc_source: "https://x12.org/codes/claim-adjustment-reason-codes"
carc_checked: "2026-10-18"
semrush_volume_note: "no Semrush data in today's pull (volume TBD)"
coder_review: ""  # TONY DECISION: certified coder review before publish
tech_section:  # reusable <TechSection> component; edit here
  body: "Claim scrubbers and billing automation can catch many missing authorizations by matching scheduled services to authorization records before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-197 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# CO-197 denial code: meaning, causes and fixes

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** CO-197 means the payer found no required precertification, authorization, notification or pre-treatment approval for the service. X12 defines CARC 197 as "Precertification/authorization/notification/pre-treatment absent." First check whether an authorization actually exists and was left off the claim; if so, correct and resubmit. If none was obtained, ask about retro-authorization or appeal options, and fix the front-end process so it doesn't recur.

This guide explains denial code CO-197: the official definition, what usually causes it, how to fix it and how to prevent it. It's part of our [denial management](/denial-management/) guide and the [denial code guides](/denial-codes/) series.

## Official definition (X12 CARC 197)

Claim adjustment reason codes (CARCs) are maintained by X12 and describe "why a claim or service line was paid differently than it was billed." CARC 197 reads:

> "Precertification/authorization/notification/pre-treatment absent."

Source: [X12 Claim Adjustment Reason Codes](https://x12.org/codes/claim-adjustment-reason-codes), checked October 18, 2026. 

## What the "CO" prefix means

The letters before the number are a claim adjustment **group code**. X12 says group codes "generally assign responsibility for the adjustment amounts" and defines them as CO (Contractual Obligation), PR (Patient Responsibility), OA (Other Adjustment) and PI (Payer Initiated Reductions) ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). With CO, the adjustment is generally treated as the provider's responsibility under its payer contract rather than the patient's, so check your contract before billing the patient for a CO amount. The same reason code can appear with a different group code (for example PR or OA), which changes who is responsible.

## Common causes

- No authorization was requested before the service
- An authorization exists but the number wasn't on the claim
- The authorization was for a different provider, location, date range or service
- Authorized units or visits were exceeded (X12 uses CARC 198 for 'exceeded')
- The authorization expired (CARC 302 covers an expired time limit)

## How to fix it

1. Search your records and the payer portal for an existing authorization.
2. If found, correct the claim with the authorization number and resubmit.
3. If the authorization covers a different provider or service, check CARCs 284 and 296, which X12 uses when an authorization number may be valid but doesn't apply.
4. If none exists, ask the payer about retro-authorization or appeal, with documentation of medical necessity and urgency.
5. Feed the miss back to the PA owner.

## How to prevent it

- Maintain a prior authorization matrix by payer and service
- Make authorization part of scheduling, not an afterthought
- Track units, visits and expirations (see [prior authorization specialist and outsourcing](/prior-authorization-specialist/))
- Make sure authorization numbers flow onto claims automatically

## Who should work these denials

Denials need an owner with payer knowledge and time to follow up before deadlines. See [denial management](/denial-management/) and [what an AR specialist does](/ar-specialist/). If your team doesn't have the capacity, you can [request help](/contact/); requests may be referred to [Alliance Global Solutions](/approved-vendors/alliance-global-solutions/), which operates this site and is currently our only [approved vendor](/approved-vendors/). For A/R follow-up and denial rework capacity, see its [remote accounting staff](https://www.allianceglobalsolutions.com/virtual-assistant-skills/accounting/) page.

*This guide is general information, not coding or legal advice. Payer rules vary; check the payer's policy and the remark codes on your remittance.*

## Technology

Claim scrubbers and billing automation can catch many missing authorizations by matching scheduled services to authorization records before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-197 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [Denial management (hub)](/denial-management/)
- [CO-204: not covered under the plan](/denial-codes/co-204/)
- [CO-16: missing information](/denial-codes/co-16/)
- [What is revenue cycle management?](/what-is-revenue-cycle-management/)
- [CO-29 timely filing denials](/denial-codes/co-29/)

## FAQ

### What does denial code CO-197 mean?

X12 defines CARC 197 as "Precertification/authorization/notification/pre-treatment absent." The payer found no required authorization for the service.

### How do I fix a CO-197 denial?

Check for an existing authorization and correct the claim if one exists; otherwise ask the payer about retro-authorization or appeal with documentation.

### What is the difference between CARC 197 and 198?

X12 defines 197 as authorization absent and 198 as precertification, notification, authorization or pre-treatment exceeded.

### Are prior authorization denials worth appealing?

Often. KFF data cited by the AMA shows 81.7% of appealed Medicare Advantage PA denials in 2023 were fully or partially overturned, though only 11.7% were appealed.

### How do I prevent CO-197 denials?

Keep a PA matrix by payer and service, build authorization into scheduling, track units and expirations, and make sure authorization numbers reach the claim.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*

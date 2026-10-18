---
title: "CO-204 Denial Code: Not Covered Under Benefit Plan"
meta_description: "CO-204 denial code explained: the X12 CARC 204 definition, why services aren't covered under the patient's plan, what to check, and how to prevent it."
slug: "/denial-codes/co-204/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What does denial code CO-204 mean?"
    a: "X12 defines CARC 204 as \"This service/equipment/drug is not covered under the patient's current benefit plan.\""
  - q: "How do I fix a CO-204 denial?"
    a: "Confirm the exclusion with the payer, check coding, check whether a carve-out administrator should receive the claim, and ask about exceptions or appeals when clinically appropriate."
  - q: "Can I bill the patient for CO-204?"
    a: "Check your contract, any advance-notice rules and state law first. A CO group code generally indicates the adjustment is the provider's responsibility."
  - q: "How is CO-204 different from CO-22?"
    a: "CO-204 means the plan doesn't cover the service. CO-22 means another payer may be primary under coordination of benefits."
  - q: "How do I prevent CO-204 denials?"
    a: "Verify benefits for the specific service before it's provided, identify carve-outs, and give advance notice of non-covered services where rules allow."
canonical: "https://medicalbillingteam.com/denial-codes/co-204/"
primary_keyword: "co 204 denial code"
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
carc: "204"
carc_source: "https://x12.org/codes/claim-adjustment-reason-codes"
carc_checked: "2026-10-18"
semrush_volume_note: "co 204 denial code (260/mo), denial code 204 (210)"
coder_review: ""  # TONY DECISION: certified coder review before publish
tech_section:  # reusable <TechSection> component; edit here
  body: "Claim scrubbers and billing automation can catch many non-covered services through benefit checks before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-204 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# CO-204 denial code: meaning, causes and fixes

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** CO-204 means the service, equipment or drug isn't covered under the patient's current benefit plan. X12 defines CARC 204 as "This service/equipment/drug is not covered under the patient's current benefit plan." Check whether the plan really excludes the service, whether it was billed with the right codes, and whether a coverage exception or appeal applies. Prevent it by verifying benefits for the specific service before it's provided.

This guide explains denial code CO-204: the official definition, what usually causes it, how to fix it and how to prevent it. It's part of our [denial management](/denial-management/) guide and the [denial code guides](/denial-management/#denial-code-guides) series.

## Official definition (X12 CARC 204)

Claim adjustment reason codes (CARCs) are maintained by X12 and describe "why a claim or service line was paid differently than it was billed." CARC 204 reads:

> "This service/equipment/drug is not covered under the patient's current benefit plan"

Source: [X12 Claim Adjustment Reason Codes](https://x12.org/codes/claim-adjustment-reason-codes), checked October 18, 2026. 

## What the "CO" prefix means

The letters before the number are a claim adjustment **group code**. X12 says group codes "generally assign responsibility for the adjustment amounts" and defines them as CO (Contractual Obligation), PR (Patient Responsibility), OA (Other Adjustment) and PI (Payer Initiated Reductions) ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). With CO, the adjustment is generally treated as the provider's responsibility under its payer contract rather than the patient's, so check your contract before billing the patient for a CO amount. The same reason code can appear with a different group code (for example PR or OA), which changes who is responsible.

## Common causes

- The plan excludes the service (benefit exclusion)
- The service is covered only under a different benefit (for example, a carved-out behavioral health or pharmacy benefit)
- Coding doesn't reflect the covered service
- The patient changed plans and the new plan doesn't cover the service
- The service required a coverage exception that wasn't requested

## How to fix it

1. Confirm the exclusion with the payer and get the reference number.
2. Check coding: does a covered code accurately describe the service?
3. Check whether another benefit or administrator should receive the claim (carve-outs).
4. If clinically appropriate, ask about an exception or appeal process.
5. Before billing the patient, check your payer contract, any advance notice or waiver rules, and state law; CO generally indicates provider liability.

## How to prevent it

- Verify benefits for the specific service, not just active coverage
- Identify carve-outs during eligibility checks (see [treatment center VOB](/treatment-center-vob/))
- Give patients advance notice of non-covered services where your policies and payer rules allow

## Who should work these denials

Denials need an owner with payer knowledge and time to follow up before deadlines. See [denial management](/denial-management/) and [what an AR specialist does](/ar-specialist/). If your team doesn't have the capacity, you can [request help](/contact/); requests may be referred to Alliance Global Solutions, which operates this site and is currently our only [approved vendor](/approved-vendors/).

*This guide is general information, not coding or legal advice. Payer rules vary; check the payer's policy and the remark codes on your remittance.*

## Technology

Claim scrubbers and billing automation can catch many non-covered services through benefit checks before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-204 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [Denial management (hub)](/denial-management/)
- [CO-22: coordination of benefits](/denial-codes/co-22/)
- [CO-197: authorization absent](/denial-codes/co-197/)
- [What is revenue cycle management?](/what-is-revenue-cycle-management/)

## FAQ

### What does denial code CO-204 mean?

X12 defines CARC 204 as "This service/equipment/drug is not covered under the patient's current benefit plan."

### How do I fix a CO-204 denial?

Confirm the exclusion with the payer, check coding, check whether a carve-out administrator should receive the claim, and ask about exceptions or appeals when clinically appropriate.

### Can I bill the patient for CO-204?

Check your contract, any advance-notice rules and state law first. A CO group code generally indicates the adjustment is the provider's responsibility.

### How is CO-204 different from CO-22?

CO-204 means the plan doesn't cover the service. CO-22 means another payer may be primary under coordination of benefits.

### How do I prevent CO-204 denials?

Verify benefits for the specific service before it's provided, identify carve-outs, and give advance notice of non-covered services where rules allow.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*

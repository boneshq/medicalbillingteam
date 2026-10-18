---
title: "CO-97 Denial Code: Bundled Services Explained"
meta_description: "CO-97 denial code explained: the X12 CARC 97 definition, why a service was bundled into another payment, when modifiers apply, and how to fix it."
slug: "/denial-codes/co-97/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What does denial code CO-97 mean?"
    a: "X12 defines CARC 97 as \"The benefit for this service is included in the payment/allowance for another service/procedure that has already been adjudicated.\" The service was bundled."
  - q: "How do I fix a CO-97 denial?"
    a: "Find the service it was bundled into, review documentation, and if the service was separate and distinct, correct the claim with the appropriate modifier or appeal with documentation per payer policy."
  - q: "Should I add a modifier to every CO-97 line?"
    a: "No. Use modifiers only when documentation supports a separate, distinct service. Unsupported modifier use creates compliance risk."
  - q: "Can I bill the patient for a bundled service?"
    a: "Generally no. A CO adjustment indicates a contractual obligation rather than patient responsibility."
  - q: "How do I prevent CO-97 denials?"
    a: "Run code-pair edits before submission, train coders on payer bundling and modifier rules, and audit modifier use."
canonical: "https://medicalbillingteam.com/denial-codes/co-97/"
primary_keyword: "co 97 denial code"
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
carc: "97"
carc_source: "https://x12.org/codes/claim-adjustment-reason-codes"
carc_checked: "2026-10-18"
semrush_volume_note: "no Semrush data in today's pull (volume TBD)"
coder_review: ""  # TONY DECISION: certified coder review before publish
tech_section:  # reusable <TechSection> component; edit here
  body: "Claim scrubbers and billing automation can catch many bundling and modifier conflicts through edit checks before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-97 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# CO-97 denial code: meaning, causes and fixes

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** CO-97 means the payer considers the service bundled, meaning it's included in the payment for another service already processed. X12 defines CARC 97 as "The benefit for this service is included in the payment/allowance for another service/procedure that has already been adjudicated." Check payer bundling edits and documentation. If the service was truly separate and distinct, a correct modifier and supporting documentation may support a corrected claim or appeal.

This guide explains denial code CO-97: the official definition, what usually causes it, how to fix it and how to prevent it. It's part of our [denial management](/denial-management/) guide and the [denial code guides](/denial-management/#denial-code-guides) series.

## Official definition (X12 CARC 97)

Claim adjustment reason codes (CARCs) are maintained by X12 and describe "why a claim or service line was paid differently than it was billed." CARC 97 reads:

> "The benefit for this service is included in the payment/allowance for another service/procedure that has already been adjudicated."

Source: [X12 Claim Adjustment Reason Codes](https://x12.org/codes/claim-adjustment-reason-codes), checked October 18, 2026. 

## What the "CO" prefix means

The letters before the number are a claim adjustment **group code**. X12 says group codes "generally assign responsibility for the adjustment amounts" and defines them as CO (Contractual Obligation), PR (Patient Responsibility), OA (Other Adjustment) and PI (Payer Initiated Reductions) ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). With CO, the adjustment is generally treated as the provider's responsibility under its payer contract rather than the patient's, so check your contract before billing the patient for a CO amount. The same reason code can appear with a different group code (for example PR or OA), which changes who is responsible.

## Common causes

- The service is a component of another procedure billed on the same day
- Payer or national correct coding edits bundle the code pair
- A modifier indicating a separate, distinct service was missing or not supported
- The service was billed within a global period for a related procedure

## How to fix it

1. Identify which service it was bundled into (check the remittance and payer policy).
2. Review documentation: was the service separate and distinct?
3. If yes, correct the claim with the appropriate modifier per payer policy, or appeal with documentation.
4. If no, write the line off as a contractual adjustment; don't bill the patient for a CO amount.
5. Note payer-specific bundling rules for coders.

## How to prevent it

- Run code-pair edits before submission
- Train coders on modifier rules and payer policies (see [outsource medical coding](/hire-remote-medical-coders/))
- Audit modifier use regularly

## Who should work these denials

Denials need an owner with payer knowledge and time to follow up before deadlines. See [denial management](/denial-management/) and [what an AR specialist does](/ar-specialist/). If your team doesn't have the capacity, you can [request help](/contact/); requests may be referred to Alliance Global Solutions, which operates this site and is currently our only [approved vendor](/approved-vendors/).

*This guide is general information, not coding or legal advice. Payer rules vary; check the payer's policy and the remark codes on your remittance.*

## Technology

Claim scrubbers and billing automation can catch many bundling and modifier conflicts through edit checks before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-97 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [Denial management (hub)](/denial-management/)
- [CO-16: missing information](/denial-codes/co-16/)
- [CO-29: timely filing](/denial-codes/co-29/)
- [What is revenue cycle management?](/what-is-revenue-cycle-management/)

## FAQ

### What does denial code CO-97 mean?

X12 defines CARC 97 as "The benefit for this service is included in the payment/allowance for another service/procedure that has already been adjudicated." The service was bundled.

### How do I fix a CO-97 denial?

Find the service it was bundled into, review documentation, and if the service was separate and distinct, correct the claim with the appropriate modifier or appeal with documentation per payer policy.

### Should I add a modifier to every CO-97 line?

No. Use modifiers only when documentation supports a separate, distinct service. Unsupported modifier use creates compliance risk.

### Can I bill the patient for a bundled service?

Generally no. A CO adjustment indicates a contractual obligation rather than patient responsibility.

### How do I prevent CO-97 denials?

Run code-pair edits before submission, train coders on payer bundling and modifier rules, and audit modifier use.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*

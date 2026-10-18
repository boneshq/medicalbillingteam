---
title: "CO-22 Denial Code: Coordination of Benefits Fixes"
meta_description: "CO-22 denial code explained: the X12 CARC 22 definition, why coordination of benefits denials happen, and how to fix and prevent them. Free checklist."
slug: "/denial-codes/co-22/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What does denial code CO-22 mean?"
    a: "X12 defines CARC 22 as \"This care may be covered by another payer per coordination of benefits.\" The payer thinks another plan should pay first."
  - q: "How do I fix a CO-22 denial?"
    a: "Confirm the patient's other coverage and primary order, have the payer's COB record updated if needed, bill the primary first, then send the secondary claim with the primary's payment details."
  - q: "Who updates coordination of benefits with the insurer?"
    a: "Often the member must update COB directly with their plan. Your staff can explain what's needed and resubmit once it's updated."
  - q: "Are COB denials common?"
    a: "In a 2025 vendor survey of billing professionals, coordination of benefits was the most commonly cited denial reason, named by 45% of respondents."
  - q: "How do I prevent CO-22 denials?"
    a: "Ask about other coverage at every visit, review eligibility responses for other-coverage flags, and keep COB order current in your system."
canonical: "https://medicalbillingteam.com/denial-codes/co-22/"
primary_keyword: "co 22 denial code"
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
carc: "22"
carc_source: "https://x12.org/codes/claim-adjustment-reason-codes"
carc_checked: "2026-10-18"
semrush_volume_note: "co 22 denial code (880/mo)"
coder_review: ""  # TONY DECISION: certified coder review before publish
tech_section:  # reusable <TechSection> component; edit here
  body: "Claim scrubbers and billing automation can catch many coordination-of-benefits problems through up-front eligibility checks before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-22 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# CO-22 denial code: meaning, causes and fixes

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** CO-22 means the payer believes another plan should pay first under coordination of benefits (COB). X12 defines CARC 22 as "This care may be covered by another payer per coordination of benefits." To fix it, confirm the patient's other coverage and which plan is primary, update the payer and your system, bill the primary first, then send the secondary claim with the primary's payment information.

This guide explains denial code CO-22: the official definition, what usually causes it, how to fix it and how to prevent it. It's part of our [denial management](/denial-management/) guide and the [denial code guides](/denial-management/#denial-code-guides) series.

## Official definition (X12 CARC 22)

Claim adjustment reason codes (CARCs) are maintained by X12 and describe "why a claim or service line was paid differently than it was billed." CARC 22 reads:

> "This care may be covered by another payer per coordination of benefits."

Source: [X12 Claim Adjustment Reason Codes](https://x12.org/codes/claim-adjustment-reason-codes), checked October 18, 2026. 

## What the "CO" prefix means

The letters before the number are a claim adjustment **group code**. X12 says group codes "generally assign responsibility for the adjustment amounts" and defines them as CO (Contractual Obligation), PR (Patient Responsibility), OA (Other Adjustment) and PI (Payer Initiated Reductions) ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). With CO, the adjustment is generally treated as the provider's responsibility under its payer contract rather than the patient's, so check your contract before billing the patient for a CO amount. The same reason code can appear with a different group code (for example PR or OA), which changes who is responsible.

## Common causes

- The patient has other coverage (spouse's plan, employer plan, Medicare, Medicaid) that the payer lists as primary
- The payer's COB record is outdated or incomplete
- The patient didn't report other coverage at registration
- Medicare Secondary Payer situations (for example, employer coverage or liability) not identified
- The secondary claim was sent without the primary's remittance information

## How to fix it

1. Ask the patient about all current coverage and confirm which plan is primary (birthday rule, employment status, Medicare rules as applicable).
2. Have the patient update their COB information with the payer if the payer's record is wrong; many payers require the member to do this.
3. Bill the primary payer first.
4. Send the secondary claim with the primary payment and adjustment details.
5. Track the claim against timely filing limits while COB is being resolved.

## How to prevent it

- Ask about other coverage at every registration, not just new patients
- Use eligibility responses to spot other-coverage flags before the visit (see [insurance verification services](/eligibility-verification-prior-authorization/))
- Update COB order in your system as soon as it changes
- Train front-desk and [virtual receptionist](/virtual-medical-receptionist/) scripts to ask the COB questions

## Who should work these denials

Denials need an owner with payer knowledge and time to follow up before deadlines. See [denial management](/denial-management/) and [what an AR specialist does](/ar-specialist/). If your team doesn't have the capacity, you can [request help](/contact/); requests may be referred to [Alliance Global Solutions](/approved-vendors/alliance-global-solutions/), which operates this site and is currently our only [approved vendor](/approved-vendors/). For A/R follow-up and denial rework capacity, see its [remote accounting staff](https://www.allianceglobalsolutions.com/virtual-assistant-skills/accounting/) page.

*This guide is general information, not coding or legal advice. Payer rules vary; check the payer's policy and the remark codes on your remittance.*

## Technology

Claim scrubbers and billing automation can catch many coordination-of-benefits problems through up-front eligibility checks before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-22 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [Denial management (hub)](/denial-management/)
- [CO-16: missing information](/denial-codes/co-16/)
- [CO-204: not covered under the plan](/denial-codes/co-204/)
- [What is revenue cycle management?](/what-is-revenue-cycle-management/)
- [CO-29 timely filing denials](/denial-codes/co-29/)

## FAQ

### What does denial code CO-22 mean?

X12 defines CARC 22 as "This care may be covered by another payer per coordination of benefits." The payer thinks another plan should pay first.

### How do I fix a CO-22 denial?

Confirm the patient's other coverage and primary order, have the payer's COB record updated if needed, bill the primary first, then send the secondary claim with the primary's payment details.

### Who updates coordination of benefits with the insurer?

Often the member must update COB directly with their plan. Your staff can explain what's needed and resubmit once it's updated.

### Are COB denials common?

In a 2025 vendor survey of billing professionals, coordination of benefits was the most commonly cited denial reason, named by 45% of respondents.

### How do I prevent CO-22 denials?

Ask about other coverage at every visit, review eligibility responses for other-coverage flags, and keep COB order current in your system.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*

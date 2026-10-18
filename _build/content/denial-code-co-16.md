---
title: "CO-16 Denial Code: Meaning, Causes and How to Fix"
meta_description: "CO-16 denial code explained: the X12 CARC 16 definition, why claims get it, how to read the remark code, and how to fix and prevent it. Free checklist."
slug: "/denial-codes/co-16/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What does denial code CO-16 mean?"
    a: "X12 defines CARC 16 as \"Claim/service lacks information or has submission/billing error(s).\" With group code CO, the adjustment is generally the provider's responsibility under its contract."
  - q: "How do I find out what's missing on a CO-16 denial?"
    a: "Look at the remark code (RARC) on the remittance. X12 requires at least one remark code with CARC 16, and it identifies the missing or invalid information."
  - q: "Should I appeal a CO-16 denial?"
    a: "Usually not. CO-16 is typically corrected and resubmitted. Follow the payer's corrected-claim rules and watch the timely filing limit."
  - q: "Can I bill the patient for a CO-16 adjustment?"
    a: "Generally no. CO indicates a contractual obligation rather than patient responsibility. Fix and resubmit the claim instead."
  - q: "How do I prevent CO-16 denials?"
    a: "Scrub claims for required fields, verify demographics and insurance at every visit, keep provider identifiers current with payers, and track recurring remark codes."
canonical: "https://medicalbillingteam.com/denial-codes/co-16/"
primary_keyword: "co 16 denial code"
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
carc: "16"
carc_source: "https://x12.org/codes/claim-adjustment-reason-codes"
carc_checked: "2026-10-18"
semrush_volume_note: "co 16 denial code (1,600/mo), co 16 (720), co16 denial code description (590), denial code co-16 (480)"
coder_review: ""  # TONY DECISION: certified coder review before publish
tech_section:  # reusable <TechSection> component; edit here
  body: "Claim scrubbers and billing automation can catch many missing or invalid data errors before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-16 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# CO-16 denial code: meaning, causes and fixes

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** CO-16 means the payer couldn't process the claim or line because information was missing or there was a submission or billing error. X12 defines CARC 16 as "Claim/service lacks information or has submission/billing error(s)." The fix is in the remark code (RARC) that must accompany it: it tells you exactly what's missing. Correct that item and resubmit, usually as a corrected or new claim per the payer's rules.

This guide explains denial code CO-16: the official definition, what usually causes it, how to fix it and how to prevent it. It's part of our [denial management](/denial-management/) guide and the [denial code guides](/denial-management/#denial-code-guides) series.

## Official definition (X12 CARC 16)

Claim adjustment reason codes (CARCs) are maintained by X12 and describe "why a claim or service line was paid differently than it was billed." CARC 16 reads:

> "Claim/service lacks information or has submission/billing error(s)."

Source: [X12 Claim Adjustment Reason Codes](https://x12.org/codes/claim-adjustment-reason-codes), checked October 18, 2026. X12 adds that at least one Remark Code must be provided with CARC 16 (a Remittance Advice Remark Code, or RARC, or an NCPDP reject reason), and that the code should not be used for claims attachments or other documentation.

## What the "CO" prefix means

The letters before the number are a claim adjustment **group code**. X12 says group codes "generally assign responsibility for the adjustment amounts" and defines them as CO (Contractual Obligation), PR (Patient Responsibility), OA (Other Adjustment) and PI (Payer Initiated Reductions) ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). With CO, the adjustment is generally treated as the provider's responsibility under its payer contract rather than the patient's, so check your contract before billing the patient for a CO amount. The same reason code can appear with a different group code (for example PR or OA), which changes who is responsible.

## Common causes

- Missing or invalid patient demographics (name, date of birth, member ID mismatch)
- Missing or invalid provider identifiers (rendering, referring or billing NPI; taxonomy)
- Missing or invalid diagnosis pointer, place of service or modifier
- Missing information the payer requires for that service (for example, units, dates, NDC for drugs)
- Missing prior-payer information on a secondary claim
- Formatting errors that passed the clearinghouse but failed payer edits

## How to fix it

1. Read the RARC(s) on the remittance first; CO-16 alone doesn't say what's missing.
2. Fix the specific field in the practice management system so it doesn't recur on future claims.
3. Resubmit as the payer instructs (many treat CO-16 as a correct-and-resubmit, not an appeal).
4. Track resubmission against the payer's timely filing limit.
5. Log the RARC and root cause so the front desk, coders or charge entry can prevent it.

## How to prevent it

- Scrub claims for required fields before submission
- Verify demographics and insurance at every visit
- Keep provider NPI/taxonomy data current with each payer (see [credentialing services](/credentialing-services/))
- Build payer-specific edits for frequent RARCs

## Who should work these denials

Denials need an owner with payer knowledge and time to follow up before deadlines. See [denial management](/denial-management/) and [what an AR specialist does](/ar-specialist/). If your team doesn't have the capacity, you can [request help](/contact/); requests may be referred to [Alliance Global Solutions](/approved-vendors/alliance-global-solutions/), which operates this site and is currently our only [approved vendor](/approved-vendors/). For A/R follow-up and denial rework capacity, see its [remote accounting staff](https://www.allianceglobalsolutions.com/virtual-assistant-skills/accounting/) page.

*This guide is general information, not coding or legal advice. Payer rules vary; check the payer's policy and the remark codes on your remittance.*

## Technology

Claim scrubbers and billing automation can catch many missing or invalid data errors before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-16 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [Denial management (hub)](/denial-management/)
- [CO-22: coordination of benefits](/denial-codes/co-22/)
- [CO-197: authorization absent](/denial-codes/co-197/)
- [What is revenue cycle management?](/what-is-revenue-cycle-management/)
- [CO-29 timely filing denials](/denial-codes/co-29/)

## FAQ

### What does denial code CO-16 mean?

X12 defines CARC 16 as "Claim/service lacks information or has submission/billing error(s)." With group code CO, the adjustment is generally the provider's responsibility under its contract.

### How do I find out what's missing on a CO-16 denial?

Look at the remark code (RARC) on the remittance. X12 requires at least one remark code with CARC 16, and it identifies the missing or invalid information.

### Should I appeal a CO-16 denial?

Usually not. CO-16 is typically corrected and resubmitted. Follow the payer's corrected-claim rules and watch the timely filing limit.

### Can I bill the patient for a CO-16 adjustment?

Generally no. CO indicates a contractual obligation rather than patient responsibility. Fix and resubmit the claim instead.

### How do I prevent CO-16 denials?

Scrub claims for required fields, verify demographics and insurance at every visit, keep provider identifiers current with payers, and track recurring remark codes.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*

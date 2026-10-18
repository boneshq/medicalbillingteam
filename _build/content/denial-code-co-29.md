---
title: "CO-29 Denial Code: Timely Filing Limit Expired"
meta_description: "CO-29 denial code explained: the X12 CARC 29 definition, Medicare's one-year filing limit, when proof of timely filing helps, and how to prevent it."
slug: "/denial-codes/co-29/"
schema_type: ["Article", "FAQPage", "BreadcrumbList"]
faq:
  - q: "What does denial code CO-29 mean?"
    a: "X12 defines CARC 29 as \"The time limit for filing has expired.\" The payer received the claim after its filing deadline."
  - q: "What is Medicare's timely filing limit?"
    a: "CMS sets it at one calendar year from the date of service. Commercial payer limits vary by contract and are often shorter."
  - q: "Can a CO-29 denial be overturned?"
    a: "Sometimes, if you can prove the claim was filed on time, for example with clearinghouse acceptance reports, or if an exception such as retroactive eligibility applies."
  - q: "Can I bill the patient for a timely filing denial?"
    a: "Generally no. A CO adjustment indicates a contractual obligation rather than patient responsibility."
  - q: "How do I prevent CO-29 denials?"
    a: "Track payer filing limits, work clearinghouse rejections daily, follow up on A/R by age, and keep COB and credentialing delays from holding claims too long."
canonical: "https://medicalbillingteam.com/denial-codes/co-29/"
primary_keyword: "co 29 denial code"
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
carc: "29"
carc_source: "https://x12.org/codes/claim-adjustment-reason-codes"
carc_checked: "2026-10-18"
semrush_volume_note: "no Semrush data in today's pull (volume TBD)"
coder_review: ""  # TONY DECISION: certified coder review before publish
tech_section:  # reusable <TechSection> component; edit here
  body: "Claim scrubbers and billing automation can catch many claims nearing the filing limit through timely-filing alerts before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-29 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff."
  link: "/medical-billing-technology/"
---

# CO-29 denial code: meaning, causes and fixes

*By the Medical Billing Team editors · Published October 18, 2026 · Updated October 18, 2026 · [How we research and review](/about/#how-we-write-our-guides)*

**Short answer:** CO-29 means the claim was received after the payer's filing deadline. X12 defines CARC 29 as "The time limit for filing has expired." For Medicare, the limit is one calendar year from the date of service. If you have proof the claim was filed on time (clearinghouse acceptance reports, prior submissions), appeal with that proof. Otherwise the amount is usually written off, so prevention matters most.

This guide explains denial code CO-29: the official definition, what usually causes it, how to fix it and how to prevent it. It's part of our [denial management](/denial-management/) guide and the [denial code guides](/denial-management/#denial-code-guides) series.

## Official definition (X12 CARC 29)

Claim adjustment reason codes (CARCs) are maintained by X12 and describe "why a claim or service line was paid differently than it was billed." CARC 29 reads:

> "The time limit for filing has expired."

Source: [X12 Claim Adjustment Reason Codes](https://x12.org/codes/claim-adjustment-reason-codes), checked October 18, 2026. 

## What the "CO" prefix means

The letters before the number are a claim adjustment **group code**. X12 says group codes "generally assign responsibility for the adjustment amounts" and defines them as CO (Contractual Obligation), PR (Patient Responsibility), OA (Other Adjustment) and PI (Payer Initiated Reductions) ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). With CO, the adjustment is generally treated as the provider's responsibility under its payer contract rather than the patient's, so check your contract before billing the patient for a CO amount. The same reason code can appear with a different group code (for example PR or OA), which changes who is responsible.

## Common causes

- The claim was never submitted, or was rejected and never corrected
- A rejection at the clearinghouse wasn't noticed
- Coordination of benefits delays pushed the secondary claim past its limit
- Corrected claims were sent after the payer's corrected-claim deadline
- Credentialing delays held claims too long

## How to fix it

1. Gather proof of timely filing: clearinghouse acceptance reports, payer acknowledgment, or prior submission records.
2. Appeal with that proof if it exists, following the payer's process.
3. Check whether an exception applies (for example, retroactive eligibility or payer error).
4. If no proof or exception exists, write off as a contractual adjustment; don't bill the patient for a CO amount.
5. Log the root cause.

## How to prevent it

- Track filing limits for every major payer; Medicare's is one calendar year from the date of service ([CMS](https://www.cms.gov/regulations-and-guidance/guidance/manuals/downloads/clm104c01.pdf))
- Work clearinghouse rejections daily
- Work A/R by age so claims don't sit (see [days in AR](/reduce-ar-days/))
- Hold claims for credentialing only with a plan and a deadline

## Who should work these denials

Denials need an owner with payer knowledge and time to follow up before deadlines. See [denial management](/denial-management/) and [what an AR specialist does](/ar-specialist/). If your team doesn't have the capacity, you can [request help](/contact/); requests may be referred to [Alliance Global Solutions](/approved-vendors/alliance-global-solutions/), which operates this site and is currently our only [approved vendor](/approved-vendors/). For A/R follow-up and denial rework capacity, see its [remote accounting staff](https://www.allianceglobalsolutions.com/virtual-assistant-skills/accounting/) page.

*This guide is general information, not coding or legal advice. Payer rules vary; check the payer's policy and the remark codes on your remittance.*

## Technology

Claim scrubbers and billing automation can catch many claims nearing the filing limit through timely-filing alerts before a claim goes out, and denial-prediction tools flag claims that payers have rejected for CO-29 in the past. Group and reason codes come from the standard X12 code list, so remits can be routed automatically to the right work queue ([X12](https://x12.org/codes/claim-adjustment-reason-codes)). A person still has to fix the underlying cause and resubmit or appeal. Alliance Global Solutions helps clients set up AI assistant workflows alongside their dedicated staff. [Latest updates in medical billing technology →](/medical-billing-technology/)

## Related guides

- [Denial management (hub)](/denial-management/)
- [CO-16: missing information](/denial-codes/co-16/)
- [CO-97: bundled services](/denial-codes/co-97/)
- [What is revenue cycle management?](/what-is-revenue-cycle-management/)
- [CO-22 coordination of benefits](/denial-codes/co-22/)

## FAQ

### What does denial code CO-29 mean?

X12 defines CARC 29 as "The time limit for filing has expired." The payer received the claim after its filing deadline.

### What is Medicare's timely filing limit?

CMS sets it at one calendar year from the date of service. Commercial payer limits vary by contract and are often shorter.

### Can a CO-29 denial be overturned?

Sometimes, if you can prove the claim was filed on time, for example with clearinghouse acceptance reports, or if an exception such as retroactive eligibility applies.

### Can I bill the patient for a timely filing denial?

Generally no. A CO adjustment indicates a contractual obligation rather than patient responsibility.

### How do I prevent CO-29 denials?

Track payer filing limits, work clearinghouse rejections daily, follow up on A/R by age, and keep COB and credentialing delays from holding claims too long.

---
*Affiliation disclosure: Medical Billing Team is operated by Alliance Global Solutions, a provider of remote medical billing and revenue cycle staff and currently the only vendor on our [approved vendor list](/approved-vendors/). Requests submitted here may be referred to Alliance Global Solutions, and we benefit if you hire it. We may contact you about our services if you request it. [How we vet vendors](/how-we-vet-vendors/).*

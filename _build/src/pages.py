"""Site map (flat, keyword-led slugs; matches the copywriter's internal links).
key = content filename in content/<key>.md (home = index). A page with no content file
is a STUB: noindex, excluded from sitemap.xml/llms.txt, placeholder text only."""

def P(key, path, label, kind, parent, title, description):
    return dict(key=key, path=path, label=label, kind=kind, parent=parent, title=title, description=description)

PAGES = [
  P("index", "/", "Home", "home", None,
    "Medical Billing Team: Remote Billing & RCM Staffing",
    "Plain-English guides for US practices on medical billing staffing, remote RCM teams, HIPAA safeguards and costs."),
  # Pillar: medical billing staffing (outsourced / offshore / remote billers)
  P("medical-billing-staffing", "/medical-billing-staffing/", "Medical Billing Staffing", "pillar", None,
    "Medical Billing Staffing: In-House, Outsourced, Remote and Offshore",
    "How US practices staff medical billing: in-house, outsourced, remote and offshore billers, and how to choose."),
  P("hire-remote-medical-billers", "/hire-remote-medical-billers/", "Hire Remote Medical Billers", "cluster", "medical-billing-staffing",
    "How to Hire Remote Medical Billers", "What to look for when hiring a remote medical biller and how to onboard one."),
  P("outsourced-medical-billers", "/outsourced-medical-billers/", "Outsourced Medical Billers", "cluster", "medical-billing-staffing",
    "Outsourced Medical Billers: What They Do and When It Fits", "What outsourced medical billers handle and questions to ask before you outsource."),
  P("offshore-medical-billing", "/offshore-medical-billing/", "Offshore Medical Billing", "cluster", "medical-billing-staffing",
    "Offshore Medical Billing Staff: A Practical Guide", "How offshore medical billing staffing works for US practices: oversight, security and coverage."),
  P("behavioral-health-billing", "/behavioral-health-billing/", "Behavioral Health Billing", "cluster", "medical-billing-staffing",
    "Behavioral Health Billing Staff", "Staffing billing for behavioral health and therapy practices."),
  # Pillar: RCM staffing
  P("revenue-cycle-management-staffing", "/revenue-cycle-management-staffing/", "RCM Staffing", "pillar", None,
    "Revenue Cycle Management Staffing: Roles, KPIs, Costs",
    "RCM staffing explained: the workflow, roles, KPIs and how to compare in-house, outsourced and offshore RCM teams."),
  P("medical-coders", "/medical-coders/", "Medical Coders", "cluster", "revenue-cycle-management-staffing",
    "Remote Medical Coders: Roles, Credentials and Hiring", "What remote medical coders do, common credentials and how practices staff coding."),
  P("ar-specialists", "/ar-specialists/", "A/R Specialists", "cluster", "revenue-cycle-management-staffing",
    "A/R Follow-Up Specialists for Medical Billing", "How A/R follow-up specialists work aged claims and what a dedicated A/R role covers."),
  P("reduce-ar-days", "/reduce-ar-days/", "Reduce A/R Days", "cluster", "revenue-cycle-management-staffing",
    "How to Reduce A/R Days", "Practical steps to reduce days in accounts receivable."),
  P("denial-management", "/denial-management/", "Denial Management", "cluster", "revenue-cycle-management-staffing",
    "Denial Management Staffing", "How denial management staff triage, appeal and prevent claim denials."),
  P("credentialing", "/credentialing/", "Credentialing", "cluster", "revenue-cycle-management-staffing",
    "Provider Credentialing Specialists", "What credentialing and payer enrollment specialists handle."),
  P("eligibility-verification-prior-authorization", "/eligibility-verification-prior-authorization/", "Eligibility & Prior Authorization", "cluster", "revenue-cycle-management-staffing",
    "Eligibility Verification and Prior Authorization Staff", "How eligibility (VOB) and prior authorization staff fit into the revenue cycle."),
  P("virtual-medical-assistants", "/virtual-medical-assistants/", "Virtual Medical Assistants", "cluster", "revenue-cycle-management-staffing",
    "Virtual Medical Assistants for Front-Office and Billing Support", "What virtual medical assistants can take on for scheduling, intake and billing support."),
  P("medical-billing-outsourcing", "/medical-billing-outsourcing/", "Medical Billing Outsourcing", "cluster", "revenue-cycle-management-staffing",
    "Medical Billing Outsourcing vs. Dedicated Staff", "Compare full medical billing outsourcing with dedicated remote billing staff."),
  # Pillars: HIPAA, cost
  P("hipaa-outsourced-medical-billing", "/hipaa-outsourced-medical-billing/", "HIPAA Guide", "pillar", None,
    "HIPAA and Outsourced Medical Billing Staff: A Guide", "HIPAA when hiring outsourced or offshore billing staff: BAAs, minimum necessary, access controls."),
  P("medical-billing-staffing-cost", "/medical-billing-staffing-cost/", "Cost Comparison", "pillar", None,
    "Medical Billing Staffing Cost: In-House vs. Outsourced vs. Remote", "How to compare the cost of in-house billing staff, billing companies and remote staff."),
  # Supporting
  P("how-it-works", "/how-it-works/", "How It Works", "page", None, "How It Works", "How a remote billing staffing engagement works."),
  P("faq", "/faq/", "FAQ", "page", None, "Medical Billing Staffing FAQ", "Answers to common questions about medical billing and RCM staffing."),
  P("checklist", "/checklist/", "Free Checklist", "page", None, "Medical Billing Health Checklist", "A one-page self-audit for billing and RCM."),
  P("about", "/about/", "About & Disclosure", "page", None, "About This Site and Disclosure", "Who runs this site and our disclosure."),
  P("contact", "/contact/", "Contact", "form", None, "Free Medical Billing Staffing Assessment | Contact", "Request a free staffing assessment. No patient information."),
  P("privacy", "/privacy/", "Privacy", "legal", None, "Privacy Policy", "How this site collects and uses information."),
  P("terms", "/terms/", "Terms", "legal", None, "Terms of Use", "Terms of use for this site."),
  P("thank-you", "/thank-you/", "Thank You", "utility", None, "Thank You", "We received your request."),
]

NAV = [
  ("Billing Staffing", "medical-billing-staffing"),
  ("RCM Staffing", "revenue-cycle-management-staffing"),
  ("HIPAA", "hipaa-outsourced-medical-billing"),
  ("Costs", "medical-billing-staffing-cost"),
  ("How It Works", "how-it-works"),
  ("FAQ", "faq"),
]

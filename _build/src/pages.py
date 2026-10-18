"""Site map (flat, keyword-led slugs; matches the copywriter's internal links).
key = content filename in content/<key>.md (home = index). A page with no content file
is a STUB: noindex, excluded from sitemap.xml/llms.txt, placeholder text only."""

def P(key, path, label, kind, parent, title, description):
    return dict(key=key, path=path, label=label, kind=kind, parent=parent, title=title, description=description)

PAGES = [
  P("index", "/", "Home", "home", None,
    "Medical Billing Team: Remote Billing & RCM Staffing",
    "Plain-English guides for US practices on medical billing staffing, remote RCM teams, HIPAA safeguards and costs."),
  # P1 (MAJOR): RCM staffing
  P("revenue-cycle-management-staffing", "/revenue-cycle-management-staffing/", "RCM Staffing", "pillar", None,
    "Revenue Cycle Management Staffing: Roles, KPIs, Costs", "RCM staffing: workflow, roles, KPIs and costs."),
  P("denial-management", "/denial-management/", "Denial Management", "cluster", "revenue-cycle-management-staffing",
    "Denial Management Basics", "Denial management workflow and staffing."),
  P("reduce-ar-days", "/reduce-ar-days/", "Reduce A/R Days", "cluster", "revenue-cycle-management-staffing",
    "How to Reduce AR Days", "A/R workflow and staffing guide."),
  P("eligibility-verification-prior-authorization", "/eligibility-verification-prior-authorization/", "Eligibility & Prior Authorization", "cluster", "revenue-cycle-management-staffing",
    "Eligibility Verification & Prior Authorization Staffing", "Front-end workflows and staffing."),
  P("hire-remote-medical-coders", "/hire-remote-medical-coders/", "Medical Coders", "cluster", "revenue-cycle-management-staffing",
    "Hiring Remote Medical Coders", "Credentials, testing and security for remote medical coders."),
  P("ar-specialist", "/ar-specialist/", "A/R Specialists", "cluster", "revenue-cycle-management-staffing",
    "What Does an AR Specialist Do?", "The A/R follow-up role and when to hire one."),
  P("credentialing-specialist", "/credentialing-specialist/", "Credentialing", "cluster", "revenue-cycle-management-staffing",
    "Credentialing Specialist: Role, Timeline, Outsourcing", "What credentialing specialists do and how the work is staffed."),
  P("prior-authorization-specialist", "/prior-authorization-specialist/", "Prior Authorization Specialists", "cluster", "revenue-cycle-management-staffing",
    "Prior Authorization Specialist: Hiring Guide", "How to hire and onboard prior authorization staff."),
  # P2: medical billing staffing / outsourced, offshore, remote billers
  P("hire-remote-medical-billers", "/hire-remote-medical-billers/", "Billing Staffing", "pillar", None,
    "Hiring Remote and Offshore Medical Billers: A Guide", "What to look for when hiring remote and offshore medical billers."),
  P("medical-billing-outsourcing", "/medical-billing-outsourcing/", "Medical Billing Outsourcing", "cluster", "hire-remote-medical-billers",
    "Medical Billing Outsourcing: The 3 Models Compared", "Billing company vs. staffing vs. in-house."),
  P("offshore-medical-billers", "/offshore-medical-billers/", "Offshore Medical Billers", "cluster", "hire-remote-medical-billers",
    "Offshore Medical Billers: Pros, Cons, Safeguards", "How offshore billing staff work and what to check."),
  P("virtual-medical-assistant", "/virtual-medical-assistant/", "Virtual Medical Assistants", "cluster", "hire-remote-medical-billers",
    "Virtual Medical Assistants for Billing and Front Office", "What virtual medical assistants can take on."),
  # P3 HIPAA, P4 cost, P7 specialty
  P("hipaa-outsourced-medical-billing", "/hipaa-outsourced-medical-billing/", "HIPAA Guide", "pillar", None,
    "HIPAA and Outsourced Medical Billing Staff: A Guide", "HIPAA when hiring outsourced or offshore billing staff."),
  P("medical-billing-staffing-cost", "/medical-billing-staffing-cost/", "Cost Comparison", "pillar", None,
    "Medical Billing Staffing Cost: In-House vs Outsourced", "Compare in-house, billing company and remote staff costs."),
  P("behavioral-health-billing", "/behavioral-health-billing/", "Behavioral Health Billing", "pillar", None,
    "Behavioral Health & Treatment Center Billing Staff", "Billing and staffing for behavioral health practices and treatment centers."),
  # Supporting
  # Directory (positioning change, Tony via CEO/AG 2026-10-18 12:51 PM ET; LVNY hub + light vendor directory)
  P("approved-vendors", "/approved-vendors/", "Approved Vendors", "directory", None,
    "Approved Medical Billing Staffing Vendors", "Vetted medical billing and RCM staffing vendors, and how we vet them."),
  P("alliance-global-solutions", "/approved-vendors/alliance-global-solutions/", "Alliance Global Solutions", "vendor", "approved-vendors",
    "Alliance Global Solutions: Featured Vendor Profile", "Remote medical billing and RCM staff from Alliance Global Solutions."),
  P("how-we-vet-vendors", "/how-we-vet-vendors/", "How We Vet Vendors", "page", "approved-vendors",
    "How We Vet Medical Billing Staffing Vendors", "The checks a vendor must pass before we list it."),
  P("how-it-works", "/how-it-works/", "How It Works", "page", None, "How It Works", "How a remote billing staffing engagement works."),
  P("faq", "/faq/", "FAQ", "page", None, "Medical Billing Staffing FAQ", "Common questions."),
  P("checklist", "/checklist/", "Free Checklist", "page", None, "Medical Billing Health Checklist", "A one-page billing self-audit."),
  P("about", "/about/", "About & Disclosure", "page", None, "About This Site and Disclosure", "Who runs this site."),
  P("contact", "/contact/", "Contact", "form", None, "Free Medical Billing Staffing Assessment | Contact", "Request a free staffing assessment."),
  P("privacy", "/privacy/", "Privacy", "legal", None, "Privacy Policy", "Privacy policy."),
  P("terms", "/terms/", "Terms", "legal", None, "Terms of Use", "Terms of use."),
  P("thank-you", "/thank-you/", "Thank You", "utility", None, "Thank You", "We received your request."),
]

NAV = [
  ("Billing Staffing", "hire-remote-medical-billers"),
  ("RCM Staffing", "revenue-cycle-management-staffing"),
  ("HIPAA", "hipaa-outsourced-medical-billing"),
  ("Costs", "medical-billing-staffing-cost"),
  ("Approved Vendors", "approved-vendors"),
  ("FAQ", "faq"),
]

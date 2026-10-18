"""
Curated industry news datasets designed for PR & Communications analysis.
Includes realistic multi-source coverage with syndicated press releases,
competing news outlets with divergent editorial angles, and varying signal levels.
"""

from typing import List, Dict, Any

PRESET_DATASETS: Dict[str, Dict[str, Any]] = {
    "tech_ai_wave": {
        "title": "Tech & AI Ecosystem: Frontier Models, Hardware & Market Moves",
        "category": "Technology & AI",
        "description": "22 articles covering 4 core developments: Frontier Model Launch, Semiconductor Export Controls, AI Search Engine Wars, and an Executive Departures wave. Contains verbatim wire syndications and divergent tech/business angles.",
        "default_keywords": ["OpenAI", "NVIDIA", "Google", "Frontier", "Chips", "Search", "Antitrust"],
        "articles": [
            # Story 1: Nova-4 Frontier Model Announcement (Cluster A - 6 articles)
            {
                "id": "art-001",
                "title": "ApexAI Unveils Nova-4: Multimodal Frontier Model With Native Scientific Reasoning",
                "source": "ApexAI Official Press Wire",
                "url": "https://wire.apexai.example/news/nova-4-announcement",
                "date": "2026-10-17 09:00",
                "author": "ApexAI Communications",
                "content": "SAN FRANCISCO — Today ApexAI announced Nova-4, our flagship frontier intelligence model engineered from first principles for deep multimodal understanding and autonomous scientific discovery. Nova-4 establishes new state-of-the-art benchmarks on graduate-level STEM benchmarks, solving advanced biophysics and quantum chemistry equations with 42% fewer hallucinations than previous generations. Enterprise availability begins immediately via the Apex Cloud API, with dedicated HIPAA and SOC2 Type II compliance controls for bio-pharmaceutical research partners."
            },
            {
                "id": "art-002",
                "title": "ApexAI Unveils Nova-4: Multimodal Frontier Model With Native Scientific Reasoning",
                "source": "TechNewswire Global",
                "url": "https://technewswire.example/press/apexai-nova-4-stem",
                "date": "2026-10-17 09:05",
                "author": "Syndicated Press Service",
                "content": "SAN FRANCISCO — Today ApexAI announced Nova-4, our flagship frontier intelligence model engineered from first principles for deep multimodal understanding and autonomous scientific discovery. Nova-4 establishes new state-of-the-art benchmarks on graduate-level STEM benchmarks, solving advanced biophysics and quantum chemistry equations with 42% fewer hallucinations than previous generations. Enterprise availability begins immediately via the Apex Cloud API."
            },
            {
                "id": "art-003",
                "title": "ApexAI Unveils Nova-4: Frontier Model With Native Scientific Reasoning",
                "source": "MarketWatch Wire Feed",
                "url": "https://marketwatch.example/syndication/apexai-nova4",
                "date": "2026-10-17 09:12",
                "author": "Automated Wire Desk",
                "content": "SAN FRANCISCO (MarketWatch) — ApexAI has released Nova-4, a flagship artificial intelligence model targeting enterprise science and chemistry applications. The company claims 42% lower hallucination rates on STEM tests and instant enterprise API rollout. Financial terms of partner deployment with pharmaceutical giants were not disclosed."
            },
            {
                "id": "art-004",
                "title": "Nova-4 Hands-On: ApexAI Pushes Into Pharma Research, But Enterprise Pricing Raises Eyebrows",
                "source": "The Tech Insider",
                "url": "https://techinsider.example/analysis/nova-4-review-enterprise-pricing",
                "date": "2026-10-17 11:30",
                "author": "Elena Vance, Senior Enterprise Editor",
                "content": "ApexAI's launch of Nova-4 this morning is less about consumer chatbots and entirely about defending its high-margin enterprise flank against open-source challengers. While the benchmark gains in molecular modeling and quantum chemistry are indisputably impressive, early enterprise testers privately expressed dismay over token pricing, which stands nearly 3x higher than rival models. 'They are targeting Fortune 50 R&D budgets that don't blink at six-figure cloud invoices,' noted one enterprise architect."
            },
            {
                "id": "art-005",
                "title": "ApexAI Stock Surges Following Launch of Nova-4 AI Model Targeting Biotech R&D",
                "source": "Bloomberg Financial News",
                "url": "https://bloomberg.example/news/articles/apexai-nova-4-market-impact",
                "date": "2026-10-17 14:00",
                "author": "Marcus Sterling",
                "content": "Shares of enterprise AI suppliers rose sharply on Thursday following ApexAI's reveal of Nova-4. Wall Street analysts hailed the model's specialized bio-computational capabilities, estimating that life sciences licensing could generate up to $1.2B in annual recurring revenue by 2027. J.P. Morgan reiterated its Overweight rating on key hardware and cloud suppliers powering the training clusters."
            },
            {
                "id": "art-006",
                "title": "Community Skeptical as Nova-4 Benchmark Methodology Omits Direct Comparisons With Open Weights",
                "source": "Ars OpenTech",
                "url": "https://arsopentech.example/nova-4-benchmarks-scrutiny",
                "date": "2026-10-17 16:45",
                "author": "Dr. Aris Thorne",
                "content": "Independent researchers on X and Reddit are calling for reproducible evaluations of ApexAI's newly crowned Nova-4. Critics note the technical whitepaper omitted side-by-side evaluations against recent 70B open-weights releases on common reasoning benchmarks like SWE-bench, instead highlighting narrow internal organic chemistry tests. ApexAI representatives stated complete evaluation harnesses would be published next week."
            },

            # Story 2: Global Semiconductor Export Regulations (Cluster B - 5 articles)
            {
                "id": "art-007",
                "title": "Commerce Department Announces Tightened Export Restrictions on High-Bandwidth AI Accelerators",
                "source": "US Dept of Commerce Press Office",
                "url": "https://commerce.gov.example/news/accelerator-export-controls-update",
                "date": "2026-10-16 10:00",
                "author": "Bureau of Industry and Security",
                "content": "WASHINGTON — The U.S. Department of Commerce's Bureau of Industry and Security (BIS) today issued an interim final rule revising export controls on advanced computing items and semiconductor manufacturing equipment. The updated framework introduces strict total processing performance and interconnect bandwidth ceilings for GPU hardware shipped to Tier-3 jurisdictions, aimed at safeguarding national technological security while maintaining transparent licensing exemptions for allied research consortia."
            },
            {
                "id": "art-008",
                "title": "US Expands AI Chip Export Restrictions, Capping Interconnect Speeds",
                "source": "Reuters Technology Desk",
                "url": "https://reuters.example/technology/us-chip-export-rules-expanded",
                "date": "2026-10-16 10:25",
                "author": "David Shepardson",
                "content": "WASHINGTON (Reuters) — The United States on Friday widened curbs on exports of advanced AI semiconductors, closing loopholes that previously allowed chipmakers to sell modified processors with reduced memory buses. The new rules measure total interconnect throughput, directly impacting modified GPU lines designed for overseas markets. Chip stocks slid 3.4% in premarket trading."
            },
            {
                "id": "art-009",
                "title": "US Tightens Chip Export Rules: Semiconductor Makers Face New Global Trade Barriers",
                "source": "Wall Street Daily",
                "url": "https://wsdaily.example/markets/semiconductor-trade-curbs",
                "date": "2026-10-16 11:15",
                "author": "Sarah Lin & Michael Chang",
                "content": "The Biden administration's latest semiconductor restrictions represent a major escalation in international tech decoupling. Leading chip designers estimate the new regulations could erase between $3.5B and $5B in forecast quarterly revenues unless commercial waiver requests are swiftly granted by federal regulators. Trade groups warned that domestic equipment makers may suffer long-term competitiveness setbacks."
            },
            {
                "id": "art-010",
                "title": "Commerce Department Tightens Export Controls on AI Chips",
                "source": "Fintech Chronicle Wire",
                "url": "https://fintechchronicle.example/wires/commerce-dept-chip-curbs",
                "date": "2026-10-16 11:40",
                "author": "Syndicated Wire Desk",
                "content": "WASHINGTON — The U.S. Department of Commerce today updated export restrictions on advanced semiconductors and computing equipment, establishing tighter bandwidth thresholds for processors shipped abroad. Major hardware suppliers are assessing financial guidance impacts."
            },
            {
                "id": "art-011",
                "title": "How the New AI Chip Sanctions Will Accelerate Domestic Hardware Substitution",
                "source": "Asia Tech Review",
                "url": "https://asiatechreview.example/analysis/hardware-substitution-sanctions",
                "date": "2026-10-16 18:00",
                "author": "Kenji Sato",
                "content": "Far from choking regional AI infrastructure buildouts, Washington's latest bandwidth caps are triggering an unprecedented surge in state-backed procurement of domestic optical interconnects and clustered RISC-V accelerators. Regional cloud hyperscalers have already committed capital expenditure to indigenous dual-processor node architectures to offset Western import curbs."
            },

            # Story 3: AI Search Engines & Publisher Revenue Lawsuit (Cluster C - 6 articles)
            {
                "id": "art-012",
                "title": "Coalition of Major News Publishers Files Class-Action Lawsuit Against PerceptSearch Over AI Summaries",
                "source": "MediaLaw Quarterly",
                "url": "https://medialawquarterly.example/perceptsearch-publishers-lawsuit",
                "date": "2026-10-15 08:30",
                "author": "Rachel Kroll, Legal Analyst",
                "content": "NEW YORK — A coalition of 14 leading newspaper and magazine publishers filed a copyright infringement and unfair competition lawsuit in the Southern District of New York against generative search engine PerceptSearch. The plaintiffs allege PerceptSearch's zero-click synthetic answers bypass source websites entirely while ingesting copyrighted articles without attribution or licensing compensation, causing a 48% decline in referral traffic."
            },
            {
                "id": "art-013",
                "title": "Publishers Sue PerceptSearch Over AI Search Summaries Depleting Web Traffic",
                "source": "Associated Media Wire",
                "url": "https://associatedmedia.example/news/publishers-lawsuit-perceptsearch",
                "date": "2026-10-15 08:50",
                "author": "Syndicated News Staff",
                "content": "NEW YORK — Fourteen prominent news organizations filed suit against AI search engine PerceptSearch on Wednesday, accusing the platform of free-riding on investigative journalism. The complaint demands statutory damages and an injunction halting real-time web scraping without revenue-sharing licensing pacts."
            },
            {
                "id": "art-014",
                "title": "News Publishers File Major Copyright Lawsuit Against AI Search Engine PerceptSearch",
                "source": "Publishing Insider Daily",
                "url": "https://publishinginsider.example/legal/publishers-vs-perceptsearch",
                "date": "2026-10-15 09:15",
                "author": "Wire Service Feed",
                "content": "NEW YORK — Fourteen news publishers filed a joint lawsuit against generative search engine PerceptSearch on Wednesday in New York federal court. The litigation targets PerceptSearch's synthetic answer boxes, alleging unauthorized ingestion of premium journalistic reporting and catastrophic loss of ad impressions."
            },
            {
                "id": "art-015",
                "title": "PerceptSearch Responds: AI Syntheses Fall Squarely Under Fair Use, Links Drive High-Intent Traffic",
                "source": "PerceptSearch Corporate Blog",
                "url": "https://blog.perceptsearch.example/our-commitment-to-fair-use-publishers",
                "date": "2026-10-15 12:00",
                "author": "Julian Meyer, VP of Public Policy",
                "content": "At PerceptSearch, we believe generative synthesis is the natural evolution of indexing the world's knowledge. Our technology synthesizes transformative factual answers with prominent source citations that deliver high-intent readers directly to primary publications. We respect fair use jurisprudence and remain actively engaged in good-faith revenue-sharing pilots through our Publisher Innovation Fund."
            },
            {
                "id": "art-016",
                "title": "The Death of the Referral Link: Why the PerceptSearch Lawsuit is a Water Cooler Moment for PR & Media",
                "source": "PR Week Strategic Briefing",
                "url": "https://prweekstrategy.example/analysis/death-of-referral-links-pr-impact",
                "date": "2026-10-15 15:30",
                "author": "Samantha Reed",
                "content": "For communications professionals, the publishers' war against AI answer engines changes everything. Traditional earned media playbooks relied on driving clicks back to corporate landing pages and client newsrooms. As AI engines answer user queries directly without requiring a click, PR measurement must pivot from click-through volume to 'Share of Model Voice'—ensuring brands are accurately represented in the synthesized summary itself."
            },
            {
                "id": "art-017",
                "title": "Wall Street Shrugs at Publisher Litigation as AI Search Adoption Tops 300M Users",
                "source": "Silicon Venture Monitor",
                "url": "https://siliconventure.example/ai-search-growth-vs-litigation",
                "date": "2026-10-15 17:00",
                "author": "Tyler Brooks",
                "content": "Despite escalating legal headwinds from legacy print publishers, user adoption of generative search continues at a breakneck pace. PerceptSearch revealed yesterday that daily active users surpassed 310 million globally. Venture backers view publisher copyright suits as standard transitional friction that will ultimately resolve through blanket statutory licensing, similar to digital music streaming."
            },

            # Story 4: Minor Fluff / Noise Article (Syndicated fluff - 3 articles)
            {
                "id": "art-018",
                "title": "Top 10 AI Productivity Tools You Must Try This Weekend",
                "source": "ClickTech Buzz",
                "url": "https://clicktechbuzz.example/listicles/top-10-ai-tools-weekend",
                "date": "2026-10-17 07:00",
                "author": "Buzz Staff",
                "content": "Are you feeling overwhelmed by modern technology? Check out these 10 amazing artificial intelligence tools that can help organize your calendar, generate cute avatars, rewrite emails in pirate speak, and optimize your weekly grocery shopping list!"
            },
            {
                "id": "art-019",
                "title": "10 Mind-Blowing AI Apps to Supercharge Your Productivity",
                "source": "Daily Gadget Digest",
                "url": "https://gadgetdigest.example/productivity-apps-ai",
                "date": "2026-10-17 08:30",
                "author": "Content Aggregator",
                "content": "Supercharge your workflow this weekend with 10 unbelievable artificial intelligence hacks. From cute avatar creators to automatic email rewriters, these easy browser extensions will save you hours every single day."
            },
            {
                "id": "art-020",
                "title": "Weekend Roundup: The Best AI Tools for Fun and Work",
                "source": "LifeHacker Clone",
                "url": "https://lifehacksdaily.example/roundup-ai-fun",
                "date": "2026-10-17 10:00",
                "author": "Syndicated Lifehacks",
                "content": "Looking for fun things to do with artificial intelligence? We rounded up 10 cute tools to make avatars, fix calendar schedules, and automate mundane tasks. Read our full roundup here."
            }
        ]
    },

    "crisis_and_reputation": {
        "title": "Corporate Crisis Comms: Cloud Outage, Security Breach & Executive Shakeup",
        "category": "Crisis & Brand Reputation",
        "description": "16 articles covering 2 intense PR crisis events: A global multi-region cloud identity outage affecting financial systems, and a surprise CEO departure amidst whistleblower allegations. Demonstrates managing rumors vs official statements.",
        "default_keywords": ["CloudSafe", "Outage", "Breach", "CEO", "Whistleblower", "Crisis", "Investigation"],
        "articles": [
            # Incident A: CloudSafe Global Identity Outage
            {
                "id": "cr-001",
                "title": "CloudSafe Investigating Global Authentication Failure Across US-East and EU-West Regions",
                "source": "CloudSafe Official Status Page",
                "url": "https://status.cloudsafe.example/incidents/inc-2026-9941",
                "date": "2026-10-16 04:15",
                "author": "Site Reliability Engineering Team",
                "content": "INVESTIGATING: At 03:45 UTC, our monitoring systems identified widespread authentication degradation impacting SSO and IAM credential validation across US-East-1 and EU-West-2 zones. Our security and infrastructure incident response teams are actively isolating the root cause. No evidence of malicious exfiltration has been identified at this stage. Further updates provided every 30 minutes."
            },
            {
                "id": "cr-002",
                "title": "CloudSafe Authentication Outage Knocks Offline Hundreds of Banking and Healthcare Portals",
                "source": "CyberWire Daily",
                "url": "https://cyberwiredaily.example/cloudsafe-massive-outage-banking",
                "date": "2026-10-16 05:30",
                "author": "Liam Vance, Cybersecurity Correspondent",
                "content": "A cascading failure at cloud identity giant CloudSafe has paralyzed digital logins for major retail banks, airline booking engines, and hospital medical records platforms across North America and Europe. Rumors of a nation-state supply-chain compromise began circulating on cyber threat intelligence channels after encrypted ransom notes were allegedly spotted on external forums."
            },
            {
                "id": "cr-003",
                "title": "Massive CloudSafe Outage Cripples Major Websites and Financial Services",
                "source": "Global Wire News",
                "url": "https://globalwire.example/breaking/cloudsafe-outage-cripples-web",
                "date": "2026-10-16 05:45",
                "author": "Wire Editorial Desk",
                "content": "NEW YORK — An unprecedented outage at identity management provider CloudSafe has rendered countless banking portals, airline reservation systems, and enterprise portals inaccessible on Friday morning. CloudSafe confirmed an active service disruption and stated engineers are working to restore normal operations."
            },
            {
                "id": "cr-004",
                "title": "CloudSafe Clarifies: Outage Caused by Internal Configuration Deployment Bug, Not Cyberattack",
                "source": "CloudSafe Corporate Newsroom",
                "url": "https://cloudsafe.example/newsroom/incident-statement-configuration-fix",
                "date": "2026-10-16 08:00",
                "author": "Amanda Morris, Chief Information Officer",
                "content": "We want to provide our enterprise partners with complete transparency regarding this morning's disruption. The authentication failure was caused by an internal schema mismatch during a routine certificate rotation deployment, not a cyberattack or external breach. Customer data remained securely encrypted and uncompromised throughout the event. All systems have returned to 100% operational status."
            },
            {
                "id": "cr-005",
                "title": "CloudSafe Stocks Tumble 8% as Outage Exposes Single Points of Failure in Modern Fintech",
                "source": "Wall Street Journal Tech",
                "url": "https://wsjtech.example/markets/cloudsafe-single-point-of-failure",
                "date": "2026-10-16 11:30",
                "author": "Jessica Miller",
                "content": "Shares of CloudSafe plummeted nearly 8% on Friday following an 4-hour authentication blackout that cost enterprise customers millions in lost transactional revenue. Financial regulators in the UK and US have already initiated inquiries into whether critical banking infrastructure has developed unacceptable systemic concentration risk by relying on a single third-party identity vendor."
            },
            {
                "id": "cr-006",
                "title": "Crisis Comms Breakdown: How CloudSafe's 90-Minute Silence Allowed Ransomware Rumors to Run Rampant",
                "source": "Reputation & Comms Review",
                "url": "https://reputationcomms.example/cloudsafe-crisis-management-autopsy",
                "date": "2026-10-16 15:00",
                "author": "Gregory Hunt",
                "content": "CloudSafe's handling of Friday's outage will become a textbook corporate communications case study in what NOT to do. By maintaining near-total radio silence during the first 90 minutes of the crash, the company created an information vacuum quickly filled by unverified ransomware speculation. Timely, empathetic holding statements are vital to prevent reputational freefalls during technical disruptions."
            },

            # Incident B: Surprise CEO Departure & Governance Whistleblower
            {
                "id": "cr-007",
                "title": "Veloce Motors Announces Leadership Transition: CEO Mark Henderson Steps Down Immediately",
                "source": "Veloce Motors Investor Relations",
                "url": "https://ir.velocemotors.example/press/leadership-transition-henderson",
                "date": "2026-10-14 16:30",
                "author": "Veloce Board of Directors",
                "content": "DETROIT — The Board of Directors of Veloce Motors today announced that Mark Henderson has stepped down as Chief Executive Officer and board member, effective immediately. Board Chair Caroline Ortiz will serve as Interim CEO while a global executive search is conducted. The Board expresses its gratitude to Mr. Henderson for his five years of service and dedication to Veloce's electrification roadmap."
            },
            {
                "id": "cr-008",
                "title": "Veloce Motors CEO Mark Henderson Resigns Abruptly, Interim Head Appointed",
                "source": "Automotive News Wire",
                "url": "https://autonewswire.example/veloce-ceo-abrupt-resignation",
                "date": "2026-10-14 16:45",
                "author": "Wire Reporter",
                "content": "DETROIT — Electric vehicle manufacturer Veloce Motors announced the immediate departure of CEO Mark Henderson on Tuesday evening. Board Chair Caroline Ortiz will take over interim chief executive duties while the company searches for a permanent successor."
            },
            {
                "id": "cr-009",
                "title": "Behind the Veloce Shakeup: SEC Whistleblower Probe Into Battery Range Claims Prompted Ouster",
                "source": "Detroit Investigative Chronicle",
                "url": "https://detroitchronicle.example/investigations/veloce-whistleblower-battery-probe",
                "date": "2026-10-15 08:00",
                "author": "Robert Callahan",
                "content": "While Veloce Motors painted CEO Mark Henderson's abrupt Tuesday exit as an amicable leadership transition, sources with direct knowledge confirm the departure was forced by the board after federal regulators opened a confidential inquiry into consumer battery range disclosures. A whistleblower filing submitted by former quality control engineers alleges test telemetry was deliberately massaged to inflate EPA range numbers."
            },
            {
                "id": "cr-010",
                "title": "Whistleblower Scandal Hits Veloce Motors Following Abrupt Executive Exit",
                "source": "CleanTech Daily Wire",
                "url": "https://cleantechdaily.example/veloce-whistleblower-fallout",
                "date": "2026-10-15 09:30",
                "author": "Syndicated Desk",
                "content": "Veloce Motors shares sank 12% on Wednesday morning following revelations that CEO Mark Henderson's sudden resignation was tied to a regulatory investigation regarding battery efficiency claims. Interim CEO Caroline Ortiz pledged comprehensive cooperation with federal agencies."
            }
        ]
    },

    "biopharma_mna": {
        "title": "Biotech & Pharma: Breakthrough Approvals & $14B M&A Blockbuster",
        "category": "Biotech & Healthcare",
        "description": "14 articles tracking a major $14 Billion oncology buyout and a breakthrough Alzheimer's clinical trial phase III readout with syndicated PR wires and scientific commentary.",
        "default_keywords": ["Oncology", "Acquisition", "FDA", "Alzheimer", "Clinical Trial", "Pharma"],
        "articles": [
            {
                "id": "bio-001",
                "title": "Novapharm to Acquire OncoGenesis Therapeutics for $14 Billion to Expand Precision Oncology Pipeline",
                "source": "Novapharm PR Newswire Wire",
                "url": "https://prnewswire.example/novapharm-oncosystems-14b-acquisition",
                "date": "2026-10-12 06:30",
                "author": "Corporate Communications Team",
                "content": "BASEL & BOSTON — Novapharm AG and OncoGenesis Therapeutics today announced a definitive merger agreement under which Novapharm will acquire all outstanding shares of OncoGenesis for $88.00 per share in cash, representing an equity value of approximately $14 billion. The transaction secures Novapharm's commercial ownership of ONCO-302, a next-generation antibody-drug conjugate (ADC) currently in Phase III evaluation for metastatic HER2-low breast cancer."
            },
            {
                "id": "bio-002",
                "title": "Novapharm Inks $14B Deal to Buy Cancer Biotech OncoGenesis",
                "source": "Reuters Health Desk",
                "url": "https://reuters.example/health/novapharm-oncogenesis-14b-deal",
                "date": "2026-10-12 07:00",
                "author": "Hannah Lang",
                "content": "Novapharm announced on Monday it will buy U.S. cancer specialist OncoGenesis for $14 billion in cash, bolstering its presence in targeted oncology therapies. The deal gives the Swiss pharma heavyweight access to high-demand antibody-drug conjugate technologies designed to seek out and destroy malignant cells while sparing healthy tissue."
            },
            {
                "id": "bio-003",
                "title": "Novapharm to Acquire OncoGenesis for $14B in Cash",
                "source": "BioPharma Wire Service",
                "url": "https://biopharmawire.example/mna/novapharm-buys-oncogenesis",
                "date": "2026-10-12 07:15",
                "author": "Automated Wire Desk",
                "content": "Novapharm agreed Monday to acquire OncoGenesis Therapeutics for $88.00 per share, an enterprise valuation of $14 billion. The deal focuses on adding OncoGenesis's flagship Phase III ADC drug for metastatic breast cancer to Novapharm's commercial cancer portfolio."
            },
            {
                "id": "bio-004",
                "title": "Why Novapharm Paid a 65% Premium for OncoGenesis: The High-Stakes Battle for ADC Dominance",
                "source": "Endpoints News Analysis",
                "url": "https://endpointsnews.example/in-depth/novapharm-adc-premium-gamble",
                "date": "2026-10-12 10:45",
                "author": "Amber Chen, Senior Oncology Editor",
                "content": "Novapharm's $14 billion takeover of OncoGenesis isn't just another bolt-on acquisition; it is an aggressive defensive moat against impending patent cliffs on Novapharm's legacy blockbuster biologics. At a staggering 65% premium over OncoGenesis's 30-day volume-weighted average price, Novapharm is paying top dollar to prevent rivals AstraZeneca and Daiichi Sankyo from monopolizing next-generation ADC payloads."
            },
            {
                "id": "bio-005",
                "title": "Wall Street Applauds Novapharm M&A Deal But Notes FTC Scrutiny Looms for Pharma Consolidation",
                "source": "BioTech Investor Quarterly",
                "url": "https://biotechinvestor.example/market-views/novapharm-oncogenesis-antitrust",
                "date": "2026-10-12 14:00",
                "author": "Jonathan Drake",
                "content": "Financial analysts reacted positively to Novapharm's strategic clarity in acquiring OncoGenesis, noting immediate accretion potential by 2028. However, legal experts caution that federal antitrust regulators are scrutinizing multi-billion pharma mergers with unprecedented vigor, specifically examining whether bundling cancer therapies could disadvantage biosimilar competitors."
            }
        ]
    }
}

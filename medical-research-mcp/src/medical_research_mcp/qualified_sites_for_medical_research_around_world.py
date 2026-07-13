from __future__ import annotations

QUALIFIED_SOURCES = {
    "clinical_guidelines": [
        {"name": "American Diabetes Association Standards of Care", "authority": "ADA", "region": "United States", "url": "https://professional.diabetes.org/standards-of-care", "topics": ["diabetes", "comorbidities", "care standards"]},
        {"name": "WHO Diabetes", "authority": "World Health Organization", "region": "global", "url": "https://www.who.int/news-room/fact-sheets/detail/diabetes", "topics": ["epidemiology", "complications", "public health"]},
        {"name": "CDC Diabetes", "authority": "US CDC", "region": "United States", "url": "https://www.cdc.gov/diabetes/", "topics": ["public health", "complications", "surveillance"]},
        {"name": "NICE Type 1 Diabetes NG17", "authority": "NICE", "region": "United Kingdom", "url": "https://www.nice.org.uk/guidance/ng17", "topics": ["type 1 diabetes", "complications", "care pathways"]},
        {"name": "NICE Type 2 Diabetes NG28", "authority": "NICE", "region": "United Kingdom", "url": "https://www.nice.org.uk/guidance/ng28", "topics": ["type 2 diabetes", "care pathways", "complications"]},
        {"name": "KDIGO Diabetes and CKD", "authority": "KDIGO", "region": "global nephrology", "url": "https://kdigo.org/guidelines/diabetes-ckd/", "topics": ["chronic kidney disease", "diabetes", "nephrology"]},
        {"name": "International Diabetes Federation", "authority": "IDF", "region": "global", "url": "https://idf.org/", "topics": ["global diabetes", "epidemiology", "education"]},
    ],
    "literature": [
        {"name": "PubMed", "authority": "NIH/NLM", "region": "global", "access": "NCBI E-utilities", "url": "https://pubmed.ncbi.nlm.nih.gov/"},
        {"name": "Europe PMC", "authority": "EMBL-EBI/Europe PMC", "region": "Europe/global", "access": "REST API", "url": "https://europepmc.org/"},
        {"name": "Cochrane Library", "authority": "Cochrane", "region": "global", "access": "licensed search", "url": "https://www.cochranelibrary.com/"},
        {"name": "WHO IRIS", "authority": "WHO", "region": "global", "access": "repository", "url": "https://iris.who.int/"},
        {"name": "NIH Bookshelf", "authority": "NIH/NLM", "region": "global", "access": "repository", "url": "https://www.ncbi.nlm.nih.gov/books/"},
    ],
    "trials": [
        {"name": "ClinicalTrials.gov", "authority": "NIH/NLM", "region": "United States/global", "access": "API v2", "url": "https://clinicaltrials.gov/"},
        {"name": "WHO ICTRP", "authority": "WHO", "region": "global", "access": "portal/approved export", "url": "https://www.who.int/clinical-trials-registry-platform"},
        {"name": "EU CTIS", "authority": "EMA", "region": "European Union", "access": "public portal", "url": "https://euclinicaltrials.eu/"},
        {"name": "ISRCTN", "authority": "ISRCTN", "region": "global", "access": "registry", "url": "https://www.isrctn.com/"},
        {"name": "ANZCTR", "authority": "WHO primary registry", "region": "Australia/New Zealand", "access": "registry", "url": "https://www.anzctr.org.au/"},
        {"name": "ReBEC", "authority": "Brazil/WHO network", "region": "Brazil/Latin America", "access": "registry", "url": "https://ensaiosclinicos.gov.br/"},
        {"name": "ChiCTR", "authority": "WHO primary registry", "region": "China", "access": "registry", "url": "https://www.chictr.org.cn/"},
        {"name": "JPRN", "authority": "WHO primary registry", "region": "Japan", "access": "registry", "url": "https://jrct.niph.go.jp/"},
        {"name": "CTRI", "authority": "WHO primary registry", "region": "India", "access": "registry", "url": "https://ctri.nic.in/"},
        {"name": "PACTR", "authority": "WHO primary registry", "region": "Africa", "access": "registry", "url": "https://pactr.samrc.ac.za/"},
    ],
    "regulatory": [
        {"name": "FDA", "region": "United States", "url": "https://www.fda.gov/medical-devices/software-medical-device-samd"},
        {"name": "EMA", "region": "European Union", "url": "https://www.ema.europa.eu/"},
        {"name": "ANVISA", "region": "Brazil", "url": "https://www.gov.br/anvisa/"},
        {"name": "MHRA", "region": "United Kingdom", "url": "https://www.gov.uk/government/organisations/medicines-and-healthcare-products-regulatory-agency"},
        {"name": "Health Canada", "region": "Canada", "url": "https://www.canada.ca/en/health-canada.html"},
        {"name": "TGA", "region": "Australia", "url": "https://www.tga.gov.au/"},
        {"name": "PMDA", "region": "Japan", "url": "https://www.pmda.go.jp/english/"},
    ],
    "bio_chemistry": [
        {"name": "UniProt", "authority": "UniProt Consortium", "url": "https://www.uniprot.org/", "topics": ["proteins", "pathways"]},
        {"name": "ChEMBL", "authority": "EMBL-EBI", "url": "https://www.ebi.ac.uk/chembl/", "topics": ["bioactivity", "drug discovery"]},
        {"name": "PubChem", "authority": "NIH/NCBI", "url": "https://pubchem.ncbi.nlm.nih.gov/", "topics": ["chemistry", "compounds"]},
        {"name": "Reactome", "authority": "Reactome", "url": "https://reactome.org/", "topics": ["pathways", "systems biology"]},
        {"name": "KEGG", "authority": "Kanehisa Laboratories", "url": "https://www.kegg.jp/", "topics": ["pathways", "metabolism"]},
    ],
}


def source_registry() -> dict:
    return QUALIFIED_SOURCES


def source_policy() -> list[str]:
    return [
        "Prefer official APIs, society guidelines, regulatory sources, systematic reviews, and licensed exports.",
        "Preserve query, source, retrieval date, source version, identifiers, provenance, and evidence tier.",
        "Separate clinical guideline statements, trial evidence, mechanistic biology, chemistry, and implementation evidence.",
        "Check corrections, retractions, expressions of concern, duplicate records, conflicts of interest, and publication type.",
        "Do not use abstracts, news, blogs, or vendor claims as sole support for high-impact medical or AI safety claims.",
        "Do not scrape patient-identifiable or access-controlled content.",
        "Retain negative, null, contradictory, and subgroup-specific evidence.",
        "Do not produce autonomous diagnosis, treatment recommendation, cure claim, or experimentation authorization.",
    ]

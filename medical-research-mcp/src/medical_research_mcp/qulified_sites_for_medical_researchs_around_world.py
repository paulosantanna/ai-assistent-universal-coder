QUALIFIED_SOURCES={
 "literature":[
  {"name":"PubMed","authority":"NIH/NLM","access":"NCBI E-utilities"},
  {"name":"Europe PMC","authority":"EMBL-EBI/Europe PMC","access":"REST API"},
  {"name":"WHO IRIS","authority":"WHO","access":"repository"},
  {"name":"Cochrane Library","authority":"Cochrane","access":"licensed search"}],
 "trials":[
  {"name":"ClinicalTrials.gov","authority":"NIH/NLM","access":"API v2"},
  {"name":"WHO ICTRP","authority":"WHO","access":"portal/approved export"},
  {"name":"EU CTIS","authority":"EMA","access":"public portal"},
  {"name":"ISRCTN","authority":"ISRCTN","access":"registry"},
  {"name":"ANZCTR","authority":"WHO primary registry","access":"registry"},
  {"name":"ReBEC","authority":"Brazil/WHO network","access":"registry"},
  {"name":"ChiCTR","authority":"WHO primary registry","access":"registry"},
  {"name":"JPRN","authority":"WHO primary registry","access":"registry"},
  {"name":"CTRI","authority":"WHO primary registry","access":"registry"},
  {"name":"PACTR","authority":"WHO primary registry","access":"registry"}],
 "regulatory":["FDA","EMA","ANVISA","MHRA","Health Canada","TGA","PMDA"],
}
def source_registry()->dict:return QUALIFIED_SOURCES
def source_policy()->list[str]:
    return ["Prefer official APIs and licensed exports.","Preserve query, identifiers, date and provenance.",
    "Respect terms, copyright, robots policies and rate limits.","Never scrape patient-identifiable or access-controlled content.",
    "Retain corrections, retractions and contradictory evidence."]

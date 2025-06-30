from typing import List

MOCK_CASE_DATABASE = [
    {
        "case_name": "Terry v. Ohio",
        "citation": "392 U.S. 1 (1968)",
        "year": 1968,
        "court": "U.S. Supreme Court",
        "facts": "Police officer observed suspicious behavior and conducted a pat-down search for weapons",
        "legal_principle": "Fourth Amendment protection against unreasonable searches and seizures",
        "ruling": "Police may conduct limited search for weapons based on reasonable suspicion",
        "keywords": ["terry stop", "pat down", "reasonable suspicion", "search", "weapons", "fourth amendment"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Pennsylvania v. Mimms",
        "citation": "434 U.S. 106 (1977)", 
        "year": 1977,
        "court": "U.S. Supreme Court",
        "facts": "Officer ordered driver out of vehicle during routine traffic stop",
        "legal_principle": "Officer safety during traffic stops",
        "ruling": "Officers may order drivers out of vehicles during lawful traffic stops",
        "keywords": ["traffic stop", "officer safety", "vehicle", "driver", "exit vehicle"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "United States v. Ross",
        "citation": "456 U.S. 798 (1982)",
        "year": 1982,
        "court": "U.S. Supreme Court", 
        "facts": "Police searched vehicle and containers within based on probable cause",
        "legal_principle": "Automobile exception to warrant requirement",
        "ruling": "Police may search vehicle and containers within if they have probable cause",
        "keywords": ["vehicle search", "automobile exception", "probable cause", "containers", "warrant"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "California v. Acevedo",
        "citation": "500 U.S. 565 (1991)",
        "year": 1991,
        "court": "U.S. Supreme Court",
        "facts": "Police searched closed container in vehicle based on probable cause to believe it contained contraband",
        "legal_principle": "Container searches in vehicles",
        "ruling": "Police may search containers in vehicles without warrant if they have probable cause",
        "keywords": ["container search", "vehicle", "probable cause", "contraband", "closed container"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Illinois v. Caballes",
        "citation": "543 U.S. 405 (2005)",
        "year": 2005,
        "court": "U.S. Supreme Court",
        "facts": "Drug dog alerted to vehicle during traffic stop",
        "legal_principle": "Use of drug detection dogs during traffic stops",
        "ruling": "Dog sniff during lawful traffic stop does not violate Fourth Amendment",
        "keywords": ["drug dog", "canine", "traffic stop", "sniff", "fourth amendment", "detection"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "State v. Johnson",
        "citation": "234 N.J. 567 (2018)",
        "year": 2018,
        "court": "New Jersey Supreme Court",
        "facts": "Officer conducted search incident to arrest for marijuana possession",
        "legal_principle": "Search incident to arrest in marijuana cases",
        "ruling": "Limited search incident to arrest permitted for officer safety",
        "keywords": ["search incident", "arrest", "marijuana", "officer safety", "new jersey"],
        "jurisdiction": "new_jersey"
    },
    {
        "case_name": "Commonwealth v. Smith",
        "citation": "456 Pa. 123 (2019)",
        "year": 2019,
        "court": "Pennsylvania Supreme Court",
        "facts": "Traffic stop led to vehicle search based on odor of marijuana",
        "legal_principle": "Probable cause from marijuana odor",
        "ruling": "Marijuana odor alone may not constitute probable cause in some circumstances",
        "keywords": ["marijuana odor", "probable cause", "vehicle search", "traffic stop", "pennsylvania"],
        "jurisdiction": "pennsylvania"
    },
    {
        "case_name": "People v. Rodriguez",
        "citation": "789 N.Y.2d 456 (2020)",
        "year": 2020,
        "court": "New York Court of Appeals",
        "facts": "Stop and frisk conducted in high-crime area based on suspicious behavior",
        "legal_principle": "Stop and frisk in high-crime areas",
        "ruling": "Location in high-crime area alone insufficient for reasonable suspicion",
        "keywords": ["stop and frisk", "high crime area", "reasonable suspicion", "terry stop", "new york"],
        "jurisdiction": "new_york"
    },
    {
        "case_name": "Miranda v. Arizona",
        "citation": "384 U.S. 436 (1966)",
        "year": 1966,
        "court": "U.S. Supreme Court",
        "facts": "Suspect questioned without being informed of constitutional rights",
        "legal_principle": "Fifth Amendment right against self-incrimination during custodial interrogation",
        "ruling": "Suspects must be informed of rights before custodial interrogation",
        "keywords": ["miranda rights", "custodial interrogation", "fifth amendment", "right to counsel", "self-incrimination"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Tennessee v. Garner",
        "citation": "471 U.S. 1 (1985)",
        "year": 1985,
        "court": "U.S. Supreme Court",
        "facts": "Officer shot fleeing unarmed burglary suspect",
        "legal_principle": "Use of deadly force against fleeing suspects",
        "ruling": "Deadly force may not be used unless suspect poses threat of serious harm",
        "keywords": ["deadly force", "fleeing suspect", "fourth amendment", "use of force", "unarmed suspect"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Graham v. Connor",
        "citation": "490 U.S. 386 (1989)",
        "year": 1989,
        "court": "U.S. Supreme Court",
        "facts": "Officers used force on diabetic man during investigative stop",
        "legal_principle": "Objective reasonableness standard for excessive force claims",
        "ruling": "Force must be objectively reasonable based on totality of circumstances",
        "keywords": ["excessive force", "objective reasonableness", "fourth amendment", "police brutality", "investigative stop"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Mapp v. Ohio",
        "citation": "367 U.S. 643 (1961)",
        "year": 1961,
        "court": "U.S. Supreme Court",
        "facts": "Evidence obtained through illegal search used in state prosecution",
        "legal_principle": "Exclusionary rule application to state courts",
        "ruling": "Illegally obtained evidence cannot be used in state criminal prosecutions",
        "keywords": ["exclusionary rule", "illegal search", "fourth amendment", "evidence suppression", "state courts"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Arizona v. Gant",
        "citation": "556 U.S. 332 (2009)",
        "year": 2009,
        "court": "U.S. Supreme Court",
        "facts": "Police searched vehicle after arrest when arrestee was secured",
        "legal_principle": "Search incident to arrest of vehicle occupants",
        "ruling": "Vehicle search limited to passenger compartment when arrestee could access it",
        "keywords": ["search incident to arrest", "vehicle search", "passenger compartment", "arrestee access"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Kentucky v. King",
        "citation": "563 U.S. 452 (2011)",
        "year": 2011,
        "court": "U.S. Supreme Court",
        "facts": "Police entered apartment without warrant based on exigent circumstances",
        "legal_principle": "Exigent circumstances exception to warrant requirement",
        "ruling": "Police may enter without warrant when exigent circumstances exist",
        "keywords": ["exigent circumstances", "warrantless entry", "hot pursuit", "destruction of evidence"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Riley v. California",
        "citation": "573 U.S. 373 (2014)",
        "year": 2014,
        "court": "U.S. Supreme Court",
        "facts": "Police searched digital contents of cell phone incident to arrest",
        "legal_principle": "Search of digital devices incident to arrest",
        "ruling": "Generally requires warrant to search digital information on cell phones",
        "keywords": ["cell phone search", "digital evidence", "search incident to arrest", "warrant requirement", "technology"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Rodriguez v. United States",
        "citation": "575 U.S. 348 (2015)",
        "year": 2015,
        "court": "U.S. Supreme Court",
        "facts": "Officer extended traffic stop to conduct dog sniff after completing stop purpose",
        "legal_principle": "Duration limits on traffic stops",
        "ruling": "Traffic stop may not be extended without reasonable suspicion",
        "keywords": ["traffic stop duration", "dog sniff", "reasonable suspicion", "mission creep", "fourth amendment"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Utah v. Strieff",
        "citation": "579 U.S. 232 (2016)",
        "year": 2016,
        "court": "U.S. Supreme Court",
        "facts": "Evidence discovered after illegal stop but during arrest on outstanding warrant",
        "legal_principle": "Attenuation doctrine and fruit of poisonous tree",
        "ruling": "Evidence admissible when discovery sufficiently attenuated from illegal conduct",
        "keywords": ["attenuation doctrine", "fruit of poisonous tree", "outstanding warrant", "illegal stop"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Carpenter v. United States",
        "citation": "585 U.S. ___ (2018)",
        "year": 2018,
        "court": "U.S. Supreme Court",
        "facts": "Government obtained cell phone location records without warrant",
        "legal_principle": "Fourth Amendment protection for digital location data",
        "ruling": "Warrant generally required to obtain cell phone location records",
        "keywords": ["cell phone location", "digital privacy", "warrant requirement", "location tracking", "technology"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "State v. Williams",
        "citation": "345 N.J. 789 (2020)",
        "year": 2020,
        "court": "New Jersey Supreme Court",
        "facts": "Officer conducted field sobriety tests during DUI investigation",
        "legal_principle": "DUI investigation procedures and field sobriety tests",
        "ruling": "Standardized field sobriety tests admissible with proper foundation",
        "keywords": ["dui", "field sobriety tests", "drunk driving", "standardized tests", "new jersey"],
        "jurisdiction": "new_jersey"
    },
    {
        "case_name": "Commonwealth v. Davis",
        "citation": "567 Pa. 234 (2021)",
        "year": 2021,
        "court": "Pennsylvania Supreme Court",
        "facts": "Police used thermal imaging to detect marijuana growing operation",
        "legal_principle": "Use of thermal imaging for surveillance",
        "ruling": "Thermal imaging of home requires warrant under state constitution",
        "keywords": ["thermal imaging", "marijuana cultivation", "warrant requirement", "home surveillance", "pennsylvania"],
        "jurisdiction": "pennsylvania"
    },
    {
        "case_name": "People v. Johnson",
        "citation": "890 N.Y.2d 123 (2019)",
        "year": 2019,
        "court": "New York Court of Appeals",
        "facts": "Officer conducted pat-down based on anonymous tip",
        "legal_principle": "Anonymous tips and reasonable suspicion",
        "ruling": "Anonymous tip alone insufficient for reasonable suspicion without corroboration",
        "keywords": ["anonymous tip", "reasonable suspicion", "pat down", "corroboration", "new york"],
        "jurisdiction": "new_york"
    },
    {
        "case_name": "State v. Thompson",
        "citation": "456 N.J. 890 (2022)",
        "year": 2022,
        "court": "New Jersey Superior Court",
        "facts": "Police searched vehicle based on odor of burnt marijuana",
        "legal_principle": "Marijuana odor as probable cause post-legalization",
        "ruling": "Marijuana odor insufficient for vehicle search after legalization",
        "keywords": ["marijuana odor", "vehicle search", "legalization", "probable cause", "new jersey"],
        "jurisdiction": "new_jersey"
    },
    {
        "case_name": "Commonwealth v. Anderson",
        "citation": "678 Pa. 345 (2020)",
        "year": 2020,
        "court": "Pennsylvania Superior Court",
        "facts": "Officer seized firearm during Terry stop based on bulge in clothing",
        "legal_principle": "Seizure of weapons during investigative stops",
        "ruling": "Officer may seize weapon if reasonable belief it poses danger",
        "keywords": ["weapon seizure", "terry stop", "officer safety", "firearm", "pennsylvania"],
        "jurisdiction": "pennsylvania"
    },
    {
        "case_name": "People v. Martinez",
        "citation": "234 N.Y.2d 567 (2021)",
        "year": 2021,
        "court": "New York Court of Appeals",
        "facts": "Police conducted inventory search of impounded vehicle",
        "legal_principle": "Inventory searches of impounded vehicles",
        "ruling": "Inventory search valid if conducted according to standardized procedures",
        "keywords": ["inventory search", "impounded vehicle", "standardized procedures", "administrative search", "new york"],
        "jurisdiction": "new_york"
    },
    {
        "case_name": "Florida v. Jardines",
        "citation": "569 U.S. 1 (2013)",
        "year": 2013,
        "court": "U.S. Supreme Court",
        "facts": "Police used drug-detection dog on front porch of home",
        "legal_principle": "Use of drug dogs at private residences",
        "ruling": "Dog sniff at front door of home requires warrant",
        "keywords": ["drug dog", "home", "curtilage", "warrant requirement", "front porch"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Kyllo v. United States",
        "citation": "533 U.S. 27 (2001)",
        "year": 2001,
        "court": "U.S. Supreme Court",
        "facts": "Police used thermal imaging device to detect heat from home",
        "legal_principle": "Use of sense-enhancing technology to gather information from homes",
        "ruling": "Thermal imaging of home interior requires warrant",
        "keywords": ["thermal imaging", "sense-enhancing technology", "home", "warrant requirement", "privacy"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Berghuis v. Thompkins",
        "citation": "560 U.S. 370 (2010)",
        "year": 2010,
        "court": "U.S. Supreme Court",
        "facts": "Suspect remained silent during interrogation then made incriminating statement",
        "legal_principle": "Invocation and waiver of Miranda rights",
        "ruling": "Suspect must unambiguously invoke right to remain silent",
        "keywords": ["miranda waiver", "right to remain silent", "ambiguous invocation", "interrogation"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Davis v. United States",
        "citation": "512 U.S. 452 (1994)",
        "year": 1994,
        "court": "U.S. Supreme Court",
        "facts": "Suspect made ambiguous request for counsel during interrogation",
        "legal_principle": "Ambiguous invocation of right to counsel",
        "ruling": "Request for counsel must be clear and unambiguous",
        "keywords": ["right to counsel", "ambiguous invocation", "interrogation", "miranda rights"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Montejo v. Louisiana",
        "citation": "556 U.S. 778 (2009)",
        "year": 2009,
        "court": "U.S. Supreme Court",
        "facts": "Police interrogated defendant after counsel appointed but before meeting",
        "legal_principle": "Interrogation after counsel appointed",
        "ruling": "Police may approach defendant for interrogation even after counsel appointed",
        "keywords": ["appointed counsel", "interrogation", "sixth amendment", "right to counsel"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "State v. Brown",
        "citation": "789 N.J. 456 (2023)",
        "year": 2023,
        "court": "New Jersey Supreme Court",
        "facts": "Officer conducted search based on consent obtained through interpreter",
        "legal_principle": "Consent searches and language barriers",
        "ruling": "Consent must be clearly understood regardless of language barrier",
        "keywords": ["consent search", "language barrier", "interpreter", "voluntary consent", "new jersey"],
        "jurisdiction": "new_jersey"
    },
    {
        "case_name": "Commonwealth v. Garcia",
        "citation": "890 Pa. 567 (2022)",
        "year": 2022,
        "court": "Pennsylvania Supreme Court",
        "facts": "Police used body-worn camera footage as evidence in excessive force case",
        "legal_principle": "Body-worn cameras and evidence authentication",
        "ruling": "Body camera footage admissible with proper chain of custody",
        "keywords": ["body camera", "video evidence", "chain of custody", "authentication", "pennsylvania"],
        "jurisdiction": "pennsylvania"
    },
    {
        "case_name": "People v. Chen",
        "citation": "345 N.Y.2d 678 (2023)",
        "year": 2023,
        "court": "New York Court of Appeals",
        "facts": "Officer conducted search of suspect's backpack during arrest for jaywalking",
        "legal_principle": "Scope of search incident to arrest for minor offenses",
        "ruling": "Search must be proportionate to offense and safety concerns",
        "keywords": ["search incident to arrest", "minor offense", "proportionality", "jaywalking", "new york"],
        "jurisdiction": "new_york"
    },
    {
        "case_name": "United States v. Jones",
        "citation": "565 U.S. 400 (2012)",
        "year": 2012,
        "court": "U.S. Supreme Court",
        "facts": "Police attached GPS tracking device to vehicle without warrant",
        "legal_principle": "GPS tracking and Fourth Amendment protection",
        "ruling": "Physical intrusion for GPS tracking constitutes search requiring warrant",
        "keywords": ["gps tracking", "vehicle tracking", "physical intrusion", "warrant requirement", "surveillance"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Maryland v. King",
        "citation": "569 U.S. 435 (2013)",
        "year": 2013,
        "court": "U.S. Supreme Court",
        "facts": "Police collected DNA sample from arrestee for serious offense",
        "legal_principle": "DNA collection from arrestees",
        "ruling": "DNA collection from arrestees for serious offenses is reasonable",
        "keywords": ["dna collection", "arrestee", "booking procedure", "identification", "serious offense"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "Heien v. North Carolina",
        "citation": "574 U.S. 54 (2014)",
        "year": 2014,
        "court": "U.S. Supreme Court",
        "facts": "Officer made traffic stop based on mistaken understanding of law",
        "legal_principle": "Reasonable mistake of law by police officers",
        "ruling": "Reasonable mistake of law can provide reasonable suspicion for stop",
        "keywords": ["mistake of law", "reasonable suspicion", "traffic stop", "officer error", "good faith"],
        "jurisdiction": "federal"
    },
    {
        "case_name": "State v. Wilson",
        "citation": "567 N.J. 234 (2024)",
        "year": 2024,
        "court": "New Jersey Superior Court",
        "facts": "Police used facial recognition technology to identify suspect",
        "legal_principle": "Use of facial recognition technology in investigations",
        "ruling": "Facial recognition results require corroboration for probable cause",
        "keywords": ["facial recognition", "identification", "technology", "corroboration", "new jersey"],
        "jurisdiction": "new_jersey"
    },
    {
        "case_name": "Commonwealth v. White",
        "citation": "234 Pa. 789 (2023)",
        "year": 2023,
        "court": "Pennsylvania Superior Court",
        "facts": "Officer conducted warrantless search based on hot pursuit",
        "legal_principle": "Hot pursuit exception to warrant requirement",
        "ruling": "Hot pursuit must be immediate and continuous to justify warrantless entry",
        "keywords": ["hot pursuit", "warrantless entry", "immediate pursuit", "exigent circumstances", "pennsylvania"],
        "jurisdiction": "pennsylvania"
    },
    {
        "case_name": "People v. Lopez",
        "citation": "456 N.Y.2d 890 (2024)",
        "year": 2024,
        "court": "New York Court of Appeals",
        "facts": "Police conducted community caretaking function check on welfare",
        "legal_principle": "Community caretaking function and Fourth Amendment",
        "ruling": "Welfare checks must have reasonable basis and be conducted reasonably",
        "keywords": ["community caretaking", "welfare check", "reasonable basis", "fourth amendment", "new york"],
        "jurisdiction": "new_york"
    }
]

def search_cases_by_keywords(query: str, jurisdiction: str = "federal", max_results: int = 10) -> List[dict]:
    """Search mock database for relevant cases based on keywords and jurisdiction"""
    query_lower = query.lower()
    relevant_cases = []
    
    for case in MOCK_CASE_DATABASE:
        # Filter by jurisdiction
        if jurisdiction != "all" and case.get("jurisdiction", "federal") != jurisdiction:
            continue
            
        relevance_score = 0
        
        # Check keywords
        for keyword in case["keywords"]:
            if keyword in query_lower:
                relevance_score += 2
        
        # Check case name
        if any(word in case["case_name"].lower() for word in query_lower.split()):
            relevance_score += 1
            
        # Check facts and legal principle
        if any(word in case["facts"].lower() for word in query_lower.split()):
            relevance_score += 1
        if any(word in case["legal_principle"].lower() for word in query_lower.split()):
            relevance_score += 1
            
        if relevance_score > 0:
            case_copy = case.copy()
            case_copy["relevance_score"] = relevance_score
            relevant_cases.append(case_copy)
    
    # Sort by relevance score
    relevant_cases.sort(key=lambda x: x["relevance_score"], reverse=True)
    return relevant_cases[:max_results]

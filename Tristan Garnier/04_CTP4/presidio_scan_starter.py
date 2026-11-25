"""CTP 4 - Exercise 1b STARTER: find PII hidden in free text with Microsoft Presidio.
Run from 04_CTP4:  python presidio_scan_starter.py
"""
import pandas as pd
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.predefined_recognizers import PhoneRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig

# 1. Small English model (fits 8 GB laptops). Default would download the large model.
nlp = NlpEngineProvider(nlp_configuration={"nlp_engine_name": "spacy",
                                           "models": [{"lang_code": "en", "model_name": "en_core_web_sm"}]}).create_engine()
analyzer = AnalyzerEngine(nlp_engine=nlp, supported_languages=["en"])
# TODO 2: the default phone recognizer only knows some countries (print PhoneRecognizer().supported_regions).
#         ShopFast also sells in Belgium and Spain: add PhoneRecognizer(supported_regions=["BE", "ES"]) to analyzer.registry.

ENTITIES = ["PERSON", "EMAIL_ADDRESS", "PHONE_NUMBER", "IBAN_CODE", "CREDIT_CARD", "DATE_TIME", "LOCATION"]
df = pd.read_csv("../shopfast-kit/data/support_tickets.csv", dtype=str).fillna("")

hits = []
for _, row in df.iterrows():
    for col in ["message", "agent_notes"]:
        for r in analyzer.analyze(text=row[col], language="en", entities=ENTITIES, score_threshold=0.4):
            hits.append({"ticket_id": row["ticket_id"], "column": col, "entity": r.entity_type,
                         "text": row[col][r.start:r.end], "score": round(r.score, 2)})
hits = pd.DataFrame(hits)
hits.to_csv("pii_findings.csv", index=False)
print(hits.groupby(["column", "entity"]).size().to_string())

# TODO 3: open pii_findings.csv. Look at 20 DATE_TIME and PERSON findings: how many are real PII? (precision)
# TODO 4: tune ENTITIES per column to remove the false positives - and re-run
# TODO 5: redact the texts with presidio_anonymizer.AnonymizerEngine and save support_tickets_redacted.csv

"""
  The Goal: Classify insurance document images into categories (Patient Bills, KYC
  Document, Medical Report, etc.) while spending as few API tokens as possible.

  ---
  It works in 3 stages, cheapest first:

  Stage 1 — Filename Check (free, instant)

  ▎ "Does the filename match a known pattern?"

  If the file is named bill_innovh_01.png, bill_innovh_02.png, etc. — we already know
  it's a Patient Bill just from the name. No need to open the file at all.

  Stage 2 — OCR + Keywords (cheap, no API call)

  ▎ "Can we read the text in the image and spot clue words?"

  Uses the easyocr library to extract all text from the image locally (on your machine).
   Then checks if that text contains keywords like:
  - aadhaar, pan card, passport → KYC Document
  - diagnosis, blood test, MRI → Medical Report
  - rx, tablet, dosage → Prescription
  - claim form, policy number → Claim Form
  - invoice, total amount → Patient Bills

  Stage 3 — LLM (expensive, last resort)

  ▎ "We couldn't figure it out — let the AI look at the image."

  Only images that pass through both stages without a match get sent to Gemini. The AI
  looks at the actual image and decides the category.

  ---
  Why this matters:

  Stage 1: 0 cost  — filename is enough
  Stage 2: ~0 cost — runs on your laptop
  Stage 3: 💰 cost — hits the Google API

  If 10 out of 40 images are caught by Stage 1, and 20 more by Stage 2 — only 10 need an
   API call. That's 75% savings in API costs.

  The summary printed at the end shows exactly how many files each stage handled and the
   total API calls saved.

Output of the function: - 

03ac1d4117.png                      3-llm      Prescription  
05a5de87a2.png                      3-llm      Prescription  
0c205798ca.png                      2-ocr      KYC Document  (text: tot India AADHAAR Unique Identificati...)
139bb4f7b2.png                      2-ocr      Medical Report  (text:  Clinical Pathology Laboratory ISO 1518...)
1943d55a29.png                      2-ocr      Medical Report  (text: SRL Pathology Lab ReportID RPT597...)
1b9d9c79d7.png                      3-llm      Prescription  
1f27fb123a.png                      3-llm      Prescription  
2561b8be1b.png                      2-ocr      KYC Document  (text: tot India AADHAAR Unique Identiticati...)
31d1b528ee.png                      2-ocr      KYC Document  (text: tof India AADHAAR Unique Identiticati...)
32912630ec.png                      2-ocr      Medical Report  (text:  Clinical Pathology Laboratory ISO 1518...)
3f106e6cf9.png                      2-ocr      KYC Document  (text: hul Mehta Date of Birth 27/'11/1980 Rerm...)
4115f113f3.png                      2-ocr      Medical Report  (text: SRL Pathology Lab ReportID RPT397...)
452dc2ddff.png                      2-ocr      Medical Report  (text:  Clinical Pathology Laboratory ISO 1518...)
47e3246946.png                      2-ocr      Medical Report  (text:  Clinical Pathology Laboratory ISO 1518...)
51e4f5bc5c.png                      3-llm      Prescription  
554581e3c6.png                      3-llm      Prescription  
6206d614b8.png                      2-ocr      Medical Report  (text: SRL Pathology Lab ReportID RPT503...)
79b6c74862.png                      2-ocr      KYC Document  (text: hul Mehta Date of Birth 08,01/1975 Perma...)
8bc6fff099.png                      3-llm      Prescription  
8beea3ceef.png                      3-llm      Prescription  
8fa03a84d1.png                      2-ocr      KYC Document  (text: eepa Nair Date of Birth 03,09/1995 Rerma...)
964d8d9ef6.png                      2-ocr      Medical Report  (text:  Clinical Pathology Laboratory ISO 1518...)
977387cb9e.png                      2-ocr      KYC Document  (text: ali Patel Date of Birth 1408/'1992 Perma...)
99da361705.png                      2-ocr      KYC Document  (text: ali Patel Date of Birth 27/11/1980 Perma...)
9wfojio23.png                       2-ocr      KYC Document  (text: Anand Rao Date of Birth: 14,08/1992 Gend...)
ZLKMXcsoikn.png                     2-ocr      KYC Document  (text: ha Sharma Date of Birth: 08,01/1975 Gend...)
a35d0f5a19.png                      2-ocr      Medical Report  (text:  Clinical Pathology Laboratory ISO 1518...)
a3d57c975e.png                      3-llm      Prescription  
a6f949d89a.png                      2-ocr      Medical Report  (text:  Clinical Pathology Laboratory ISO 1518...)
acjn0i923nxa.png                    2-ocr      KYC Document  (text: eer Jcshi Date of Birth: 12,04/'1988 Gen...)
acmslkvqef.png                      2-ocr      KYC Document  (text: e: Arvind Date of Birth: 12,04/'1988 Gen...)
bedfb6a400.png                      2-ocr      KYC Document  (text: tot India AADHAAR Unique Identiticati...)
bill_innovh_01.png                  1-regex    Patient Bills  
bill_innovh_02.png                  1-regex    Patient Bills  
bill_innovh_03.png                  1-regex    Patient Bills  
bill_innovh_04.png                  1-regex    Patient Bills  
bill_innovh_05.png                  1-regex    Patient Bills  
bill_innovh_06.png                  1-regex    Patient Bills  
bill_innovh_07.png                  1-regex    Patient Bills  
bill_innovh_08.png                  1-regex    Patient Bills  
bill_innovh_09.png                  1-regex    Patient Bills  
bill_innovh_10.png                  1-regex    Patient Bills  
ckmwd-0q12.png                      2-ocr      KYC Document  (text: esh Patel Date of Birth: 08,01/1975 Gend...)
dlkjjwdkokf.png                     2-ocr      KYC Document  (text: eera Shah Date of Birth: 27/11/1980 Gend...)
ea37c9fadc.png                      3-llm      Prescription  
ebc3152f15.png                      2-ocr      KYC Document  (text: tot India AADHAAR Unique Identificati...)
knadwq0-2.png                       2-ocr      KYC Document  (text: me: Gupta Date of Birth: 14,08/1992 Gend...)
scanned_012389984.png               2-ocr      KYC Document  (text:  Krishnan Date of Birth: 03,09/1995 Gend...)
sdik9q32ei.png                      2-ocr      KYC Document  (text: anka lyer Date of Birth: 08,01/1975 Gend...)
zljnkcjwd990.png                    2-ocr      KYC Document  (text: vya Reddy Date of Birth: 12,004/'1988 Ge...)
--------------------------------------------------------------------------------

Summary:
  Stage 1 (filename regex) : 10 files
  Stage 2 (OCR keywords)   : 30 files
  Stage 3 (LLM API call)   : 10 files

  API calls saved: 40/50 (80%)

"""

from google import genai
from google.genai import types
from google.genai.errors import ClientError
from dotenv import load_dotenv
import os
import re
import time
import warnings
import easyocr

warnings.filterwarnings("ignore", category=UserWarning, module="torch")

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

CATEGORIES = [
    "Patient Bills",
    "Claim Form",
    "KYC Document",
    "Medical Report",
    "Prescription",
    "Unknown"
]

OCR_RULES = [
    (
        "KYC Document",
        re.compile(
            r"\b(aadhaar|aadhar|pan\s*card|pan\s*number|passport|voter\s*id|voter\s*card|"
            r"driving\s*licen[sc]e|date\s*of\s*birth|dob|proof\s*of\s*identity|"
            r"proof\s*of\s*address|kyc|government\s*id|national\s*id)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Prescription",
        re.compile(
            r"\b(rx|prescribed\s*by|dosage|tablet|capsule|\bmg\b|twice\s*daily|"
            r"once\s*daily|thrice\s*daily|sig:|dispense|refill|pharmacy)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Medical Report",
        re.compile(
            r"\b(diagnosis|laboratory|lab\s*report|blood\s*test|radiology|mri|x[\s-]?ray|"
            r"cbc|haemoglobin|hemoglobin|pathology|biopsy|ct\s*scan|ultrasound|"
            r"test\s*result|patient\s*report)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Claim Form",
        re.compile(
            r"\b(claim\s*form|claim\s*number|claimant|insurance\s*claim|"
            r"policy\s*number|reimbursement|hospitalisation|hospitalization|"
            r"tpa|third\s*party\s*administrator|cashless)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "Patient Bills",
        re.compile(
            r"\b(invoice|bill\s*no|bill\s*number|total\s*amount|amount\s*due|"
            r"patient\s*name|admission|discharge|receipt|hospital\s*bill)\b",
            re.IGNORECASE,
        ),
    ),
]

ocr_reader = None


def get_ocr_reader():
    global ocr_reader
    if ocr_reader is None:
        ocr_reader = easyocr.Reader(["en"], verbose=False)
    return ocr_reader


# Stage 1: filename regex — zero cost
def stage1_filename(filename: str) -> str | None:
    if re.match(r"^bill_innovh_\d+\.(png|jpg|jpeg)$", filename, re.IGNORECASE):
        return "Patient Bills"
    return None


# Stage 2: OCR + keyword matching — no LLM cost
def stage2_ocr(image_path: str) -> tuple[str, str] | None:
    reader = get_ocr_reader()
    results = reader.readtext(image_path, detail=0)
    text = " ".join(results)
    for category, pattern in OCR_RULES:
        m = pattern.search(text)
        if m:
            snippet = text[max(0, m.start() - 10): m.end() + 20].replace("\n", " ")
            return category, snippet
    return None


_llm_quota_exhausted = False


def _is_daily_quota_exhausted(e: ClientError) -> bool:
    try:
        msg = str(e)
        return "PerDay" in msg and "429" in msg
    except Exception:
        return False


def _get_status_code(e: ClientError) -> int:
    # google-genai ClientError stores status code in args[0] or .code
    for attr in ("code", "status_code"):
        val = getattr(e, attr, None)
        if val is not None:
            return int(val)
    return e.args[0] if e.args else 0


# Stage 3: LLM fallback with exponential backoff
def stage3_llm(image_path: str) -> str:
    global _llm_quota_exhausted
    if _llm_quota_exhausted:
        return "Unknown (quota exhausted)"

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    prompt = (
        f"You are a document classifier for a health insurance firm.\n"
        f"Classify the document in this image into exactly one of these categories:\n"
        f"{', '.join(CATEGORIES)}\n"
        f"Reply with only the category name, nothing else."
    )
    max_retries = 5
    delay = 5
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model="gemma-4-31b-it",
                contents=[
                    types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
                    types.Part.from_text(text=prompt),
                ],
            )
            result = response.text.strip()
            return result if result in CATEGORIES else "Unknown"
        except ClientError as e:
            if _is_daily_quota_exhausted(e):
                print("  [daily quota exhausted] skipping remaining LLM calls")
                _llm_quota_exhausted = True
                return "Unknown (quota exhausted)"
            if _get_status_code(e) == 429 and attempt < max_retries - 1:
                print(f"  [rate limited] retrying in {delay}s...")
                time.sleep(delay)
                delay *= 2
            else:
                raise


def classify_insurance_document(image_path: str) -> tuple[str, str, str]:
    """Returns (category, stage_label, detail)"""
    filename = os.path.basename(image_path)

    category = stage1_filename(filename)
    if category:
        return category, "1-regex", ""

    result = stage2_ocr(image_path)
    if result:
        category, snippet = result
        return category, "2-ocr", f"(text: {snippet[:40]}...)"

    category = stage3_llm(image_path)
    return category, "3-llm", ""


if __name__ == "__main__":
    dataset_dir = os.path.join(os.path.dirname(__file__), "dataset")
    images = sorted(f for f in os.listdir(dataset_dir) if f.lower().endswith((".png", ".jpg", ".jpeg")))
    total = len(images)
    counts = {"1-regex": 0, "2-ocr": 0, "3-llm": 0}

    for filename in images:
        image_path = os.path.join(dataset_dir, filename)
        category, stage, detail = classify_insurance_document(image_path)
        if "quota exhausted" not in category:
            counts[stage] += 1
            print(f"{filename:<35} {stage:<10} {category}  {detail}")

    print("-" * 80)
    print("\nSummary:")
    print(f"  Stage 1 (filename regex) : {counts['1-regex']} files")
    print(f"  Stage 2 (OCR keywords)   : {counts['2-ocr']} files")
    print(f"  Stage 3 (LLM API call)   : {counts['3-llm']} files")
    llm_saved = counts["1-regex"] + counts["2-ocr"]
    print(f"\n  API calls saved: {llm_saved}/{total} ({llm_saved * 100 // total}%)")

# Insurance Document Classifier

**The Goal:** Classify insurance document images into categories (Patient Bills, KYC Document, Medical Report, etc.) while spending as few API tokens as possible.

---

## How It Works

It works in 3 stages, cheapest first:

### Stage 1 — Filename Check _(free, instant)_

> "Does the filename match a known pattern?"

If the file is named `bill_innovh_01.png`, `bill_innovh_02.png`, etc. — we already know it's a Patient Bill just from the name. No need to open the file at all.

### Stage 2 — OCR + Keywords _(cheap, no API call)_

> "Can we read the text in the image and spot clue words?"

Uses the `easyocr` library to extract all text from the image locally (on your machine). Then checks if that text contains keywords like:

| Keywords | Category |
|---|---|
| aadhaar, pan card, passport | KYC Document |
| diagnosis, blood test, MRI | Medical Report |
| rx, tablet, dosage | Prescription |
| claim form, policy number | Claim Form |
| invoice, total amount | Patient Bills |

### Stage 3 — LLM _(expensive, last resort)_

> "We couldn't figure it out — let the AI look at the image."

Only images that pass through both stages without a match get sent to Gemini. The AI looks at the actual image and decides the category.

---

## Cost Breakdown

| Stage | Cost | Method |
|---|---|---|
| Stage 1 | 0 | filename is enough |
| Stage 2 | ~0 | runs on your laptop |
| Stage 3 | 💰 | hits the Google API |

If 10 out of 40 images are caught by Stage 1, and 20 more by Stage 2 — only 10 need an API call. That's **75% savings in API costs**.

The summary printed at the end shows exactly how many files each stage handled and the total API calls saved.

---

## Sample Output

```
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
```

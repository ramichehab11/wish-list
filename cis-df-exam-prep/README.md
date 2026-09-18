# CIS-DF (Data Foundations: CMDB and CSDM) - 3-Day Exam Prep Kit

Exam: ServiceNow Certified Implementation Specialist - Data Foundations (CMDB and CSDM), "CIS-DF".
Exam night: Saturday. Available study time: ~3 h Thursday, Friday, Saturday daytime.

## What is in this folder

**Start with `index.html`.** It is the guided companion app: open it in a browser and it walks you through the
three days with checkable steps, links into every section below, flip flashcards, self-grading tests with
per-domain scores, the lab checklist and a button that opens the 386-question bank. Progress is saved in that
browser. The markdown files remain the readable source of the same content.

| File | Use it for | When |
|---|---|---|
| `01-study-guide.md` | Condensed notes per exam domain, weighted to the blueprint. CSDM section is deliberately the longest. | Thu + Fri |
| `02-terminology-flashcards.md` | ~100 term -> definition pairs. Cover the right column and self-test. | Every day, 10 min |
| `03-diagnostic-quiz.md` + `03-diagnostic-answer-key.md` | 30 questions to find your weak domains. Time-box it to 35 min. | Thu, first thing |
| `04-mock-exam-A.md` + `04-mock-exam-A-answer-key.md` | 40-question timed mock (50 min). | Fri evening or Sat morning |
| `05-hands-on-pdi-checklist.md` | 60-90 min of clicks in a Personal Developer Instance on the features the exam names. | Fri |
| `06-common-traps.md` | Confusable pairs the exam loves. Read the night before. | Sat |
| `07-practice-bank-386-questions.html` | Interactive 386-question bank (5 quizzes, review mode, drag-and-drop). Your main testing tool. | Thu-Sat |
| `walk.html` | **Night walk mode** for the phone: reads 20-second briefings, flashcards and quiz questions aloud with a thinking pause, hands-free. Zero reading required. | Every evening |
| `08-blueprint-addendum.md` | Official blueprint sub-topics mapped to the kit, plus the topics added after reading it and the 3 official sample questions. | Fri |

## Exam facts (from the official blueprint, KB0012913, updated November 2025)

| Item | Value |
|---|---|
| Domains and weights | Configuration 15% · Ingest 19% · **Govern 35%** · Insight 20% · CSDM Fundamentals 11% |
| Questions and time | **75 questions, 90 minutes** (about 72 seconds per question) |
| Item types | Multiple choice (3+ options), multiple select (states how many to pick, **no partial credit**), **drag-and-drop matching** (three variants, **no partial credit**), scenario-based items in either format |
| Passing | A predetermined cut score that ServiceNow does not publish and that is **not always 70%**. Section percentages on the result report do not determine the result. |
| Delivery | Pearson VUE test centre or OnVUE online proctoring. Result shown immediately as a conditional pass/fail. |
| Recommended background | CSA, 2+ years CMDB, CSDM foundational knowledge, experience with duplicates, lifecycle (retire/archive), compliance audit remediation, multisource/CMDB 360 |
| Official prep courses | CMDB Fundamentals · CMDB Health Micro-Certification Simulator · Configure the CMDB Micro-Certification Simulator · CSDM Fundamentals · CMDB Health Deep Dive; extras: Introduction to CMDB Workspace, Design a Successful CMDB, Discovery / Service Mapping / ACC / Service Graph Connector / MID Server fundamentals, Now Create CMDB and CSDM Data Foundations |
| Official practice exam | MeasureUp, see KB0013408 on ServiceNow University |

Govern + Insight together are 55% of the exam. Your CMDB experience helps most in Configuration and Ingest. The
biggest point swings are in Govern (Health, Data Manager, lifecycle, governance roles) and in CSDM terminology.

**Read `08-blueprint-addendum.md` before Friday.** It maps every sub-topic on the official blueprint to the kit
and covers the ones the first version of the study guide under-served: asset-CI alignment, the six health metrics,
principal classes, the de-duplication wizard, Data Foundations Dashboard playbooks, Unified Map, Natural Language
Query and CMDB saved queries. It also contains the three official sample questions.

## The 3-day plan

### Thursday (3 hours)

| Time | Activity |
|---|---|
| 0:00 - 0:35 | Take `03-diagnostic-quiz.md` cold, timed. No notes. Write answers as `1-B, 2-AC, ...`. |
| 0:35 - 1:00 | Grade with the key. Mark each miss with its domain. Send me your answers so I can target the rest of the kit. |
| 1:00 - 2:00 | `01-study-guide.md` section 6 (CSDM) end to end. Then flashcards, CSDM block only. |
| 2:00 - 2:10 | Break. |
| 2:10 - 2:50 | `01-study-guide.md` section 4 (Govern). This is 35% of the exam. |
| 2:50 - 3:00 | Re-answer the diagnostic questions you missed, from memory. |

### Friday

| Block | Activity |
|---|---|
| 1 (60 min) | Study guide sections 3 (Ingest) and 2 (Configuration). Skim what you already live in, slow down on IRE rule types, data precedence, refresh rules, Service Graph Connectors vs IntegrationHub ETL. |
| 2 (30 min) | Study guide section 5 (Insight): CMDB Workspace, CMDB 360, Query Builder, Data Foundations Dashboard. |
| 3 (60-90 min) | `05-hands-on-pdi-checklist.md` in a PDI. Seeing Health Preferences, Data Manager policies and the IRE simulator once is worth more than rereading. |
| 4 (50 min + 30 min) | `04-mock-exam-A.md` timed, then grade and read every explanation, including questions you got right by luck. |
| 5 (10 min) | Flashcards, all blocks. |

### Saturday (exam day)

| Block | Activity |
|---|---|
| Morning (45 min) | `06-common-traps.md`, then flashcards once more. |
| Midday (45 min) | Redo every question you missed on both tests. If I have sent you a second mock, take it now. |
| Afternoon | Stop studying 3 hours before the exam. Check the proctoring setup (webcam, ID, clean desk, browser). |
| During exam | 90 min for 75 questions = 72 seconds per question. Flag and move on. Multi-select states how many to pick and gives no partial credit, so never leave one short. Drag-and-drop also gives no partial credit: an unused option is allowed in one variant, and one right-hand item may match several left-hand items in another. Eliminate answers that name the wrong tool for the job (see traps file). |

## What I need from you to tune this kit

1. Your diagnostic answers (just the letters). I will grade, explain misses and build a second mock focused on your gaps.
2. Whether you have a PDI (developer.servicenow.com) and which release it is on. If yes, do the lab checklist.
3. Whether you can access the free "Data Foundations Fundamentals" on-demand course on ServiceNow University. If yes, watch only the CSDM and CMDB Health modules at 1.5x.
4. Any official practice-exam questions you have seen and could not answer. Paste them and I will explain the reasoning.
5. After Thursday: tell me which two topics still feel foggy. I will write a focused drill for each.

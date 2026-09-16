# CIS-DF (Data Foundations: CMDB and CSDM) - 3-Day Exam Prep Kit

Exam: ServiceNow Certified Implementation Specialist - Data Foundations (CMDB and CSDM), "CIS-DF".
Exam night: Saturday. Available study time: ~3 h Thursday, Friday, Saturday daytime.

## What is in this folder

| File | Use it for | When |
|---|---|---|
| `01-study-guide.md` | Condensed notes per exam domain, weighted to the blueprint. CSDM section is deliberately the longest. | Thu + Fri |
| `02-terminology-flashcards.md` | ~100 term -> definition pairs. Cover the right column and self-test. | Every day, 10 min |
| `03-diagnostic-quiz.md` + `03-diagnostic-answer-key.md` | 30 questions to find your weak domains. Time-box it to 35 min. | Thu, first thing |
| `04-mock-exam-A.md` + `04-mock-exam-A-answer-key.md` | 40-question timed mock (50 min). | Fri evening or Sat morning |
| `05-hands-on-pdi-checklist.md` | 60-90 min of clicks in a Personal Developer Instance on the features the exam names. | Fri |
| `06-common-traps.md` | Confusable pairs the exam loves. Read the night before. | Sat |

## Exam facts (from public blueprint summaries)

| Item | Value |
|---|---|
| Domains and weights | Configuration 15% · Ingest 19% · **Govern 35%** · Insight 20% · CSDM Fundamentals 11% |
| Format | Multiple choice + multiple select, online proctored, 90 minutes |
| Questions | Public sources say 60 to 75. Check your exam confirmation email. |
| Passing | Approximately 70% (ServiceNow does not publish a fixed cut score) |
| Recommended background | CSA + about 2 years of CMDB experience |
| Official prep | "Implementer Data Foundations (CMDB and CSDM)" credential path on ServiceNow University; official blueprint is KB0012913 on learning.servicenow.com |

Govern + Insight together are 55% of the exam. Your CMDB experience helps most in Configuration and Ingest. The
biggest point swings are in Govern (Health, Data Manager, lifecycle, governance roles) and in CSDM terminology.

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
| During exam | 90 min for ~60-75 questions = about 1:15 per question. Flag and move on. For multi-select, the count of correct answers is stated. Eliminate answers that name the wrong tool for the job (see traps file). |

## What I need from you to tune this kit

1. Your diagnostic answers (just the letters). I will grade, explain misses and build a second mock focused on your gaps.
2. Whether you have a PDI (developer.servicenow.com) and which release it is on. If yes, do the lab checklist.
3. Whether you can access the free "Data Foundations Fundamentals" on-demand course on ServiceNow University. If yes, watch only the CSDM and CMDB Health modules at 1.5x.
4. Any official practice-exam questions you have seen and could not answer. Paste them and I will explain the reasoning.
5. After Thursday: tell me which two topics still feel foggy. I will write a focused drill for each.

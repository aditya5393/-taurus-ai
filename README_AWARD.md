# Taurus AI - Award Edition: All 8 Improvements Added

## What was added (8 points)

1. **ONE Killer Story** - `docs/killer_story.md` - One end-to-end demo story: Research + Draft + Calendar + Report from ONE goal
2. **Measurable Self-Learning** - `app/evaluation.py` - 20-task test set, Day 1 vs Day 7, Learning Curve graph. Run: `python -c "from app.evaluation import learning_curve; print(learning_curve())"`
3. **Adaptive Routing That Learns YOU** - `app/adaptive_routing.py` - Tracks per-user model success, prefers best model for YOU. `best_model_for()` + `adaptive_summary()`
4. **Failure + Recovery Demo** - `app/failure_recovery.py` - Controlled buggy code -> Critic -> Fixed -> Success. Use in video.
5. **Real Users + Real Numbers** - `app/feedback.py` - Collect feedback from 10 classmates, `summary()` gives poster line: "Tested by X students, saved Y hours"
6. **Multimodal / RAG** - `app/rag.py` - Personal Knowledge Base: Upload notes to `knowledge_base/`, `answer_from_notes()` answers ONLY from your notes (RAG). For PDF: PyPDF2, for images: pytesseract OCR.
7. **Safety + Privacy** - `app/safety.py` - Approval-gated (never auto-send), Local-first memory, Deletable memory, Full trace, `privacy_summary()`
8. **Award Package** - `docs/award_poster_outline.md` (1-page poster), `docs/video_script.md` (2-min video), `docs/killer_story.md`, this README

## How to use for awards
1. Run evaluation Day 1, get corrections, run Day 7 -> show Learning Curve
2. Get 10 classmates to try, collect feedback via `feedback.py`
3. Record 2-min video using `video_script.md`
4. Print poster using `award_poster_outline.md`
5. Deploy Streamlit v4 + have backup video file

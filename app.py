# Workout Progress Tracker — Streamlit (Liquid Glass theme, no sidebar)
# Save as: app.py
# Run with: streamlit run app.py

import json
from datetime import date

import pandas as pd
import streamlit as st

# -----------------------
# Page Config (no sidebar)
# -----------------------
st.set_page_config(
    page_title="Workout Progress Tracker",
    page_icon="🏋️",
    layout="wide",
)

# =======================
# Liquid Glass THEME CSS
# =======================
st.markdown(
    """
    <style>
      /* Import clean modern fonts */
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@400;600;700&display=swap');

      html, body, [class^="css"]  { font-family: 'Plus Jakarta Sans', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif; }

      /* Vivid animated gradient background */
      .liquid-bg {
        position: fixed; inset: 0; z-index: -1; overflow: hidden;
        background: radial-gradient(1200px 600px at 20% -10%, rgba(99,102,241,0.20), transparent),
                    radial-gradient(900px 500px at 80% -10%, rgba(16,185,129,0.18), transparent),
                    radial-gradient(700px 400px at 50% 110%, rgba(236,72,153,0.18), transparent),
                    linear-gradient(180deg, #0b1020 0%, #0e1222 100%);
      }
      .bubble { position:absolute; border-radius:50%; filter: blur(24px); opacity:.45; animation: drift 26s ease-in-out infinite alternate; }
      .b1 { width:480px; height:480px; background:#60a5fa55; left:5%; top:15%; }
      .b2 { width:380px; height:380px; background:#34d39955; right:8%; top:8%; animation-duration: 32s; }
      .b3 { width:520px; height:520px; background:#f472b655; left:35%; bottom:-10%; animation-duration: 28s; }
      @keyframes drift { from { transform: translateY(-10px) translateX(-10px) } to { transform: translateY(20px) translateX(20px) } }

      /* Glass containers */
      .glass { backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); background: rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.10); border-radius:16px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); }
      .glass-soft { backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.08); border-radius:14px; }

      /* Header */
      .app-header { padding: 22px 22px; margin-top: 4px; }
      .app-title { font-family:'Space Grotesk', sans-serif; font-weight:800; font-size: 30px; margin:0; color: #e5e7eb; letter-spacing: .3px; }
      .app-sub { color: #9fb3c8; margin: 6px 0 0 0; }

      /* Top toolbar sticky */
      .toolbar { position: sticky; top: 0; z-index: 50; padding: 10px; margin: 12px 0 14px; }
      .toolbar-inner { display:flex; gap:10px; align-items:center; justify-content:space-between; }
      .toolbar-left { display:flex; gap:10px; align-items:center; flex-wrap:wrap; }
      .toolbar-right { display:flex; gap:8px; align-items:center; }

      /* Inputs styling (subtle glass) */
      .stSelectbox, .stDateInput, .stFileUploader, .stDownloadButton, .stTextInput { filter: drop-shadow(0 2px 10px rgba(0,0,0,.15)); }

      /* KPI chips */
      .kpi { display:flex; flex-direction:column; gap:4px; padding: 14px; }
      .kpi h3 { margin:0; font-size:12px; color:#9fb3c8; font-weight:700; letter-spacing:.3px; }
      .kpi p { margin:0; font-size:22px; font-weight:800; color:#e5e7eb; }

      /* Exercise card */
      .card { padding: 14px 14px; margin-bottom: 12px; }
      .card h4 { margin:0; font-weight:800; color:#eaf2ff; letter-spacing:.2px; }
      .muted { color:#a7b7cc; }
      .tag {
        display:inline-block; padding:6px 10px; font-size:12px; border-radius:999px; margin-right:6px;
        background: linear-gradient(90deg, rgba(99,102,241,0.35), rgba(16,185,129,0.35)); color:#eaf2ff; border:1px solid rgba(255,255,255,0.10)
      }
      .hr { height:1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent); margin:10px 0 12px; }

      /* Set pills */
      .set-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); gap:8px; }
      .set-pill { display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:12px; border:1px solid rgba(255,255,255,0.12);
                  background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); }

      /* Buttons */
      .btn-row { display:flex; gap:8px; }

      /* Space tightening */
      .block-gap { margin-top: 8px; margin-bottom: 6px; }
    </style>
    <div class="liquid-bg">
      <div class="bubble b1"></div>
      <div class="bubble b2"></div>
      <div class="bubble b3"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------
# Structured 5-day workout program
# ---------------------------------
WORKOUT_PLAN = {
    "Day 1 – Push (Chest, Shoulders, Triceps)": [
        {"name": "Warm-up: Cycle", "sets": 1, "reps": "5 min"},
        {"name": "Chest Press", "sets": 4, "reps": "10–12"},
        {"name": "Incline Press", "sets": 4, "reps": "8–10"},
        {"name": "Shoulder Press", "sets": 4, "reps": "10–12"},
        {"name": "Pec Fly (machine)", "sets": 3, "reps": "12–15"},
        {"name": "Dumbbell Lateral Raises", "sets": 3, "reps": "12–15"},
        {"name": "Push-ups (burn-out)", "sets": 2, "reps": "Failure"},
    ],
    "Day 2 – Pull (Back, Biceps, Rear Delts)": [
        {"name": "Warm-up: Cycle", "sets": 1, "reps": "5 min"},
        {"name": "Lat Pulldown", "sets": 4, "reps": "8–12"},
        {"name": "Seated Row", "sets": 4, "reps": "8–12"},
        {"name": "Rear Delt Machine", "sets": 3, "reps": "12–15"},
        {"name": "Dumbbell Bicep Curls", "sets": 3, "reps": "10–12"},
        {"name": "Hammer Curls", "sets": 3, "reps": "10–12"},
        {"name": "Face Pulls", "sets": 2, "reps": "12–15"},
    ],
    "Day 3 – Legs (Quads, Hamstrings, Glutes, Calves)": [
        {"name": "Warm-up: Incline Walk", "sets": 1, "reps": "5 min"},
        {"name": "Leg Press", "sets": 4, "reps": "10–12"},
        {"name": "Leg Extension", "sets": 4, "reps": "12–15"},
        {"name": "Leg Curl", "sets": 4, "reps": "12–15"},
        {"name": "Hip Abductor", "sets": 3, "reps": "15–20"},
        {"name": "Walking Lunges", "sets": 3, "reps": "12 each leg"},
        {"name": "Standing Calf Raises", "sets": 3, "reps": "15–20"},
    ],
    "Day 4 – Push/Pull Hybrid (Upper Body Pump + Core)": [
        {"name": "Warm-up: Cycle", "sets": 1, "reps": "5 min"},
        {"name": "Incline Press", "sets": 4, "reps": "8–10"},
        {"name": "Lat Pulldown", "sets": 4, "reps": "8–10"},
        {"name": "Shoulder Press", "sets": 3, "reps": "10–12"},
        {"name": "Seated Row", "sets": 3, "reps": "10–12"},
        {"name": "Pec Fly", "sets": 3, "reps": "12–15"},
        {"name": "Rear Delt Machine", "sets": 3, "reps": "12–15"},
        {"name": "Planks / Hanging Knee Raises", "sets": 3, "reps": "30–60 sec"},
    ],
    "Day 5 – Conditioning + Full Body Burn": [
        {"name": "Warm-up: Treadmill", "sets": 1, "reps": "5 min"},
        {"name": "Dumbbell Thrusters", "sets": 3, "reps": "12"},
        {"name": "Dumbbell Romanian Deadlift", "sets": 3, "reps": "12"},
        {"name": "Push-ups", "sets": 3, "reps": "12–15"},
        {"name": "Dumbbell Rows", "sets": 3, "reps": "12 each side"},
        {"name": "Cycle Intervals", "sets": 10, "reps": "20s sprint / 40s easy"},
        {"name": "Core Finisher (Russian Twists + Leg Raises)", "sets": 3, "reps": "15 each"},
    ],
}

DAY_OPTIONS = list(WORKOUT_PLAN.keys())

# Utility: build a stable, unique key for each set checkbox

def set_key(d_str: str, day: str, ex_idx: int, set_idx: int) -> str:
    return f"chk::{d_str}::{day}::ex{ex_idx}::set{set_idx}"


def exercise_done_ratio(d_str: str, day: str):
    total_sets, done_sets, full_exercises = 0, 0, 0
    for i, ex in enumerate(WORKOUT_PLAN[day]):
        sets = ex["sets"]
        total_sets += sets
        ex_done = True
        for s in range(sets):
            if st.session_state.get(set_key(d_str, day, i, s), False):
                done_sets += 1
            else:
                ex_done = False
        if ex_done:
            full_exercises += 1
    return total_sets, done_sets, full_exercises


def _safe_rerun():
    try:
        st.rerun()
    except Exception:
        st.experimental_rerun()

# ==============
# App Header
# ==============
st.markdown('<div class="glass app-header"><h1 class="app-title">Workout Progress Tracker</h1><p class="app-sub">Track sets across a 5‑day split. Liquid glass UI · No sidebar · Colorful & compact.</p></div>', unsafe_allow_html=True)

# Top sticky toolbar (no sidebar)
with st.container():
    st.markdown('<div class="glass toolbar"><div class="toolbar-inner">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.2, 1.5, 2, 2])
    with c1:
        selected_date = st.date_input("Training Date", value=date.today(), format="YYYY-MM-DD")
        date_str = selected_date.isoformat()
    with c2:
        # Day quick picker
        day_short = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
        default_idx = 0 if "__day_idx__" not in st.session_state else st.session_state["__day_idx__"]
        idx = st.selectbox("Day", options=list(range(5)), format_func=lambda i: day_short[i], index=default_idx, key="__select_day__")
        st.session_state["__day_idx__"] = idx
        day = DAY_OPTIONS[idx]
    with c3:
        ex_names = [ex["name"] for ex in WORKOUT_PLAN[day]]
        chosen = st.selectbox("Workout", ["All exercises"] + ex_names, key=f"__ex_select_{idx}")
    with c4:
        # Compact Sync & Reset controls
        with st.expander("☁️ Sync & Reset", expanded=False):
            export_data = {k: v for k, v in st.session_state.items() if isinstance(v, bool) and k.startswith("chk::")}
            if export_data:
                st.download_button(
                    "Export progress (JSON)",
                    data=json.dumps(export_data, indent=2),
                    file_name="workout_progress.json",
                    mime="application/json",
                    use_container_width=True,
                )
            else:
                st.caption("No progress yet to export.")

            uploaded = st.file_uploader("Import progress JSON", type=["json"], help="Merges into current session")
            if uploaded is not None:
                try:
                    incoming = json.load(uploaded)
                    if isinstance(incoming, dict):
                        for k, v in incoming.items():
                            if isinstance(v, bool) and k.startswith("chk::"):
                                st.session_state[k] = v
                        st.success("Imported progress. If you don't see updates, change a control to refresh.")
                    else:
                        st.error("Invalid file structure.")
                except Exception as e:
                    st.error(f"Import failed: {e}")

            st.markdown("---")
            colA, colB = st.columns(2)
            with colA:
                if st.button("🔁 Reset selected exercise", use_container_width=True):
                    if chosen != "All exercises":
                        eidx = ex_names.index(chosen)
                        st.session_state["__pending_action__"] = {"type": "exercise", "date": date_str, "day": day, "ex_idx": eidx, "value": False, "msg": f"Reset: {chosen}"}
                        _safe_rerun()
                    else:
                        st.info("Pick a single workout to reset.")
            with colB:
                if st.button("🧹 Reset this day", use_container_width=True):
                    st.session_state["__pending_action__"] = {"type": "day", "date": date_str, "day": day, "value": False, "msg": f"Cleared all sets for {day} on {date_str}"}
                    _safe_rerun()

    st.markdown('</div></div>', unsafe_allow_html=True)

# Apply any deferred actions BEFORE rendering widgets below
action = st.session_state.pop("__pending_action__", None)
if action:
    if action["type"] == "exercise":
        ex = WORKOUT_PLAN[action["day"]][action["ex_idx"]]
        for s in range(ex["sets"]):
            st.session_state[set_key(action["date"], action["day"], action["ex_idx"], s)] = action["value"]
        st.toast(action.get("msg", "Updated"))
    elif action["type"] == "day":
        for i, ex in enumerate(WORKOUT_PLAN[action["day"]]):
            for s in range(ex["sets"]):
                st.session_state[set_key(action["date"], action["day"], i, s)] = action["value"]
        st.toast(action.get("msg", "Updated"))

# ==============
# KPI Row
# ==============
T, D, E = exercise_done_ratio(date_str, day)
pct = int((D / T * 100) if T else 0)

k1, k2, k3, k4 = st.columns([1,1,1,1])
with k1:
    st.markdown('<div class="glass kpi"><h3>DAY</h3><p>'+day.split('–')[0].strip()+'</p></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="glass kpi"><h3>COMPLETED SETS</h3><p>{D} / {T}</p></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="glass kpi"><h3>COMPLETION</h3><p>{pct}%</p></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="glass kpi"><h3>EXERCISES DONE</h3><p>{E} / {len(WORKOUT_PLAN[day])}</p></div>', unsafe_allow_html=True)

st.progress(pct / 100 if T else 0.0, text=f"{pct}% complete")

st.markdown("<div class='block-gap'></div>", unsafe_allow_html=True)

# ==========================
# Tracker: compact grid cards
# ==========================
# Render one or many exercise cards
render_all = chosen == "All exercises"
exercises = WORKOUT_PLAN[day]

cols = st.columns(2, gap="small")

for i, ex in enumerate(exercises):
    if (not render_all) and (ex["name"] != chosen):
        continue

    col = cols[i % 2]
    with col:
        st.markdown('<div class="glass card">', unsafe_allow_html=True)
        top_l, top_r = st.columns([3,1])
        with top_l:
            st.markdown(f"<h4>{ex['name']}</h4>", unsafe_allow_html=True)
            st.markdown(f"<span class='tag'>Sets: {ex['sets']}</span> <span class='tag'>Target: {ex['reps']}</span>", unsafe_allow_html=True)
        with top_r:
            all_done = all(st.session_state.get(set_key(date_str, day, i, s), False) for s in range(ex["sets"]))
            st.markdown(f"<p class='muted' style='text-align:right'>{'✅ All done' if all_done else '⏳ In progress'}</p>", unsafe_allow_html=True)

        st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

        # Initialize keys and show set pills
        st.markdown('<div class="set-grid">', unsafe_allow_html=True)
        for s in range(ex["sets"]):
            key = set_key(date_str, day, i, s)
            if key not in st.session_state:
                st.session_state[key] = False
            with st.container():
                st.markdown('<div class="set-pill">', unsafe_allow_html=True)
                st.checkbox(f"Set {s+1}", key=key)
                st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Buttons (defer mutations)
        b1, b2 = st.columns([1,1])
        with b1:
            if st.button("Mark all done", key=f"done_{idx}_{i}", use_container_width=True):
                st.session_state["__pending_action__"] = {"type":"exercise","date":date_str,"day":day,"ex_idx":i,"value":True,"msg":f"Completed: {ex['name']}"}
                _safe_rerun()
        with b2:
            if st.button("Reset", key=f"reset_{idx}_{i}", use_container_width=True):
                st.session_state["__pending_action__"] = {"type":"exercise","date":date_str,"day":day,"ex_idx":i,"value":False,"msg":f"Reset: {ex['name']}"}
                _safe_rerun()

        st.markdown('</div>', unsafe_allow_html=True)

# ==========================
# Session Summary (optional)
# ==========================
with st.expander("📈 Session Summary"):
    summary = []
    for k, v in st.session_state.items():
        if isinstance(v, bool) and k.startswith("chk::"):
            try:
                _, dstr, dday, rest = k.split("::", 3)
            except ValueError:
                continue
            summary.append((dstr, dday, v))

    if not summary:
        st.info("No data yet. Check off a few sets to populate progress.")
    else:
        df = (
            pd.DataFrame(summary, columns=["date", "day", "done"])\
              .groupby(["date", "day"]).agg(total_sets=("done", "size"), completed=("done", "sum"))
              .reset_index()
        )
        df["completion_%"] = (df["completed"] / df["total_sets"]).round(3) * 100
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.set_index("date")["completion_%"], use_container_width=True)

# ---------------
# End of script
# ---------------

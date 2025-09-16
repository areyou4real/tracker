# Workout Progress Tracker — Streamlit (Liquid Glass MAX theme, no sidebar)
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
# Liquid Glass MAX THEME CSS (animations galore)
# =======================
st.markdown(
    """
    <style>
      /* Fonts */
      @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@400;600;700&display=swap');
      html, body, [class^="css"]  { font-family: 'Plus Jakarta Sans', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', sans-serif; }

      /* Root color tokens */
      :root{
        --bg-dark:#0b1020; --bg-darker:#0a0f1e; --fg:#e5e7eb; --muted:#9fb3c8;
        --accentA:#6366f1; --accentB:#10b981; --accentC:#ec4899; --accentD:#f59e0b;
        --glass: rgba(255,255,255,0.06); --glass-soft: rgba(255,255,255,0.05);
      }

      /* Background: animated gradients + parallax bubbles */
      .liquid-bg { position: fixed; inset: 0; z-index: -2; overflow: hidden; background: linear-gradient(180deg, var(--bg-dark), var(--bg-darker)); }
      .blob { position:absolute; border-radius:50%; filter: blur(26px); opacity:.45; animation: drift 26s ease-in-out infinite alternate; }
      .b1 { width:520px; height:520px; background: color-mix(in oklab, var(--accentA) 45%, transparent); left:5%; top:12%; animation-duration:30s; }
      .b2 { width:420px; height:420px; background: color-mix(in oklab, var(--accentB) 45%, transparent); right:8%; top:8%; animation-duration: 36s; }
      .b3 { width:620px; height:620px; background: color-mix(in oklab, var(--accentC) 45%, transparent); left:35%; bottom:-15%; animation-duration: 28s; }
      @keyframes drift { from { transform: translateY(-12px) translateX(-12px) } to { transform: translateY(22px) translateX(22px) } }

      /* Star sparkle layer */
      .stars { position: fixed; inset:0; z-index:-1; background: radial-gradient(2px 2px at 20% 30%, #ffffff33, transparent), radial-gradient(1px 1px at 70% 60%, #ffffff22, transparent), radial-gradient(1px 1px at 40% 80%, #ffffff22, transparent); animation: twinkle 6s ease-in-out infinite alternate; }
      @keyframes twinkle { from { opacity:.6 } to { opacity:1 } }

      /* Glass with animated border glow */
      .glass { position: relative; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); background: var(--glass); border:1px solid rgba(255,255,255,0.10); border-radius:18px; box-shadow: 0 10px 30px rgba(0,0,0,0.25); overflow:hidden; }
      .glass::before{ content:""; position:absolute; inset:-1px; border-radius:inherit; padding:1px; background: conic-gradient(from 0deg, var(--accentA), var(--accentB), var(--accentC), var(--accentD), var(--accentA)); -webkit-mask:linear-gradient(#000,#000) content-box, linear-gradient(#000,#000); -webkit-mask-composite: xor; mask-composite: exclude; animation: spin 18s linear infinite; opacity:.28; }
      @keyframes spin { to { transform: rotate(360deg) } }

      /* Header */
      .app-header { padding: 22px 22px; margin-top: 4px; }
      .app-title { font-family:'Space Grotesk', sans-serif; font-weight:800; font-size: 34px; margin:0; color: var(--fg); letter-spacing: .3px; background: linear-gradient(90deg, #fff, #c7d2fe, #a7f3d0, #fbcfe8); -webkit-background-clip:text; background-clip:text; color:transparent; animation: sheen 10s linear infinite; background-size:300% 100%; }
      @keyframes sheen { 0%{background-position:0% 50%} 100%{background-position:100% 50%} }
      .app-sub { color: var(--muted); margin: 6px 0 0 0; }

      /* Sticky toolbar */
      .toolbar { position: sticky; top: 0; z-index: 50; padding: 10px; margin: 12px 0 14px; }
      .toolbar-inner { display:flex; gap:10px; align-items:center; justify-content:space-between; }
      .toolbar-left, .toolbar-right { display:flex; gap:10px; align-items:center; flex-wrap:wrap; }

      /* Streamlit inputs subtle styling */
      .stSelectbox, .stDateInput, .stFileUploader, .stDownloadButton, .stTextInput { filter: drop-shadow(0 2px 10px rgba(0,0,0,.15)); }

      /* KPI chips with pulse glow */
      .kpi { display:flex; flex-direction:column; gap:4px; padding: 16px; transition: transform .2s ease, box-shadow .3s ease; }
      .kpi h3 { margin:0; font-size:12px; color:var(--muted); font-weight:800; letter-spacing:.3px; }
      .kpi p { margin:0; font-size:22px; font-weight:800; color:var(--fg); }
      .kpi:hover { transform: translateY(-2px); box-shadow: 0 12px 30px rgba(0,0,0,.25); }

      /* Exercise cards with tilt-on-hover */
      .card { padding: 16px 16px; margin-bottom: 12px; transform-style: preserve-3d; transition: transform .25s ease, box-shadow .25s ease; }
      .card:hover { transform: translateY(-4px) rotateX(1deg) rotateY(-1deg); box-shadow: 0 16px 40px rgba(0,0,0,.35); }
      .card h4 { margin:0; font-weight:800; color:#eaf2ff; letter-spacing:.2px; }
      .muted { color:var(--muted); }
      .tag { display:inline-block; padding:6px 10px; font-size:12px; border-radius:999px; margin-right:6px; background: linear-gradient(90deg, rgba(99,102,241,0.35), rgba(16,185,129,0.35)); color:#eaf2ff; border:1px solid rgba(255,255,255,0.10); animation: tagPulse 3.5s ease-in-out infinite; }
      @keyframes tagPulse { 0%,100%{filter: drop-shadow(0 0 0 rgba(99,102,241,.0))} 50%{filter: drop-shadow(0 0 8px rgba(99,102,241,.45))} }
      .hr { height:1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent); margin:10px 0 12px; }

      /* Set grid & pill states */
      .set-grid { display:grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap:10px; }
      .set-pill { display:flex; align-items:center; gap:10px; padding:10px 12px; border-radius:12px; border:1px solid rgba(255,255,255,0.12); background: linear-gradient(180deg, rgba(255,255,255,0.05), rgba(255,255,255,0.03)); transition: transform .15s ease, box-shadow .2s ease, background .2s ease; }
      .set-pill:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(0,0,0,.25); }
      /* Prefer CSS :has to glow when inner checkbox is checked (modern browsers) */
      .set-pill:has(input:checked) { background: linear-gradient(180deg, rgba(16,185,129,0.15), rgba(16,185,129,0.08)); box-shadow: 0 0 0 1px rgba(16,185,129,0.35) inset, 0 12px 30px rgba(16,185,129,0.25); }

      /* Buttons with ripple */
      .stButton>button { position: relative; overflow: hidden; border-radius:12px; font-weight:700; }
      .stButton>button:after { content:""; position:absolute; left:50%; top:50%; width:0; height:0; background: radial-gradient(circle, rgba(255,255,255,.35) 10%, transparent 60%); transform: translate(-50%,-50%); transition: width .35s ease, height .35s ease; }
      .stButton>button:active:after { width:220px; height:220px; }

      /* Progress bar: animated stripes */
      div[role="progressbar"] div { background-image: linear-gradient(90deg, rgba(99,102,241,.9), rgba(16,185,129,.9)); position: relative; }
      div[role="progressbar"] div::after{ content:""; position:absolute; inset:0; background-size: 28px 28px; background-image: repeating-linear-gradient(45deg, rgba(255,255,255,.25) 0 14px, transparent 14px 28px); mix-blend-mode: overlay; animation: slide 2s linear infinite; }
      @keyframes slide { to { background-position: 28px 0 } }

      /* Space tightening */
      .block-gap { margin-top: 8px; margin-bottom: 6px; }

      /* Reduced motion */
      @media (prefers-reduced-motion: reduce){
        .blob, .card:hover, .kpi:hover, .tag, .glass::before, .app-title, .stars, div[role="progressbar"] div::after { animation: none !important; }
      }
    </style>
    <div class="liquid-bg">
      <div class="blob b1"></div>
      <div class="blob b2"></div>
      <div class="blob b3"></div>
      <div class="stars"></div>
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
st.markdown('<div class="glass app-header"><h1 class="app-title">Workout Progress Tracker</h1><p class="app-sub">Liquid glass · Animated UI · No sidebar · Compact, colorful controls.</p></div>', unsafe_allow_html=True)

# Top sticky toolbar (no sidebar)
with st.container():
    st.markdown('<div class="glass toolbar"><div class="toolbar-inner">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([1.2, 1.5, 2, 2])
    with c1:
        selected_date = st.date_input("Training Date", value=date.today(), format="YYYY-MM-DD")
        date_str = selected_date.isoformat()
    with c2:
        day_short = ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
        default_idx = 0 if "__day_idx__" not in st.session_state else st.session_state["__day_idx__"]
        idx = st.selectbox("Day", options=list(range(5)), format_func=lambda i: day_short[i], index=default_idx, key="__select_day__")
        st.session_state["__day_idx__"] = idx
        day = DAY_OPTIONS[idx]
    with c3:
        ex_names = [ex["name"] for ex in WORKOUT_PLAN[day]]
        chosen = st.selectbox("Workout", ["All exercises"] + ex_names, key=f"__ex_select_{idx}")
    with c4:
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
# Tracker: compact grid cards (unchanged functionality)
# ==========================
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

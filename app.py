# Workout Progress Tracker — Streamlit
# Save as: app.py
# Run with: streamlit run app.py

import json
from datetime import date

import pandas as pd
import streamlit as st

# -----------------------
# Page Config & Theming
# -----------------------
st.set_page_config(
    page_title="Workout Progress Tracker",
    page_icon="🏋️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Custom CSS for a clean, modern UI ----------
st.markdown(
    """
    <style>
      .app-header {
        background: radial-gradient(1200px 400px at 15% -10%, rgba(99,102,241,0.25), transparent),
                    radial-gradient(1200px 400px at 85% -10%, rgba(16,185,129,0.25), transparent);
        padding: 24px 16px; border-radius: 18px; border: 1px solid rgba(255,255,255,0.06);
      }
      .app-title { font-size: 28px; font-weight: 800; margin: 0; }
      .app-sub { color: rgba(148,163,184,0.9); margin-top: 4px; }

      .card { border-radius: 16px; padding: 16px; margin-bottom: 12px;
              border: 1px solid rgba(148,163,184,0.25);
              background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); }
      .card h4 { margin: 0 0 6px 0; font-weight: 800; }
      .tag {
        display: inline-block; font-size: 12px; padding: 4px 8px; border-radius: 999px;
        border: 1px solid rgba(148,163,184,0.35); color: rgba(148,163,184,0.95);
        margin-right: 6px;
      }
      .small-dim { color: rgba(148,163,184,0.9); font-size: 12px; }
      .tight { margin-top: 4px; margin-bottom: 0; }
      .muted { color: rgba(148,163,184,0.9); }
      .hr { height: 1px; background: rgba(148,163,184,0.25); margin: 10px 0 14px; }
      .pill { display:inline-flex; align-items:center; gap:8px; padding:6px 10px; border-radius:999px;
              border:1px solid rgba(148,163,184,0.35); font-size:12px; }
      .kpi { border-radius: 14px; padding: 12px 14px; border: 1px solid rgba(148,163,184,0.25); }
      .kpi h3 { margin: 0; font-size: 14px; font-weight: 700; color: rgba(148,163,184,0.95); }
      .kpi p { margin: 4px 0 0 0; font-size: 22px; font-weight: 800; }
    </style>
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


# -----------------------
# Sidebar Controls
# -----------------------
with st.sidebar:
    st.markdown("### ⚙️ Session Controls")
    selected_date = st.date_input("Training Date", value=date.today())
    date_str = selected_date.isoformat()

    day = st.selectbox("Select Day", DAY_OPTIONS, index=0)

    ex_names = [ex["name"] for ex in WORKOUT_PLAN[day]]
    chosen = st.selectbox("Workout", ["All exercises"] + ex_names)

    st.markdown("---")
    st.markdown("#### 💾 Save / Load Progress")
    # Export current checkbox states
    export_data = {
        k: v for k, v in st.session_state.items() if isinstance(v, bool) and k.startswith("chk::")
    }
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
    if st.button("🔁 Reset selected exercise", use_container_width=True, type="secondary"):
        if chosen != "All exercises":
            idx = ex_names.index(chosen)
            sets = WORKOUT_PLAN[day][idx]["sets"]
            for s in range(sets):
                st.session_state[set_key(date_str, day, idx, s)] = False
            st.toast(f"Reset: {chosen}")
        else:
            st.info("Pick a single workout to reset.")

    if st.button("🧹 Reset this day", use_container_width=True):
        for i, ex in enumerate(WORKOUT_PLAN[day]):
            for s in range(ex["sets"]):
                st.session_state[set_key(date_str, day, i, s)] = False
        st.toast(f"Cleared all sets for {day} on {date_str}")


# -----------------------
# Header & KPIs
# -----------------------
st.markdown(
    f"""
    <div class="app-header">
      <div class="pill">📆 <span>{date_str}</span></div>
      <h1 class="app-title">Workout Progress Tracker</h1>
      <p class="app-sub">Select your day & workout, then check off sets as you go. Export or import progress anytime.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# KPIs row
k1, k2, k3, k4 = st.columns([1,1,1,1])
T, D, E = exercise_done_ratio(date_str, day)
with k1:
    st.markdown('<div class="kpi"><h3>Day</h3><p>'+day.split('–')[0].strip()+"</p></div>", unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi"><h3>Completed Sets</h3><p>{D} / {T}</p></div>', unsafe_allow_html=True)
with k3:
    pct = int((D / T * 100) if T else 0)
    st.markdown(f'<div class="kpi"><h3>Completion</h3><p>{pct}%</p></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi"><h3>Exercises Done</h3><p>{E} / {len(WORKOUT_PLAN[day])}</p></div>', unsafe_allow_html=True)

st.progress(pct / 100 if T else 0.0, text=f"{pct}% complete")

st.markdown(" ")

# -----------------------
# Tracker Tabs
# -----------------------
tracker_tab, progress_tab = st.tabs(["✅ Tracker", "📈 Progress (this session)"])

with tracker_tab:
    # Render one or many exercise cards
    render_all = chosen == "All exercises"
    exercises = WORKOUT_PLAN[day]

    for i, ex in enumerate(exercises):
        if (not render_all) and (ex["name"] != chosen):
            continue

        with st.container():
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            c1, c2 = st.columns([3, 1])
            with c1:
                st.markdown(f"<h4>{ex['name']}</h4>", unsafe_allow_html=True)
                st.markdown(
                    f"<p class='tight'><span class='tag'>Sets: {ex['sets']}</span> "
                    f"<span class='tag'>Target: {ex['reps']}</span></p>",
                    unsafe_allow_html=True,
                )
            with c2:
                all_done = all(
                    st.session_state.get(set_key(date_str, day, i, s), False)
                    for s in range(ex["sets"])
                )
                st.markdown(
                    f"<p class='small-dim' style='text-align:right'>{'✅ All sets done' if all_done else '⏳ In progress'}</p>",
                    unsafe_allow_html=True,
                )

            st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

            # Render set checkboxes in a responsive grid
            cols = st.columns(min(5, ex["sets"]))
            for s in range(ex["sets"]):
                with cols[s % len(cols)]:
                    st.checkbox(
                        f"Set {s+1}",
                        key=set_key(date_str, day, i, s),
                    )

            # Action buttons for this exercise
            b1, b2, _ = st.columns([1,1,4])
            with b1:
                if st.button("Mark all done", key=f"done_{i}"):
                    for s in range(ex["sets"]):
                        st.session_state[set_key(date_str, day, i, s)] = True
                    st.toast(f"Completed: {ex['name']}")
            with b2:
                if st.button("Reset", key=f"reset_{i}"):
                    for s in range(ex["sets"]):
                        st.session_state[set_key(date_str, day, i, s)] = False
                    st.toast(f"Reset: {ex['name']}")

            st.markdown("</div>", unsafe_allow_html=True)

with progress_tab:
    st.caption("This summary reflects only data from the current Streamlit session (unless you import saved JSON).")

    # Aggregate completion across all date/day keys present in session state
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
        st.bar_chart(
            df.set_index("date")["completion_%"],
            use_container_width=True,
        )

# ---------------
# End of script
# ---------------


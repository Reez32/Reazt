# app.py
import streamlit as st
import random

# --- Korean surnames ---
korean_surnames = ["Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Yoon", "Seo", "Han", "Lim"]

# --- K-pop reality shows list ---
kpop_shows = [
    "I-LAND",
    "Produce 101",
    "Produce 101 (S2)",
    "Sixteen",
    "Girls Planet 999",
    "Boys Planet",
    "Dream Academy",
    "RUNext",
    "Produce 48",
    "Produce X101"
]

# --- Mapping: show -> (debut group or note) ---
# Filled with well-known outcomes where available; for ambiguous/cancelled shows we put a note.
debut_groups = {
    "I-LAND": "ENHYPEN",
    "Produce 101": "I.O.I",
    "Produce 101 (S2)": "Wanna One",
    "Sixteen": "TWICE",
    "Girls Planet 999": "Kep1er",
    "Boys Planet": "ZEROBASEONE (ZB1)",
    "Dream Academy": "Katseye",
    "RUNext": "Illit",
    "Produce 48": "Iz*One",
    "Produce X101": "X1"
}

# --- Random events ---
events = [
    ("Mentor Praise 🌟", {"Popularity": 15}),
    ("Fan Vote Boost ❤️", {"Popularity": 20}),
    ("Minor Injury 🤕", {"Dancing": -15}),
    ("Rumor Scandal 😱", {"Popularity": -20}),
    ("Extra Vocal Lesson 🎤", {"Singing": 10}),
    ("Team Bonding Retreat 🤝", {"Teamwork": 10}),
]

# --- Initialize session state ---
if "page" not in st.session_state:
    st.session_state.page = "intro"
if "stats" not in st.session_state:
    st.session_state.stats = {"Singing": 50, "Dancing": 50, "Popularity": 50, "Teamwork": 50}
if "history" not in st.session_state:
    st.session_state.history = []
if "name" not in st.session_state:
    st.session_state.name = None
if "show" not in st.session_state:
    st.session_state.show = None
if "rivals" not in st.session_state:
    st.session_state.rivals = []
if "random_event_active" not in st.session_state:
    st.session_state.random_event_active = False


# --- Helper functions ---
def update_stats(updates, reason=""):
    for k, v in updates.items():
        if k in st.session_state.stats:
            st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k] + v))
    if reason:
        st.session_state.history.append(f"{reason} → {updates}")


def go_to(page):
    st.session_state.page = page


def generate_rivals():
    rivals = []
    first_names = ["Minho", "Jisoo", "Eunbi", "Hana", "Taeyong", "Somi", "Hyunwoo", "Yeri", "Seojin", "Mina"]
    for i in range(4):  # 4 rivals
        surname = random.choice(korean_surnames)
        name = f"{surname} {random.choice(first_names)}"
        stats = {
            "Singing": random.randint(40, 70),
            "Dancing": random.randint(40, 70),
            "Popularity": random.randint(40, 70),
            "Teamwork": random.randint(40, 70),
        }
        rivals.append({"name": name, "stats": stats})
    return rivals


def get_score(stats):
    return stats.get("Singing", 0) + stats.get("Dancing", 0) + stats.get("Popularity", 0) + stats.get("Teamwork", 0)


def show_rankings():
    player_score = get_score(st.session_state.stats)
    scores = [{"name": st.session_state.name, "score": player_score}]
    for r in st.session_state.rivals:
        scores.append({"name": r["name"], "score": get_score(r["stats"])})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    st.write("### Current Rankings:")
    for idx, s in enumerate(scores, start=1):
        st.write(f"{idx}. {s['name']} - {s['score']} pts")
    return scores


def random_event():
    # 50% chance to trigger once per episode when called
    if random.random() < 0.5:
        event, effect = random.choice(events)
        st.info(f"Random Event: **{event}**")
        update_stats(effect, f"Event: {event}")


def reset_game():
    st.session_state.page = "intro"
    st.session_state.stats = {"Singing": 50, "Dancing": 50, "Popularity": 50, "Teamwork": 50}
    st.session_state.history = []
    st.session_state.name = None
    st.session_state.show = None
    st.session_state.rivals = []
    st.session_state.random_event_active = False


# --- Pages ---
def intro():
    st.title("🎤 K-Pop Survival: The Debut Mission")
    st.write("Enter your first name and choose a survival show to start.")

    # Input fields
    name_input = st.text_input("Enter your first name:", key="name_input")
    show_choice = st.selectbox("Choose the reality show you’ll join:", kpop_shows, key="show_choice_select")

    if st.button("Start Game"):
        if not name_input or not name_input.strip():
            st.warning("Please enter your name to continue.")
            return
        # create stage name
        surname = random.choice(korean_surnames)
        st.session_state.name = f"{surname} {name_input.strip()}"
        st.session_state.show = show_choice
        st.session_state.rivals = generate_rivals()
        st.session_state.random_event_active = False
        go_to("audition")


def audition():
    st.header(f"Episode 1: Audition Stage ({st.session_state.show})")
    st.write(f"You are **{st.session_state.name}**, a contestant on **{st.session_state.show}**. It’s your first chance to impress the judges.")

    if st.button("🎶 Belt out high notes (risky)"):
        roll = random.randint(1, 20)
        if roll > 12:
            update_stats({"Singing": 15, "Popularity": 10}, "Strong vocals impressed everyone")
            st.success("You nailed the high notes! The judges are impressed.")
        else:
            update_stats({"Singing": -10, "Popularity": -5}, "Voice cracked under pressure")
            st.error("Your voice cracked! Ouch, tough start.")
        go_to("ranking1")

    if st.button("💃 Dance power performance"):
        roll = random.randint(1, 20)
        if roll > 10:
            update_stats({"Dancing": 15, "Popularity": 5}, "Dance moves wowed the audience")
            st.success("Your dance lit up the stage!")
        else:
            update_stats({"Dancing": -10}, "Missed a few steps")
            st.error("You stumbled a little. Not your best.")
        go_to("ranking1")

    if st.button("🤝 Safe teamwork approach"):
        update_stats({"Teamwork": 10, "Popularity": 3}, "Played safe with group focus")
        st.info("You didn’t stand out much, but you built trust with peers.")
        go_to("ranking1")


def ranking1():
    st.subheader("📊 Audition Rankings")
    scores = show_rankings()
    player_rank = next((i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name), None)
    # fallback safety
    if player_rank is None:
        player_rank = len(scores) + 1

    if player_rank > 4:
        st.error("💔 You ranked too low in the auditions and got eliminated early.")
        if st.button("Play Again"):
            reset_game()
    else:
        st.success("✅ You survived the auditions and move on to training camp!")
        if st.button("Next Episode"):
            go_to("training1")


def training1():
    st.header("Episode 2: Training Camp - Vocals")
    st.write("The mentors assign vocal training tasks.")

    if st.button("🎵 Solo practice"):
        update_stats({"Singing": 12}, "Focused on solo practice")
        random_event()
        go_to("ranking2")

    if st.button("🎶 Duet with rival"):
        update_stats({"Teamwork": 10, "Singing": 5}, "Improved singing with partner")
        random_event()
        go_to("ranking2")


def ranking2():
    st.subheader("📊 Training Camp Rankings")
    scores = show_rankings()
    player_rank = next((i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name), None)
    if player_rank is None:
        player_rank = len(scores) + 1

    if player_rank > 4:
        st.error("💔 You ranked too low and were eliminated.")
        if st.button("Play Again"):
            reset_game()
    else:
        if st.button("Next Episode"):
            go_to("training2")


def training2():
    st.header("Episode 3: Training Camp - Dance")
    st.write("Dance mentors test your choreography skills.")

    if st.button("💃 Take center position"):
        roll = random.randint(1, 20)
        if roll > 12:
            update_stats({"Dancing": 15, "Popularity": 5}, "Strong stage presence")
            st.success("You wowed the mentors!")
        else:
            update_stats({"Dancing": -5}, "Struggled in center role")
            st.error("You lost balance under pressure.")
        random_event()
        go_to("ranking3")

    if st.button("🩰 Support group choreography"):
        update_stats({"Teamwork": 10, "Dancing": 8}, "Helped group shine")
        random_event()
        go_to("ranking3")


def ranking3():
    st.subheader("📊 Training Camp 2 Rankings")
    scores = show_rankings()
    player_rank = next((i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name), None)
    if player_rank is None:
        player_rank = len(scores) + 1

    if player_rank > 4:
        st.error("💔 You ranked too low and were eliminated.")
        if st.button("Play Again"):
            reset_game()
    else:
        if st.button("Next Episode"):
            go_to("team_battle")


def team_battle():
    st.header("Episode 4: Team Battle")
    st.write("Trainees are split into teams to perform a rival group’s hit song.")

    if st.button("🧑‍✈️ Lead the team"):
        update_stats({"Teamwork": 15, "Popularity": 5}, "Led your team successfully")
        random_event()
        go_to("ranking4")

    if st.button("🎶 Focus on your part only"):
        update_stats({"Singing": 10}, "Safe choice but less spotlight")
        random_event()
        go_to("ranking4")


def ranking4():
    st.subheader("📊 Team Battle Rankings")
    scores = show_rankings()
    player_rank = next((i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name), None)
    if player_rank is None:
        player_rank = len(scores) + 1

    if player_rank > 4:
        st.error("💔 You ranked too low and were eliminated.")
        if st.button("Play Again"):
            reset_game()
    else:
        if st.button("Next Episode"):
            go_to("concept_eval")


def concept_eval():
    st.header("Episode 5: Concept Evaluation")
    st.write("You must choose between two concept stages.")

    if st.button("🔥 Charismatic Hip-Hop Concept"):
        update_stats({"Popularity": 15, "Dancing": 10}, "Bold concept choice")
        random_event()
        go_to("ranking5")

    if st.button("✨ Cute & Bright Concept"):
        update_stats({"Popularity": 12, "Teamwork": 8}, "Safe but loved by fans")
        random_event()
        go_to("ranking5")


def ranking5():
    st.subheader("📊 Concept Evaluation Rankings")
    scores = show_rankings()
    player_rank = next((i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name), None)
    if player_rank is None:
        player_rank = len(scores) + 1

    if player_rank > 4:
        st.error("💔 You ranked too low and were eliminated.")
        if st.button("Play Again"):
            reset_game()
    else:
        if st.button("Final Episode"):
            go_to("final_performance")


def final_performance():
    st.header("Episode 6: Final Live Performance 🌟")
    st.write("The last performance decides your debut fate.")
    st.json(st.session_state.stats)

    if st.button("See Final Rankings"):
        go_to("final_results")


def final_results():
    st.subheader("📊 Final Rankings")
    scores = show_rankings()
    player_rank = next((i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name), None)
    if player_rank is None:
        player_rank = len(scores) + 1

    # Show which group they debut in (if mapped)
    group_note = debut_groups.get(st.session_state.show, None)
    st.write("---")
    if group_note:
        st.write(f"If this season produced a debut group, the canonical outcome for **{st.session_state.show}** is **{group_note}**.")
    else:
        st.write(f"No known debut-group mapping for **{st.session_state.show}**. You could add one to `debut_groups`.")

    # Outcome by ranking
    if player_rank <= 2:
        st.success(f"🎉 Congratulations {st.session_state.name}! You made the debut lineup for this season!")
    elif player_rank <= 4:
        st.warning(f"✨ {st.session_state.name}, you performed strongly and almost debuted.")
    else:
        st.error(f"💔 {st.session_state.name}, you were eliminated before the debut lineup.")

    st.write("### Your Journey & Choices")
    st.write(st.session_state.history)

    if st.button("Play Again"):
        reset_game()


# --- Router ---
page = st.session_state.page
if page == "intro":
    intro()
elif page == "audition":
    audition()
elif page == "ranking1":
    ranking1()
elif page == "training1":
    training1()
elif page == "ranking2":
    ranking2()
elif page == "training2":
    training2()
elif page == "ranking3":
    ranking3()
elif page == "team_battle":
    team_battle()
elif page == "ranking4":
    ranking4()
elif page == "concept_eval":
    concept_eval()
elif page == "ranking5":
    ranking5()
elif page == "final_performance":
    final_performance()
elif page == "final_results":
    final_results()
else:
    # fallback
    intro()

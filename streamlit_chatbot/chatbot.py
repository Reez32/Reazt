import streamlit as st
import pandas as pd
import google.generativeai as genai

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def main():
    st.title("My First Chatbot")
    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
     if message["role"] == "assistant":
         with st.chat_message("assistant", avatar=robot_img):
            st.write(f"{message['content']}")
    else:
         with st.chat_message("user", avatar=user_emoji):
            st.write(f"{message['content']}")

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Add simple bot response
        response = f"You said: {prompt}"
        with st.chat_message("assistant"):
            st.write(response)
        
        st.session_state.messages.append({"role": "assistant", "content": response})


with st.sidebar:
    st.title("Sidebar") 
    ("hi gooners")
    st.radio("Radio-button select", ["Friendly", "Formal", "Funny"], index=0)
    st.multiselect("Multi-select", ["Movies", "Travel", "Food", "Sports"], default=["Food"])
    st.selectbox("Dropdown select", ["Data", "Code", "Travel", "Food", "Sports"], index=0)
    st.slider("Slider", min_value=1, max_value=200, value=60)
    st.select_slider("Option Slider", options=["Very Sad", "Sad", "Okay", "Happy", "Very Happy"], value="Okay")

import streamlit as st
import google.generativeai as genai

import streamlit as st
import google.generativeai as genai

# Configure Gemini API
GOOGLE_API_KEY = "AIzaSyBEGMzFNsVxD23D_Nd7SM5TwwEp1QwmzEQ"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []

def get_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

def main():
    st.title("Gemini AI Chatbot")
    
    initialize_session_state()

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Chat with Gemini"):
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)
        
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
    # Get Gemini response
        response = get_gemini_response(prompt,)
       ##Find the "get_gemini_response" function in your code and replace it with this function below

        # Display assistant response
        with st.chat_message("assistant"):
            st.write(response)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()

import streamlit as st
import random

# --- Korean surnames ---
korean_surnames = ["Kim", "Park", "Lee", "Choi", "Jung", "Kang", "Yoon", "Seo", "Han", "Lim"]

# --- K-pop reality shows list ---
kpop_shows = [
    "I-LAND", "Produce 101", "Sixteen", "Girls Planet 999",
    "The Unit", "Mix Nine", "Loud", "Queendom Puzzle", "RUNext", "Dream Academy"
]

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


# --- Helper functions ---
def update_stats(updates, reason=""):
    for k, v in updates.items():
        st.session_state.stats[k] += v
        st.session_state.stats[k] = max(0, min(100, st.session_state.stats[k]))
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
    return stats["Singing"] + stats["Dancing"] + stats["Popularity"] + stats["Teamwork"]


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
    if random.random() < 0.5:  # 50% chance of event
        event, effect = random.choice(events)
        st.info(f"Random Event: **{event}**")
        update_stats(effect, f"Event: {event}")


# --- Pages ---
def intro():
    st.title("🎤 K-Pop Survival: The Debut Mission")

    if st.session_state.name is None:
        name_input = st.text_input("Enter your first name:")
        show_choice = st.selectbox("Choose the reality show you’ll join:", kpop_shows)

        if st.button("Start Game"):
            if name_input.strip() != "":
                surname = random.choice(korean_surnames)
                st.session_state.name = f"{surname} {name_input}"
                st.session_state.show = show_choice
                st.session_state.rivals = generate_rivals()
                go_to("audition")
            else:
                st.warning("Please enter your name to continue.")
    else:
        if st.button("Continue"):
            go_to("audition")


def audition():
    st.header(f"Episode 1: Audition Stage ({st.session_state.show})")
    st.write(f"You are **{st.session_state.name}**, a contestant on **{st.session_state.show}**. "
             "It’s your first chance to impress the judges and viewers.")
    
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
    player_rank = [i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name][0]

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
    player_rank = [i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name][0]

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
    player_rank = [i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name][0]

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
    player_rank = [i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name][0]

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
    player_rank = [i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name][0]

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
    player_rank = [i for i, s in enumerate(scores, start=1) if s["name"] == st.session_state.name][0]

    if player_rank <= 2:
        go_to("debut")
    elif player_rank <= 4:
        go_to("almost")
    else:
        go_to("eliminated")


def debut():
    st.success(f"🎉 Congratulations {st.session_state.name}! You debuted in the final lineup of {st.session_state.show}!")
    st.write("History of your choices:")
    st.write(st.session_state.history)
    if st.button("Play Again"):
        reset_game()


def almost():
    st.warning(f"✨ {st.session_state.name}, you gave a strong performance and almost made it, "
               "but you were just short of debut. The audience loved you though!")
    st.write("History of your choices:")
    st.write(st.session_state.history)
    if st.button("Play Again"):
        reset_game()


def eliminated():
    st.error(f"💔 Sadly, {st.session_state.name}, you were eliminated in the final round of {st.session_state.show}. "
             "But every end is a new beginning.")
    st.write("History of your choices:")
    st.write(st.session_state.history)
    if st.button("Play Again"):
        reset_game()


def reset_game():
    st.session_state.page = "intro"
    st.session_state.stats = {"Singing": 50, "Dancing": 50, "Popularity": 50, "Teamwork": 50}
    st.session_state.history = []
    st.session_state.name = None
    st.session_state.show = None
    st.session_state.rivals = []


# --- Router ---
if st.session_state.page == "intro":
    intro()
elif st.session_state.page == "audition":
    audition()
elif st.session_state.page == "ranking1":
    ranking1()
elif st.session_state.page == "training1":
    training1()
elif st.session_state.page == "ranking2":
    ranking2()
elif st.session_state.page == "training2":
    training2()
elif st.session_state.page == "ranking3":
    ranking3()
elif st.session_state.page == "team_battle":
    team_battle()
elif st.session_state.page == "ranking4":
    ranking4()
elif st.session_state.page == "concept_eval":
    concept_eval()
elif st.session_state.page == "ranking5":
    ranking5()
elif st.session_state.page == "final_performance":
    final_performance()
elif st.session_state.page == "final_results":
    final_results()
elif st.session_state.page == "debut":
    debut()
elif st.session_state.page == "almost":
    almost()
elif st.session_state.page == "eliminated":
    eliminated()

# Genshin-inspired Text RPG (Streamlit single-file app)
# Save this file as genshin_streamlit_rpg.py and run: streamlit run genshin_streamlit_rpg.py
# Author: ChatGPT (example single-file text RPG inspired by Genshin Impact)

import streamlit as st
import random
import time
from dataclasses import dataclass, field
from typing import List, Dict

st.set_page_config(page_title="Tales of Aetheria - Text RPG", layout="wide")

# ----------------------------- Data classes -----------------------------
@dataclass
class Item:
    name: str
    description: str
    power: int = 0

@dataclass
class Enemy:
    name: str
    level: int
    hp: int
    atk: int
    element: str
    loot: List[Item] = field(default_factory=list)

@dataclass
class Quest:
    id: str
    title: str
    description: str
    level_req: int
    reward_xp: int
    reward_items: List[Item]
    completed: bool = False

@dataclass
class Player:
    name: str
    surname: str
    level: int = 1
    xp: int = 0
    hp: int = 100
    max_hp: int = 100
    atk: int = 10
    element: str = "Anemo"
    region: str = "Mondhaven"
    inventory: List[Item] = field(default_factory=list)
    gold: int = 0
    quests: Dict[str, Quest] = field(default_factory=dict)

    def add_xp(self, amount: int):
        self.xp += amount
        leveled = False
        while self.xp >= self.xp_to_next():
            self.xp -= self.xp_to_next()
            self.level += 1
            self.max_hp += 10
            self.atk += 2
            self.hp = self.max_hp
            leveled = True
        return leveled

    def xp_to_next(self):
        # simple exponential progression
        return 50 + (self.level - 1) * 25

    def add_item(self, item: Item):
        self.inventory.append(item)

    def has_item(self, name: str) -> bool:
        return any(i.name == name for i in self.inventory)

# ----------------------------- World data -----------------------------
REGIONS = [
    ("Mondhaven", "Verdant fields, wind-swept cliffs and travellers' taverns."),
    ("Liyuport", "Bustling harbors and ancient contracts written on scrolls."),
    ("Inazua", "Isles of cherry trees and disciplined sword schools."),
    ("Sumeron", "Golden deserts and hidden libraries of astronomers."),
]

ELEMENTS = ["Anemo", "Geo", "Pyro", "Hydro", "Electro", "Cryo", "Dendro"]

# Starter items
STARTER_WEAPONS = {
    "Anemo": Item("Windblade", "A light sword favored by wind practitioners.", power=3),
    "Geo": Item("Stonebrand", "A steady, slow-hitting blade from the earth.", power=4),
    "Pyro": Item("Flarerapier", "A sword warm to the touch.", power=4),
    "Hydro": Item("Tidecutter", "Flows around defenses.", power=3),
    "Electro": Item("Sparkedge", "Small static charges in the metal.", power=3),
    "Cryo": Item("Frostbite", "Chilly steel that glitters.", power=3),
    "Dendro": Item("Rootstaff", "A wooden weapon imbued with life.", power=2),
}

# Some items
ITEM_POOL = [
    Item("Healing Tonic", "Restores a good chunk of HP.", power=25),
    Item("Ironchunk", "Material for forging.", power=0),
    Item("Wisp Crystal", "Elemental shard used in upgrades.", power=0),
    Item("Emberseed", "A spark that warms a small fire.", power=0),
]

# Sample enemies by region
ENEMY_TEMPLATES = {
    "Mondhaven": [
        ("Hollow Wolf", 1, 40, 7, "Cryo"),
        ("Breeze Sprite", 2, 30, 5, "Anemo"),
        ("Bandit Scout", 3, 60, 9, "Pyro"),
    ],
    "Liyuport": [
        ("Harbor Rat", 1, 30, 6, "Hydro"),
        ("Contract Wisp", 4, 80, 12, "Electro"),
    ],
    "Inazua": [
        ("Training Dummy", 2, 50, 6, "Geo"),
        ("Blossom Fox", 5, 120, 15, "Dendro"),
    ],
    "Sumeron": [
        ("Sand Wraith", 3, 70, 10, "Geo"),
        ("Sun Seraph", 6, 150, 20, "Pyro"),
    ],
}

# Lore quests
QUEST_POOL = {
    "Mondhaven": [
        Quest(
            id="q_mond_1",
            title="Whispers on the Wind",
            description=("Children say a phantom sings atop the cliffs. Investigate and help or silence it."),
            level_req=1,
            reward_xp=40,
            reward_items=[Item("Wisp Crystal", "A faint shard of elemental energy.")],
        ),
        Quest(
            id="q_mond_2",
            title="Bandits at the Crossroad",
            description=("Traders were harassed at the east road. Drive off the bandits or negotiate."),
            level_req=2,
            reward_xp=80,
            reward_items=[Item("Ironchunk", "Rough forging material.")],
        ),
    ],
    "Liyuport": [
        Quest(
            id="q_liyu_1",
            title="Letters Lost at Sea",
            description=("A box of important letters fell overboard. Recover them from the shore or barter info from smugglers."),
            level_req=3,
            reward_xp=100,
            reward_items=[Item("Emberseed", "A small ember used in rituals.")],
        )
    ],
}

# ----------------------------- Helpers -----------------------------

def init_player():
    if "player" not in st.session_state:
        # Default starter creation
        st.session_state.player = Player(name="Traveller", surname=random.choice(["Kim", "Park", "Seo", "Lee", "Choi"]))
        st.session_state.player.inventory = [Item("Rations", "Food for the road.")] + [STARTER_WEAPONS[st.session_state.player.element]]


def random_enemy_for_region(region: str):
    template = random.choice(ENEMY_TEMPLATES.get(region, ENEMY_TEMPLATES["Mondhaven"]))
    name, lvl, hp, atk, element = template
    # scale by a small random factor
    hp = int(hp + lvl * 10 + random.randint(-5, 10))
    atk = int(atk + lvl // 2 + random.randint(-1, 3))
    loot = [random.choice(ITEM_POOL) for _ in range(random.randint(0, 2))]
    return Enemy(name=name, level=lvl, hp=hp, atk=atk, element=element, loot=loot)


def encounter_combat(player: Player, enemy: Enemy):
    log = []
    log.append(f"Encounter started: {enemy.name} (Lv {enemy.level}) — Element: {enemy.element}")
    # Simple turn-based combat
    while enemy.hp > 0 and player.hp > 0:
        # Player choice
        choice = st.session_state.get("combat_choice", "Attack")
        if choice == "Attack":
            damage = max(1, player.atk + random.randint(-3, 3))
            enemy.hp -= damage
            log.append(f"You attack and deal {damage} damage. Enemy HP: {max(0, enemy.hp)}")
        elif choice == "Skill":
            # simple elemental skill
            skill_power = player.atk + random.randint(0, 8)
            damage = skill_power + (player.level // 2)
            enemy.hp -= damage
            log.append(f"You use a skill and deal {damage} damage. Enemy HP: {max(0, enemy.hp)}")
            # drawback cost
            player.hp -= max(0, enemy.level // 2)
        elif choice == "Item":
            # try find a healing item
            tonic = next((i for i in player.inventory if i.name == "Healing Tonic"), None)
            if tonic:
                player.hp = min(player.max_hp, player.hp + tonic.power)
                player.inventory.remove(tonic)
                log.append(f"You used Healing Tonic and recovered {tonic.power} HP. Your HP: {player.hp}")
            else:
                log.append("You fumble — no healing items!")
        elif choice == "Flee":
            flee_chance = random.random()
            if flee_chance > 0.6:
                log.append("You successfully escaped the encounter.")
                return {"result":"fled","log":log}
            else:
                log.append("Escape failed.")

        # Enemy turn if still alive
        if enemy.hp > 0:
            edamage = max(1, enemy.atk + random.randint(-2, 3))
            player.hp -= edamage
            log.append(f"{enemy.name} attacks and deals {edamage} damage. Your HP: {max(0, player.hp)}")

    if player.hp <= 0:
        log.append("You collapsed. The world fades to black... You wake up later at the last safe inn.")
        # Penalty
        player.gold = max(0, player.gold - 10)
        player.hp = player.max_hp // 2
        return {"result":"dead","log":log}
    else:
        # victory
        xp_gain = enemy.level * 20 + random.randint(0, 15)
        lev = player.add_xp(xp_gain)
        # collect loot
        for it in enemy.loot:
            player.add_item(it)
        gold_gain = enemy.level * 5 + random.randint(0, 20)
        player.gold += gold_gain
        log.append(f"Victory! You gained {xp_gain} XP and {gold_gain} gold.")
        if enemy.loot:
            log.append("Loot: " + ", ".join(i.name for i in enemy.loot))
        if lev:
            log.append(f"You leveled up to Level {player.level}!")
        return {"result":"victory","log":log}

# ----------------------------- UI sections -----------------------------

init_player()
player: Player = st.session_state.player

# Header
st.title("Tales of Aetheria — Text RPG")
st.markdown("A long, lore-rich, text RPG inspired by a familiar fantasy world. Many choices, levels, quests and fun.")

# Left column: Player panel
col1, col2 = st.columns([1,2])
with col1:
    st.header("Traveler")
    st.write(f"**{player.name} {player.surname}** — Level {player.level}")
    st.write(f"Region: {player.region}")
    st.write(f"Element: {player.element}")
    st.write(f"HP: {player.hp}/{player.max_hp}")
    st.write(f"ATK: {player.atk}")
    st.write(f"XP: {player.xp}/{player.xp_to_next()}")
    st.write(f"Gold: {player.gold}")
    st.markdown("**Inventory**")
    if player.inventory:
        for i in player.inventory:
            st.write(f"- {i.name}: {i.description}")
    else:
        st.write("(empty)")
    if st.button("Rest at the Inn (restore HP, cost 10 gold) "):
        if player.gold >= 10:
            player.gold -= 10
            player.hp = player.max_hp
            st.success("You rested and feel refreshed.")
        else:
            st.error("Not enough gold.")

    # Quick save
    if st.button("Save Progress"):
        st.session_state.player = player
        st.success("Progress saved.")

with col2:
    st.header("World & Actions")

    # Character creation / update
    with st.expander("Character Creation & Customization", expanded=False):
        name = st.text_input("Name", value=player.name)
        surname = st.text_input("Surname", value=player.surname)
        region = st.selectbox("Choose your home region", [r[0] for r in REGIONS], index=[r[0] for r in REGIONS].index(player.region))
        element = st.selectbox("Choose your element", ELEMENTS, index=ELEMENTS.index(player.element))
        if st.button("Update Character"):
            player.name = name
            player.surname = surname
            player.region = region
            player.element = element
            # make sure starter weapon exists for element
            if not any(w.name == STARTER_WEAPONS[element].name for w in player.inventory):
                player.add_item(STARTER_WEAPONS[element])
            st.success("Saved character changes.")

    # Navigation
    st.subheader("Travel & Explore")
    dest = st.selectbox("Travel to:", [r[0] for r in REGIONS], index=[r[0] for r in REGIONS].index(player.region))
    if st.button("Travel"):
        # travel consequences
        travel_cost = random.randint(0, 20)
        player.region = dest
        if travel_cost > player.gold:
            st.warning("Travel was hardship but you made it. You lose stamina instead of gold.")
            player.hp = max(1, player.hp - travel_cost)
        else:
            player.gold = max(0, player.gold - travel_cost)
            st.success(f"You travel to {dest}. Travel cost {travel_cost} gold.")
    st.write("---")

    # Quests
    st.subheader("Available Quests")
    region_quests = QUEST_POOL.get(player.region, [])
    for q in region_quests:
        if not q.completed and player.level >= q.level_req:
            with st.expander(f"{q.title} (Lvl {q.level_req}) - {q.reward_xp} XP"):
                st.write(q.description)
                if st.button(f"Accept: {q.id}", key=f"accept_{q.id}"):
                    player.quests[q.id] = q
                    st.success("Quest accepted. Check your quest log to track progress.")

    # Active quests
    if player.quests:
        st.subheader("Quest Log")
        for qid, q in list(player.quests.items()):
            st.write(f"**{q.title}** — {'Completed' if q.completed else 'Active'}")
            st.write(q.description)
            if not q.completed:
                if st.button(f"Progress quest: {qid}", key=f"prog_{qid}"):
                    # simple progress: random chance success
                    chance = random.random()
                    if chance > 0.4:
                        q.completed = True
                        player.add_xp(q.reward_xp)
                        for it in q.reward_items:
                            player.add_item(it)
                        st.success(f"Quest completed. +{q.reward_xp} XP and rewards added.")
                    else:
                        st.info("You made little progress. Keep trying.")
            else:
                if st.button(f"Turn in: {qid}", key=f"turnin_{qid}"):
                    # turn in and remove
                    del player.quests[qid]
                    st.success("Quest turned in and removed from log.")

    st.write("---")

    # Exploration / encounter
    st.subheader("Explore the area")
    if st.button("Scout around"):
        outcome = random.random()
        if outcome < 0.5:
            enemy = random_enemy_for_region(player.region)
            st.session_state.current_enemy = enemy
            st.session_state.in_combat = True
            st.experimental_rerun()
        else:
            # random find
            found = random.choice(ITEM_POOL)
            player.add_item(found)
            gold_found = random.randint(0, 50)
            player.gold += gold_found
            st.success(f"You found {found.name} and {gold_found} gold while exploring.")

# Combat UI (centered modal style)
if st.session_state.get("in_combat", False):
    enemy: Enemy = st.session_state.current_enemy
    st.sidebar.header("Combat")
    st.sidebar.write(f"Enemy: {enemy.name} (Lv {enemy.level})")
    st.sidebar.write(f"HP: {enemy.hp}")
    st.sidebar.write(f"Element: {enemy.element}")

    st.sidebar.write("Choose action:")
    choice = st.sidebar.selectbox("Action", ["Attack", "Skill", "Item", "Flee"], index=0)
    st.session_state.combat_choice = choice
    if st.sidebar.button("Execute"):
        res = encounter_combat(player, enemy)
        # show log
        for line in res["log"]:
            st.write(line)
        if res["result"] in ("victory", "dead"):
            st.session_state.in_combat = False
            # remove enemy
            st.session_state.current_enemy = None
            # save player
            st.session_state.player = player
            st.success("Encounter resolved. Check your status panel for updates.")

# Side content: Lore and long-form story
st.write("---")
st.header("Tales & Lore")
with st.expander("Read the Chronicle of Aetheria", expanded=False):
    st.markdown(
        """
        Long ago, the Seven Threads wove the sky and stone, and Archons of different elements kept the balance.
        Merchants and scholars, pilgrims and pirates, they all made their marks on the continents.

        You are one traveler among many. Across plains, ports, and temples your choices echo. Will you seek knowledge,
        fight for the weak, chase fortune, or craft your own legend? Quests are not merely tasks. They are the steps
        of a story you shape.
        """
    )

# Mini games & training (levels)
st.write("---")
st.header("Training Grounds")
col3, col4 = st.columns(2)
with col3:
    st.subheader("Duel a sparring partner")
    spar_cost = 0
    if st.button("Spar (earn XP)"):
        # simple training
        xp = 10 + random.randint(0, 20)
        lvlup = player.add_xp(xp)
        st.success(f"You sparred and earned {xp} XP.")
        if lvlup:
            st.balloons()
            st.success(f"You reached level {player.level}!")
        st.session_state.player = player

with col4:
    st.subheader("Practice elemental skill")
    if st.button("Practice skill (chance to improve attack)"):
        if random.random() > 0.5:
            inc = random.randint(1, 3)
            player.atk += inc
            st.success(f"Your practice was successful. ATK +{inc}.")
        else:
            st.info("Today was not your day. Keep training.")
        st.session_state.player = player

# Crafting and shop
st.write("---")
st.header("Crafting & Shop")
with st.expander("Crafting Bench", expanded=False):
    st.write("Combine materials to make useful items. (Simple system)")
    mat1 = st.selectbox("Material 1", [i.name for i in player.inventory] + ["(none)"], index=0)
    mat2 = st.selectbox("Material 2", [i.name for i in player.inventory] + ["(none)"], index=0)
    if st.button("Attempt Crafting"):
        if mat1 == "(none)" or mat2 == "(none)":
            st.error("Choose two materials from inventory.")
        elif mat1 == mat2:
            st.error("You need two different items to craft.")
        else:
            # simple crafting outcomes
            if "Ironchunk" in (mat1, mat2):
                crafted = Item("Short Sword", "A basic forged weapon.", power=5)
                player.add_item(crafted)
                st.success("Crafted Short Sword. Added to inventory.")
            else:
                crafted = Item("Minor Tonic", "A modest healing brew.", power=15)
                player.add_item(crafted)
                st.success("Crafted Minor Tonic. Added to inventory.")
            # remove used items
            for name in (mat1, mat2):
                for it in player.inventory:
                    if it.name == name:
                        player.inventory.remove(it)
                        break
            st.session_state.player = player

with st.expander("Market", expanded=False):
    st.write("Buy common items from a traveling merchant.")
    market_items = [Item("Healing Tonic", "Restores HP.", power=25), Item("Lockpick", "Useful for chests.")]
    for mi in market_items:
        cola, colb = st.columns([3,1])
        with cola:
            st.write(f"**{mi.name}** — {mi.description}")
        with colb:
            price = 30 if mi.name == "Healing Tonic" else 15
            if st.button(f"Buy ({price}g)", key=f"buy_{mi.name}"):
                if player.gold >= price:
                    player.gold -= price
                    player.add_item(mi)
                    st.success(f"Bought {mi.name}.")
                    st.session_state.player = player
                else:
                    st.error("Not enough gold.")

st.write("---")
st.caption("Design note: this app is a single-file text RPG prototype. Want more characters, deeper story arcs, or a save/load export? Tell me what you want next.")

# Auto-save to session
st.session_state.player = player

# Footer with tips
st.write("---")
st.info("Tip: Explore different regions to unlock new quests. Use items smartly in combat. Many choices have small long-term effects.")

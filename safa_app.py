import streamlit as st
from google import genai

# ═══════════════════════════════════════════════════════════════
# 1. THE SAFA PRODUCT CATALOG & HARSH CHEMICAL DATABASE
# ═══════════════════════════════════════════════════════════════
safa_products = {
    "Hair Growth Oil": {
        "ingredients": "Rosemary, Castor oil, Peppermint, Coconut oil base",
        "benefits": "Stimulates follicles, thickens strands, reduces breakage",
        "best_for": ["hair growth", "thinning", "breakage", "dry scalp"],
        "usage": "Massage into scalp 3x/week, leave 2+ hours or overnight"
    },
    "Organic Shampoo": {
        "ingredients": "Aloe vera, Tea tree, Coconut-derived cleansers, Hibiscus",
        "benefits": "Cleanses without stripping, soothes itch, fights dandruff",
        "best_for": ["dandruff", "itchy scalp", "oily scalp", "all hair types"],
        "usage": "Wash 2-3x/week"
    },
    "Beard Growth Oil": {
        "ingredients": "Jojoba, Argan, Cedarwood, Vitamin E",
        "benefits": "Softens beard, kills itch, fills patchy zones",
        "best_for": ["beard growth", "patchy beard", "beard itch", "dry beard"],
        "usage": "Few drops daily, massage into skin under beard"
    },
    "Natural Detergent": {
        "ingredients": "Soap nuts, Baking soda, Essential oils, Plant-based surfactants",
        "benefits": "Hypoallergenic, tough on stains, safe for babies & sensitive skin",
        "best_for": ["sensitive skin", "baby clothes", "eczema", "chemical-free home"],
        "usage": "Use like regular detergent"
    }
}

harsh_chemicals = [
    ("sulfate", "Sulfates (SLS/SLES)", "Harsh foaming detergents that strip your scalp's natural oils, causing dryness and irritation."),
    ("paraben", "Parabens", "Preservatives linked to hormone disruption. Often hidden as methyl-/propylparaben."),
    ("parfum", "Synthetic Fragrance (Parfum)", "An undisclosed chemical cocktail and a top cause of skin allergies."),
    ("fragrance", "Synthetic Fragrance", "An undisclosed chemical cocktail and a top cause of skin allergies."),
    ("dimethicone", "Silicones (Dimethicone)", "Give fake smoothness but build up over time, suffocating hair and blocking moisture."),
    ("mineral oil", "Mineral Oil", "A petroleum by-product that coats hair and blocks moisture absorption."),
    ("formaldehyde", "Formaldehyde", "A preservative and known carcinogen."),
    ("triclosan", "Triclosan", "An antibacterial agent linked to hormone disruption."),
    ("phthalate", "Phthalates", "Plasticizers linked to hormone disruption, often hidden under 'fragrance'.")
]

# ═══════════════════════════════════════════════════════════════
# 2. SAFA COACH TOOL FUNCTIONS
# ═══════════════════════════════════════════════════════════════
def recommend_safa_product(concern: str) -> str:
    """Searches the Safa product catalog and returns the best-matching product(s) with benefits and usage for a customer's concern or goal (e.g., 'patchy beard', 'dandruff', 'baby clothes')."""
    concern = concern.lower()
    matches = []

    for name, info in safa_products.items():
        for keyword in info["best_for"]:
            if keyword in concern or any(w in concern for w in keyword.split() if len(w) > 4):
                matches.append(name)
                break

    if not matches:
        return "No exact match. Safa's core lineup: Hair Growth Oil, Organic Shampoo, Beard Growth Oil, Natural Detergent. Ask the customer to clarify their goal."

    results = []
    for name in dict.fromkeys(matches):
        info = safa_products[name]
        results.append(f"🌿 {name} | Ingredients: {info['ingredients']} | Benefits: {info['benefits']} | How to use: {info['usage']}")

    return "RECOMMENDED SAFA PRODUCTS:\n" + "\n".join(results)


def build_30day_plan(goal: str) -> str:
    """Returns a structured week-by-week 30-day routine plan using Safa products for goals like 'beard growth', 'hair growth', 'dandruff control', or 'chemical-free home'."""
    goal = goal.lower()

    plans = {
        "beard": "WEEK 1 (Days 1-7): Wash beard 2x with Safa Organic Shampoo. Apply Safa Beard Growth Oil every night. Mild itch is normal. | WEEK 2 (Days 8-14): Oil daily + 2-min massage to stimulate follicles. Itch fades. | WEEK 3 (Days 15-21): Comb daily to train direction. Keep nightly oil. | WEEK 4 (Days 22-30): Trim strays, maintain routine, take Day-30 photo to compare.",
        "hair": "WEEK 1: Scalp massage with Safa Hair Growth Oil 3x/week (leave 2+ hrs). Wash 2x/week with Safa Organic Shampoo. | WEEK 2: Same routine. Expect less breakage, calmer scalp. | WEEK 3: Add ONE overnight oil treatment. | WEEK 4: Check for baby hairs at hairline. Real growth shows week 4-8.",
        "dandruff": "WEEK 1: Wash with Safa Organic Shampoo 3x (tea tree fights flakes). Light oil on non-wash days. | WEEK 2: Flakes reduce. Wash 2-3x/week. | WEEK 3-4: Maintain 2x/week. Scalp rebalances after chemical shampoo 'purge'.",
        "home": "WEEK 1: Switch ALL laundry to Safa Natural Detergent. Wash baby/sensitive clothes first. | WEEK 2: Notice reduced skin irritation. Deep-clean bedding. | WEEK 3-4: Fully chemical-free home. Share your Safa story!"
    }

    for key, plan in plans.items():
        if key in goal:
            return f"30-DAY SAFA PLAN ({key.upper()}):\n{plan}"
    return "No matching plan. Available: beard growth, hair growth, dandruff control, chemical-free home. Ask the customer to pick one."


def check_ingredient_safety(ingredients_text: str) -> str:
    """Checks a pasted product ingredient list against Safa's harsh-chemical database. Returns flagged chemicals with plain-language explanations, or confirms the list is clean."""
    text = ingredients_text.lower()
    flagged = []
    seen = set()

    for key, name, explanation in harsh_chemicals:
        if key in text and name not in seen:
            seen.add(name)
            flagged.append(f"⚠️ {name}: {explanation}")

    if flagged:
        return "HARSH CHEMICALS FOUND:\n" + "\n".join(flagged) + "\n\nA Safa natural alternative exists for this product type - recommend it."
    return "✅ No harsh chemicals detected. This list looks clean!"


def troubleshoot_symptom(week: int, symptom: str) -> str:
    """Gives coaching advice for common symptoms customers report during their 30-day natural journey, based on the week number and symptom (e.g., week=2, symptom='itch')."""
    symptom = symptom.lower()

    if "itch" in symptom:
        return "Itch in weeks 1-2 is NORMAL - your skin is rebalancing after chemical products. Apply Safa oil at night, don't scratch. Fades by week 3."
    if "no growth" in symptom or "not growing" in symptom:
        return "Hair grows ~1.25cm/month - too slow to see daily. Take weekly photos in same lighting. Visible change at week 4-8. Stay consistent!"
    if "greasy" in symptom or "oily" in symptom:
        return "You're using too much oil. Reduce to 3-5 drops, massage fully in. Natural oils absorb best on slightly damp hair/beard."
    if "flake" in symptom or "purge" in symptom:
        return "This is the 'transition purge' - your scalp is detoxing from silicones/sulfates in old products. Lasts 1-2 weeks. Keep using Safa Organic Shampoo."
    return "Stay consistent with your Safa routine, hydrate, and sleep well. If it persists beyond week 3, consult a professional."


# ═══════════════════════════════════════════════════════════════
# 3. STREAMLIT APP & CHAT INTERFACE
# ═══════════════════════════════════════════════════════════════
st.set_page_config(page_title="Safa Glow-Up Coach", page_icon="🌿")
st.title("🌿 Safa Glow-Up Coach")
st.caption("Your friendly AI coach for organic beauty & home care routines")

api_key = None
try:
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    pass

if not api_key:
    st.error("⚠️ GEMINI_API_KEY not found in st.secrets! Please configure it in your Streamlit secrets.")
    st.stop()
else:
    # Initialize GenAI Client and Chat Session
    if "chat" not in st.session_state:
        client = genai.Client(api_key=api_key)
        model_config = {
            "tools": [recommend_safa_product, build_30day_plan, check_ingredient_safety, troubleshoot_symptom],
            "system_instruction": """You are the Safa Glow-Up Coach, the friendly and knowledgeable AI salesperson for Safa, an organic beauty & home care brand.

YOUR RULES:
1. ALWAYS use your tools to look up products, plans, or ingredient analysis BEFORE answering. Never guess.
2. Be warm, encouraging, and HONEST. Never overpromise (e.g., say visible growth takes 4-8 weeks).
3. When you flag harsh chemicals, ALWAYS follow up by recommending the matching Safa alternative.
4. Keep replies concise, friendly, and easy to read. Use a few emojis.
5. End conversations by making the customer feel supported on their natural journey."""
        }
        st.session_state.chat = client.chats.create(
            model="gemma-4-26b-a4b-it",
            config=model_config
        )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display prior chat messages
    for message in st.session_state.messages:
        avatar = "🌿" if message["role"] == "assistant" else None
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # User prompt input
    if prompt := st.chat_input("Ask about your hair, beard, or home routine..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar="🌿"):
            response = st.session_state.chat.send_message(prompt)
            st.markdown(response.text)

        st.session_state.messages.append({"role": "assistant", "content": response.text})

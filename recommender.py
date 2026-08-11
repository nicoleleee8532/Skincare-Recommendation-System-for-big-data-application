from __future__ import annotations

import argparse
import ast
import csv
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Sequence, Set, Tuple


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
PRODUCTS_PATH = DATA_DIR / "skincare_products_clean.csv"


SKIN_TYPE_KEYWORDS: Dict[str, Set[str]] = {
    "oily": {"oily", "greasy", "shiny", "oiliness", "excess oil"},
    "dry": {"dry", "flaky", "tight", "rough", "dry patches", "peeling"},
    "combination": {"combination", "oily t-zone", "oily t zone", "t-zone", "t zone"},
    "sensitive": {"sensitive", "reactive", "easily irritated", "burns", "stings", "stinging"},
    "normal": {"normal", "balanced"},
}


CONCERN_KEYWORDS: Dict[str, Set[str]] = {
    "acne": {"acne", "pimple", "pimples", "breakout", "breakouts", "zits", "spots"},
    "pores": {"pores", "large pores", "visible pores"},
    "blackheads": {"blackhead", "blackheads", "clogged pores", "black dots"},
    "oiliness": {"oily", "greasy", "shiny", "oiliness", "excess oil"},
    "dehydration": {"dehydrated", "dehydration", "tight", "tightness", "lacking water"},
    "dryness_flaking": {"flaky", "flaking", "peeling", "dry patches", "tight skin", "rough dry"},
    "redness": {"red", "redness", "flushed", "inflamed"},
    "barrier_repair": {"barrier", "damaged barrier", "skin barrier", "over exfoliated", "over-exfoliated"},
    "irritation": {"irritated", "irritation", "burning", "stinging", "itchy", "itching"},
    "dark_spots": {"dark spots", "dark marks", "post acne marks", "post-acne marks", "hyperpigmentation"},
    "melasma": {"melasma"},
    "dullness": {"dull", "dullness", "tired skin"},
    "texture": {"texture", "rough texture", "bumpy", "bumps", "uneven"},
    "aging": {"aging", "anti aging", "anti-aging", "mature skin"},
    "fine_lines": {"fine lines", "lines"},
    "wrinkles": {"wrinkles", "wrinkle"},
    "sun_protection": {"sun", "sunscreen", "spf", "sun protection"},
    "fungal_acne": {"fungal acne", "malassezia"},
    "rosacea_like": {"rosacea", "flushes", "flushing"},
    "eczema_like": {"eczema", "eczema-like", "very dry patches"},
}


PREFERRED_FLAG_KEYWORDS: Dict[str, Set[str]] = {
    "fragrance_free": {"fragrance free", "fragrance-free", "no fragrance"},
    "alcohol_free": {"alcohol free", "alcohol-free", "no alcohol"},
    "oil_free": {"oil free", "oil-free"},
    "non_comedogenic": {"non comedogenic", "non-comedogenic", "won't clog pores"},
    "ceramides": {"ceramide", "ceramides"},
    "centella": {"centella", "cica"},
    "mineral": {"mineral", "zinc oxide", "titanium dioxide"},
    "niacinamide": {"niacinamide"},
    "vitamin_c": {"vitamin c", "ascorbic"},
    "retinol": {"retinol", "retinoid"},
    "peptides": {"peptide", "peptides"},
    "hyaluronic_acid": {"hyaluronic acid"},
    "colloidal_oat": {"colloidal oat", "oat"},
    "fungal_safe": {"fungal safe", "fungal-acne safe", "malassezia safe"},
}


AVOID_FLAG_KEYWORDS: Dict[str, Set[str]] = {
    "fragrance": {"avoid fragrance", "avoiding fragrance", "avoid skincare with fragrance", "avoiding skincare with fragrance", "without fragrance", "fragrance irritates", "sensitive to fragrance", "no fragrance"},
    "alcohol": {"avoid alcohol", "avoiding alcohol", "avoid skincare with alcohol", "avoiding skincare with alcohol", "without alcohol", "alcohol irritates", "sensitive to alcohol", "no alcohol"},
    "acids": {"avoid acids", "avoiding acids", "without acids", "acids irritate", "aha irritates", "bha irritates"},
    "retinoids": {"avoid retinoids", "avoiding retinoids", "avoid retinol", "avoiding retinol", "without retinol", "retinol irritates", "pregnant", "pregnancy"},
    "essential_oils": {"essential oils irritate", "avoid essential oils"},
    "heavy_oils": {"avoid heavy oils", "heavy oils break me out"},
    "fatty_esters": {"fatty esters", "avoid esters"},
    "benzoyl_peroxide": {"benzoyl peroxide irritates", "avoid benzoyl peroxide"},
    "niacinamide_sensitive": {"niacinamide irritates", "sensitive to niacinamide"},
    "vitamin_c_sensitive": {"vitamin c irritates", "sensitive to vitamin c"},
}


def split_pipe(value: str) -> Set[str]:
    value = (value or "").strip().lower()
    unknown_values = {"none", "i don't know", "i dont know", "idk", "unknown", "not sure", "no preference"}
    if not value or value in unknown_values:
        return set()
    return {item.strip() for item in value.split("|") if item.strip()}


def parse_ingredients(value: str) -> List[str]:
    if not value:
        return []
    try:
        parsed = ast.literal_eval(value)
    except (SyntaxError, ValueError):
        return [item.strip().lower() for item in value.split(",") if item.strip()]
    if isinstance(parsed, list):
        return [str(item).strip().lower() for item in parsed if str(item).strip()]
    return []


def parse_price(value: str) -> float:
    digits = "".join(character for character in str(value) if character.isdigit() or character == ".")
    return float(digits) if digits else 0.0


def has_any(text: str, keywords: Set[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def infer_product_metadata(name: str, category: str, ingredients: List[str]) -> Tuple[Set[str], Set[str], Set[str], Set[str]]:
    text = f"{name} {category} {' '.join(ingredients)}".lower()
    ingredient_flags: Set[str] = set()
    concerns: Set[str] = set()
    avoid_for: Set[str] = set()
    skin_types: Set[str] = {"normal", "combination"}

    if has_any(text, {"sodium hyaluronate", "hyaluronic", "glycerin", "urea", "sodium pca"}):
        ingredient_flags.add("hyaluronic_acid")
        concerns.update({"dehydration", "dryness_flaking"})
        skin_types.update({"dry", "sensitive"})
    if has_any(text, {"ceramide", "cholesterol", "phytosphingosine"}):
        ingredient_flags.add("ceramides")
        concerns.update({"barrier_repair", "dehydration"})
        skin_types.update({"dry", "sensitive"})
    if has_any(text, {"niacinamide", "zinc"}):
        ingredient_flags.add("niacinamide")
        concerns.update({"acne", "pores", "oiliness", "dark_spots"})
        skin_types.update({"oily", "combination"})
    if has_any(text, {"salicylic", "bha"}):
        ingredient_flags.add("bha")
        concerns.update({"acne", "pores", "blackheads", "oiliness"})
        skin_types.update({"oily", "combination"})
        avoid_for.update({"very_sensitive_skin", "eczema_prone", "acids"})
    if has_any(text, {"glycolic", "lactic acid", "mandelic", "aha"}):
        ingredient_flags.add("aha")
        concerns.update({"texture", "dullness", "dark_spots"})
        avoid_for.update({"very_sensitive_skin", "eczema_prone", "acids"})
    if has_any(text, {"retinol", "retinal", "retinyl"}):
        ingredient_flags.add("retinol")
        concerns.update({"aging", "fine_lines", "wrinkles", "texture", "dark_spots"})
        avoid_for.update({"retinoids", "pregnancy", "highly_sensitive_skin"})
    if has_any(text, {"ascorbic", "vitamin c"}):
        ingredient_flags.add("vitamin_c")
        concerns.update({"dark_spots", "dullness", "aging"})
        avoid_for.add("vitamin_c_sensitive")
    if has_any(text, {"peptide", "palmitoyl"}):
        ingredient_flags.add("peptides")
        concerns.update({"aging", "fine_lines", "wrinkles"})
    if has_any(text, {"centella", "madecassoside", "allantoin", "panthenol", "oat"}):
        ingredient_flags.update({"centella", "alcohol_free"})
        concerns.update({"redness", "irritation", "barrier_repair"})
        skin_types.update({"sensitive", "dry"})
    if has_any(text, {"zinc oxide", "titanium dioxide", "homosalate", "octocrylene", "spf", "sunscreen"}):
        ingredient_flags.add("mineral")
        concerns.update({"sun_protection", "dark_spots", "melasma"})
    if has_any(text, {"oil-free", "oil free", "silica"}):
        ingredient_flags.add("oil_free")
        skin_types.update({"oily", "combination"})

    fragrance_terms = {"parfum", "fragrance", "limonene", "linalool", "citronellol", "geraniol", "coumarin"}
    if has_any(text, fragrance_terms):
        avoid_for.update({"fragrance", "essential_oils"})
    else:
        ingredient_flags.add("fragrance_free")

    alcohol_terms = {"alcohol denat", "sd alcohol", "ethanol"}
    if has_any(text, alcohol_terms):
        avoid_for.add("alcohol")
    else:
        ingredient_flags.add("alcohol_free")

    if "cleanser" in category.lower() or "cleanser" in name.lower():
        concerns.update({"barrier_repair", "irritation"})
    if "moistur" in category.lower() or "cream" in name.lower() or "lotion" in name.lower():
        concerns.add("dehydration")
        skin_types.update({"dry", "normal"})
    if "serum" in name.lower():
        concerns.add("dullness")
    if "sunscreen" in name.lower() or "spf" in name.lower():
        concerns.add("sun_protection")

    if not concerns:
        concerns.update({"dehydration", "barrier_repair"})
    if {"bha", "aha", "retinol"} & ingredient_flags:
        skin_types.discard("sensitive")

    return skin_types, concerns, ingredient_flags, avoid_for


def product_from_clean_row(row: dict, index: int) -> Product:
    ingredients = parse_ingredients(row.get("clean_ingreds", ""))
    category = row.get("product_type", "Product")
    skin_types, concerns, ingredient_flags, avoid_for = infer_product_metadata(
        row.get("product_name", ""),
        category,
        ingredients,
    )
    return Product(
        product_id=f"SK{index:05d}",
        product_name=row.get("product_name", f"Product {index}"),
        product_url=row.get("product_url", ""),
        category=category,
        target_skin_types=skin_types,
        target_concerns=concerns,
        ingredient_flags=ingredient_flags,
        avoid_for=avoid_for,
        price=parse_price(row.get("price", "")),
    )


def contains_keyword(text: str, keywords: Set[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def extract_matches(text: str, keyword_map: Dict[str, Set[str]]) -> Set[str]:
    return {label for label, keywords in keyword_map.items() if contains_keyword(text, keywords)}


def infer_sensitivity(text: str, concerns: Set[str], avoid_flags: Set[str]) -> str:
    high_markers = {
        "sensitive",
        "reactive",
        "burning",
        "stinging",
        "irritated",
        "irritation",
        "eczema",
        "rosacea",
        "allergic",
        "rash",
    }
    low_markers = {"not sensitive", "low sensitivity", "skin is not sensitive"}
    if contains_keyword(text, low_markers):
        return "low"
    if contains_keyword(text, high_markers) or {"redness", "irritation", "rosacea_like", "eczema_like"} & concerns or avoid_flags:
        return "high"
    return "medium"


def infer_skin_type(text: str, concerns: Set[str]) -> str:
    matches = extract_matches(text, SKIN_TYPE_KEYWORDS)
    if "combination" in matches:
        return "combination"
    if "oily" in matches:
        return "oily"
    if "dry" in matches:
        return "dry"
    if "sensitive" in matches:
        return "sensitive"
    if "oiliness" in concerns:
        return "oily"
    if {"dehydration", "dryness_flaking", "eczema_like"} & concerns:
        return "dry"
    return "normal"


def profile_from_text(text: str, user_id: str = "TEXT_INPUT") -> UserProfile:
    normalized = text.lower()
    concerns = extract_matches(normalized, CONCERN_KEYWORDS)
    preferred_flags = extract_matches(normalized, PREFERRED_FLAG_KEYWORDS)
    avoid_flags = extract_matches(normalized, AVOID_FLAG_KEYWORDS)
    skin_type = infer_skin_type(normalized, concerns)
    sensitivity = infer_sensitivity(normalized, concerns, avoid_flags)

    return UserProfile(
        user_id=user_id,
        age_group="custom",
        skin_type=skin_type,
        concerns=concerns,
        sensitivity=sensitivity,
        preferred_flags=preferred_flags,
        avoid_flags=avoid_flags,
        budget_level="not_used",
    )


@dataclass
class Product:
    product_id: str
    product_name: str
    product_url: str
    category: str
    target_skin_types: Set[str]
    target_concerns: Set[str]
    ingredient_flags: Set[str]
    avoid_for: Set[str]
    price: float


@dataclass
class UserProfile:
    user_id: str
    age_group: str
    skin_type: str
    concerns: Set[str]
    sensitivity: str
    preferred_flags: Set[str]
    avoid_flags: Set[str]
    budget_level: str


@dataclass
class Recommendation:
    product: Product
    final_score: float
    reasons: List[str]


def load_products(path: Path) -> List[Product]:
    products: List[Product] = []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = set(reader.fieldnames or [])
        for row in reader:
            if "clean_ingreds" in fieldnames:
                category = row.get("product_type", "").lower()
                if category in {"bath salts", "body wash", "bath oil"}:
                    continue
                products.append(product_from_clean_row(row, len(products) + 1))
            else:
                products.append(
                    Product(
                        product_id=row["product_id"],
                        product_name=row["product_name"],
                        product_url=row.get("product_url", ""),
                        category=row["category"],
                        target_skin_types=split_pipe(row["target_skin_types"]),
                        target_concerns=split_pipe(row["target_concerns"]),
                        ingredient_flags=split_pipe(row["ingredient_flags"]),
                        avoid_for=split_pipe(row["avoid_for"]),
                        price=parse_price(row.get("price", "")),
                    )
                )
    return products


def load_users(path: Path) -> Dict[str, UserProfile]:
    users: Dict[str, UserProfile] = {}
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            profile = UserProfile(
                user_id=row["user_id"],
                age_group=row["age_group"],
                skin_type=row["skin_type"],
                concerns=split_pipe(row["concerns"]),
                sensitivity=row["sensitivity"],
                preferred_flags=split_pipe(row["preferred_flags"]),
                avoid_flags=split_pipe(row["avoid_flags"]),
                budget_level=row["budget_level"],
            )
            users[profile.user_id] = profile
    return users


def score_product(user: UserProfile, product: Product) -> Tuple[float, List[str]]:
    score = 0.0
    reasons: List[str] = []

    if user.skin_type in product.target_skin_types:
        score += 4.0
        reasons.append(f"matches {user.skin_type} skin")

    concern_overlap = user.concerns & product.target_concerns
    if concern_overlap:
        score += 2.5 * len(concern_overlap)
        reasons.append("targets " + ", ".join(sorted(concern_overlap)))

    preferred_overlap = user.preferred_flags & product.ingredient_flags
    if preferred_overlap:
        score += 1.4 * len(preferred_overlap)
        reasons.append("includes " + ", ".join(sorted(preferred_overlap)))

    if user.sensitivity == "high":
        gentle_flags = {"fragrance_free", "alcohol_free", "mineral", "ceramides", "centella", "colloidal_oat"}
        gentle_overlap = gentle_flags & product.ingredient_flags
        if gentle_overlap:
            score += 1.5
            reasons.append("gentler option for sensitive skin")

    avoid_overlap = user.avoid_flags & (product.ingredient_flags | product.avoid_for)
    if avoid_overlap:
        score -= 4.0 * len(avoid_overlap)
        reasons.append("penalty for " + ", ".join(sorted(avoid_overlap)))

    return round(score, 3), reasons


def recommend_products(
    user: UserProfile,
    products: Sequence[Product],
    top_n: int,
) -> List[Recommendation]:
    ranked: List[Recommendation] = []
    for product in products:
        final_score, reasons = score_product(user, product)
        ranked.append(Recommendation(product=product, final_score=final_score, reasons=reasons))

    ranked.sort(key=lambda item: item.final_score, reverse=True)
    return ranked[:top_n]


def summarize_catalog(products: Sequence[Product], users: Dict[str, UserProfile]) -> str:
    categories = Counter(product.category for product in products)
    skin_types = Counter()
    product_concerns = Counter()
    user_concerns = Counter()

    for product in products:
        skin_types.update(product.target_skin_types)
        product_concerns.update(product.target_concerns)
    for user in users.values():
        user_concerns.update(user.concerns)

    lines = [
        "Catalog summary",
        f"- products: {len(products)}",
        f"- user profiles: {len(users)}",
        f"- categories: {dict(categories)}",
        f"- skin types covered: {dict(skin_types.most_common())}",
        f"- top product concerns: {dict(product_concerns.most_common(10))}",
        f"- top user concerns: {dict(user_concerns.most_common(10))}",
    ]
    return "\n".join(lines)


def normalize_choice(value: str, valid_values: Set[str], default: str) -> str:
    normalized = value.strip().lower()
    if not normalized:
        return default
    if normalized not in valid_values:
        choices = ", ".join(sorted(valid_values))
        print(f"Unknown value '{value}'. Using '{default}'. Valid choices: {choices}")
        return default
    return normalized


def prompt_pipe_set(prompt: str, examples: str, default: str = "none") -> Set[str]:
    print(f"{prompt}")
    print(f"Examples: {examples}")
    print("If you do not know, type: i dont know")
    value = input("> ").strip().lower()
    return split_pipe(value or default)


def build_interactive_profile() -> UserProfile:
    print("Interactive skincare recommendation")
    print("Describe your skin in a sentence, or press Enter to answer structured questions.")
    description = input("> ").strip()
    if description:
        user = profile_from_text(description, user_id="INTERACTIVE_TEXT")
        if not user.concerns:
            print("I could not detect a specific concern, so I will use structured questions.")
        else:
            return user

    print("Use | between multiple answers, for example: acne|pores|oiliness")
    print()

    skin_type = normalize_choice(
        input("Skin type (oily, dry, combination, normal, sensitive): "),
        {"oily", "dry", "combination", "normal", "sensitive"},
        "normal",
    )
    concerns = prompt_pipe_set(
        "What skin problems do you want to solve?",
        "acne|pores|blackheads|oiliness|dehydration|redness|barrier_repair|irritation|dark_spots|melasma|dullness|texture|aging|fine_lines|wrinkles|sun_protection|fungal_acne|rosacea_like|eczema_like",
    )
    sensitivity = normalize_choice(
        input("Sensitivity level (low, medium, high): "),
        {"low", "medium", "high"},
        "medium",
    )
    preferred_flags = prompt_pipe_set(
        "Preferred ingredients or product flags",
        "fragrance_free|alcohol_free|oil_free|non_comedogenic|ceramides|centella|mineral|niacinamide|vitamin_c|retinol|peptides|hyaluronic_acid|colloidal_oat|fungal_safe",
        "none",
    )
    avoid_flags = prompt_pipe_set(
        "Ingredients or flags to avoid",
        "fragrance|alcohol|acids|retinoids|essential_oils|heavy_oils|fatty_esters|benzoyl_peroxide|niacinamide_sensitive|vitamin_c_sensitive",
        "none",
    )

    return UserProfile(
        user_id="INTERACTIVE",
        age_group="custom",
        skin_type=skin_type,
        concerns=concerns,
        sensitivity=sensitivity,
        preferred_flags=preferred_flags,
        avoid_flags=avoid_flags,
        budget_level="not_used",
    )


def print_recommendations(user: UserProfile, recommendations: Sequence[Recommendation]) -> None:
    print(f"Recommendations for {user.user_id}")
    print(
        f"Profile: skin_type={user.skin_type}, concerns={sorted(user.concerns)}, "
        f"sensitivity={user.sensitivity}, preferred={sorted(user.preferred_flags)}, "
        f"avoid={sorted(user.avoid_flags)}"
    )
    print("-" * 72)

    for index, item in enumerate(recommendations, start=1):
        product = item.product
        reason_text = "; ".join(item.reasons[:4])
        print(
            f"{index}. {product.product_name} ({product.category}) | "
            f"score={item.final_score}"
        )
        print(f"   concerns={sorted(product.target_concerns)}")
        if product.product_url:
            print(f"   url={product.product_url}")
        print(f"   reasons={reason_text}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Offline skincare recommendation demo")
    parser.add_argument("--user", help="User ID, for example U001")
    parser.add_argument("--interactive", action="store_true", help="Ask for skin concerns and recommend live")
    parser.add_argument("--text", help="Natural-language skin description to recommend from")
    parser.add_argument("--top", type=int, default=5, help="Number of recommendations to return")
    parser.add_argument("--summary", action="store_true", help="Print a dataset summary before recommendations")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    products = load_products(PRODUCTS_PATH)
    users = load_users(DATA_DIR / "user_profiles.csv")

    if args.summary:
        print(summarize_catalog(products, users))
        print()

    if args.interactive:
        user = build_interactive_profile()
        recommendations = recommend_products(user, products, args.top)
        print()
        print_recommendations(user, recommendations)
        return

    if args.text:
        user = profile_from_text(args.text)
        recommendations = recommend_products(user, products, args.top)
        print_recommendations(user, recommendations)
        return

    if not args.user:
        raise SystemExit("Please provide --user U001 or use --interactive.")

    user = users.get(args.user)
    if not user:
        available_ids = ", ".join(sorted(users))
        raise SystemExit(f"Unknown user '{args.user}'. Available users: {available_ids}")

    recommendations = recommend_products(user, products, args.top)
    print_recommendations(user, recommendations)


if __name__ == "__main__":
    main()

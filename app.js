const productFallback = [
  {
    product_name: "CeraVe Facial Moisturising Lotion SPF 25 52ml",
    product_url: "https://www.lookfantastic.com/cerave-facial-moisturising-lotion-spf-25-52ml/11798689.html",
    product_type: "Moisturiser",
    clean_ingreds: "['glycerin','niacinamide','sodium hyaluronate','ceramide np','ceramide ap','cholesterol']"
  },
  {
    product_name: "The Ordinary Hyaluronic Acid 2% + B5 Hydration Support Formula 30ml",
    product_url: "https://www.lookfantastic.com/the-ordinary-hyaluronic-acid-2-b5-hydration-support-formula-30ml/11363395.html",
    product_type: "Serum",
    clean_ingreds: "['sodium hyaluronate','panthenol','glycerin']"
  },
  {
    product_name: "CeraVe Smoothing Cream 177ml",
    product_url: "https://www.lookfantastic.com/cerave-smoothing-cream-177ml/12207665.html",
    product_type: "Moisturiser",
    clean_ingreds: "['salicylic acid','glycerin','ceramide np','niacinamide','urea']"
  },
  {
    product_name: "Clinique Redness Solutions Daily Relief Cream 50ml",
    product_url: "https://www.lookfantastic.com/clinique-redness-solutions-daily-relief-cream-50ml/11144771.html",
    product_type: "Moisturiser",
    clean_ingreds: "['glycerin','caffeine','sodium hyaluronate','titanium dioxide','cholesterol']"
  },
  {
    product_name: "The Ordinary Marine Hyaluronics 30ml",
    product_url: "https://www.lookfantastic.com/the-ordinary-marine-hyaluronics-30ml/11751840.html",
    product_type: "Serum",
    clean_ingreds: "['glycerin','amino acids','sodium hyaluronate']"
  },
  {
    product_name: "The Ordinary Retinol 0.2% in Squalane 30ml",
    product_url: "https://www.lookfantastic.com/",
    product_type: "Serum",
    clean_ingreds: "['squalane','retinol','tocopherol']"
  },
  {
    product_name: "La Roche-Posay Anthelios Ultra-Light SPF50",
    product_url: "https://www.lookfantastic.com/",
    product_type: "Sunscreen",
    clean_ingreds: "['glycerin','silica','titanium dioxide','zinc oxide']"
  },
  {
    product_name: "Paula's Choice Skin Perfecting 2% BHA Liquid Exfoliant",
    product_url: "https://www.lookfantastic.com/",
    product_type: "Exfoliator",
    clean_ingreds: "['salicylic acid','green tea','methylpropanediol']"
  }
];

const concernKeywords = {
  acne: ["acne", "pimple", "pimples", "breakout", "breakouts", "zits", "spots"],
  pores: ["pores", "large pores", "visible pores"],
  blackheads: ["blackhead", "blackheads", "clogged pores", "black dots"],
  oiliness: ["oily", "greasy", "shiny", "oiliness", "excess oil"],
  dehydration: ["dehydrated", "dehydration", "tight", "tightness", "lacking water"],
  dryness_flaking: ["flaky", "flaking", "peeling", "dry patches", "tight skin", "rough dry"],
  redness: ["red", "redness", "flushed", "inflamed"],
  barrier_repair: ["barrier", "damaged barrier", "skin barrier", "over exfoliated", "over-exfoliated"],
  irritation: ["irritated", "irritation", "burning", "stinging", "itchy", "itching"],
  dark_spots: ["dark spots", "dark marks", "post acne marks", "post-acne marks", "hyperpigmentation"],
  melasma: ["melasma"],
  dullness: ["dull", "dullness", "tired skin"],
  texture: ["texture", "rough texture", "bumpy", "bumps", "uneven"],
  aging: ["aging", "anti aging", "anti-aging", "mature skin"],
  fine_lines: ["fine lines", "lines"],
  wrinkles: ["wrinkles", "wrinkle"],
  sun_protection: ["sun", "sunscreen", "spf", "sun protection"],
  fungal_acne: ["fungal acne", "malassezia"],
  rosacea_like: ["rosacea", "flushes", "flushing"],
  eczema_like: ["eczema", "eczema-like", "very dry patches"]
};

const skinTypeKeywords = {
  oily: ["oily", "greasy", "shiny", "oiliness", "excess oil"],
  dry: ["dry", "flaky", "tight", "rough", "dry patches", "peeling"],
  combination: ["combination", "oily t-zone", "oily t zone", "t-zone", "t zone"],
  sensitive: ["sensitive", "reactive", "easily irritated", "burns", "stings", "stinging"],
  normal: ["normal", "balanced"]
};

const preferredKeywords = {
  fragrance_free: ["fragrance free", "fragrance-free", "no fragrance"],
  alcohol_free: ["alcohol free", "alcohol-free", "no alcohol"],
  oil_free: ["oil free", "oil-free"],
  non_comedogenic: ["non comedogenic", "non-comedogenic", "won't clog pores"],
  ceramides: ["ceramide", "ceramides"],
  centella: ["centella", "cica"],
  mineral: ["mineral", "zinc oxide", "titanium dioxide"],
  niacinamide: ["niacinamide"],
  vitamin_c: ["vitamin c", "ascorbic"],
  retinol: ["retinol", "retinoid"],
  peptides: ["peptide", "peptides"],
  hyaluronic_acid: ["hyaluronic acid"],
  colloidal_oat: ["colloidal oat", "oat"],
  fungal_safe: ["fungal safe", "fungal-acne safe", "malassezia safe"]
};

const avoidKeywords = {
  fragrance: ["avoid fragrance", "avoiding fragrance", "avoid skincare with fragrance", "avoiding skincare with fragrance", "without fragrance", "fragrance irritates", "sensitive to fragrance", "no fragrance"],
  alcohol: ["avoid alcohol", "avoiding alcohol", "avoid skincare with alcohol", "avoiding skincare with alcohol", "without alcohol", "alcohol irritates", "sensitive to alcohol", "no alcohol"],
  acids: ["avoid acids", "avoiding acids", "without acids", "acids irritate", "aha irritates", "bha irritates"],
  retinoids: ["avoid retinoids", "avoiding retinoids", "avoid retinol", "avoiding retinol", "without retinol", "retinol irritates", "pregnant", "pregnancy"],
  essential_oils: ["essential oils irritate", "avoid essential oils"],
  heavy_oils: ["avoid heavy oils", "heavy oils break me out"],
  fatty_esters: ["fatty esters", "avoid esters"],
  benzoyl_peroxide: ["benzoyl peroxide irritates", "avoid benzoyl peroxide"],
  niacinamide_sensitive: ["niacinamide irritates", "sensitive to niacinamide"],
  vitamin_c_sensitive: ["vitamin c irritates", "sensitive to vitamin c"]
};

let products = [];

const elements = {
  form: document.querySelector("#recommenderForm"),
  text: document.querySelector("#skinText"),
  status: document.querySelector("#catalogStatus"),
  skinType: document.querySelector("#skinTypeOutput"),
  sensitivity: document.querySelector("#sensitivityOutput"),
  concerns: document.querySelector("#concernOutput"),
  avoid: document.querySelector("#avoidOutput"),
  results: document.querySelector("#resultsGrid"),
  fillExample: document.querySelector("#fillExample")
};

function includesAny(text, words) {
  return words.some((word) => text.includes(word));
}

function extractMatches(text, dictionary) {
  return Object.entries(dictionary)
    .filter(([, words]) => includesAny(text, words))
    .map(([label]) => label);
}

function inferSkinType(text, concerns) {
  const matches = extractMatches(text, skinTypeKeywords);
  if (matches.includes("combination")) return "combination";
  if (matches.includes("oily")) return "oily";
  if (matches.includes("dry")) return "dry";
  if (matches.includes("sensitive")) return "sensitive";
  if (concerns.includes("oiliness")) return "oily";
  if (concerns.some((item) => ["dehydration", "dryness_flaking", "eczema_like"].includes(item))) return "dry";
  return "normal";
}

function inferSensitivity(text, concerns, avoid) {
  const highWords = ["sensitive", "reactive", "burning", "stinging", "irritated", "eczema", "rosacea", "allergic", "rash"];
  if (text.includes("not sensitive") || text.includes("low sensitivity")) return "low";
  if (includesAny(text, highWords) || avoid.length > 0 || concerns.some((item) => ["redness", "irritation", "rosacea_like", "eczema_like"].includes(item))) return "high";
  return "medium";
}

function profileFromText(rawText) {
  const text = rawText.toLowerCase();
  const concerns = extractMatches(text, concernKeywords);
  const preferred = extractMatches(text, preferredKeywords);
  const avoid = extractMatches(text, avoidKeywords);
  return {
    skinType: inferSkinType(text, concerns),
    sensitivity: inferSensitivity(text, concerns, avoid),
    concerns,
    preferred,
    avoid
  };
}

function parseCsv(csvText) {
  const rows = [];
  let field = "";
  let row = [];
  let quoted = false;

  for (let index = 0; index < csvText.length; index += 1) {
    const character = csvText[index];
    const next = csvText[index + 1];

    if (character === "\"" && quoted && next === "\"") {
      field += "\"";
      index += 1;
    } else if (character === "\"") {
      quoted = !quoted;
    } else if (character === "," && !quoted) {
      row.push(field);
      field = "";
    } else if ((character === "\n" || character === "\r") && !quoted) {
      if (field || row.length) {
        row.push(field);
        rows.push(row);
        field = "";
        row = [];
      }
      if (character === "\r" && next === "\n") index += 1;
    } else {
      field += character;
    }
  }

  if (field || row.length) {
    row.push(field);
    rows.push(row);
  }

  const headers = rows.shift();
  return rows.map((values) => Object.fromEntries(headers.map((header, index) => [header, values[index] || ""])));
}

function parseIngredients(value) {
  return value
    .replace(/[\[\]']/g, "")
    .split(",")
    .map((item) => item.trim().toLowerCase())
    .filter(Boolean);
}

function inferProduct(product, index) {
  const ingredients = parseIngredients(product.clean_ingreds || "");
  const text = `${product.product_name || ""} ${product.product_type || ""} ${ingredients.join(" ")}`.toLowerCase();
  const flags = new Set();
  const concerns = new Set();
  const avoid = new Set();
  const skinTypes = new Set(["normal", "combination"]);

  const add = (set, values) => values.forEach((value) => set.add(value));

  if (includesAny(text, ["sodium hyaluronate", "hyaluronic", "glycerin", "urea", "sodium pca"])) {
    flags.add("hyaluronic_acid");
    add(concerns, ["dehydration", "dryness_flaking"]);
    add(skinTypes, ["dry", "sensitive"]);
  }
  if (includesAny(text, ["ceramide", "cholesterol", "phytosphingosine"])) {
    flags.add("ceramides");
    add(concerns, ["barrier_repair", "dehydration"]);
    add(skinTypes, ["dry", "sensitive"]);
  }
  if (includesAny(text, ["niacinamide", "zinc"])) {
    flags.add("niacinamide");
    add(concerns, ["acne", "pores", "oiliness", "dark_spots"]);
    add(skinTypes, ["oily", "combination"]);
  }
  if (includesAny(text, ["salicylic", "bha"])) {
    flags.add("bha");
    add(concerns, ["acne", "pores", "blackheads", "oiliness"]);
    add(skinTypes, ["oily", "combination"]);
    add(avoid, ["very_sensitive_skin", "eczema_prone", "acids"]);
  }
  if (includesAny(text, ["glycolic", "lactic acid", "mandelic", "aha"])) {
    flags.add("aha");
    add(concerns, ["texture", "dullness", "dark_spots"]);
    add(avoid, ["very_sensitive_skin", "eczema_prone", "acids"]);
  }
  if (includesAny(text, ["retinol", "retinal", "retinyl"])) {
    flags.add("retinol");
    add(concerns, ["aging", "fine_lines", "wrinkles", "texture", "dark_spots"]);
    add(avoid, ["retinoids", "pregnancy", "highly_sensitive_skin"]);
  }
  if (includesAny(text, ["ascorbic", "vitamin c"])) {
    flags.add("vitamin_c");
    add(concerns, ["dark_spots", "dullness", "aging"]);
    avoid.add("vitamin_c_sensitive");
  }
  if (includesAny(text, ["peptide", "palmitoyl"])) {
    flags.add("peptides");
    add(concerns, ["aging", "fine_lines", "wrinkles"]);
  }
  if (includesAny(text, ["centella", "madecassoside", "allantoin", "panthenol", "oat"])) {
    add(flags, ["centella", "alcohol_free"]);
    add(concerns, ["redness", "irritation", "barrier_repair"]);
    add(skinTypes, ["sensitive", "dry"]);
  }
  if (includesAny(text, ["zinc oxide", "titanium dioxide", "homosalate", "octocrylene", "spf", "sunscreen"])) {
    flags.add("mineral");
    add(concerns, ["sun_protection", "dark_spots", "melasma"]);
  }
  if (includesAny(text, ["oil-free", "oil free", "silica"])) {
    flags.add("oil_free");
    add(skinTypes, ["oily", "combination"]);
  }

  if (includesAny(text, ["parfum", "fragrance", "limonene", "linalool", "citronellol", "geraniol", "coumarin"])) {
    add(avoid, ["fragrance", "essential_oils"]);
  } else {
    flags.add("fragrance_free");
  }

  if (includesAny(text, ["alcohol denat", "sd alcohol", "ethanol"])) {
    avoid.add("alcohol");
  } else {
    flags.add("alcohol_free");
  }

  if (text.includes("cleanser")) add(concerns, ["barrier_repair", "irritation"]);
  if (text.includes("moistur") || text.includes("cream") || text.includes("lotion")) {
    concerns.add("dehydration");
    add(skinTypes, ["dry", "normal"]);
  }
  if (text.includes("serum")) concerns.add("dullness");
  if (text.includes("sunscreen") || text.includes("spf")) concerns.add("sun_protection");
  if (concerns.size === 0) add(concerns, ["dehydration", "barrier_repair"]);
  if (flags.has("bha") || flags.has("aha") || flags.has("retinol")) skinTypes.delete("sensitive");

  return {
    id: `SK${String(index + 1).padStart(5, "0")}`,
    name: product.product_name || `Product ${index + 1}`,
    url: product.product_url || "",
    type: product.product_type || "Product",
    flags: [...flags],
    concerns: [...concerns],
    avoid: [...avoid],
    skinTypes: [...skinTypes]
  };
}

function scoreProduct(profile, product) {
  let score = 0;
  const reasons = [];
  const concernOverlap = profile.concerns.filter((item) => product.concerns.includes(item));
  const preferredOverlap = profile.preferred.filter((item) => product.flags.includes(item));
  const avoidOverlap = profile.avoid.filter((item) => product.flags.includes(item) || product.avoid.includes(item));

  if (product.skinTypes.includes(profile.skinType)) {
    score += 4;
    reasons.push(`Matches ${profile.skinType} skin`);
  }
  if (concernOverlap.length) {
    score += concernOverlap.length * 2.5;
    reasons.push(`Targets ${concernOverlap.map(formatLabel).join(", ")}`);
  }
  if (preferredOverlap.length) {
    score += preferredOverlap.length * 1.4;
    reasons.push(`Includes ${preferredOverlap.map(formatLabel).join(", ")}`);
  }
  if (profile.sensitivity === "high" && product.flags.some((item) => ["fragrance_free", "alcohol_free", "mineral", "ceramides", "centella", "colloidal_oat"].includes(item))) {
    score += 1.5;
    reasons.push("Gentler option for sensitive skin");
  }
  if (avoidOverlap.length) {
    score -= avoidOverlap.length * 4;
    reasons.push(`Penalty for ${avoidOverlap.map(formatLabel).join(", ")}`);
  }

  return { ...product, score: Number(score.toFixed(2)), reasons };
}

function maxPossibleScore(profile) {
  let maxScore = 4;
  maxScore += profile.concerns.length * 2.5;
  maxScore += profile.preferred.length * 1.4;
  if (profile.sensitivity === "high") {
    maxScore += 1.5;
  }
  return Math.max(maxScore, 1);
}

function normalizeMatchPercent(score, profile) {
  const percent = Math.round((Math.max(score, 0) / maxPossibleScore(profile)) * 100);
  return Math.min(Math.max(percent, 0), 100);
}

function formatLabel(label) {
  return label.replaceAll("_", " ");
}

function renderChips(target, values) {
  target.innerHTML = "";
  if (!values.length) {
    target.innerHTML = '<span class="chip muted">None detected</span>';
    return;
  }
  values.forEach((value) => {
    const chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = formatLabel(value);
    target.appendChild(chip);
  });
}

function renderProfile(profile) {
  elements.skinType.textContent = profile.skinType;
  elements.sensitivity.textContent = profile.sensitivity;
  renderChips(elements.concerns, profile.concerns);
  renderChips(elements.avoid, profile.avoid);
}

function recommend(profile) {
  return products
    .map((product) => scoreProduct(profile, product))
    .filter((product) => product.score > 0)
    .map((product) => ({ ...product, matchPercent: normalizeMatchPercent(product.score, profile) }))
    .sort((left, right) => right.score - left.score)
    .slice(0, 6);
}

function renderResults(recommendations) {
  elements.results.innerHTML = "";
  if (!recommendations.length) {
    elements.results.innerHTML = `
      <article class="empty-state">
        <h3>No confident matches</h3>
        <p>Try adding more details, such as skin type, breakouts, redness, dryness, or ingredients you avoid.</p>
      </article>
    `;
    return;
  }

  recommendations.forEach((product, index) => {
    const card = document.createElement("article");
    card.className = "result-card";
    card.style.animationDelay = `${index * 70}ms`;
    card.innerHTML = `
      <span class="rank">${index + 1}</span>
      <h3>${product.name}</h3>
      <p class="product-type">${product.type}</p>
      <p class="score">Match: ${product.matchPercent}%</p>
      <ul class="reason-list">
        ${product.reasons.slice(0, 4).map((reason) => `<li>${reason}</li>`).join("")}
      </ul>
      ${product.url ? `<a class="product-link" href="${product.url}" target="_blank" rel="noreferrer">View product</a>` : ""}
    `;
    elements.results.appendChild(card);
  });
}

async function loadProducts() {
  try {
    const response = await fetch("../data/skincare_products_clean.csv");
    if (!response.ok) throw new Error("CSV not available");
    const rows = parseCsv(await response.text());
    products = rows
      .filter((row) => !["Bath Salts", "Body Wash", "Bath Oil"].includes(row.product_type))
      .map(inferProduct);
    elements.status.textContent = `Loaded ${products.length} products from skincare_products_clean.csv`;
  } catch (error) {
    products = productFallback.map(inferProduct);
    elements.status.textContent = `Using built-in demo catalog (${products.length} products). Serve from a local server to load the full CSV.`;
  }
}

elements.form.addEventListener("submit", (event) => {
  event.preventDefault();
  const text = elements.text.value.trim();
  if (!text) {
    elements.text.focus();
    return;
  }
  const profile = profileFromText(text);
  renderProfile(profile);
  renderResults(recommend(profile));
});

elements.fillExample.addEventListener("click", () => {
  elements.text.value = "My skin is oily and I get pimples, blackheads, and large pores. Fragrance irritates my face.";
  document.querySelector("#recommender").scrollIntoView({ behavior: "smooth", block: "start" });
  elements.form.requestSubmit();
});

loadProducts();

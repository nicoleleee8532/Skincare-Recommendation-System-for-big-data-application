# Skincare Recommendation System for Big Data Applications

This project is an offline skincare recommendation system that recommends real products from a cleaned skincare product CSV. It uses natural-language input, ingredient-based feature extraction, and content-based matching to recommend products for different skin types and skin problems.

The demo runs without internet access. It still applies big data concepts because the same design can scale from local CSV files to distributed storage, Spark processing, and much larger product catalogs.

## Problem Statement

Choosing skincare products is difficult because people have different face types, skin problems, sensitivities, and ingredient restrictions. A product that works for oily acne-prone skin may be unsuitable for dry, sensitive, or barrier-damaged skin.

The system recommends skincare products by combining:

1. natural-language understanding of user skin descriptions
2. ingredient-based feature extraction from product metadata
3. content-based matching between user needs and product properties

## Big Data Concepts Used

This project is designed around core big data ideas:

- Volume: product catalogs and ingredient datasets can grow to millions of records
- Velocity: new products and ingredient updates can be added over time
- Variety: product names, product types, URLs, ingredient lists, and user text descriptions
- Veracity: skincare labels and ingredient lists may be inconsistent, incomplete, or noisy
- Value: personalized skincare recommendations can improve product discovery and user satisfaction

## Suggested Big Data Architecture

1. Data sources
   - user skincare descriptions
   - skincare product catalog
   - cleaned ingredient lists
   - optional expert ingredient labels or review text
2. Data ingestion
   - batch ingestion from CSV or database exports
   - future ingestion from e-commerce product feeds
3. Storage
   - raw zone in HDFS, S3, or cloud object storage
   - cleaned analytics tables in Parquet
4. Processing
   - Apache Spark for cleaning, joins, feature engineering, and ranking
   - optional NLP on review text for concern extraction and sentiment
5. Serving
   - expose top-N recommendations through an API, dashboard, or mobile app

## Recommendation Logic

Each product gets a score based on:

- skin type compatibility
- concern matching
- sensitivity compatibility
- preferred ingredient flags
- avoided ingredient penalties

The current prototype uses:

`final_score = profile_match + concern_match + ingredient_bonus - penalty_score`

## Project Structure

```text
.
|-- README.md
|-- environment.yml
|-- data
|   |-- skincare_products_clean.csv
|   `-- user_profiles.csv
|-- docs
|   `-- project_proposal.md
`-- src
    `-- recommender.py
```

## Dataset Description

### `skincare_products_clean.csv`

The product catalog is loaded from the cleaned skincare dataset. It contains real product names, product URLs, product types, cleaned ingredient lists, and prices. The recommender infers skin concerns and ingredient flags from the product name, product type, and ingredient list.

It covers concerns such as acne, pores, oiliness, dehydration, redness, barrier repair, irritation, dark spots, melasma, dullness, texture, fine lines, wrinkles, sun protection, fungal-acne-style restrictions, and rosacea-like redness.

### `user_profiles.csv`

The generated user profile dataset is only used for sample-user demo mode. Interactive and natural-language modes do not require a stored user profile.

For ingredient preference questions, users can type `i dont know` or leave the answer blank.

## Simple Demo Flow

1. load the cleaned skincare product catalog
2. accept a natural-language skin description or structured profile answers
3. extract concerns such as acne, pores, dark spots, redness, and irritation
4. infer product concern tags and ingredient flags from product metadata
5. match the entered profile with products
6. rank products using weighted content-based scoring
7. output top recommendations with explanations and product URLs

## How to Run

Frontend website:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/web/
```

Interactive mode:

```bash
python src/recommender.py --interactive --top 5 --summary
```

Natural-language mode:

```bash
python src/recommender.py --text "My skin is oily and I get pimples, blackheads, and large pores. Fragrance irritates my face." --top 5
```

Stored sample-user mode:

```bash
python src/recommender.py --user U001 --top 5 --summary
```

## Ideas to Extend for Final Submission

- build a Spark version with DataFrame transformations
- add review-text sentiment analysis
- improve natural-language parsing with NLP models
- use a larger ingredient knowledge base
- evaluate recommendation quality with user feedback
- build a Streamlit or Power BI dashboard

## Report Sections You Can Reuse

1. introduction and business problem
2. dataset and data sources
3. big data characteristics
4. system architecture
5. natural-language feature extraction
6. recommendation algorithm
7. implementation details
8. results and sample outputs
9. limitations and future work

## View PPT
(https://canva.link/s8lxc4kcseff9m5)

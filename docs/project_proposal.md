# Project Proposal

## Title

Big Data Skincare Recommendation System for Different Face Types and Skin Problems

## Introduction

Choosing skincare products is difficult because people have different skin types, sensitivity levels, ingredient restrictions, and skin concerns. A product that works well for oily acne-prone skin may be unsuitable for dry, sensitive, or barrier-damaged skin. This project designs a recommendation system that helps users find suitable skincare products from a cleaned skincare product catalog.

The system is framed as a big data application because real skincare platforms generate large product catalogs with product metadata, ingredient lists, URLs, user descriptions, and review text. Big data tools make it possible to process these datasets efficiently and produce personalized recommendations at scale.

## Objectives

The project aims to:

1. build a recommendation engine for skincare products
2. accept natural-language skin descriptions from users
3. infer skincare concerns from user text
4. infer product concern tags from cleaned ingredient lists
5. cover problems such as acne, redness, dehydration, barrier repair, melasma, dark spots, texture, aging, fungal-acne-style restrictions, and rosacea-like redness
6. demonstrate big data concepts including data preprocessing, feature extraction, and scalable ranking
7. provide explainable recommendations instead of only black-box output

## Target Users

- people with oily, dry, combination, normal, or sensitive skin
- users with concerns such as acne, redness, dehydration, aging, pores, dark spots, melasma, irritation, or barrier damage
- online skincare stores or beauty platforms that want personalized product suggestions

## Data Sources

The prototype uses:

- a cleaned skincare product catalog
- product names and product URLs
- product types
- cleaned ingredient lists
- generated sample user profiles for demo mode

In a real-world big data system, these could be replaced or extended by e-commerce product feeds, review datasets, dermatologist ingredient labels, and large-scale user feedback.

## Big Data Characteristics

### Volume

A skincare platform may contain thousands or millions of products, ingredients, and user descriptions.

### Velocity

New products, ingredient updates, and user descriptions can be added continuously.

### Variety

The system uses product names, URLs, product types, cleaned ingredient lists, structured profile fields, and unstructured natural-language user descriptions.

### Veracity

Product labels and ingredient lists may be inconsistent, incomplete, or noisy, so data cleaning and validation are important.

### Value

The recommendation system helps users discover more suitable products and helps businesses improve user satisfaction and product discovery.

## System Design

### Input Features

- natural-language skin description
- inferred skin type
- inferred skin concerns
- sensitivity level
- preferred ingredient flags
- avoided ingredient flags
- product type
- cleaned product ingredients

### Recommendation Method

The proposed model uses a content-based approach:

1. text understanding
   - maps user language such as pimples, flaky skin, dark marks, or fragrance irritation into structured features
2. product feature extraction
   - maps ingredient lists into tags such as hyaluronic acid, ceramides, niacinamide, retinol, fragrance, and acids
3. ranking
   - scores products based on concern overlap, skin type compatibility, helpful ingredient flags, and avoidance penalties

## Big Data Technologies

Suggested stack:

- Hadoop or cloud object storage for raw data
- Apache Spark for distributed preprocessing and feature engineering
- Parquet for analytics storage
- Python for prototype logic
- optional Streamlit, Power BI, or a web API for demo visualization

## Processing Workflow

1. load cleaned product data
2. parse user natural-language input
3. infer user skin concerns and ingredient restrictions
4. infer product features from ingredient lists
5. compute ranking scores
6. return top-N recommendations for each user

## Evaluation

The system can be evaluated using:

- precision at k with user feedback
- coverage of different skin types and concerns
- expert review of recommendation explanations
- user satisfaction survey

## Expected Output

For each user, the system returns:

- top recommended products
- score for each recommendation
- product URL
- explanation such as "matches oily skin", "targets acne and pores", or "gentler option for sensitive skin"

## Future Improvements

- sentiment analysis on product reviews
- improved NLP for natural-language skin descriptions
- larger real-world product and ingredient datasets
- dermatologist or expert knowledge graph integration
- dashboard or web application interface

## Conclusion

This project is a practical big data application because it combines product metadata, ingredient feature extraction, natural-language user input, and explainable ranking logic to create personalized skincare recommendations.

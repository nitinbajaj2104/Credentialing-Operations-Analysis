# Credentialing-Operations-Analysis
This project analyzes US healthcare provider data to generate operational insights for credentialing and network validation. The analysis focuses on identifying provider distribution patterns, specialty concentration, data completeness gaps, and potential group practice indicators that are relevant to operational decision-making.

# Business Context

Credentialing teams depend on accurate provider information to ensure efficient network validation and compliance. This analysis helps answer key operational questions such as:

-> How providers are distributed across high-volume states

-> Which specialties are most prevalent

-> Where data quality issues may impact credentialing timelines

-> How shared practice locations can indicate group practices

# Data Source

Dataset: https://www.kaggle.com/datasets/shivd24coder/us-healthcare-providers-by-cities

Source: Kaggle

Format: JSON

Scope: Active individual healthcare providers across US cities

# Tools & Technologies

SQL: Primary tool for analysis and business queries

SQLite: Structured storage for querying and analysis

Python: Data preparation and database loading

Dashboarding: Google Looker Studio


# Data Processing & Database Setup

A Python-based data processing script was used to prepare and structure the provider data for analysis. It includes:

-> Reading the raw provider dataset in JSON format

-> Filtering individual providers (NPI-1) located in New York, California, and Texas

-> Creating a new SQLite database file named providers.db

-> Creating a structured table named provider_registry

-> Inserting the cleaned and filtered provider records into the database

This approach ensures the data is stored in a consistent, query-ready format for downstream analysis.


# SQL Analysis

The queries.sql file contains SQL queries designed to answer key credentialing and operational questions, including:

Total provider count by state

Top 10 most common provider specialties across all states

Cardiology providers in New York with practice city details

Data completeness assessment for missing provider names

Identification of shared practice addresses used by five or more providers

Query outputs were exported to spreadsheet format for validation and visualization.


# Dashboard

A one-page interactive dashboard was created to present insights in a leadership-friendly format, including:

Provider count by state

Top provider specialties

Percentage of providers with incomplete name data

Shared practice address analysis


# Key Insights & Recommendations

1. Significant concentration of providers in California

California dominates the provider network with 472 providers, representing 93% of all providers
across the three states. New York has only 23 providers (4.5%) and Texas just 11 providers
(2.2%).
This highlights the need for stronger credentialing workforce capacity planning and higher
automation coverage in high-volume states like California (CA) to reduce manual workload and
improve turnaround times. This also at the same time provides opportunity for targeted provider
recruitment in underrepresented regions like New York (NY) and Texas (TX)

2. Specialty Concentration in Behavioral Health Fields

The dataset is heavily skewed toward behavioral health, with Behavioral Technicians and
Marriage & Family Therapists representing the top common specialties. Notably, there are no
providers in New York (NY) whose primary specialty is related to 'Cardiology'.
Credentialing rules, license validation, and taxonomy checks for behavioral health providers
should be standardized and optimized, as they represent a large share of recurring credentialing
work. Also, the complete absence of cardiology providers in New York (NY) highlights critical
specialty gaps and suggests an immediate strategic recruitment opportunity in underserved
specialties.

3. Reliable identity data, but no large group practices detected

The data show 0% of providers missing both first and last name, indicating strong core identity
data quality. No practice address is shared by 5 or more providers, suggesting low likelihood of
large group practices in the current dataset in these three states.

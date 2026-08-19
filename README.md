# Bluestock MF Capstone — Mutual Fund Analytics Platform

End-to-end data engineering and analytics project for Bluestock Fintech: ETL pipeline, SQL data warehouse, exploratory data analysis, fund performance analytics, an interactive Power BI dashboard, and an advanced analytics layer — built on real AMFI India mutual fund data.

**Status: Complete — v1.0**

---

## Project Overview

This project simulates the analytics workflow of a real fintech data platform. Starting from 10 raw AMFI-anchored datasets covering 40 mutual fund schemes across 10 fund houses (Jan 2022 – May 2026), it builds a full pipeline: ingest → clean → load into a relational database → explore → analyse performance and risk → visualise → recommend.

NAV values are anchored to real historical data pulled live from the public mfapi.in API. Investor transaction data is synthetically generated using realistic demographic and behavioural distributions observed in the Indian mutual fund market — not records of real individuals.

---
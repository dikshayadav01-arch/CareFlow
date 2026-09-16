# CareFlow: Clinical Pathway Process Mining

## Overview

CareFlow is a healthcare operations analytics project that uses process mining to analyze real-world patient journeys through an Emergency Room.

Traditional BI dashboards can show metrics such as average waiting time, but they often fail to reveal the actual sequence of activities patients experience.

CareFlow addresses this problem by analyzing timestamped Electronic Health Record (EHR) event logs and discovering the actual patient flow.

## Problem Statement

Hospital administrators may know that Emergency Room waiting times are high, but average waiting-time metrics alone do not explain where operational bottlenecks occur.

CareFlow uses process mining to identify hidden patterns such as repeated activities, unexpected transitions, delays, and loop-backs in patient journeys.

## Example Bottleneck

A simulated patient journey may contain:

Registration → Triage → Doctor Consultation → X-Ray → Triage → Doctor Consultation → Treatment → Discharge

The repeated return to Triage represents a process loop that can contribute to additional waiting time.

## Technology Stack

* Python
* Pandas
* NumPy
* Faker
* Google BigQuery
* dbt
* PM4Py
* NetworkX
* Power BI
* Git / GitHub

## Architecture

Python EHR Generator
↓
Raw Event Logs
↓
Google BigQuery
↓
dbt Transformation
↓
Clean Event Log
↓
PM4Py Process Discovery
↓
Bottleneck & Conformance Analysis
↓
Power BI Dashboard

## Project Objectives

1. Generate realistic synthetic EHR event logs.
2. Store chronological healthcare events in BigQuery.
3. Transform raw EHR data into a standardized event-log structure using dbt.
4. Discover actual patient processes using PM4Py.
5. Identify bottlenecks and repeated process activities.
6. Calculate transition waiting times.
7. Perform conformance checking against an ideal patient pathway.
8. Build an interactive healthcare operations dashboard in Power BI.
9. Simulate the operational impact of correcting an identified bottleneck.

## Data Privacy

This project uses synthetic/mock healthcare data for educational and portfolio purposes.

No real patient records or personally identifiable health information are used.

## Project Status

### Week 1

* [x] Project structure
* [x] Git repository
* [ ] Synthetic EHR event generator
* [ ] Raw event dataset
* [ ] BigQuery setup

### Week 2

* [ ] dbt transformation
* [ ] Standard event-log model
* [ ] PM4Py process discovery
* [ ] Process map

### Week 3

* [ ] Transition-time analysis
* [ ] Bottleneck analysis
* [ ] Power BI dashboard
* [ ] Process visualization

### Week 4

* [ ] Conformance checking
* [ ] Actual vs ideal process comparison
* [ ] Dashboard refinement
* [ ] Intervention simulation
* [ ] Final documentation

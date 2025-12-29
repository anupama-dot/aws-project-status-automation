# AWS Project Status & Risk Automation

## Overview
This project demonstrates an event-driven AWS solution to automate project status reporting, milestone tracking, and risk notifications for delivery governance.

## Problem Statement
Manual project status reporting is time-consuming, error-prone, and often inconsistent across stakeholders. This solution automates governance checks and proactively alerts stakeholders to delivery risks and overdue milestones.

## Architecture
- Amazon S3 – Stores project status JSON files
- AWS Lambda – Evaluates project health, milestones, and risks
- Amazon SNS – Sends automated email notifications
- Amazon CloudWatch – Logs and monitoring

## How It Works
1. A project status file is uploaded to an S3 bucket
2. An S3 PUT event triggers the Lambda function
3. Lambda evaluates milestones and risks
4. SNS sends notifications to stakeholder email ID when thresholds are breached

## Technologies Used
- AWS S3
- AWS Lambda (Python)
- AWS SNS
- AWS CloudWatch

## Sample Input
See `sample-data/project_status_sample.json`

## Notes
- IAM roles are used for secure service access
- This project focuses on delivery governance automation rather than application development

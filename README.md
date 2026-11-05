# FieldFlow

FieldFlow is a full-stack field service management project for small plumbing, HVAC, and electrical service businesses.

The planned MVP helps internal teams coordinate technician assignments, track work orders, and review job completion notes.

## Project Status

Day 1 requirements analysis is complete. Requirements v0.1 is the approved initial MVP baseline. Application implementation has not started.

## Target Users

- **Admin / Manager:** Manage internal accounts and oversee work orders.
- **Dispatcher:** Create work orders, assign technicians, and track progress.
- **Technician:** View assigned jobs, update availability and progress, and submit completion notes.

Customers do not have accounts in the MVP.

## Planned MVP Features

- User login and basic role-based access control
- Work order management with customer and service information
- One technician assigned per work order
- Manually maintained technician availability
- Work order status updates
- Completion notes

## Core Business Rules

- Technician availability is manually controlled.
- Completing a work order does not automatically change technician availability.
- Customer information is stored directly in each work order.
- The assigned technician completes an In Progress work order by submitting non-empty completion notes.
- Completion does not require dispatcher approval.

## Documentation

- [Product Requirements — v0.1](docs/REQUIREMENTS.md)

## Outside the MVP

Customer accounts, independent customer management, photo uploads, analytics, email notifications, advanced scheduling and conflict detection, invoicing and payments, PDF reports, and completion approval are outside the approved MVP scope.

## Demo Data

All demonstrations will use fictional customer and company data.
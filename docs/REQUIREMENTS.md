# FieldFlow — Product Requirements Document

**Version:** 0.1  
**Status:** Approved for MVP Planning  
**Date:** November 5, 2026  
**Project Type:** Full-Stack Web Application

## 1. Project Overview

FieldFlow is a web-based field service management system for small Plumbing, HVAC, and Electrical service businesses.

The system helps dispatchers coordinate technician assignments, track work orders, and monitor job progress.

The MVP focuses on internal operations rather than customer-facing features.

## 2. Problem Statements

### PS-01 — Assignment Coordination

Dispatchers lack a reliable way to view technician-reported availability and coordinate job assignments.

This can result in inefficient communication and uncertainty about which technicians can take new jobs.

### PS-02 — Work Progress Visibility

Dispatchers lack timely updates on work order progress, making it difficult to track ongoing jobs and provide accurate information to customers.

## 3. Target Users

### Admin / Manager
- Manage internal user accounts.
- View all work orders.
- Oversee company operations.

### Dispatcher
- Create and edit work orders.
- View technician availability.
- Assign work orders to technicians.
- Track work order progress.
- Review completion notes.

### Technician
- Log in to their account.
- View assigned work orders and service addresses.
- Manually update availability.
- Update assigned work order status.
- Submit completion notes.

Customers do not have accounts in the MVP.

## 4. User Stories

### US-01 — Technician Availability

As a dispatcher, I want to see technicians' reported availability, so that I can identify technicians who may be able to take new jobs.

### US-02 — Job Completion Reporting

As a technician, I want to submit completion notes after finishing a job, so that dispatchers can see that the work order has been completed and review the work performed.

Additional user stories for login, work order creation, assignment, and progress updates will be refined before implementation.

## 5. Acceptance Criteria

### US-01 — Technician Availability

**AC-01**

Given a dispatcher is authenticated and authorized,

When the dispatcher opens the technician list,

Then the system displays each technician's current manually maintained availability status.

**AC-02**

Given an authenticated technician,

When the technician changes their availability to Available or Unavailable,

Then the system saves the new status and makes it visible to dispatchers.

**Business Rule:** Availability is manually controlled. It is not automatically calculated from scheduled or completed work orders.

### US-02 — Job Completion Reporting

**AC-01**

Given a technician is assigned to an In Progress work order,

When the technician submits valid, non-empty completion notes,

Then the system saves the notes and changes the work order status to Completed.

**AC-02**

Given a work order has been completed,

When an authorized dispatcher opens the work order,

Then the dispatcher can see its Completed status and submitted completion notes.

**AC-03**

Given a technician is not assigned to a work order,

When the technician attempts to complete that work order,

Then the system rejects the operation.

**Business Rule:** Completing a work order does not automatically change the technician's availability.

## 6. MVP Scope

### In Scope

1. User Login and Basic Role-Based Access Control.
2. Work Order Management.
3. Technician Assignment.
4. Manual Technician Availability.
5. Work Order Status Updates.
6. Completion Notes.

Each work order includes essential customer information such as customer name, contact information, and service address.

Each work order can be assigned to one technician.

### Out of Scope

- Customer accounts and customer portal.
- Independent Customer Management module.
- Photo uploads.
- Analytics Dashboard.
- Email notifications.
- Automatic technician availability calculation.
- Advanced scheduling and conflict detection.
- Invoicing and payments.
- PDF reports.
- Completion approval workflow.

## 7. Core Work Order Workflow

1. Dispatcher logs in.
2. Dispatcher creates a work order with customer and service information.
3. Dispatcher views technician-reported availability.
4. Dispatcher assigns a technician.
5. Technician logs in and views the assigned work order.
6. Technician updates the work order to In Progress.
7. Technician submits completion notes.
8. System updates the work order to Completed.
9. Dispatcher views the updated status and completion notes.

## 8. Confirmed Business Rules

- Only authenticated and authorized users can access protected operations.
- Technicians can update only their assigned work orders.
- Technician availability is manually controlled.
- Completing a work order does not automatically change availability.
- Customer information is stored directly with the work order.
- Completion requires non-empty notes.
- Completion does not require dispatcher approval.
- Photo uploads are not required in the MVP.

## 9. Open Questions for Future Refinement

- Can technicians accept or reject assignments?
- Which fields are mandatory when creating a work order?
- What exact status transitions are permitted?
- Can a Completed work order be reopened?
- Can dispatchers reassign In Progress work orders?
- How should unavailable technicians be handled during assignment?

These questions do not expand the approved MVP scope and will be resolved before implementing the affected features.

## 10. MVP Success Criteria

The MVP is successful when:

- A dispatcher can log in and create a work order.
- A dispatcher can view technician availability and assign a technician.
- A technician can log in and view assigned work orders.
- A technician can update work progress and submit completion notes.
- The system persists work order information and status changes.
- A dispatcher can view the completed work order and its notes.
- Unauthorized operations are rejected.

All demonstrations will use fictional customer and company data.

---

**Approval Status:** Requirements v0.1 approved as the initial MVP baseline. Additional details may be refined without expanding the agreed scope.
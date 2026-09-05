# SIH 2026 Project --- Farmer--Buyer Agricultural Trade Platform

> **Working Project Planning Document**
>
> This file is the single source of truth for the project. It contains
> the idea, product planning, user roles, features, workflows, UI
> direction, technical approach, MVP scope, future features, and open
> decisions.
>
> **Problem Statement:** SIH 26033\
> **Hackathon:** Smart India Hackathon 2026\
> **Status:** Planning / Concept Stage\
> **Last updated:** 2026-09-04

------------------------------------------------------------------------

## 1. Project Overview

### Working Concept

A **farmer-centric digital agricultural trading and fulfilment
platform** that connects farmers directly with buyers.

The platform is designed around three role types:

1.  **Farmer** --- supplies and sells agricultural produce.
2.  **Buyer** --- purchases agricultural produce in any required quantity.
3.  **Admin / Authorized Agriculture Officer** --- manages platform operations,
    verifies users, manages categories and reference data, handles disputes,
    manages cold-storage registrations, and performs authorized moderation and
    administrative actions.

The Buyer remains a unified account type; there are no separate bulk-buyer and
small-buyer roles.

A buyer is **not separated into "bulk buyer" and "small buyer"
accounts**. Every buyer has one account and can enter the quantity they
require while creating a request or placing an order.

The platform supports the complete journey:

``` text
Produce / Inventory
        ↓
Buyer Discovery or Buyer Requirement
        ↓
Farmer–Buyer Matching
        ↓
Order Request / Offer
        ↓
Accept / Reject / Counter-Offer
        ↓
Price Comparison and Decision Support
        ↓
Logistics
        ↓
Delivery Tracking
        ↓
Payment and Order History
```

### Core Vision

> Make agricultural trade easier by helping farmers manage produce,
> discover relevant buyers, understand market prices, respond to
> suitable orders, and manage fulfilment through a simple digital
> platform.

### Primary Goal

Create a simple and accessible platform supporting:

-   Inventory management
-   Produce discovery
-   Buyer requirements
-   Direct order requests
-   Quantity-based matching
-   Market/Mandi price visibility
-   Order negotiation
-   Logistics
-   Delivery tracking
-   Sales and purchase records
-   Multilingual accessibility

------------------------------------------------------------------------

## 2. Problem Being Addressed

The project aims to address:

-   Difficulty in directly connecting relevant farmers and buyers.
-   Fragmented communication during buying and selling.
-   Difficulty managing available produce and inventory.
-   Limited price visibility while evaluating an offer.
-   Difficulty finding suppliers with the required quantity.
-   Difficulty finding buyers interested in available produce.
-   Requests being sent to farmers who may not be interested in that
    quantity range.
-   Logistics challenges after a transaction is agreed.
-   Language and digital usability barriers.

------------------------------------------------------------------------

## 3. Proposed Solution

The solution is a web-based agricultural trading platform with
role-based dashboards.

### Main Modules

#### Farmer Module

The farmer can:

-   Register and log in using OTP when a suitable free OTP service is available;
    otherwise use phone number + password authentication.
-   Create and manage a farmer profile.
-   Upload/update a profile image.
-   Receive a unique Farmer ID generated at registration and display it in the
    profile.
-   Provide address and geographical information.
-   Add farm location(s), including an option to paste a Google Maps link or
    coordinates for the farm/land.
-   Optionally provide Aadhaar/government ID information for verification.
-   Receive a Verified Farmer badge only after the configured verification
    condition is satisfied.
-   Add produce to inventory.
-   Update available quantity.
-   Set product availability.
-   Receive buyer requirements and direct order requests.
-   Accept an order.
-   Reject an order.
-   Send a counter-offer.
-   Compare buyer offers with market/Mandi rates.
-   View sales and order history.
-   Book/request transportation.
-   Track deliveries.
-   View payments and earnings.
-   Access help and support.
-   Change language.
-   Configure the quantity ranges or order preferences they are willing
    to serve.

#### Buyer Module

A buyer has one unified account.

The buyer can:

-   Register and log in using OTP when a suitable free OTP service is available;
    otherwise use phone number + password authentication.
-   Create and manage a buyer/business profile.
-   Upload/update a profile image.
-   Receive a unique Buyer ID generated at registration and display it in the
    profile.
-   Provide business address and geographical information.
-   Optionally provide Aadhaar/government ID information for verification.
-   Receive a Verified Buyer badge only after the configured verification
    condition is satisfied.
-   Browse available produce.
-   Search for farmers and products.
-   Send a direct request to a selected farmer.
-   Post a general requirement.
-   Enter the required quantity.
-   Receive responses/offers from matching farmers.
-   Compare multiple farmer offers.
-   Select a preferred farmer.
-   Track active orders and delivery.
-   View payment and invoice history.
-   Save favourite farmers.
-   View market/Mandi rates.

**Important decision:** There are no separate "bulk buyer" and "small
buyer" account types. The buyer simply enters the required quantity.

------------------------------------------------------------------------


## 5. Admin / Authorized Agriculture Officer Module

The platform includes a third role for authorized administrative management.
For the SIH prototype this role may be represented as an **Admin / Authorized
Agriculture Officer**. Access must be protected with role-based permissions.

### Core Admin Responsibilities

The admin can:

-   Log in through a protected admin authentication flow.
-   View and manage farmer and buyer accounts.
-   Review farmer/buyer verification information and verification status.
-   Approve, reject, suspend, restrict, or restore accounts where permitted.
-   Review disputes registered between farmers and buyers.
-   Record dispute decisions, actions taken, evidence/notes, and resolution
    status.
-   Take authorized action against a farmer or buyer when a dispute or
    platform-rule violation requires intervention.
-   Manage produce/category master data and add new categories that appear in
    farmer and buyer selection fields.
-   Manage crop/product names, units, quality-grade options, and other
    configurable reference data.
-   Review and manage cold-storage registrations.
-   Add/register newly opened cold storages and update their details,
    availability, capacity, location, contact information, and services.
-   Manage featured/important government schemes and information-board posts.
-   Manage platform announcements and important notifications.
-   Review reports, flagged conversations/orders, and suspicious activity.
-   View operational dashboards for users, orders, disputes, and logistics.
-   Maintain an audit trail for important administrative actions.

### Recommended Admin Dashboard

Summary cards:

-   Total Farmers
-   Total Buyers
-   Pending Verifications
-   Open Disputes
-   Active Orders
-   Registered Cold Storages

Quick actions:

-   Verify User
-   Add Category
-   Review Disputes
-   Register Cold Storage
-   Publish Government Scheme
-   Review Reports

### Admin Permission Principle

Administrative actions should be permission-based rather than giving every
admin unrestricted access. Sensitive actions should be logged with the admin
ID, timestamp, target user/order, action, and reason.


## 5. Buyer--Farmer Matching Model

The platform supports both workflows.

### Workflow A: Direct Request

``` text
Buyer
  ↓
Browse Available Produce
  ↓
Select Product / Farmer
  ↓
View Availability
  ↓
Enter Required Quantity
  ↓
Send Request
  ↓
Farmer Accepts / Rejects / Counter-Offers
```

### Workflow B: Requirement-Based Matching

``` text
Buyer
  ↓
Post Requirement
  ↓
Enter Product + Quantity + Other Requirements
  ↓
System Finds Relevant Farmers
  ↓
Request Shared with Eligible / Interested Farmers
  ↓
Farmers Respond
  ↓
Buyer Compares Offers
  ↓
Buyer Selects an Offer
```

### Recommended Product Design

Support **both** direct requests and requirement-based matching.

This gives the buyer two choices:

1.  Browse and send a request to a specific farmer.
2.  Post a requirement and receive offers from matching farmers.

------------------------------------------------------------------------

## 6. Quantity and Farmer Interest Logic

The buyer enters the required quantity instead of selecting a bulk/small
order mode.

Farmers can configure:

-   Quantity ranges they are interested in serving.
-   Minimum quantity willing to sell.
-   Maximum quantity available per order, if applicable.
-   Whether they are open to all quantities.

When a buyer posts a requirement, matching can consider:

-   Product match.
-   Available quantity.
-   Farmer quantity preference.
-   Location/service area.
-   Availability status.
-   Quality requirements.
-   Price compatibility where applicable.

Only relevant farmers should receive the request.

Example:

``` text
Buyer requires:
Product: Wheat
Quantity: 2,000 kg

System checks:
✓ Farmer sells Wheat
✓ Farmer has enough quantity or can offer available quantity
✓ Farmer accepts this quantity range
✓ Farmer is available

Result:
Request is sent only to matching farmers.
```

------------------------------------------------------------------------

## 7. Farmer Dashboard

The farmer dashboard should prioritize simplicity and accessibility.

### UI Principles

-   Large buttons.
-   Clear icons.
-   Minimal steps.
-   Simple labels.
-   Important information visible immediately.
-   Multilingual support.

### Summary Cards

-   **Total Inventory**
-   **Active Orders**
-   **Total Sales**
-   **Pending Payments**

### Quick Actions

-   Add Produce
-   View Orders
-   Sell Produce
-   Market / Mandi Rates
-   Book Transport
-   Buy Seeds / Fertilizers
-   Voice Assistant
-   Visiting Card
-   Chat / Messages
-   Find Cold Storage
-   Government Schemes

### Main Sections

#### Inventory Overview

Display:

-   Product name.
-   Available quantity.
-   Unit.
-   Inventory distribution.
-   Low inventory alerts.

#### Recent Buyer Requests

Display:

-   Product.
-   Quantity requested.
-   Buyer.
-   Offered price.
-   Request date.
-   Review Order action.

#### Recent Sales

Display:

-   Product.
-   Quantity.
-   Amount.
-   Date.
-   Status.

#### Today's Mandi Rates

Display:

-   Selected Mandi.
-   Product.
-   Current/average price.
-   Minimum price.
-   Maximum price.
-   Price change.
-   Last updated time.

#### Transport Booking

Quick access to:

-   Book transport.
-   Vehicle requirement.
-   Pickup.
-   Destination.
-   Delivery tracking.

#### Help & Support

Provide:

-   Contact support.
-   FAQs.
-   Tutorials.
-   Voice assistance.

------------------------------------------------------------------------

## 8. Farmer Navigation

``` text
Dashboard
My Inventory
Buyer Orders
Sell Produce
Market / Mandi Rates
Logistics & Transport
Buy Seeds & Fertilizers
Payments & Earnings
Notifications
Help & Support
Profile Settings
Language
Logout
```

------------------------------------------------------------------------

## 9. Inventory Management

Suggested product fields:

-   Product/Crop Name
-   Quantity Available
-   Unit: kg / quintal / ton
-   Expected Price
-   Quality Grade
-   Harvest Date
-   Location
-   Produce Images
-   Availability Status

Example:

``` text
Wheat
Available: 5,000 kg
Expected Price: ₹24/kg
Market Rate: ₹23.50/kg
Quality: Grade A

[Edit] [Mark as Sold] [View Buyer Requests]
```

### Inventory Validation

Before accepting an order:

``` text
Buyer requests: 3,000 kg
Farmer inventory: 1,500 kg

Result:
⚠ Insufficient quantity available

Suggested action:
Offer available quantity: 1,500 kg
```

------------------------------------------------------------------------

## 10. Buyer Requirement System

A major feature is **Post New Requirement**.

Suggested fields:

-   Product
-   Quantity Required
-   Unit
-   Required Quality
-   Expected Price/Budget
-   Delivery Location
-   Required By Date
-   Additional Notes

Workflow:

``` text
Buyer Posts Requirement
        ↓
Validate Requirement
        ↓
Find Matching Farmers
        ↓
Check Product + Quantity + Preferences
        ↓
Send to Relevant Farmers
        ↓
Receive Farmer Responses
```

------------------------------------------------------------------------

## 11. Farmer Order Actions

When a farmer receives a request, show:

-   Product.
-   Quantity requested.
-   Buyer details.
-   Offered price.
-   Current Mandi rate.
-   Delivery location.
-   Estimated transport cost, if available.
-   Required delivery date.
-   Available inventory.

Actions:

-   **Accept**
-   **Reject**
-   **Counter-Offer**

Example counter-offer:

``` text
Buyer request:
5,000 kg at ₹20/kg

Farmer counter-offer:
Available Quantity: 4,000 kg
Requested Price: ₹22/kg
```

------------------------------------------------------------------------

## 12. Market / Mandi Rates

Show market information to support informed decisions.

Suggested information:

-   Product name.
-   Selected Mandi.
-   Minimum price.
-   Maximum price.
-   Average/current price.
-   Price movement.
-   Last updated time.

### Buyer-Side Offer Entry

When a buyer enters an offer while creating an order/request, show the
relevant Mandi rate for the selected product alongside the offer field.

Example:

``` text
Product: Potatoes
Quantity: 100 kg
Current Mandi Rate: ₹23.50/kg
Your Offer: ₹____/kg
```

The buyer can use the displayed market rate as decision support while entering
the offer.

### Offer Comparison

``` text
Buyer's Offer: ₹25/kg
Market Average: ₹23.50/kg

Status:
🟢 Offer is above the displayed market average.
```

or:

``` text
Buyer's Offer: ₹21/kg
Market Average: ₹23.50/kg

Status:
⚠ Offer is below the displayed market average.
```

------------------------------------------------------------------------

## 13. Smart Order Decision Assistance

Potential advanced feature: **Analyze Order**.

Compare:

-   Buyer offered price.
-   Current Mandi rate.
-   Farmer expected price.
-   Available inventory.
-   Distance.
-   Estimated logistics cost.

Suggested outcomes:

-   🟢 **Good Deal**
-   🟡 **Consider Negotiating**
-   🔴 **Review Carefully**

The system assists the farmer; it does not make the final decision
automatically.

------------------------------------------------------------------------

## 14. Logistics & Transport

Proposed workflow:

``` text
Order Confirmed
      ↓
Confirm Pickup Location
      ↓
Enter Delivery Location
      ↓
Enter Quantity / Product
      ↓
Select Delivery Date
      ↓
Identify Vehicle Requirement
      ↓
View Transport Options
      ↓
Book / Request Transport
      ↓
Transport Assigned
      ↓
Track Delivery
```

Possible vehicle types:

-   Mini Truck
-   Pickup Vehicle
-   Medium Truck
-   Large Truck
-   Refrigerated Vehicle
-   Cold-chain Transport

Future smart recommendation factors:

-   Quantity
-   Weight
-   Product type
-   Distance
-   Temperature/storage requirements

------------------------------------------------------------------------

## 15. Cold Storage --- Core Project Feature

The platform should provide a **Find / Book Cold Storage** module.

The farmer may:

-   Search nearby cold storages using farm/current location.
-   View cold-storage name, address and map location.
-   View available capacity.
-   View availability status.
-   View approximate charges.
-   View storage type/temperature or supported produce where available.
-   Contact the cold-storage operator.
-   Request/book storage space.
-   Track the status of the storage request.

### Cold Storage Registration

The Admin / Authorized Agriculture Officer can:

-   Register newly opened cold storages.
-   Approve or manage cold-storage listings.
-   Update capacity, availability, charges, services and contact details.
-   Maintain location/map information.
-   Suspend outdated or invalid listings.

This module is part of the initial project implementation rather than a
deferred future-only feature.

## 16. Farm Supplies Marketplace --- Initial Advanced Feature

Provide a marketplace where farmers can purchase agricultural inputs and
related products.

### Categories

-   Seeds
-   Fertilizers
-   Farming equipment
-   Irrigation products
-   Crop-protection/agricultural supplies where appropriate

### Functionality

-   Browse categories.
-   Search/filter products.
-   View vendors/products.
-   Compare options.
-   View product details and pricing.
-   Place orders.
-   View marketplace order history.

This feature is included in the first project implementation alongside the
other Priority 3 advanced features.

## 17. Shared Utilities and Communication

### Digital Visiting Card

Both farmers and buyers/business buyers should have a **Visiting Card**
utility generated automatically from their profile.

The card can contain:

-   Name / business name
-   Profile image
-   Role
-   Farmer ID / Buyer ID
-   Location
-   Crops/products or business category
-   Verification badge, if applicable
-   Short profile/business description
-   Contact options controlled by privacy settings

Users can:

-   Open their visiting card from the app.
-   Preview it.
-   Share it with another farmer or buyer.
-   Use a shareable digital-card format without exposing restricted personal
    information.

### Profile Pop-up

When a user clicks the profile picture/name of another farmer or buyer, show
a compact profile pop-up with basic details.

The mobile number must **not** be shown by default. Before sharing a personal
mobile number, the owner must explicitly enable/check a **Share my mobile
number** option. The same privacy rule applies to other sensitive personal
contact details.

### Chat and Communication

Provide a communication layer between farmers and buyers with:

-   Text chat.
-   Voice-chat/call capability where technically available.
-   Click-to-call action for a phone number that has been explicitly shared.
-   Order-linked conversations.
-   Offer and counter-offer cards inside the conversation.
-   Order status and delivery tracking inside the conversation.
-   Communication history retained as the transaction conversation history.

Phone numbers must not be automatically exposed merely because two users are
chatting.

### Order-Linked Chat

A chat thread can be associated with one or more relevant orders.

Within the chat, users should be able to:

1.  Discuss the selected product.
2.  See the current offer.
3.  Send a counter-offer.
4.  Accept/reject an offer where the order state permits it.
5.  View the related order.
6.  View order/delivery status.
7.  Access delivery-partner contact details when they are available.
8.  Continue using the conversation as a history of negotiation and
    fulfilment communication.

### Delivery Partner Contact

For an active delivery, the delivery details should include the assigned
delivery partner/driver contact information when available and authorized.
Both farmer and buyer should be able to contact the delivery partner for
delivery follow-up.


## 17. Notifications

### Farmer Notifications

-   New buyer request.
-   New direct order.
-   Counter-offer accepted.
-   Order confirmed.
-   Payment received.
-   Significant market price update.
-   Transport update.
-   Delivery completed.

### Buyer Notifications

-   New farmer response.
-   New counter-offer.
-   Requirement responses received.
-   Order accepted.
-   Transport assigned.
-   Delivery updates.
-   Payment/invoice updates.

------------------------------------------------------------------------

## 18. Multilingual Support

The application should be architected for broad multilingual support rather
than limiting the prototype to Hindi and English.

### Initial / Target Languages

-   English
-   Hindi
-   Marathi
-   Tamil
-   Telugu
-   Other major Indian languages relevant to farming communities, added
    through the same translation architecture.

All UI labels, important notifications, help content, and farmer-facing
information should use translation keys rather than hard-coded strings.

Voice assistance should also be designed so additional Indian languages can
be added where speech services support them.

## 19. Voice Assistance --- Advanced Feature

Potential voice interactions:

``` text
"गेहूं का भाव क्या है?"
```

``` text
"मेरे पास 500 किलो आलू है"
```

Potential uses:

-   Ask for market rates.
-   Start adding inventory.
-   Search orders.
-   Navigation help.

------------------------------------------------------------------------

## 20. Trust and Verification

### Identity and IDs

Every Farmer and Buyer receives a unique system-generated ID at registration.
The ID acts as the primary application identifier and is displayed in the
profile/visiting card where appropriate.

### Farmer Profile

Suggested information:

-   Farmer ID
-   Name
-   Profile image
-   Mobile number
-   Address
-   Farm location(s)
-   Google Maps link / coordinates
-   Crops grown
-   Preferred language
-   Verification status
-   Verified badge, when eligible

### Buyer Profile

Suggested information:

-   Buyer ID
-   Name/organisation
-   Profile image
-   Mobile number
-   Business details if applicable
-   Address
-   Location
-   Preferred language
-   Verification status
-   Verified badge, when eligible

### Aadhaar / Government ID

Aadhaar or another supported government ID is **optional**, not mandatory.

If supplied, the prototype can store the required verification data securely
and use it to represent a verification workflow. A future implementation may
integrate a government-supported identity flow such as DigiLocker, subject to
availability, authorization, privacy requirements, and API access.

For the SIH prototype:

-   No Aadhaar/government ID means the user can still use the platform.
-   Users who provide the required identity information can be marked as
    **verification pending/verified** according to the prototype workflow.
-   The **Verified Farmer** / **Verified Buyer** badge must only be displayed
    when the configured verification condition has been met.
-   Admins can review and manage verification status.

Do not expose Aadhaar or sensitive identity information in public profiles,
visiting cards, chat, or search results.

## 21. Ratings and Reviews

After completed transactions:

### Buyer rates Farmer

Potential criteria:

-   Product quality.
-   Quantity accuracy.
-   Communication.
-   Delivery cooperation.

### Farmer rates Buyer

Potential criteria:

-   Payment experience.
-   Communication.
-   Reliability.

Simple model:

``` text
⭐ 1–5
```

------------------------------------------------------------------------

## 22. Buyer Dashboard

The buyer dashboard is tailored to purchasing.

### Current UI Direction

-   **Orange and white theme**
-   Clean, modern layout
-   Rounded cards
-   Search at the top
-   Prominent quantity field
-   No separate bulk/small order buttons

### Summary Cards

-   Active Orders
-   Pending Responses
-   Orders in Delivery
-   Pending Actions

### Quick Actions

-   Post Requirement
-   Browse Produce
-   Find Farmers
-   Track Delivery
-   Request History

### Prominent Post Requirement Form

Fields:

-   Product
-   Quantity Required
-   Unit
-   Delivery Location
-   Required By Date
-   Submit/Post Requirement

### Recent Farmer Responses

Display:

-   Farmer.
-   Product.
-   Available quantity.
-   Price.
-   Approximate location/distance.
-   Response time.
-   View Offer.

### Active Orders

Display:

-   Product.
-   Order ID.
-   Quantity.
-   Amount.
-   Delivery date.
-   Status.

Statuses:

-   Confirmed
-   Transport Assigned
-   In Delivery
-   Delivered

### Other Sections

-   Market Prices
-   Profile / Manage Profile
-   Visiting Card
-   Chat / Messages
-   Notifications
-   Support & Help

------------------------------------------------------------------------

## 23. Buyer Navigation

``` text
Dashboard
Browse Produce
Post Requirement
My Orders
Farmer Responses
Favourite Farmers
Track Delivery
Payments & Invoices
Notifications
Support & Help
Settings
Logout
```

------------------------------------------------------------------------

## 24. Farmer Offer Comparison

When multiple farmers respond, compare:

  Factor                  Purpose
  ----------------------- ---------------------------
  Farmer                  Identify supplier
  Product                 Confirm requested product
  Available Quantity      Confirm supply
  Price                   Compare cost
  Quality                 Compare suitability
  Location/Distance       Estimate logistics
  Rating                  Assess trust
  Delivery Availability   Assess fulfilment

Workflow:

``` text
Requirement Posted
        ↓
Multiple Farmers Respond
        ↓
Compare Offers
        ↓
Select Preferred Farmer
        ↓
Confirm Order
```

------------------------------------------------------------------------

## 25. Smart Matching / Recommendation

Potential matching factors:

``` text
Product Match
+ Quantity Match
+ Farmer Availability
+ Quantity Preference
+ Location / Distance
+ Quality Match
+ Price Compatibility
+ Verification / Rating
```

For the first prototype, use a **rule-based matching system** if needed.
AI/ML is not required for the MVP.

------------------------------------------------------------------------

## 26. Order Tracking

Suggested timeline:

``` text
✓ Request Sent
        ↓
✓ Farmer Accepted
        ↓
✓ Order Confirmed
        ↓
✓ Produce Prepared
        ↓
🚚 Transport Assigned
        ↓
📍 On the Way
        ↓
📦 Delivered
        ↓
💰 Payment Completed
```

------------------------------------------------------------------------

## 27. Payments and Transaction History

### Farmer

-   Total earnings.
-   Pending payments.
-   Completed payments.
-   Payment history.

### Buyer

-   Total spent.
-   Pending payments.
-   Completed payments.
-   Invoice/order history.
-   Total amount spent across historical orders (shown in order history,
    not as a homepage summary card).

Payment integration may be simulated for the prototype if necessary.

Future possibilities:

-   Payment confirmation.
-   Digital invoices.
-   Protected/escrow-like workflows subject to legal and business
    feasibility.

------------------------------------------------------------------------

## 28. Help and Information

Include:

### How It Works

1.  Register.
2.  Add produce or post a requirement.
3.  Find relevant matches.
4.  Send/receive requests.
5.  Accept or negotiate.
6.  Arrange logistics.
7.  Track delivery.
8.  Complete payment.

Also:

-   FAQs
-   Short visual tutorials
-   Voice assistance
-   Contact support

------------------------------------------------------------------------

## 29. Public Landing Page

### Hero Section

Suggested message:

> Better Markets. Better Connections. Smarter Agricultural Trade.

Supporting statement:

> Connect farmers and buyers through a simpler platform for produce
> discovery, requirements, orders, market information and fulfilment.

Primary actions:

-   I am a Farmer
-   I am a Buyer

### How It Works

Farmer:

``` text
Add Produce
    ↓
Receive Buyer Requests
    ↓
Accept / Negotiate
    ↓
Arrange Transport
    ↓
Deliver & Complete Order
```

Buyer:

``` text
Browse Produce / Post Requirement
    ↓
Find Matching Farmers
    ↓
Receive Offers
    ↓
Compare & Select
    ↓
Track Delivery
```

### Feature Highlights

-   Direct Farmer--Buyer Connection
-   Inventory Management
-   Quantity-Based Requirements
-   Market/Mandi Rates
-   Offer Comparison
-   Logistics Support
-   Multilingual Access
-   Voice Assistance (planned)

------------------------------------------------------------------------

## 30. Technical Approach

### Suggested Stack

#### Frontend

-   React.js
-   Tailwind CSS

#### Backend

-   Node.js
-   Express.js

#### Database

-   MongoDB

#### Authentication

-   JWT
-   Role-Based Access Control
-   Phone-number based authentication
-   Preferred: free/zero-cost OTP service if a suitable service is available
  and practical for the prototype
-   Fallback: phone number + password stored securely (password hash, never
  plaintext) and verified from the database
-   OTP/password implementation must be isolated behind an authentication
  service so the provider can be changed later


#### Potential Integrations

-   Market/Mandi data source or API.
-   Maps/geolocation.
-   Notifications.
-   Translation.
-   Speech-to-text/text-to-speech.
-   Logistics APIs/partners.

### Suggested Architecture

``` text
React Frontend
      ↓
REST API / Backend
      ↓
Authentication + Business Logic
      ↓
MongoDB
      ↓
External Services
├── Market/Mandi Data
├── Maps / Location
├── Notifications
├── Translation
└── Voice / Logistics (optional)
```

------------------------------------------------------------------------

## 31. Development Methodology

### User-Centred Design

Prioritize simple workflows for both roles.

### Modular Development

Suggested modules:

1.  Authentication
2.  Farmer profile
3.  Buyer profile
4.  Inventory
5.  Produce browsing
6.  Requirements
7.  Orders
8.  Matching
9.  Market rates
10. Logistics
11. Payments/history
12. Notifications
13. Chat & Communication
14. Visiting Cards
15. Cold Storage
16. Farm Supplies Marketplace
17. Government Schemes / Information Board
18. Admin & Verification
19. Disputes & Moderation
20. Profile / Privacy

### Agile / Iterative Process

``` text
Plan
 ↓
Design
 ↓
Build MVP
 ↓
Test
 ↓
Get Feedback
 ↓
Improve
 ↓
Add Next Module
```

------------------------------------------------------------------------

## 32. MVP Scope

### Priority 1 --- Essential

#### Authentication

-   Register
-   Login
-   Farmer role
-   Buyer role

#### Farmer

-   Add/manage produce.
-   View inventory.
-   Receive requests.
-   Accept/reject/counter-offer.
-   View basic sales/order history.

#### Buyer

-   Browse produce.
-   Search/filter.
-   Send direct request.
-   Post requirement with quantity.
-   Receive farmer responses.
-   Compare offers.
-   Select an offer.

#### Matching

-   Product match.
-   Quantity match.
-   Farmer preference/eligibility.

#### Market Information

-   Display market/Mandi rates.
-   Compare offer with market information.

#### Order Status

-   Request.
-   Response.
-   Confirmation.
-   Delivery status.

### Priority 2 --- Strong Prototype Enhancements

-   Basic logistics booking/request.
-   Delivery tracking statuses.
-   Notifications.
-   Multilingual support.
-   Verified profile indicators.

### Priority 3 --- Advanced / Future

-   Voice assistant.
-   Smart order analysis.
-   AI/ML recommendations.
-   Price prediction.
-   Demand prediction.
-   Cold storage booking.
-   Farm supplies marketplace.
-   Advanced logistics recommendations.
-   Ratings and reviews.
-   Full payment integration.

------------------------------------------------------------------------

## 33. Key Differentiators

The project should not be positioned as only a basic marketplace.

1.  **Farmer-first design**
    -   Simple and accessible.
2.  **Unified Buyer Model**
    -   One buyer account for all quantities.
3.  **Quantity-Based Matching**
    -   Buyers enter required quantity.
    -   Requests reach relevant/interested farmers.
4.  **Two Purchase Workflows**
    -   Direct request.
    -   Requirement-based matching.
5.  **Market-Aware Decisions**
    -   Market/Mandi visibility.
    -   Offer comparison.
6.  **Negotiation**
    -   Accept.
    -   Reject.
    -   Counter-offer.
7.  **End-to-End Fulfilment Vision**
    -   Trade.
    -   Logistics.
    -   Delivery tracking.
    -   Payment history.

------------------------------------------------------------------------

## 34. Feasibility and Risks

### Why the MVP Is Feasible

-   Mature technology stack.
-   React, Node.js, Express.js and MongoDB support rapid development.
-   Modular development.
-   Advanced features can be deferred.
-   External APIs can be integrated gradually.

### Challenges and Strategies

  -----------------------------------------------------------------------
  Challenge                           Strategy
  ----------------------------------- -----------------------------------
  Reliable market data                Prefer authoritative/official
                                      sources and show update time

  Digital literacy                    Large buttons, icons, simple
                                      wording, multilingual support

  Trust                               Verification, ratings, transaction
                                      history

  Logistics                           Start with request/booking flow,
                                      integrate providers later

  Fraud/security                      Secure authentication, validation,
                                      role-based access, order history
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 35. Expected Impact

### Farmers

-   Better visibility to buyers.
-   Easier inventory management.
-   Easier order management.
-   Better market awareness.
-   More informed decisions.
-   Logistics support.

### Buyers

-   Easier supplier discovery.
-   Clearer product availability.
-   Quantity-based requirements.
-   Multiple offers for comparison.
-   Order and delivery tracking.

### Economic

-   Improved market connectivity.
-   More efficient procurement coordination.
-   Better information flow.
-   Reduced friction in agricultural trade.

### Social

-   Multilingual accessibility.
-   Improved digital inclusion.
-   Farmer-friendly technology design.

### Environmental / Supply Chain

-   Better logistics coordination.
-   Potential reduction in avoidable delays and wastage.
-   Future cold-storage support.

------------------------------------------------------------------------

## 36. Presentation / PPT Structure

### Slide 1 --- Title

-   Project name
-   SIH 2026
-   Problem Statement: SIH 26033
-   Official theme
-   Team name
-   Team members
-   College/university
-   Tagline

### Slide 2 --- Idea / Proposed Solution

-   Problem
-   Proposed solution
-   How it addresses the problem
-   Innovation and uniqueness

### Slide 3 --- Technical Approach

-   Technology stack
-   Programming languages
-   Development methodology
-   Architecture/process
-   Flowchart
-   Dashboard/prototype screenshots

### Slide 4 --- Feasibility & Viability

-   Why feasible
-   Challenges
-   Risks
-   Mitigation strategies

### Slide 5 --- Impact & Benefits

-   Farmer benefits
-   Buyer benefits
-   Economic impact
-   Social impact
-   Environmental/supply-chain impact

### Slide 6 --- Research & References

Only include sources actually used:

-   Official SIH documentation
-   Official agricultural/market sources
-   Government reports
-   Research papers
-   Technical documentation

------------------------------------------------------------------------

## 37. Main Product Flow

``` text
                         PLATFORM

              ┌──────────────┴──────────────┐
              ↓                             ↓
           FARMER                         BUYER
              ↓                             ↓
      Add Produce / Inventory       Browse / Search Produce
              ↓                             │
              ↓                             ├───────────────┐
              ↓                             ↓               ↓
      Receive Direct Request         Direct Request   Post Requirement
              │                             │               │
              │                             └───────┬───────┘
              ↓                                     ↓
      Check Quantity + Price                 Matching System
              ↓                                     ↓
      Accept / Reject / Counter          Relevant Farmers Notified
              │                                     ↓
              └──────────────────┬──────────────────┘
                                 ↓
                         Offer / Order Confirmed
                                 ↓
                       Market Price Comparison
                                 ↓
                        Logistics Arrangement
                                 ↓
                          Delivery Tracking
                                 ↓
                       Payment / Order History
```

------------------------------------------------------------------------

## 38. Coding AI Agent Instructions

Treat this file as the product requirements document.

### Rules

1.  Do not assume undocumented features without checking.
2.  Preserve two primary user roles: Farmer and Buyer.
3.  Do not create separate bulk-buyer and small-buyer account roles.
4.  Buyers enter required quantity.
5.  Support both direct requests and requirement-based matching.
6.  Requirement requests should go only to relevant/eligible/interested
    farmers.
7.  Farmer UI must prioritize simplicity and accessibility.
8.  Build the MVP before advanced features.
9.  Keep the architecture modular.
10. Use placeholders/mocks where real external integrations are
    unavailable.
11. Advanced AI features are not required for the initial MVP unless
    explicitly added later.
12. Before making a major decision that conflicts with this file, update
    the plan or ask for clarification.

------------------------------------------------------------------------

## 39. Open Decisions / To Be Finalized

### Product Identity

-   Final project name.
-   Final tagline.
-   Official SIH theme wording.
-   Logo.
-   Shared brand/design system.

### Order Logic

-   Exact minimum/maximum quantity preference model.
-   Whether multiple farmers can partially fulfil one requirement.
-   Whether buyers can edit a requirement after responses begin.
-   Exact counter-offer workflow.
-   Whether in-app chat is required for MVP.

### Matching

-   Exact ranking formula.
-   Location radius.
-   Whether distance is required in MVP.
-   Quality grade standardization.

### Payments

-   Real integration vs prototype simulation.
-   Payment confirmation workflow.
-   Invoice requirements.

### Logistics

-   Mock data vs real provider/API.
-   Vehicle selection logic.
-   Tracking method.

### Verification

-   Farmer verification requirements.
-   Buyer verification requirements.
-   Manual/API/prototype verification.

### Market Data

-   Final data source/API.
-   Update frequency.
-   Geographic coverage.

------------------------------------------------------------------------

## 40. Change Log

  -----------------------------------------------------------------------
  Date                    Change                  Reason / Notes
  ----------------------- ----------------------- -----------------------
  2026-09-04              Initial planning        Consolidated project
                          document created        discussions

  2026-09-04              Unified Buyer role      Buyer enters required
                          confirmed               quantity; no bulk/small
                                                  account split

  2026-09-04              Buyer dashboard         Orange and white theme
                          direction confirmed     

  TBD                                             
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## 41. Current MVP Definition

``` text
Authentication
    ↓
Farmer Dashboard + Inventory
    ↓
Buyer Dashboard
    ↓
Browse Produce
    ↓
Direct Request
    +
Post Requirement
    ↓
Quantity-Based Matching
    ↓
Farmer Response
    ↓
Accept / Reject / Counter-Offer
    ↓
Order Status Tracking
    ↓
Market/Mandi Rate Display
    ↓
Basic Logistics Request
    ↓
Transaction / Order History
```

### MVP Success Scenario

The final prototype should demonstrate:

1.  A farmer registers and adds Wheat to inventory.
2.  The farmer configures availability/preferences.
3.  A buyer registers.
4.  The buyer searches for Wheat or posts a requirement with a specific
    quantity.
5.  The platform identifies matching farmers.
6.  Relevant farmers receive the request.
7.  A farmer accepts, rejects or counter-offers.
8.  The buyer compares/selects an offer.
9.  The order is confirmed.
10. Market rate information is visible.
11. A transport/logistics request can be initiated.
12. Both users can view order status.

------------------------------------------------------------------------

## End of Current Planning Document

**This document will evolve with the project. Add, remove, or revise
requirements here before implementing major new functionality.**

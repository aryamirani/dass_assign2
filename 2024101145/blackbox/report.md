# Black Box API Testing Report

## 3.1 Test Case Design
We designed a comprehensive suite of 29 automated test cases using `pytest` and `requests`. These tests target the QuickCart REST API endpoints documented in the specification, focusing on headers, data validation, and integrated system logic.

### Categories of Tests
- **Authentication & Headers**: Verified `X-Roll-Number` and `X-User-ID` requirements across all endpoints.
- **Profile Management**: Validated character length constraints for names and digit counts for phone numbers.
- **Addresses**: Tested CRUD operations, label constraints (HOME, OFFICE, OTHER), and the single-default-address business logic.
- **Products**: Verified active-only visibility and product lookup failures.
- **Cart**: Tested the logic for adding, updating, and clearing items, including stock constraints.
- **Wallet & Loyalty**: Validated transaction limits ($0 - $100,000) and balance sufficiency logic.
- **Reviews**: Tested rating boundaries (1-5) and comment length validations.
- **Support Tickets**: Validated subject/message lengths and state transition rules (OPEN -> IN_PROGRESS -> CLOSED).
- **Checkout & Coupons**: Verified payment method restrictions and the $5,000 COD limit rule.

## 3.2 Bug Report
During testing, four critical deviations from the API documentation were discovered.

### Bug 1: Cart Accepts Non-Positive Quantities
- **Endpoint**: `POST /api/v1/cart/add`
- **Request Payload**:
  ```json
  {"product_id": 1, "quantity": 0}
  ```
- **Expected Result**: 400 Bad Request (Documentation: "quantity must be at least 1... negative number must be rejected").
- **Actual Result**: 200 OK. The server allowed adding 0 or negative quantities to the cart.

### Bug 2: Reviews Accept Invalid Ratings
- **Endpoint**: `POST /api/v1/products/{product_id}/reviews`
- **Request Payload**:
  ```json
  {"rating": 6, "comment": "Excellent!"}
  ```
- **Expected Result**: 400 Bad Request (Documentation: "rating must be between 1 and 5. Anything outside that range must be rejected").
- **Actual Result**: 200 OK. The server accepted a rating of 6.

### Bug 3: COD Limit Not Enforced
- **Endpoint**: `POST /api/v1/checkout`
- **Request Payload**:
  ```json
  {"payment_method": "COD"}
  ```
  *(Scenario: Cart contains 100 units of Product 1 at $120 each, total $12,000)*
- **Expected Result**: 400 Bad Request (Documentation: "COD is not allowed if the order total is more than 5000").
- **Actual Result**: 200 OK. The server allowed a $12,000 order to proceed using Cash on Delivery.

### Bug 4: Profile Update Response Missing Data
- **Endpoint**: `PUT /api/v1/profile`
- **Request Payload**:
  ```json
  {"name": "John Doe", "phone": "1234567890"}
  ```
- **Expected Result**: A response containing the updated user data (matching the "Address Update" pattern).
- **Actual Result**: Returns only `{"message": "Profile updated successfully"}`. While not a strict logical failure, it deviates from the consistency established in the Address management documentation.

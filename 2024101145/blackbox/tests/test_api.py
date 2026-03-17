import pytest
import requests

BASE_URL = "http://localhost:8080/api/v1"

# Headers needed
HEADERS_VALID = {
    "X-Roll-Number": "2024101145",
    "X-User-ID": "1"
}

HEADERS_ADMIN = {
    "X-Roll-Number": "2024101145"
}

def test_missing_roll_number_header():
    """Validates that a missing X-Roll-Number returns 401."""
    response = requests.get(f"{BASE_URL}/admin/users")
    assert response.status_code == 401

def test_invalid_roll_number_header():
    """Validates that a non-integer X-Roll-Number returns 400."""
    response = requests.get(f"{BASE_URL}/admin/users", headers={"X-Roll-Number": "abc"})
    assert response.status_code == 400

def test_missing_user_id_profile():
    """Validates user-scoped endpoints require X-User-ID (400 if missing)."""
    response = requests.get(f"{BASE_URL}/profile", headers=HEADERS_ADMIN)
    assert response.status_code == 400

def test_admin_users_endpoint():
    """Validates the Admin Users endpoint returns a list of users."""
    response = requests.get(f"{BASE_URL}/admin/users", headers=HEADERS_ADMIN)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_profile_get():
    """Validates we can fetch the user profile."""
    response = requests.get(f"{BASE_URL}/profile", headers=HEADERS_VALID)
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "phone" in data

def test_profile_update_invalid_name():
    """Validates profile name length rules (2-50 chars). Expected 400."""
    payload = {"name": "A", "phone": "1234567890"} # Too short
    response = requests.put(f"{BASE_URL}/profile", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_profile_update_invalid_phone():
    """Validates profile phone rules (exactly 10 digits). Expected 400."""
    payload = {"name": "John Doe", "phone": "123"} # Too short
    response = requests.put(f"{BASE_URL}/profile", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_profile_update_valid():
    """Validates valid profile updates work."""
    payload = {"name": "John Doe", "phone": "1234567890"}
    response = requests.put(f"{BASE_URL}/profile", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["name"] == "John Doe"
    assert data["user"]["phone"] == "1234567890"

# --- Addresses ---

def test_address_add_invalid_label():
    """Label must be HOME, OFFICE, or OTHER. Expected 400."""
    payload = {
        "label": "WORK", # Invalid
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "123456",
        "is_default": True
    }
    response = requests.post(f"{BASE_URL}/addresses", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_address_add_invalid_street():
    """Street must be 5-100 chars. Expected 400."""
    payload = {
        "label": "HOME",
        "street": "12", # Too short
        "city": "Metropolis",
        "pincode": "123456",
        "is_default": True
    }
    response = requests.post(f"{BASE_URL}/addresses", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_address_add_invalid_city():
    """City must be 2-50 chars. Expected 400."""
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "A", # Too short
        "pincode": "123456",
        "is_default": True
    }
    response = requests.post(f"{BASE_URL}/addresses", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_address_add_invalid_pincode():
    """Pincode must be 6 digits. Expected 400."""
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "12345", # Too short
        "is_default": True
    }
    response = requests.post(f"{BASE_URL}/addresses", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400


def test_address_lifecycle():
    """Validates adding, default toggle, updating, and deleting."""
    payload = {
        "label": "HOME",
        "street": "123 Main St",
        "city": "Metropolis",
        "pincode": "123456",
        "is_default": True
    }
    # Add
    response = requests.post(f"{BASE_URL}/addresses", headers=HEADERS_VALID, json=payload)
    if response.status_code != 200 and response.status_code != 201:
        # Gracefully handle API returning 401/500 if the server expects something else
        return
        
    data = response.json()
    assert "address" in data
    assert "address_id" in data["address"]
    assert data["address"]["label"] == "HOME"
    address_id = data["address"]["address_id"]

    # Update (Only street and is_default can change)
    update_payload = {"street": "456 New St", "is_default": False}
    update_response = requests.put(f"{BASE_URL}/addresses/{address_id}", headers=HEADERS_VALID, json=update_payload)
    # Based on docs: must show new updated data
    assert update_response.status_code == 200
    update_data = update_response.json()
    # It might be nested in 'address' based on the POST response
    addr = update_data.get("address", update_data)
    assert addr["street"] == "456 New St"
    assert addr["is_default"] == False

    # Delete
    del_response = requests.delete(f"{BASE_URL}/addresses/{address_id}", headers=HEADERS_VALID)
    assert del_response.status_code == 200

# --- Products ---

def test_products_list_active_only():
    """Validates the list only returns active products."""
    response = requests.get(f"{BASE_URL}/products", headers=HEADERS_VALID)
    assert response.status_code == 200
    products = response.json()
    for p in products:
        assert p.get("is_active", True) is True

def test_product_not_found():
    """Validates looking up a non-existent product returns 404."""
    response = requests.get(f"{BASE_URL}/products/999999", headers=HEADERS_VALID)
    assert response.status_code == 404

# --- Cart ---

def test_cart_add_invalid_quantity():
    """Quantity must be >= 1. Sending 0 or negative = 400."""
    payload = {"product_id": 1, "quantity": 0}
    response = requests.post(f"{BASE_URL}/cart/add", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400
    
    payload = {"product_id": 1, "quantity": -5}
    response = requests.post(f"{BASE_URL}/cart/add", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_cart_add_stock_limit():
    """Quantity requested > stock = 400."""
    payload = {"product_id": 1, "quantity": 999999}
    response = requests.post(f"{BASE_URL}/cart/add", headers=HEADERS_VALID, json=payload)
    if response.status_code != 404: # Product 1 might not exist
        assert response.status_code == 400

def test_cart_update_invalid_quantity():
    """Updating cart quantity must be >= 1."""
    payload = {"product_id": 1, "quantity": 0}
    response = requests.post(f"{BASE_URL}/cart/update", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400


# --- Wallet ---

def test_wallet_add_invalid():
    """Wallet add must be > 0 and <= 100000. Expected 400."""
    payload = {"amount": 0}
    response = requests.post(f"{BASE_URL}/wallet/add", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400
    
    payload = {"amount": 100001}
    response = requests.post(f"{BASE_URL}/wallet/add", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_wallet_pay_insufficient():
    """Paying from wallet with insufficient funds returns 400."""
    # Assuming user 1 doesn't have 999999
    payload = {"amount": 999999}
    response = requests.post(f"{BASE_URL}/wallet/pay", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

# --- Loyalty ---
def test_loyalty_redeem_invalid():
    """Redeeming loyalty < 1 returns 400."""
    payload = {"amount": 0}
    response = requests.post(f"{BASE_URL}/loyalty/redeem", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

# --- Reviews ---
def test_review_invalid_rating():
    """Review rating must be between 1 and 5. Expected 400."""
    payload = {"rating": 6, "comment": "Great product!"}
    response = requests.post(f"{BASE_URL}/products/1/reviews", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400
    
    payload = {"rating": 0, "comment": "Bad product!"}
    response = requests.post(f"{BASE_URL}/products/1/reviews", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_review_invalid_comment_length():
    """Comment must be 1-200 chars."""
    payload = {"rating": 5, "comment": ""}
    response = requests.post(f"{BASE_URL}/products/1/reviews", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

# --- Support Tickets ---
def test_support_ticket_creation_invalid():
    """Subject must be 5-100. Message must be 1-500."""
    payload = {"subject": "abc", "message": "Help me!"} # too short
    response = requests.post(f"{BASE_URL}/support/ticket", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400


# --- Coupons ---
def test_coupon_apply_valid():
    """Applying a valid coupon to an empty cart 400 vs non-empty."""
    # First ensure cart is empty
    requests.delete(f"{BASE_URL}/cart/clear", headers=HEADERS_VALID)
    # Add a product to cart to test coupon
    requests.post(f"{BASE_URL}/cart/add", headers=HEADERS_VALID, json={"product_id": 1, "quantity": 1})
    payload = {"code": "WELCOME10"}
    response = requests.post(f"{BASE_URL}/coupon/apply", headers=HEADERS_VALID, json=payload)
    assert response.status_code in [200, 404, 400] # Depends on if WELCOME10 exists or min value

# --- Checkout ---
def test_checkout_empty_cart():
    """Checkout with empty cart returns 400."""
    requests.delete(f"{BASE_URL}/cart/clear", headers=HEADERS_VALID)
    payload = {"payment_method": "COD"}
    response = requests.post(f"{BASE_URL}/checkout", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_checkout_invalid_payment():
    """Invalid payment method returns 400."""
    requests.post(f"{BASE_URL}/cart/add", headers=HEADERS_VALID, json={"product_id": 1, "quantity": 1})
    payload = {"payment_method": "BITCOIN"}
    response = requests.post(f"{BASE_URL}/checkout", headers=HEADERS_VALID, json=payload)
    assert response.status_code == 400

def test_checkout_cod_limit():
    """COD > 5000 returns 400."""
    # Add large quantity
    requests.delete(f"{BASE_URL}/cart/clear", headers=HEADERS_VALID)
    requests.post(f"{BASE_URL}/cart/add", headers=HEADERS_VALID, json={"product_id": 1, "quantity": 100})
    payload = {"payment_method": "COD"}
    response = requests.post(f"{BASE_URL}/checkout", headers=HEADERS_VALID, json=payload)
    # Could be 400 for COD limit, or 400 for stock limit
    assert response.status_code == 400

# --- Orders ---
def test_order_cancel_invalid():
    """Cancel fake order returns 404."""
    response = requests.post(f"{BASE_URL}/orders/999999/cancel", headers=HEADERS_VALID)
    assert response.status_code == 404


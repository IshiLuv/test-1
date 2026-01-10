DEFAULT_CURRENCY = "USD"
TAX_RATE = 0.21

SAVE10_RATE = 0.10
SAVE20_RATE_HIGH = 0.20
SAVE20_RATE_LOW = 0.05
SAVE20_THRESHOLD = 200

VIP_DISCOUNT_HIGH = 50
VIP_DISCOUNT_LOW = 10
VIP_THRESHOLD = 100


def parse_request(request):
    user_id = request.get("user_id")
    items = request.get("items")
    coupon = request.get("coupon")
    currency = request.get("currency")
    return user_id, items, coupon, currency


def validate_user_id(user_id):
    if user_id is None:
        raise ValueError("user_id is required")


def validate_items(items):
    if items is None:
        raise ValueError("items is required")

    if type(items) is not list:
        raise ValueError("items must be a list")

    if len(items) == 0:
        raise ValueError("items must not be empty")

    for it in items:
        if "price" not in it or "qty" not in it:
            raise ValueError("item must have price and qty")
        if it["price"] <= 0:
            raise ValueError("price must be positive")
        if it["qty"] <= 0:
            raise ValueError("qty must be positive")


def normalize_currency(currency):
    if currency is None:
        return DEFAULT_CURRENCY
    return currency


def calc_subtotal(items):
    subtotal = 0
    for it in items:
        subtotal += it["price"] * it["qty"]
    return subtotal


def calc_discount(subtotal, coupon):
    if coupon is None or coupon == "":
        return 0

    if coupon == "SAVE10":
        return int(subtotal * SAVE10_RATE)

    if coupon == "SAVE20":
        if subtotal >= SAVE20_THRESHOLD:
            return int(subtotal * SAVE20_RATE_HIGH)
        return int(subtotal * SAVE20_RATE_LOW)

    if coupon == "VIP":
        discount = VIP_DISCOUNT_HIGH
        if subtotal < VIP_THRESHOLD:
            discount = VIP_DISCOUNT_LOW
        return discount

    raise ValueError("unknown coupon")


def apply_discount(subtotal, discount):
    total_after_discount = subtotal - discount
    if total_after_discount < 0:
        total_after_discount = 0
    return total_after_discount


def calc_tax(total_after_discount):
    return int(total_after_discount * TAX_RATE)


def build_order_id(user_id, items_count):
    return str(user_id) + "-" + str(items_count) + "-" + "X"


def process_checkout(request):
    user_id, items, coupon, currency = parse_request(request)
    validate_user_id(user_id)
    validate_items(items)
    currency = normalize_currency(currency)
    subtotal = calc_subtotal(items)
    discount = calc_discount(subtotal, coupon)
    total_after_discount = apply_discount(subtotal, discount)
    tax = calc_tax(total_after_discount)
    total = total_after_discount + tax

    order_id = build_order_id(user_id, len(items))

    return {
        "order_id": order_id,
        "user_id": user_id,
        "currency": currency,
        "subtotal": subtotal,
        "discount": discount,
        "tax": tax,
        "total": total,
        "items_count": len(items),
    }

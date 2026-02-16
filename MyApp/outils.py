from decimal import Decimal

COMMISSION_RATE = Decimal('0.10')  # 10%

def Calculate_commission(price):
    commission = price * COMMISSION_RATE
    seller_amount = price - commission
    return commission, seller_amount

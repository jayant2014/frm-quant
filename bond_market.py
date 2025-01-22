class ZeroCouponBond:

    def __init__(self, principal, maturity, interest_rate):
        # Face value
        self.principal = principal
        # Date to maturity
        self.maturity = maturity
        # Market interest rate (discounting)
        self.interest_rate = interest_rate / 100

    def present_value(self, x, n):
        return x / (1+self.interest_rate)**n

    def calculate_price(self):
        return self.present_value(self.principal, self.maturity)

class CouponBond:

    def __init__(self, principal, rate, maturity, interest_rate):
        # Face value
        self.principal = principal
        # Coupon rate
        self.rate = rate / 100
        # Date to maturity
        self.maturity = maturity
        # Interest rate
        self.interest_rate = interest_rate / 100

    def present_value(self, x, n):
        return x / (1+self.interest_rate)**n

    def calculate_price(self):
        price = 0

        # Discount the coupon payments
        for t in range(1, self.maturity+1):
            price = price + self.present_value(self.principal * self.rate, t)

        # Discount principal
        price = price + self.present_value(self.principal, self.maturity)

        return price

if __name__ == '__main__':

    bond = ZeroCouponBond(100, 2, 4)
    print("Price of the zero coupon bond: %.2f" % bond.calculate_price())

    bond = CouponBond(100, 10, 3, 4)
    print("Price of the coupon bond: %.2f" % bond.calculate_price())

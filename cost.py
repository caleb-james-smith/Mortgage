# cost.py
# compare mortgage and renting costs
# mortgage monthly payment equation: https://mathworld.wolfram.com/Mortgage.html
# mortgage amortization example: https://www.rocketmortgage.com/learn/mortgage-amortization

class Mortgage:
    def __init__(self, num_years, purchase_price, down_payment, closing_costs, annual_interest_rate, annual_prop_tax_rate, annual_insurance_rate, monthly_hoa, selling_price, selling_realtor_fee_rate):
        self.num_years                  = num_years
        self.num_months                 = 12 * num_years
        self.purchase_price             = purchase_price
        self.down_payment               = down_payment
        self.closing_costs              = closing_costs
        self.annual_interest_rate       = annual_interest_rate
        self.monthly_interest_rate      = self.annual_interest_rate / 12
        self.monthly_hoa                = monthly_hoa
        self.selling_price              = selling_price
        self.selling_realtor_fee_rate   = selling_realtor_fee_rate
        self.selling_realtor_fee        = self.selling_realtor_fee_rate * self.selling_price
        self.monthly_tax                = self.purchase_price * annual_prop_tax_rate  / 12 
        self.monthly_insurance          = self.purchase_price * annual_insurance_rate / 12  
        self.total_cost                 = self.down_payment + self.closing_costs
        self.total_mortgage_cost        = 0
        self.setLoan(self.purchase_price - self.down_payment)
        self.setAmountOwed(self.loan)
        self.setMonthlyMortgagePayment(self.calcMonthlyMortgagePayment())
        self.setMonthlyPayment(self.monthly_mortgage_payment + self.monthly_tax + self.monthly_insurance + self.monthly_hoa)

    def getPurchasePrice(self):
        return self.purchase_price
    
    def getDownPayment(self):
        return self.down_payment
    
    def setLoan(self, loan):
        self.loan = loan

    def getLoan(self):
        return self.loan

    def setAmountOwed(self, amount):
        self.amount_owed = amount

    def getAmountOwed(self):
        return self.amount_owed
    
    def setMonthlyMortgagePayment(self, monthly_mortgage_payment):
        self.monthly_mortgage_payment = monthly_mortgage_payment
    
    def getMonthlyMortgagePayment(self):
        return self.monthly_mortgage_payment

    def setMonthlyPayment(self, monthly_payment):
        self.monthly_payment = monthly_payment

    def getMonthlyPayment(self):
        return self.monthly_payment

    def calcMonthlyMortgagePayment(self):
        x       = (1 + self.monthly_interest_rate) ** self.num_months
        payment = self.loan * self.monthly_interest_rate * (x / (x - 1))
        return payment

    def calcAmountOwedAfterMonth(self):
        amount = self.amount_owed * (1 + self.monthly_interest_rate) - self.monthly_mortgage_payment 
        return amount

    def calcEquity(self):
        equity = self.purchase_price - self.amount_owed
        return equity

    def calcPaidForPrincipal(self):
        amount = self.calcEquity() - self.getDownPayment()
        return amount

    def calcPaidForInterest(self):
        amount = self.getMortgageCost() - self.calcPaidForPrincipal()
        return amount

    def calcAmountEarnedInSale(self):
        amount = self.selling_price - self.amount_owed - self.selling_realtor_fee 
        return amount

    def addToMortgageCost(self, amount):
        self.total_mortgage_cost += amount

    def getMortgageCost(self):
        return self.total_mortgage_cost

    def addToTotalCost(self, amount):
        self.total_cost += amount

    def setTotalCost(self, amount):
        self.total_cost = amount

    def getTotalCost(self):
        return self.total_cost

    def setCostAfterSale(self, amount):
        self.cost_after_sale = amount

    def getCostAfterSale(self):
        return self.cost_after_sale

    def printInfo(self):
        print(50*"-")
        print("Purchase price: {0:.2f}".format(self.purchase_price))
        print("Closing costs: {0:.2f}".format(self.closing_costs))
        print("Down payment: {0:.2f}".format(self.down_payment))
        print("Loan: {0:.2f}".format(self.loan))
        print("Selling price: {0:.2f}".format(self.selling_price))
        print("Number of years: {0}".format(self.num_years))
        print("Annual interest rate: {0}".format(self.annual_interest_rate))
        print("Mortgage monthly payment: {0:.2f}".format(self.monthly_mortgage_payment))
        print("Total monthly payment: {0:.2f}".format(self.monthly_payment))
        print(50*"-")

class Rent:
    def __init__(self, monthly_rent):
        self.total_cost   = 0
        self.setMonthlyRent(monthly_rent)
        self.setYearlyRent(12 * self.monthly_rent)

    def setMonthlyRent(self, monthly_rent):
        self.monthly_rent = monthly_rent

    def getMonthlyRent(self):
        return self.monthly_rent
    
    def setYearlyRent(self, yearly_rent):
        self.yearly_rent = yearly_rent

    def getYearlyRent(self):
        return self.yearly_rent

    def addToTotalCost(self, amount):
        self.total_cost += amount

    def setTotalCost(self, amount):
        self.total_cost = amount
    
    def getTotalCost(self):
        return self.total_cost


def main():
    nYears = 15
    r = Rent(monthly_rent=1000.00)
    m = Mortgage(
                    num_years=nYears,
                    purchase_price=150000.00,
                    down_payment=30000.00,
                    closing_costs=5000.0,
                    annual_interest_rate=0.02440,
                    annual_prop_tax_rate=0.0133,
                    annual_insurance_rate=0.0042,
                    monthly_hoa=0.00,
                    selling_price=160000.00,
                    selling_realtor_fee_rate=0.06
                )
    m.printInfo()
    for i in range(1, nYears + 1):
        r.addToTotalCost(r.getYearlyRent())
        print("year {0}, rent cost: {1:.2f}".format(i, r.getTotalCost()))
    # reset rent cost to calculate for each year
    r.setTotalCost(0)
    for i in range(1, nYears + 1):
        r.addToTotalCost(r.getYearlyRent())
        for j in range(1, 13):
            m.setAmountOwed(m.calcAmountOwedAfterMonth())
            m.addToMortgageCost(m.getMonthlyMortgagePayment())
            m.addToTotalCost(m.getMonthlyPayment())
            m.setCostAfterSale(m.getTotalCost() - m.calcAmountEarnedInSale())
        #print("year {0}, owed: {1:.2f}, equity: {2:.2f}, paid principal: {3:.2f}, paid interest: {4:.2f}, mortgage cost: {5:.2f}".format(i, m.getAmountOwed(), m.calcEquity(), m.calcPaidForPrincipal(), m.calcPaidForInterest(), m.getMortgageCost()))
        #print("year {0}, owed: {1:.2f}, equity: {2:.2f}, buy cost before sale: {3:.2f}, buy cost after sale: {4:.2f}".format(i, m.getAmountOwed(), m.calcEquity(), m.getTotalCost(), m.getTotalCost() - m.calcAmountEarnedInSale()))
        print("year {0}, rent cost: {1:.2f}, buy cost after sale: {2:.2f}, cost diff (rent - buy): {3:.2f}".format(i, r.getTotalCost(), m.getCostAfterSale(), r.getTotalCost() - m.getCostAfterSale()))

if __name__ == "__main__":
    main()


import pandas as pd

# Constants & Assumptions
NUM_SEGMENTS = 3 * 4 * 12          # 3 roundtrips monthly × 4 segments each
SEAT_FEE = 15                      # $ per segment if not waived
INCIDENTAL_SPEND = 0               # $ spent on upgrades, Wi-Fi, food, etc.
LOUNGE_VISITS = 24                 # number of lounge visits per year
LOUNGE_VISIT_VALUE = 18            # $ saved per lounge visit
ANNUAL_FLIGHT_SPEND = 36 * 400     # $ charged to card on flights annually
ANNUAL_OTHER_SPEND = 2000*12          # $ charged to card on non-flight purchases

# Card definitions with separate earn rates
cards = [
    {
        'name': 'Citi AAdvantage MileUp',
        'af': 0,
        'signup_bonus': 15000,
        'point_value': 0.012,
        'inc_credit': 0,
        'seat_waiver': False,
        'lounge_access': False,
        'flight_rate': 2,
        'other_rate': 1
    },
    {
        'name': 'Barclays Aviator Red',
        'af': 95,
        'signup_bonus': 60000,
        'point_value': 0.012,
        'inc_credit': 0,
        'seat_waiver': False,
        'lounge_access': False,
        'flight_rate': 2,
        'other_rate': 1
    },
    {
        'name': 'Citi AAdvantage Platinum Select',
        'af': 95,
        'signup_bonus': 50000,
        'point_value': 0.012,
        'inc_credit': 0,
        'seat_waiver': True,
        'lounge_access': False,
        'flight_rate': 2,
        'other_rate': 1
    },
    {
        'name': 'Capital One Venture',
        'af': 95,
        'signup_bonus': 75000,
        'point_value': 0.010,
        'inc_credit': 0,
        'seat_waiver': False,
        'lounge_access': False,
        'flight_rate': 2,
        'other_rate': 2
    },
    {
        'name': 'Chase Sapphire Preferred',
        'af': 95,
        'signup_bonus': 60000,
        'point_value': 0.015,
        'inc_credit': 0,
        'seat_waiver': False,
        'lounge_access': False,
        'flight_rate': 2,
        'other_rate': 1
    },
    {
        'name': 'Chase Sapphire Reserve',
        'af': 550,
        'signup_bonus': 60000,
        'point_value': 0.015,
        'inc_credit': 300,
        'seat_waiver': False,
        'lounge_access': True,
        'flight_rate': 3,
        'other_rate': 1
    },
    {
        'name': 'Capital One Venture X',
        'af': 395,
        'signup_bonus': 75000,
        'point_value': 0.010,
        'inc_credit': 300,
        'seat_waiver': False,
        'lounge_access': True,
        'flight_rate': 5,
        'other_rate': 2
    },
    {
        'name': 'Amex Platinum',
        'af': 695,
        'signup_bonus': 80000,
        'point_value': 0.017,
        'inc_credit': 200,
        'seat_waiver': False,
        'lounge_access': True,
        'flight_rate': 5,
        'other_rate': 1
    },
    {
        'name': 'Citi AAdvantage Executive',
        'af': 595+175,
        'signup_bonus': 100000,
        'point_value': 0.012,
        'inc_credit': 0,
        'seat_waiver': True,
        'lounge_access': True,
        'flight_rate': 4,
        'other_rate': 1
    }
]

# Calculation
results = []
for c in cards:
    signup_value = c['signup_bonus'] * c['point_value']
    seat_value = NUM_SEGMENTS * SEAT_FEE if c['seat_waiver'] else 0
    inc_value = min(INCIDENTAL_SPEND, c['inc_credit'])
    lounge_value = LOUNGE_VISITS * LOUNGE_VISIT_VALUE if c['lounge_access'] else 0
    flight_earnings = ANNUAL_FLIGHT_SPEND * c['flight_rate'] * c['point_value']
    other_earnings = ANNUAL_OTHER_SPEND * c['other_rate'] * c['point_value']
    gross_value = signup_value + seat_value + inc_value + lounge_value + flight_earnings + other_earnings
    net_value = gross_value - c['af']
    
    if c['name'] == 'Citi AAdvantage Executive':

        #print individual values for debugging
        print(f"Card: {c['name']}")
        print(f"Signup Bonus Value: {signup_value}")
        print(f"Seat Value: {seat_value}")
        print(f"Incidental Credit Value: {inc_value}")
        print(f"Lounge Value: {lounge_value}")
        print(f"Flight Earnings Value: {flight_earnings}")
        print(f"Other Earnings Value: {other_earnings}")
        print(f"Gross Value: {gross_value}")
        print(f"Net Value: {net_value}")
        print(f"Annual Fee: {c['af']}")

    # repeat for 2nd year
    gross_value_2 = seat_value + inc_value + lounge_value + flight_earnings + other_earnings
    net_value_2 = gross_value_2 - c['af']

    #2 year total
    total_value = net_value + net_value_2

    #n year total
    n = 15
    n_total_value = net_value * n + (gross_value_2 - c['af']) * (n - 1)


    results.append({
        'Card': c['name'],
        'Annual Fee ($)': c['af'],
        'Gross First-Year Value ($)': gross_value,
        'Net First-Year Value ($)': net_value,
        'Gross Second-Year Value ($)': gross_value_2,
        'Net Second-Year Value ($)': net_value_2,
        '2-Year Net Value ($)': total_value
    })

df = pd.DataFrame(results).sort_values(by='2-Year Net Value ($)', ascending=False)
print(df.to_string(index=False))

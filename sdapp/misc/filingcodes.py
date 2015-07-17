
# Source url:
# https://www.sec.gov/about/forms/form4data.pdf
filingcodes = {
    # General Transaction Codes
    "P": "Discretionary purchase",
    "S": "Discretionary sale",
    "V": "Early reported transaction",
    # Rule 16b-3 Transaction Codes
    "A": "Grant",
    "D": "Disposition to the issuer",
    "F": "Payment of excercise price or tax by delivery",
    "I": "Employee benefit plan transaction",
    "M": "Conversion",
    # Derivative Securities Codes (Except for transactions
    # exempted pursuant to Rule 16b-3)
    "C": "Conversion",
    "E": "Expiration of short position",
    "H": "Expiration of long position",  # with value received
    "O": "Exercise of out-of-the-money derivative",
    "X": "Exercise of in- or at-the-money derivative",
    # Other Section 16(b) Exempt Transaction and Small Acquisition
    # Codes (except for Rule 16b-3 codes above)
    "G": "Gift",
    "L": "Small acquisition",
    "W": "Inheritance transaction",
    "Z": "Voting trust transaction",
    # Other Transaction Codes
    "J": "Other transaction",
    "K": "Swap transaction",
    "U": "Sale in tender offer",
}

acq_disp_codes = {
    "A": "Acquisition",
    "P": "Disposition",
}

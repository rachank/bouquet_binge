import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('bouquet_binge')


def obtain_sales_info():
    """
    This function asks the user to enter 7 numbers, sparated by commas 
    of bouquet sales for the previous week. 
    It continues to ask until the numbers are valid and returns a list
    of 7 integers.
    """

    # Variable to track if data is valid 
    valid_info = False

    # Loop until data is valid
    while not valid_info:
        print("Please enter bouquet sales data from the last week of sales.")
        print("Data order: Roses, Orchids, Lilies, Carnations, Hydrandeas, Mums, and Seasonal.")
        print("Example: 20,30,20,10,20,30,25\n")

        # Get users input
        user_str = input("Enter The Weekly Data Here:\n")

        # Convert the string to a list split with commas
        sales_info = user_str.split(",")

        # Validate if the input contains 7 values.
        if len(sales_info) != 7:
            print("Error. Please enter exactly 7 numbers seperated by commas.")
            print(f"You entered {len(sales_info)} values.")
            continue

        # Check that all values are integers by iterating over each value.
        all_values = True
        for value in sales_info:
            try:
                int(value)
            except ValueError:
                all_values = False
                print(f"Error: '{value}' is not a valid integer.")

        # If all values are integers, then proceed.
        if all_values:
            print("Sales Information is Valid. Thanks!")
            valid_info = True

    # Convert values to integers
    sales_info = [int(value) for value in sales_info]

    print("Sales data:", sales_info)
    
    return sales_info

    
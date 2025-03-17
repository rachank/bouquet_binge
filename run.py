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
   
    while True:
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
        
    # Convert values to integers.
    sales_info = [int(value) for value in sales_info]

    print("Sales data:", sales_info)

    return sales_info


def update_sales_worksheet(info):
    """
    Update sales worksheet by adding new row according to the list data given.
    """
    print("Updating Sales Worksheet....\n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(info)
    print("Sales Worksheet has Updated Successfully!\n")


def update_excess_worksheet(info):
    """
    Update excess worksheet by adding new row according to the list data given.
    """
    print("Updating Excess Worksheet...\n")
    excess_worksheet = SHEET.worksheet("excess")
    surplus_worksheet.append_row(info)
    print("Excess Worksheet Updated successfully!\n")


def calc_excess_info(sales_row):
    """
    This compares the sales with the inventory and then calculates the excess or short amount for each bouquet type.
    The excess is evaluated as the number of sales subtracted from the inventory.
    * A Negative excess points to the requirement of additional inventory made that week.
    * A Positive excess results in the number of bouquets that were thrown away.
    """
    # Let the user know the calculation is starting.
    print("Determining Excess data...\n")

    # Get Values from Inventory Worksheet.
    inventory = SHEET.worksheet("inventory").get_all_info()

    # Get last row of stock data
    inventory_row = inventory[-1]

    # List to store excess calculation
    excess_info = []

    # Loop through each value in inventory & sales rows
    for i in range(len(inventory_row)):

        # Convert inventory to integer
        inventory_value = int(inventory_row[i])

        # Get sales value from same row
        sales_value = sales_row[i]

        # Calculate excess
        excess = inventory_value - sales_value

        # Add new excess values to list
        excess_info.append(excess)

    return excess_info







print("Welcome to the Bouquet Binge Flower Shop Inventory Information") 





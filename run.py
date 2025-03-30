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
        print("Data order: Roses, Orchids, Lilies, Carnations, Hydrangeas, Mums, and Seasonal.")
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
            break
        
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

        # Note: try/except is not necessary because inventory is already a validated 
        # integer from above.
        inventory_value = int(inventory_row[i])

        # Get sales value from same row
        sales_value = sales_row[i]

        # Calculate excess
        excess = inventory_value - sales_value

        # Add new excess values to list
        excess_info.append(excess)

    return excess_info


def get_latest_sales_info():
    """
    Retreives the lastest of 5 weeks of Bouquet sales from the spreadsheet.
    Returned as a list of lists.
    """
    # Access sales worksheet
    sales_sheet = SHEET.worksheet("sales")

    # Empty list to store last 5 entries
    last_5_entries = []

    # Loop through columns 1-7
    for col_index in range(1,8):
        
        # Get current column values
        column_info = sales_sheet.col_values(col_index)

        last_5 = column_info[2:]

        # Add the last 5 values to list
        last_5_entries.append(last_5)

    return last_5_entries


def calc_inventory_info(info):
    """
    This calculates the average inventory for each item type, 
    adding 15% for additional available inventory
    """
    # Informing user calculations begin
    print("Calcualting Inventory Information...\n")

    # Loop through each column in inventory, convert values to integers
    # And calculate average
    for colum in info:
        int_column = sum(int_column) / len(int_column)
        average = sum(int_column) / len(int_column)

        # Increase average inventory value by 15%.
        inventory_num = average * 1.15

        # Round stock number to nearest whole number, add to list
        new_inventory_data.append(round(inventory_num)) 

    return new_inventory_data

def main():
    """"
    A function to run all of the program functions
    """
    sales_info = obtain_sales_info()
    update_sales_worksheet(sales_info)
    new_excess_info = calc_excess_info(sales_info)
    update_excess_worksheet(new_excess_info)
    latest_sales = get_latest_sales_info()
    inventory_info = calc_inventory_info(latest_sales)
    update_worksheet(inventory_info, "inventory")


print("Welcome to the Bouquet Binge Flower Shop Inventory Information") 
main()



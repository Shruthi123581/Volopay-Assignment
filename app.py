import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)

# Read the dataset into a pandas DataFrame
dataset_path = 'https://drive.google.com/file/d/1YfhCPZbofAekMy9tPH_7ZXChVX8w_OUF/view?usp=sharing.csv'  
df = pd.read_csv(dataset_path)

@app.route('/api/total_items', methods=['GET'])
def total_items_sold():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    department = request.args.get('department')

    # Filter the dataset based on the specified date range and department
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date) & (df['department'] == department)]

    # Calculate the total items sold
    total_items = filtered_df['quantity'].sum()

    # Return the total count of items as the API response
    return jsonify({'total_items': total_items})

@app.route('/api/nth_most_total_item', methods=['GET'])
def nth_most_total_item():
    item_by = request.args.get('item_by')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    n = int(request.args.get('n'))

    # Filter the dataset based on the specified date range
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    if item_by == 'quantity':
        # Group the dataset by item name and calculate the total quantity sold for each item
        item_quantity = filtered_df.groupby('item_name')['quantity'].sum().reset_index()

        # Sort the items by quantity in descending order
        sorted_items = item_quantity.sort_values('quantity', ascending=False)

        # Get the name of the nth most sold item in terms of quantity
        nth_item = sorted_items.iloc[n-1]['item_name']
    elif item_by == 'price':
        # Group the dataset by item name and calculate the total price for each item
        item_price = filtered_df.groupby('item_name')['price'].sum().reset_index()

        # Sort the items by price in descending order
        sorted_items = item_price.sort_values('price', ascending=False)

        # Get the name of the nth most sold item in terms of price
        nth_item = sorted_items.iloc[n-1]['item_name']
    else:
        return jsonify({'error': 'Invalid item_by parameter'})

    # Return the name of the item as the API response
    return jsonify({'item_name': nth_item})

@app.route('/api/percentage_of_department_wise_sold_items', methods=['GET'])
def percentage_of_department_wise_sold_items():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Filter the dataset based on the specified date range
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]

    # Calculate the percentage of sold items for each department
    department_wise_percentage = filtered_df.groupby('department')['quantity'].sum() / filtered_df['quantity'].sum() * 100
    department_wise_percentage = department_wise_percentage.reset_index().rename(columns={'quantity': 'percentage'})

    # Return the department-wise percentage as the API response
    return jsonify(department_wise_percentage.to_dict(orient='records'))

@app.route('/api/monthly_sales', methods=['GET'])
def monthly_sales():
    product = request.args.get('product')
    year = int(request.args.get('year'))

    # Filter the dataset based on the specified product and year
    filtered_df = df[(df['product'] == product) & (df['year'] == year)]

    # Calculate the monthly sales for the product
    monthly_sales = filtered_df.groupby('month')['sales'].sum().tolist()

    # Return the monthly sales as the API response
    return jsonify(monthly_sales)

if __name__ == '__main__':
    app.run()

from flask import Flask, render_template, request
from google.cloud import bigquery

app = Flask(__name__)

# Configure BigQuery client (replace with your project ID and dataset ID)
client = bigquery.Client(project='qwiklabs-gcp-03-24a1cd658bd5')
dataset_id = 'qwiklabs-gcp-03-24a1cd658bd5.customerdata'

@app.route('/')
def user_form():
    return render_template('user_form.html')

@app.route('/submit', methods=['POST'])
def submit_user_details():
    name = request.form['name']
    age = int(request.form['age'])  # Ensure integer conversion
    email = request.form['email']
    phone_number = request.form['phone_number']

    # Create a BigQuery table schema
    schema = [
        bigquery.SchemaField('name', 'STRING'),
        bigquery.SchemaField('age', 'INTEGER'),
        bigquery.SchemaField('email', 'STRING'),
        bigquery.SchemaField('phone_number', 'STRING')
    ]

    # Create a BigQuery table if it doesn't exist
    table_ref = client.dataset(dataset_id).table('user_details')
    table = bigquery.Table(table_ref, schema=schema)
    try:
        client.create_table(table)
        print('Table created successfully!')
    except Exception as e:
        print(f'Error creating table: {e}')

    # Insert user details into BigQuery
    rows_to_insert = [(name, age, email, phone_number)]
    errors = client.insert_rows(table_ref, rows_to_insert)

    if not errors:
        print('User details inserted successfully!')
    else:
        for err in errors:
            print(f'Error: {err}')

    return render_template('submission_result.html')

if __name__ == '__main__':
    app.run(debug=True)  # Set debug=False for production deployment

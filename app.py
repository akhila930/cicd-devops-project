import boto3
import pandas as pd
from flask import Flask, render_template_string
import io
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>User Analytics Dashboard</title>
    <style>
        body {
            font-family: Arial;
            margin: 40px;
            background: #f4f6f8;
        }
        h1 {
            color: #1F4E79;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 30px;
        }
        th {
            background: #1F4E79;
            color: white;
            padding: 10px;
        }
        td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        tr:nth-child(even) {
            background: #f2f2f2;
        }
    </style>
</head>
<body>
    <h1>User Analytics Dashboard</h1>
    <h2>Total Users: {{ total }}</h2>

    <h2>Age Distribution</h2>
    <table>
        <tr>
            <th>Age Group</th>
            <th>Count</th>
        </tr>
        {% for row in age_dist %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
        </tr>
        {% endfor %}
    </table>

    <h2>Occupation Grouping</h2>
    <table>
        <tr>
            <th>Occupation</th>
            <th>Count</th>
        </tr>
        {% for row in occ_group %}
        <tr>
            <td>{{ row[0] }}</td>
            <td>{{ row[1] }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route('/')
def index():
    s3 = boto3.client(
        's3',
        region_name=os.environ.get('AWS_REGION', 'us-east-1')
    )

    bucket = os.environ.get(
        'S3_BUCKET',
        'my-cicd-bucket-akhila-2026'
    )

    obj = s3.get_object(Bucket=bucket, Key='u.user')

    df = pd.read_csv(
        io.BytesIO(obj['Body'].read()),
        sep='|',
        header=None,
        names=['user_id', 'age', 'gender', 'occupation', 'zip_code']
    )

    total = len(df)

    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 18, 25, 35, 50, 100],
        labels=['<18', '18-25', '26-35', '36-50', '50+']
    )

    age_dist = (
        df['age_group']
        .value_counts()
        .sort_index()
        .reset_index()
        .values
        .tolist()
    )

    occ_group = (
        df['occupation']
        .value_counts()
        .reset_index()
        .values
        .tolist()
    )

    return render_template_string(
        HTML,
        total=total,
        age_dist=age_dist,
        occ_group=occ_group
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
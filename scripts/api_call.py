#!/usr/bin/env python3
# Yahoo Finance API - Cryptocurrency Raw Data Extraction

# Import required libraries
import pandas as pd
from datetime import datetime
import time
import json
import os
import http.client
import boto3
from botocore.exceptions import ClientError

# RapidAPI configuration
RAPIDAPI_KEY = os.environ.get('RAPIDAPI_KEY')  # Get API key from environment variable
RAPIDAPI_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"

# Cryptocurrency symbols (with Yahoo Finance suffix for crypto)
CRYPTO_SYMBOLS = {
    "BTC": "BTC-USD",
    "ETH": "ETH-USD", 
    "DOGE": "DOGE-USD"
}

# Time range (January 1, 2020 to current date)
START_DATE = datetime(2020, 1, 1)
END_DATE = datetime.now()

print(f"Data range: {START_DATE.strftime('%Y-%m-%d')} to {END_DATE.strftime('%Y-%m-%d')}")
print(f"API Host: {RAPIDAPI_HOST}")
print(f"Cryptocurrencies: {', '.join(CRYPTO_SYMBOLS.keys())}")

# Create directories for output
os.makedirs('data', exist_ok=True)
os.makedirs('raw_responses', exist_ok=True)

# Function for API data fetching
def get_historical_data(symbol, interval="1d", range_period="5y"):
    """
    Fetches historical price data for a cryptocurrency from Yahoo Finance via RapidAPI.
    
    Parameters:
    - symbol: The Yahoo Finance symbol for the cryptocurrency
    - interval: Time interval between data points (1d for daily)
    - range_period: How far back to get data (5y = 5 years)
    
    Returns:
    - DataFrame with historical price data
    - None if there was an error
    """
    try:
        print(f"Fetching {interval} data for {symbol} over {range_period}...")
        
        # Create connection to RapidAPI Yahoo Finance endpoint
        conn = http.client.HTTPSConnection("yh-finance.p.rapidapi.com")
        
        # Set headers with API key
        headers = {
            'X-RapidAPI-Key': RAPIDAPI_KEY,
            'X-RapidAPI-Host': RAPIDAPI_HOST
        }
        
        # Build the API endpoint with query parameters
        endpoint = f"/stock/v3/get-chart?interval={interval}&symbol={symbol}&range={range_period}"
        endpoint += "&includePrePost=false&useYfid=true&includeAdjustedClose=true&events=capitalGain,div,split"
        
        # Make the request
        print(f"Requesting: {endpoint}")
        conn.request("GET", endpoint, headers=headers)
        
        # Get the response
        res = conn.getresponse()
        
        # Check if response is successful
        if res.status != 200:
            print(f"Error: Received status code {res.status} for {symbol}")
            print(f"Response: {res.read().decode('utf-8')}")
            return None
        
        # Read and parse the response
        data_bytes = res.read()
        
        # Save raw response for debugging (optional)
        with open(f"raw_responses/{symbol}_{interval}_{range_period}.json", 'w') as f:
            json.dump(json.loads(data_bytes.decode('utf-8')), f, indent=2)
            
        # Parse the JSON data
        data = json.loads(data_bytes.decode('utf-8'))
        
        # Check for errors in the response
        if 'chart' in data and data['chart'].get('error'):
            print(f"API returned an error for {symbol}: {data['chart']['error']}")
            return None
            
        # Extract the relevant data from the response
        if 'chart' in data and 'result' in data['chart'] and len(data['chart']['result']) > 0:
            result = data['chart']['result'][0]
            
            # Get timestamps and convert to datetime
            timestamps = result.get('timestamp', [])
            if not timestamps:
                print(f"No timestamp data found for {symbol}")
                return None
                
            datetime_index = [datetime.fromtimestamp(ts) for ts in timestamps]
            
            # Extract price data
            indicators = result.get('indicators', {})
            quotes = indicators.get('quote', [{}])[0]
            
            # Create DataFrame
            df_data = {
                'date': datetime_index,
                'open': quotes.get('open', []),
                'high': quotes.get('high', []),
                'low': quotes.get('low', []),
                'close': quotes.get('close', []),
                'volume': quotes.get('volume', [])
            }
            
            # Create DataFrame
            df = pd.DataFrame(df_data)
            
            # Clean up any NaN values that might be in the data
            df = df.dropna(subset=['close'])
            
            # Set date as index
            df['date'] = pd.to_datetime(df['date'])
            
            print(f"Successfully retrieved {len(df)} data points for {symbol}")
            
            # Filter to data from Jan 2020 onwards
            filtered_df = df[df['date'] >= START_DATE]
            print(f"After filtering to {START_DATE.strftime('%Y-%m-%d')} onwards: {len(filtered_df)} data points")
            
            return filtered_df
        else:
            print(f"No data found for {symbol}")
            return None
            
    except Exception as e:
        print(f"Unexpected error processing data for {symbol}: {e}")
        return None

# Save raw data to CSV
def save_raw_data_to_csv(df, crypto_name):
    """
    Save raw price data to CSV file
    
    Parameters:
    - df: DataFrame with price data to save
    - crypto_name: Name of the cryptocurrency
    
    Returns:
    - Filename where data was saved
    """
    if df is None or df.empty:
        print(f"No raw data to save for {crypto_name}")
        return None
    
    # Format filename
    filename = f"data/{crypto_name}_raw_daily.csv"
    
    # Keep all price columns
    columns_to_keep = ['date', 'open', 'high', 'low', 'close', 'volume']
        
    # Save to CSV
    df[columns_to_keep].to_csv(filename, index=False)
    print(f"Saved raw daily data for {crypto_name} to {filename}")
    return filename

# Upload CSV files to Amazon S3
def upload_to_s3(file_path, bucket_name, s3_key=None):
    """
    Upload a file to an S3 bucket
    
    Parameters:
    - file_path: Path to the file to upload
    - bucket_name: Name of the S3 bucket
    - s3_key: S3 object key. If not specified, the filename will be used
    
    Returns:
    - True if file was uploaded, False otherwise
    """
    # If S3 key is not specified, use the filename
    if s3_key is None:
        s3_key = os.path.basename(file_path)
    
    # Get AWS credentials from environment variables
    aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
    aws_region = os.environ.get('AWS_REGION', 'us-east-1')
    
    # Create the S3 client using the credentials from environment variables
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    
    try:
        print(f"Uploading {file_path} to s3://{bucket_name}/{s3_key}...")
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Successfully uploaded {file_path} to S3")
        return True
    except ClientError as e:
        print(f"Error uploading {file_path} to S3: {e}")
        return False

def main():
    # Process each cryptocurrency
    for crypto_name, symbol in CRYPTO_SYMBOLS.items():
        print(f"\nProcessing data for {crypto_name} ({symbol})...")
        
        # Always fetch fresh data
        daily_data = get_historical_data(symbol, interval="1d", range_period="5y")
        
        if daily_data is not None:
            # Save raw daily data (will overwrite existing file)
            save_raw_data_to_csv(daily_data, crypto_name)
        
        # Pause between API calls to avoid rate limiting
        time.sleep(2)

    # S3 bucket name from environment variable
    S3_BUCKET_NAME = os.environ.get('AWS_S3_BUCKET_NAME', 'damg7245-crypto')
    S3_PREFIX = "raw_data"  # Optional prefix for organizing files in S3

    # Upload the files to S3 (will replace existing files)
    for crypto_name in CRYPTO_SYMBOLS.keys():
        file_name = f"{crypto_name}_raw_daily.csv"
        file_path = os.path.join("data", file_name)
        
        if os.path.exists(file_path):
            # Create S3 key with optional prefix
            s3_key = f"{S3_PREFIX}/{file_name}" if S3_PREFIX else file_name
            
            # Upload file (will replace if it exists in S3)
            upload_to_s3(file_path, S3_BUCKET_NAME, s3_key)
        else:
            print(f"Warning: Required file {file_path} not found")
    
    print("\nS3 update complete! All files have been replaced with fresh data.")

if __name__ == "__main__":
    main()
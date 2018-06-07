import boto3

url = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com'

# production v
# url = 'https://mturk-requester.us-east-1.amazonaws.com'

client = boto3.client('mturk', endpoint_url = url)

print(client.get_account_balance()['AvailableBalance'])

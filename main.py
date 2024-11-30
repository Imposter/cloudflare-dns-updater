import os
import time
import httpx
import requests
from dotenv import load_dotenv
from cloudflare import Cloudflare, DefaultHttpxClient

load_dotenv()

api_email=os.getenv('CLOUDFLARE_EMAIL')
api_key=os.getenv('CLOUDFLARE_API_KEY')

client = Cloudflare(
	api_email=api_email,
	api_key=api_key,
	http_client=DefaultHttpxClient(
		transport=httpx.HTTPTransport(local_address='0.0.0.0')
	)
)

zone_id = os.getenv('CLOUDFLARE_ZONE_ID')
records = (os.getenv('CLOUDFLARE_DNS_RECORDS') or "").split(',')

while True:
	try:
		current_ip = requests.get('https://api.ipify.org').text
	except requests.exceptions.RequestException as e:
		print('Error getting current IP:', e)
		continue

	for record in records:
		record_details = record.split(':')
		if len(record_details) != 2:
			print('Invalid record format:', record)
			continue

		(record_type, record_name) = record_details
		try:
			dns_records = client.dns.records.list(zone_id=zone_id)
		except Exception as e:
			print('Error getting DNS records:', e)
			continue

		for dns_record in dns_records:
			if dns_record.type == record_type and dns_record.name == record_name:
				if dns_record.content == current_ip:
					print(f'{record} is already up to date')
					continue

				print(f'Updating {record} from {dns_record.content} to {current_ip}')
				try:
					client.dns.records.update(dns_record_id=dns_record.id, zone_id=zone_id, content=current_ip, name=record_name, type=record_type)
				except Exception as e:
					print('Error updating DNS record:', e)

				print(f'Successfully updated {record}')
				break

	time.sleep(int(os.getenv('CLOUDFLARE_UPDATE_INTERVAL', 60) or 300))
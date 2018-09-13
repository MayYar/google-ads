# Import appropriate modules from the client library.
import tempfile

from googleads import dfp
from googleads import errors

from datetime import date, timedelta, datetime
import sys


def main(client):
	# Initialize appropriate service.
	report_service = client.GetService('ReportService', version='v201805')

	# Initialize a DataDownloader.
	report_downloader = client.GetDataDownloader(version='v201805')

	if len(sys.argv) == 3:
		report_job = {
		'reportQuery': {
						'dimensions': [
							'AD_EXCHANGE_TRANSACTION_TYPE',
							'AD_EXCHANGE_TAG_NAME',
							'AD_EXCHANGE_DFP_AD_UNIT',
							'DATE'
						],
						'adUnitView': 'TOP_LEVEL',
						'columns': [
							'AD_EXCHANGE_AD_REQUESTS',
							'AD_EXCHANGE_MATCHED_REQUESTS',
							'AD_EXCHANGE_CLICKS',
							'AD_EXCHANGE_ESTIMATED_REVENUE',
							'AD_EXCHANGE_IMPRESSIONS',
							'AD_EXCHANGE_AD_ECPM'
						],
						'dimensionAttributes': [],
						'customFieldIds': [],
						'contentMetadataKeyHierarchyCustomTargetingKeyIds': [],
						'dateRangeType': 'CUSTOM_DATE',
						'startDate': datetime.strptime(sys.argv[1], '%Y-%m-%d').date(),
						'endDate': datetime.strptime(sys.argv[2], '%Y-%m-%d').date(),
						'statement': None,
						'includeZeroSalesRows': False,
						'adxReportCurrency': 'USD',
						'timeZoneType': 'PUBLISHER'
				}
	}
	elif len(sys.argv) == 1:
		# Set the start and end dates of the report to run (past 14 days).
		end_date = datetime.now().date()
		start_date = end_date - timedelta(days=14)
		
		report_job = {
			'reportQuery': {
							'dimensions': [
								'AD_EXCHANGE_TRANSACTION_TYPE',
								'AD_EXCHANGE_TAG_NAME',
								'AD_EXCHANGE_DFP_AD_UNIT',
								'DATE'
							],
							'adUnitView': 'TOP_LEVEL',
							'columns': [
								'AD_EXCHANGE_AD_REQUESTS',
								'AD_EXCHANGE_MATCHED_REQUESTS',
								'AD_EXCHANGE_CLICKS',
								'AD_EXCHANGE_ESTIMATED_REVENUE',
								'AD_EXCHANGE_IMPRESSIONS',
								'AD_EXCHANGE_AD_ECPM'
							],
							'dimensionAttributes': [],
							'customFieldIds': [],
							'contentMetadataKeyHierarchyCustomTargetingKeyIds': [],
							'dateRangeType': 'CUSTOM_DATE',
							'startDate': start_date,
							'endDate': end_date,
							'statement': None,
							'includeZeroSalesRows': False,
							'adxReportCurrency': 'USD',
							'timeZoneType': 'PUBLISHER'
					}
		}
	else:
		print('input error')

	try:
		# Run the report and wait for it to finish.
		report_job_id = report_downloader.WaitForReport(report_job)
	except errors.DfpReportError as e:
		print ('Failed to generate report. Error was: %s' % e)
	# Change to your preferred export format.
	export_format = 'CSV_DUMP'

	# report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)
	report_file = open('output.csv.gz', 'wb')

	# Download report data.
	report_downloader.DownloadReportToFile(
		report_job_id, export_format, report_file)

	report_file.close()

	# Display results.
	print ('Report job with id "%s" downloaded to:\n%s' % (
		  report_job_id, report_file.name))
 
if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage('googleads.yaml')


  main(dfp_client)
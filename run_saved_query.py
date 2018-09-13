# Import appropriate modules from the client library.
import tempfile

from googleads import dfp
from googleads import errors

SAVED_QUERY_ID = '10153865716'


def main(client, saved_query_id):
  # Initialize appropriate service.
  report_service = client.GetService('ReportService', version='v201805')

  # Initialize a DataDownloader.
  report_downloader = client.GetDataDownloader(version='v201805')

  # Create statement object to filter for an order.
  statement = (dfp.StatementBuilder()
               .Where('id = :id')
               .WithBindVariable('id', int(saved_query_id))
               .Limit(1))

  response = report_service.getSavedQueriesByStatement(
      statement.ToStatement())
  print(response)
  if 'results' in response:
    saved_query = response['results'][0]

    if saved_query['isCompatibleWithApiVersion']:
      report_job = {}

      # Set report query and optionally modify it.
      report_job['reportQuery'] = saved_query['reportQuery']

      try:
        # Run the report and wait for it to finish.
        report_job_id = report_downloader.WaitForReport(report_job)
      except errors.DfpReportError as e:
        print ('Failed to generate report. Error was: %s' % e)
      # Change to your preferred export format.
      export_format = 'CSV_DUMP'

      report_file = tempfile.NamedTemporaryFile(suffix='.csv.gz', delete=False)

      # Download report data.
      report_downloader.DownloadReportToFile(
          report_job_id, export_format, report_file)

      report_file.close()

      # Display results.
      print ('Report job with id "%s" downloaded to:\n%s' % (
          report_job_id, report_file.name))
    else:
      print ('The query specified is not compatible with the API version.')


if __name__ == '__main__':
  # Initialize client object.
  dfp_client = dfp.DfpClient.LoadFromStorage('googleads.yaml')
  main(dfp_client, SAVED_QUERY_ID)
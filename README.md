# Policy Tag Manager with Google Cloud

This script integrates Google Cloud Data Catalog and BigQuery to apply policy tags to specific columns in BigQuery tables based on data retrieved from a CSV file stored in Google Cloud Storage (GCS).

## Overview

The script accomplishes the following:

1. **Retrieves policy tags**: It uses Google Cloud Data Catalog to retrieve the taxonomy and associated policy tags.
2. **Reads the CSV file from GCS**: It reads a file from a specified GCS bucket.
3. **Maps policy tags to columns**: Based on the contents of the CSV file, the script maps policy tags to specific columns in BigQuery tables.
4. **Applies policy tags**: The identified policy tags are applied to the respective columns in the specified BigQuery tables.

## Prerequisites

- **Google Cloud SDK**: Make sure you have the Google Cloud SDK installed and configured.
- **Python**: This script requires Python 3.x.

## Installation

Before running the script, ensure you have the necessary Python packages installed:

```bash
pip install -r requirements.txt
```

## Environment Variables

The script relies on the following environment variables:

- `project_id`: Your Google Cloud project ID.
- `taxonomy_id`: The ID of the taxonomy from Google Cloud Data Catalog.

## How to Run the Script

1. **Set up environment variables**:

   Ensure that the required environment variables are set. For example, you can set them in your shell session:

   ```bash
   export project_id="your-project-id"
   export taxonomy_id="your-taxonomy-id"
   ```

2. **Trigger the function**:

   The `main` function is designed to be triggered by an event in Google Cloud Storage. When a file is uploaded to the specified bucket, the script reads the file, retrieves the relevant policy tags, and applies them to the columns in the designated BigQuery tables.

3. **Testing Locally**:

   If you want to test the script locally:

   - Place a sample CSV file in the specified GCS bucket.
   - Trigger the function with a mock event.

## CSV File Format

The CSV file should have the following structure:

| column          | dataset         | table           | Etiqueta_seguridad |
|-----------------|-----------------|-----------------|--------------------|
| your_column_name| your_dataset_name| your_table_name  | your_security_label |

## Google Cloud Function Deployment

1. **Create a Google Cloud Function**:

   - Select the 1st generation Cloud Function.
   - Choose the appropriate region.
   - Set the event type to `On finalize` for the file in the specified bucket.

2. **Deploy the script**:

   - Deploy the `main.py` script as the main entry point.
   - Add necessary environment variables such as `tag_template_id` and `location`.

3. **Run the Function**:

   The function will be triggered when a file is uploaded to the specified GCS bucket. The function will read the file, map the columns to policy tags, and apply the tags to the BigQuery tables.

## Important Notes

- **Error Handling**: If the script encounters an error while retrieving the policy tag taxonomy or applying the tags, it will log the error.
- **Policy Tag Application**: If you attempt to apply the same policy tag multiple times to the same column, it will generate an error in the logs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
```

This `README.md` provides clear instructions on how to set up, run, and deploy your Python script. It includes details on prerequisites, environment variables, and how the script operates.
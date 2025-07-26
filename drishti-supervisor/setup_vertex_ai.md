# Google Cloud Vertex AI Setup Guide

This guide will help you set up Google Cloud Vertex AI authentication for the Graphiti knowledge graph system.

## Prerequisites

1. **Google Cloud Project**: You need an active Google Cloud project
2. **Vertex AI API Enabled**: The Vertex AI API must be enabled in your project
3. **Billing Account**: Your project must have a billing account attached

## Step 1: Enable Vertex AI API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Navigate to **APIs & Services > Library**
4. Search for "Vertex AI API" and enable it
5. Also enable "AI Platform API" if it's not already enabled

## Step 2: Authentication Setup

### Option A: Application Default Credentials (Recommended for Development)

1. **Install Google Cloud CLI**:
   ```bash
   # Windows (using installer)
   # Download from: https://cloud.google.com/sdk/docs/install
   
   # macOS
   brew install google-cloud-sdk
   
   # Linux
   curl https://sdk.cloud.google.com | bash
   ```

2. **Authenticate with Google Cloud**:
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   gcloud auth application-default login
   ```

3. **Verify authentication**:
   ```bash
   gcloud auth list
   gcloud config get-value project
   ```

### Option B: Service Account Key (Production)

1. **Create a Service Account**:
   - Go to **IAM & Admin > Service Accounts** in Google Cloud Console
   - Click **Create Service Account**
   - Give it a name like `graphiti-vertex-ai`
   - Grant it the following roles:
     - `Vertex AI User`
     - `AI Platform Developer` (if using older models)

2. **Create and Download Key**:
   - Click on your service account
   - Go to **Keys** tab
   - Click **Add Key > Create New Key**
   - Choose **JSON** format
   - Download the key file

3. **Set Environment Variable**:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
   ```

## Step 3: Environment Configuration

Create a `.env` file in `drishti-supervisor/` with:

```env
# Neo4j Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password

# Google Cloud Vertex AI Configuration (REQUIRED)
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1

# Model Configuration
LLM_CHOICE=gemini-2.5-flash
SMALL_LLM_CHOICE=gemini-1.5-flash
EMBEDDING_MODEL=text-embedding-004
VECTOR_DIMENSION=768

# Authentication (choose one):

# Option A: Service Account Key (if using Option B above)
GOOGLE_APPLICATION_CREDENTIALS=/path/to/your/service-account-key.json

# Option B: Application Default Credentials (no additional config needed if using Option A above)
# Just run: gcloud auth application-default login

# REMOVE THESE (not needed for Vertex AI):
# LLM_API_KEY=
# EMBEDDING_API_KEY=
# LLM_BASE_URL=
```

**Important**: Replace `your-project-id` with your actual Google Cloud project ID.

## Step 4: Find Your Project ID

If you don't know your project ID:

```bash
# List all projects
gcloud projects list

# Get current project
gcloud config get-value project
```

Or go to [Google Cloud Console](https://console.cloud.google.com/) and look at the project selector dropdown.

## Step 5: Choose a Region

Common regions for Vertex AI:
- `us-central1` (Iowa, USA)
- `us-east1` (South Carolina, USA)  
- `us-west1` (Oregon, USA)
- `europe-west1` (Belgium)
- `asia-southeast1` (Singapore)

Choose the region closest to you or where your data is located.

## Step 6: Test the Setup

1. **Test Google Cloud Authentication**:
   ```bash
   gcloud auth list
   gcloud config get-value project
   ```

2. **Test Vertex AI Access**:
   ```bash
   # Install the client library if not already installed
   pip install google-cloud-aiplatform

   # Test with Python
   python -c "
   from google.cloud import aiplatform
   aiplatform.init(project='YOUR_PROJECT_ID', location='us-central1')
   print('✅ Vertex AI connection successful!')
   "
   ```

3. **Test the Graphiti Setup**:
   ```bash
   cd drishti-supervisor
   python supervisor/sub_agents/tools/graph_builder.py
   ```

## Step 7: Troubleshooting

### Common Issues:

1. **"Default credentials not found"**:
   ```bash
   gcloud auth application-default login
   ```

2. **"Permission denied"**:
   - Check that Vertex AI API is enabled
   - Verify your service account has the correct roles
   - Make sure you're using the right project ID

3. **"Project not found"**:
   ```bash
   gcloud config set project YOUR_ACTUAL_PROJECT_ID
   ```

4. **"Region not supported"**:
   - Try a different region like `us-central1`
   - Check [Vertex AI regions](https://cloud.google.com/vertex-ai/docs/general/locations)

### Verification Commands:

```bash
# Check authentication
gcloud auth list

# Check project
gcloud config get-value project

# Check enabled APIs
gcloud services list --enabled | grep -E "(aiplatform|ml)"

# Test Vertex AI access
gcloud ai models list --region=us-central1
```

## Security Best Practices

1. **Never commit service account keys** to version control
2. **Use Application Default Credentials** for development
3. **Rotate service account keys** regularly in production
4. **Use least privilege principle** when assigning roles
5. **Store service account keys securely** (e.g., in secret managers)

## Cost Considerations

- Vertex AI charges per API call and token usage
- Monitor usage in Google Cloud Console > Billing
- Set up billing alerts to avoid unexpected charges
- Consider using quotas to limit usage

## Next Steps

Once configured, the system will use Google Cloud Vertex AI for:
- ✅ Gemini model inference (LLM calls)
- ✅ Text embeddings
- ✅ All authentication handled automatically
- ✅ Enterprise-grade security and compliance

Your knowledge graph system will now use Google Cloud's enterprise AI platform instead of the consumer Google AI Studio API. 
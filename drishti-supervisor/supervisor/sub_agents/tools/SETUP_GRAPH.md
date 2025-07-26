# Graph Database Setup Guide

This guide will help you resolve authentication and connection issues when running `graph_builder.py`.

## Authentication Options

You have **two options** for Google AI authentication:

### Option A: Google AI Studio (Simple API Key) 🔑
- **Easier setup**: Just need an API key
- **Good for**: Development, testing, personal projects
- **Follows**: This guide below

### Option B: Google Cloud Vertex AI (Enterprise OAuth2) 🏢
- **Enterprise-grade**: OAuth2 authentication
- **Good for**: Production, enterprise deployments
- **Follows**: See `setup_vertex_ai.md` instead

---

## Google AI Studio Setup (Option A)

### Step 1: Install and Start Neo4j Database

#### Option A: Using Docker (Recommended)
```bash
# Pull and run Neo4j
docker run -d \
  --name neo4j \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/mypassword123 \
  neo4j:latest

# Check if it's running
docker ps | grep neo4j
```

#### Option B: Neo4j Desktop
1. Download from https://neo4j.com/download/
2. Install and create a new database
3. Start the database
4. Note the connection details (usually bolt://localhost:7687)

### Step 2: Get Google AI Studio API Key

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Create a new API key
3. Copy the key for use in `.env` file

### Step 3: Create Environment File

Create a `.env` file in the `drishti-supervisor/` directory:

```env
# Neo4j Database Configuration (REQUIRED)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=mypassword123

# Google AI Studio Configuration (REQUIRED)
LLM_API_KEY=your_gemini_api_key_here
EMBEDDING_API_KEY=your_gemini_api_key_here
LLM_CHOICE=gemini-2.5-flash
SMALL_LLM_CHOICE=gemini-1.5-flash
EMBEDDING_MODEL=text-embedding-004
VECTOR_DIMENSION=768

# DO NOT SET THESE (they're for Vertex AI Option B):
# GOOGLE_CLOUD_PROJECT=
# GOOGLE_CLOUD_LOCATION=
# GOOGLE_APPLICATION_CREDENTIALS=
# LLM_BASE_URL=
# GENERATE_CONTENT_API=
```

**Replace:**
- `mypassword123` with your actual Neo4j password
- `your_gemini_api_key_here` with your actual Gemini API key from Google AI Studio

### Step 4: Test the Setup

Run the test script:
```bash
cd drishti-supervisor
python test_gemini_auth.py  # For Google AI Studio (Option A)
# OR
python test_vertex_ai.py    # For Vertex AI (Option B)
```

### Step 5: Run Graph Builder

Once the test passes, you can run the graph builder:
```bash
python supervisor/sub_agents/tools/graph_builder.py
```

## Common Issues and Solutions

### 1. "Unable to retrieve routing information"
- **Cause**: Neo4j is not running or not accessible
- **Solution**: Start Neo4j database (see Step 1)

### 2. "Authentication failed"
- **Cause**: Wrong Neo4j credentials
- **Solution**: Check NEO4J_USER and NEO4J_PASSWORD in .env

### 3. "API keys are not supported by this API"
- **Cause**: Mixing Google AI Studio API keys with Vertex AI endpoints
- **Solution**: 
  - For Google AI Studio: Use this guide and ensure no `GOOGLE_CLOUD_*` variables are set
  - For Vertex AI: Use `setup_vertex_ai.md` and remove `LLM_API_KEY`/`EMBEDDING_API_KEY`

### 4. "401 UNAUTHENTICATED" errors
- **Cause**: Invalid or missing API key
- **Solution**: Get a valid API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### 5. "ModuleNotFoundError"
- **Cause**: Missing dependencies
- **Solution**: Install requirements:
  ```bash
  pip install -r requirements.txt
  # or
  pip install graphiti-core python-dotenv
  ```

## Choosing Between Google AI Studio vs Vertex AI

| Feature | Google AI Studio | Vertex AI |
|---------|------------------|-----------|
| **Setup Complexity** | ✅ Simple (API key) | ⚠️ Complex (OAuth2) |
| **Authentication** | API Key | OAuth2/Service Account |
| **Good For** | Development, Testing | Production, Enterprise |
| **Cost** | Pay-per-use | Enterprise pricing |
| **Security** | Basic | Enterprise-grade |
| **Compliance** | Limited | Full compliance |
| **Regional Control** | Limited | Full control |

**Recommendation**: 
- 🔧 **Development**: Use Google AI Studio (this guide)
- 🏢 **Production**: Use Vertex AI (`setup_vertex_ai.md`)

## Verification Commands

```bash
# Check if Neo4j is running
curl http://localhost:7474

# Check environment variables
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('LLM_API_KEY:', 'SET' if os.getenv('LLM_API_KEY') else 'NOT SET')"

# Test connection
python test_gemini_auth.py
```

## Need Help?

If you're still having issues:
1. Check the test script output for specific error messages
2. Verify Neo4j is accessible at http://localhost:7474
3. Ensure your API key is valid and has appropriate permissions
4. For Vertex AI setup, see `setup_vertex_ai.md` 
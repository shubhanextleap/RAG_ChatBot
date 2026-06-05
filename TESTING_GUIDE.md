# Testing Guide - HDFC Mutual Fund FAQ Assistant

## Two UI Options Available

You now have two ways to test the RAG engine:

### Option 1: Web Browser UI (Recommended for Quick Testing)

**Features:**
- Modern, responsive chat interface
- Real-time message updates
- Debug mode to view backend information
- Fund scope filtering
- Example query shortcuts
- Chat history management

**How to Run:**

1. **Start the Flask API Backend:**
   ```powershell
   # Navigate to the project directory
   cd c:\RAG
   
   # Install dependencies (first time only)
   pip install -r requirements.txt
   
   # Run the API server
   python api.py
   ```
   The API will start at: `http://localhost:5000`

2. **Open the Web Interface:**
   - Open `index.html` in your web browser (double-click or drag to browser)
   - Or use: `http://localhost/path/to/index.html`
   - Or start a local server:
     ```powershell
     python -m http.server 8000
     # Then visit: http://localhost:8000/index.html
     ```

3. **Test the UI:**
   - Select a fund from the dropdown (optional)
   - Use example queries or type your own
   - Toggle Debug Mode to see backend details
   - Clear history as needed

**API Endpoints:**
- `GET /api/health` - Check if engine is running
- `POST /api/query` - Submit a question
  - Body: `{"question": "...", "fund": "optional-fund-id", "debug": true/false}`
- `GET /api/funds` - Get available funds list
- `POST /api/chat` - Chat with message history
  - Body: `{"message": "...", "history": [...], "fund": "optional"}`

---

### Option 2: Streamlit UI (Full-Featured)

**Features:**
- Integrated with RAGEngine directly
- Session state management
- Fund selection with sidebar
- Chat message history
- Compliance disclaimers
- Debug mode support

**How to Run:**

```powershell
# Navigate to the project directory
cd c:\RAG

# Install dependencies (first time only)
pip install -r requirements.txt

# Run Streamlit app
streamlit run app.py
```

The app will open automatically at: `http://localhost:8501`

---

## Comparison

| Feature | Web UI | Streamlit UI |
|---------|--------|-------------|
| Setup Time | ~1 minute | ~1 minute |
| Modern Design | ✅ | ✅ |
| API-Based | ✅ | ✗ |
| Direct Engine | ✗ | ✅ |
| Session Persistence | Manual | Automatic |
| Debug Mode | ✅ | ✅ |
| Example Queries | ✅ | ✅ |
| Responsive Design | ✅ | ✅ |

---

## Running Both Simultaneously

You can run both UIs at the same time for comprehensive testing:

```powershell
# Terminal 1 - Start Flask API
python api.py

# Terminal 2 - Start Streamlit
streamlit run app.py

# Terminal 3 (optional) - Local HTTP Server
python -m http.server 8000
```

Then:
- Visit `http://localhost:8000/index.html` for web UI (uses Flask API)
- Visit `http://localhost:8501` for Streamlit UI (uses RAGEngine directly)

---

## Troubleshooting

### Flask API not starting?
- Check if port 5000 is already in use: `netstat -ano | findstr :5000`
- Change port in `api.py`: `app.run(port=5001)`

### Web UI not connecting to API?
- Ensure Flask server is running
- Check browser console (F12) for CORS errors
- Update API URL in `index.html` if needed

### Streamlit not finding RAGEngine?
- Verify `engine.py` exists in the project root
- Check that imports in `app.py` are correct

---

## Features to Test

### 1. Query Processing
- [ ] Test with example queries
- [ ] Test with custom questions
- [ ] Verify responses are relevant

### 2. Fund Filtering
- [ ] Select different funds from dropdown
- [ ] Verify filtered results
- [ ] Test "All Funds" option

### 3. Debug Mode
- [ ] Enable debug in web UI
- [ ] View retrieval scores and metadata
- [ ] Check source document references

### 4. Chat History
- [ ] Send multiple messages
- [ ] Verify message order
- [ ] Clear history and start fresh

### 5. UI Responsiveness
- [ ] Resize browser window
- [ ] Test on mobile viewport
- [ ] Verify all buttons are clickable

---

## Customization

### To modify Web UI:
- Edit `index.html` for HTML structure
- Edit CSS in `<style>` tag for appearance
- Edit JavaScript in `<script>` tag for functionality

### To modify API:
- Edit `api.py` to add/modify endpoints
- Add more mock responses in `simulateBackendCall()`
- Implement real database integration

### To add more example queries:
In `index.html`, add buttons to the sidebar:
```html
<button class="query-btn" onclick="insertQuery('Your question here?')">Your question here?</button>
```

---

## Notes

- The web UI currently uses mock responses for demonstration
- Connect the web UI to actual API endpoints by updating the `simulateBackendCall()` function
- Both UIs will work better with a proper `requirements.txt` installed
- For production, configure CORS properly and use HTTPS

# Consent Management API Backend

A Flask-based REST API for managing user consent preferences with PostgreSQL database support.

## Features

- ✅ Complete CRUD operations for consent management
- ✅ Bulk consent operations
- ✅ Consent statistics and analytics
- ✅ User consent history tracking
- ✅ Comprehensive error handling
- ✅ PostgreSQL database support
- ✅ CORS enabled for frontend integration
- ✅ Health check endpoint
- ✅ Automated database setup and seeding

## 🚀 Quick Start (Windows PowerShell)

### **Prerequisites:**
- Python 3.7 or higher
- PostgreSQL database (or use SQLite for testing)
- `.env` file with database configuration

### **Step 1: Setup Environment**

**Navigate to backend directory:**
```powershell
cd C:\Users\YourUsername\Desktop\hackthon\backend
```

**Create virtual environment (if not exists):**
```powershell
python -m venv venv
```

**Activate virtual environment:**
```powershell
.\venv\Scripts\activate
```

**Install dependencies:**
```powershell
pip install -r requirements.txt
```

### **Step 2: Database Configuration**

**Create a `.env` file in the backend directory:**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/consent_db
```

**For SQLite testing (no setup required):**
```env
DATABASE_URL=sqlite:///test_consent.db
```

### **Step 3: Start the Server**

#### **Option A: SQLite Test Server (Recommended for Quick Start)**
```powershell
python test_local.py
```

**Expected Output:**
```
Starting Consent Management API (SQLite Test Version)
==================================================
Successfully added test purposes to the database!
Server will be available at: http://localhost:5001
API endpoints will be available at: http://localhost:5001/api
```

#### **Option B: Full Server with PostgreSQL**
```powershell
python start_server.py
```

**Expected Output:**
```
Consent Management API Startup
========================================
✓ Environment variables loaded
✓ Dependencies installed
✓ Database and tables created
✓ Initial data seeded
Starting Flask server...
Server will be available at: http://localhost:5000
API endpoints will be available at: http://localhost:5000/api
```

### **Step 4: Test the API**

**Open a NEW PowerShell window and test endpoints:**

```powershell
# Health check
curl http://localhost:5001/api/health

# Get all purposes
curl http://localhost:5001/api/purposes

# Test POST consent
curl -Method POST http://localhost:5001/api/consent -Body '{"user_id":"testuser123","purpose_id":1,"status":true}' -ContentType "application/json"

# Get user consents
curl http://localhost:5001/api/consent?user_id=testuser123

# Get statistics
curl http://localhost:5001/api/consent/stats
```

## 🔧 Troubleshooting

### **Common Issues:**

**Problem:** `python` command not found
```powershell
# Check Python installation
python --version

# If not found, install Python from python.org
# Or use py instead of python
py test_local.py
```

**Problem:** Virtual environment not activating
```powershell
# Make sure you're in the backend directory
cd C:\Users\YourUsername\Desktop\hackthon\backend

# Try different activation methods
.\venv\Scripts\activate
# OR
venv\Scripts\activate.bat
# OR
venv\Scripts\Activate.ps1
```

**Problem:** Dependencies installation failed
```powershell
# Upgrade pip first
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# If psycopg2 fails, use pg8000 (already in requirements)
```

**Problem:** Port already in use
```powershell
# Find process using the port
netstat -ano | findstr :5001
# OR
netstat -ano | findstr :5000

# Kill the process
taskkill /PID <PID> /F
```

**Problem:** Database connection failed
```powershell
# Check your .env file exists
ls .env

# For SQLite, no additional setup needed
# For PostgreSQL, make sure database is running and accessible
```

**Problem:** Module not found errors
```powershell
# Make sure virtual environment is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

## 📊 API Endpoints

### **Health Check:**
- `GET /api/health` - Check if the API is running

### **Purposes:**
- `GET /api/purposes` - Get all consent purposes
- `GET /api/purposes/{id}` - Get specific purpose

### **Consent Management:**
- `GET /api/consent?user_id={user_id}` - Get user consents
- `GET /api/consent/{id}` - Get specific consent record
- `POST /api/consent` - Create/update consent
- `POST /api/consent/bulk` - Bulk update consents
- `DELETE /api/consent/{id}` - Delete consent record
- `DELETE /api/consent/user/{user_id}` - Delete all user consents

### **Analytics:**
- `GET /api/consent/stats` - Get consent statistics
- `GET /api/consent/user/{user_id}/history` - Get user consent history
- `POST /api/consent/check` - Check consent status for multiple purposes

## 🗄️ Database Setup

### **SQLite (Default for Testing):**
- No setup required
- Database file created automatically
- Perfect for development and testing

### **PostgreSQL (Production):**
1. **Install PostgreSQL** or use AWS RDS
2. **Create database:**
   ```sql
   CREATE DATABASE consent_db;
   ```
3. **Update .env file:**
   ```env
   DATABASE_URL=postgresql://username:password@localhost:5432/consent_db
   ```

## 🧪 Testing

### **Run Test Script:**
```powershell
# Make sure server is running first
python test_api.py
```

### **Manual Testing with PowerShell:**
```powershell
# Test health endpoint
Invoke-RestMethod -Uri "http://localhost:5001/api/health" -Method Get

# Test purposes endpoint
Invoke-RestMethod -Uri "http://localhost:5001/api/purposes" -Method Get

# Test consent creation
$body = @{
    user_id = "testuser123"
    purpose_id = 1
    status = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5001/api/consent" -Method Post -Body $body -ContentType "application/json"
```

## 🚀 Production Deployment

### **Using Gunicorn:**
```powershell
# Install gunicorn
pip install gunicorn

# Run production server
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### **Using Waitress (Windows):**
```powershell
# Install waitress
pip install waitress

# Run production server
waitress-serve --host=0.0.0.0 --port=5000 app:app
```

## 📁 File Structure

```
backend/
├── app.py                 # Main Flask application
├── test_local.py          # SQLite test server
├── create_db.py           # Database creation script
├── seed_data.py           # Sample data seeding
├── test_api.py            # API testing script
├── start_server.py        # Production startup script
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
├── API_DOCUMENTATION.md   # Detailed API docs
└── README.md             # This file
```

## 🔒 Security

### **Environment Variables:**
- Store sensitive data in `.env` file
- Never commit `.env` to version control
- Use strong passwords for production databases

### **CORS Configuration:**
- CORS is enabled for frontend integration
- Configure allowed origins for production

### **Input Validation:**
- All inputs are validated
- SQL injection protection via SQLAlchemy
- XSS protection through proper escaping

## 📈 Monitoring

### **Health Checks:**
- `/api/health` endpoint for monitoring
- Database connection status
- Server uptime tracking

### **Logging:**
- Request/response logging
- Error tracking
- Performance monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

---

## 🎉 Success Checklist

After following the steps above, you should have:

- ✅ Backend server running on http://localhost:5001 (or 5000)
- ✅ Database connected and tables created
- ✅ Sample data seeded
- ✅ All API endpoints responding
- ✅ Health check returning "healthy"
- ✅ Frontend can connect to backend

**Your backend API is ready for frontend integration!** 🚀 
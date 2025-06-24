# Consent Management Frontend

A modern, responsive React application for managing user consent preferences with a beautiful UI and comprehensive analytics dashboard.

## 🚀 Features

### **Core Functionality:**
- ✅ **Cookie Consent Banner** - GDPR-compliant consent collection
- ✅ **Individual Consent Management** - Toggle specific consent types
- ✅ **Bulk Consent Operations** - Accept/Reject all with one click
- ✅ **Real-time Updates** - Instant feedback on consent changes
- ✅ **User ID Persistence** - Remembers user preferences using cookies

### **Analytics Dashboard:**
- 📊 **Consent Overview** - Visual cards showing each consent type
- 📈 **Statistics Dashboard** - Overall consent rates and metrics
- 🎯 **Progress Bars** - Visual representation of consent rates by purpose
- 📱 **Responsive Design** - Works perfectly on all devices

### **User Experience:**
- 🎨 **Modern UI** - Beautiful gradient design with smooth animations
- 🔄 **Loading States** - Professional loading spinners and error handling
- 📱 **Mobile Responsive** - Optimized for phones, tablets, and desktops
- ♿ **Accessible** - Keyboard navigation and screen reader friendly

## 🛠️ Technology Stack

- **React 18** - Modern React with hooks
- **Axios** - HTTP client for API communication
- **CSS3** - Custom styling with modern features
- **js-cookie** - Cookie management
- **uuid** - Unique user ID generation

## 🚀 Quick Start (Windows PowerShell)

### **Prerequisites:**
- Node.js (v14 or higher)
- npm or yarn
- Backend server running (see backend README)

### **Step 1: Setup Environment**

**Navigate to frontend directory:**
```powershell
cd C:\Users\YourUsername\Desktop\hackthon\frontend
```

**Check Node.js installation:**
```powershell
node --version
npm --version
```

### **Step 2: Install Dependencies**

**Install all required packages:**
```powershell
npm install
```

**Expected Output:**
```
added X packages, and audited Y packages in Zs
found 0 vulnerabilities
```

### **Step 3: Start the Development Server**

**Start the React application:**
```powershell
npm start
```

**Expected Output:**
```
Compiled successfully!

You can now view consent-management-frontend in the browser.

  Local:            http://localhost:3000
  On Your Network:  http://192.168.x.x:3000

Note that the development build is not optimized.
To create a production build, use npm run build.
```

### **Step 4: Access Your Application**

- **Open your browser** and go to: `http://localhost:3000`
- **You should see** the beautiful consent management interface

## 🔧 Configuration

### **Environment Variables:**

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:5001
```

**Default:** If not set, the app will use `http://localhost:5001`

### **Backend Connection:**

The frontend connects to your backend API endpoints:

- **Health Check:** `GET /api/health`
- **Get Purposes:** `GET /api/purposes`
- **Get Consents:** `GET /api/consent?user_id={user_id}`
- **Update Consent:** `POST /api/consent`
- **Bulk Update:** `POST /api/consent/bulk`
- **Get Statistics:** `GET /api/consent/stats`

## 📱 How to Use

### **1. Initial Visit:**
- User sees a cookie consent banner at the bottom
- Options: "Accept All", "Reject All", or "Manage Preferences"

### **2. Manage Preferences:**
- Click "Manage Preferences" to open detailed modal
- Toggle individual consent types on/off
- Save changes to update backend

### **3. Dashboard View:**
- Click "Show Dashboard" in the header
- View consent overview with status cards
- Switch to "Statistics" tab for analytics

### **4. Real-time Updates:**
- All changes are immediately sent to backend
- Statistics update automatically
- User preferences are saved in cookies

## 🎨 UI Components

### **Header:**
- App title and navigation buttons
- Dashboard toggle and preferences management

### **Consent Banner:**
- Fixed bottom banner for initial consent
- Clear call-to-action buttons
- Professional styling with gradients

### **Preferences Modal:**
- Detailed consent management interface
- Toggle switches for each consent type
- Save/cancel functionality

### **Dashboard:**
- **Consent Overview Tab:**
  - Cards for each consent purpose
  - Status badges (Allowed/Denied)
  - Toggle buttons for quick changes

- **Statistics Tab:**
  - Overall consent metrics
  - Progress bars by purpose
  - Real-time data from backend

## 🔄 State Management

### **User State:**
- `userId` - Unique identifier stored in cookies
- `purposes` - Available consent purposes from backend
- `consents` - User's current consent preferences
- `stats` - Analytics data from backend

### **UI State:**
- `showBanner` - Cookie consent banner visibility
- `showPreferences` - Preferences modal visibility
- `showDashboard` - Dashboard visibility
- `activeTab` - Current dashboard tab
- `loading` - Loading states
- `error` - Error handling

## 📊 API Integration

### **Data Flow:**
1. **App Initialization:**
   - Generate/retrieve user ID
   - Fetch purposes from backend
   - Load user's existing consents
   - Get statistics data

2. **Consent Updates:**
   - Send POST request to backend
   - Update local state
   - Refresh statistics
   - Show success feedback

3. **Error Handling:**
   - Network error detection
   - User-friendly error messages
   - Retry functionality

## 🎯 Key Features Explained

### **Cookie Consent Banner:**
- Appears on first visit
- GDPR-compliant messaging
- Three action options
- Disappears after user action

### **Bulk Operations:**
- "Accept All" - Enables all consent types
- "Reject All" - Disables all consent types
- Uses backend bulk endpoint for efficiency

### **Individual Management:**
- Toggle switches for each purpose
- Real-time backend updates
- Visual feedback on changes

### **Analytics Dashboard:**
- Real-time statistics from backend
- Visual progress bars
- Consent rate calculations
- Purpose-by-purpose breakdown

## 🔧 Development

### **Available Scripts:**
```powershell
npm start          # Start development server
npm run build      # Build for production
npm test           # Run tests
npm run eject      # Eject from Create React App
```

### **File Structure:**
```
src/
├── App.js         # Main application component
├── App.css        # Styles and responsive design
└── index.js       # Application entry point
```

## 🚀 Production Deployment

### **Build for Production:**
```powershell
npm run build
```

### **Deploy Options:**
- **Netlify** - Drag and drop build folder
- **Vercel** - Connect GitHub repository
- **AWS S3** - Upload build files
- **Heroku** - Deploy with buildpack

### **Environment Setup:**
- Set `REACT_APP_API_URL` to your production backend URL
- Ensure CORS is configured on backend
- Test all endpoints work in production

## 🔒 Privacy & Security

### **User Privacy:**
- User ID stored in cookies (1 year expiry)
- No personal data collected
- All consent data stored securely on backend
- GDPR-compliant consent collection

### **Security Features:**
- HTTPS recommended for production
- Secure cookie settings
- Input validation and sanitization
- Error handling without data exposure

## 🐛 Troubleshooting

### **Common Issues:**

1. **Backend Connection Failed:**
   - Check if backend server is running
   - Verify API URL in environment variables
   - Check CORS settings on backend

2. **Consent Not Saving:**
   - Check browser console for errors
   - Verify backend endpoints are working
   - Check network tab for failed requests

3. **UI Not Loading:**
   - Clear browser cache
   - Check for JavaScript errors
   - Verify all dependencies are installed

### **Debug Mode:**
- Open browser developer tools
- Check Console tab for errors
- Check Network tab for API calls
- Use React Developer Tools extension

## 📈 Performance

### **Optimizations:**
- Lazy loading of dashboard components
- Efficient state management
- Optimized API calls
- Responsive image handling
- CSS animations for smooth UX

### **Monitoring:**
- Real-time consent tracking
- User interaction analytics
- Performance metrics
- Error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For support and questions:
- Check the troubleshooting section
- Review the backend documentation
- Open an issue on GitHub

---

## 🎉 Success Checklist

After following the steps above, you should have:

- ✅ Frontend server running on http://localhost:3000
- ✅ Beautiful consent management interface in browser
- ✅ Working cookie consent banner
- ✅ Functional analytics dashboard
- ✅ Real-time consent management
- ✅ Backend integration working

**Your frontend is ready and connected to the backend!** 🚀 
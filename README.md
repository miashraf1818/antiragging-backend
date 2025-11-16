# 🚨 Anti-Ragging Complaint Management System - Backend

> **Secure Django REST API for college anti-ragging complaints with admin panel, authentication, and database management.**



## 📌 About The Project

A **production-ready backend system** designed to provide a safe, anonymous, and secure platform for students to report ragging incidents in educational institutions. Built with Django REST Framework, this API enables confidential complaint submission, real-time tracking, and administrative oversight.

### **Why This Matters**
- Ragging is a serious issue affecting student well-being
- Victims need a **safe, anonymous** way to report incidents
- Institutions require **centralized tracking** and accountability
- Legal compliance with anti-ragging laws (UGC guidelines)

***

## ✨ Key Features

### **For Students**
- 🔒 **Anonymous Complaint Submission** - No login required for victim safety
- 📝 **Detailed Incident Reporting** - Upload evidence (images, documents)
- 🔍 **Complaint Tracking** - Check status with unique tracking ID
- 📧 **Email Notifications** - Get updates on complaint progress

### **For Administrators**
- 👁️ **Centralized Dashboard** - View all complaints in one place
- ⚡ **Real-Time Updates** - Instant notification on new reports
- 📊 **Analytics & Reports** - Track patterns and trends
- 🛡️ **Role-Based Access** - Admin, Warden, Committee Member roles
- ✅ **Complaint Management** - Mark as pending/investigating/resolved

### **Security & Compliance**
- 🔐 **JWT Authentication** - Secure admin access
- 🚫 **CORS Protection** - Controlled frontend access
- 📜 **Audit Logs** - Track all admin actions
- 🔒 **Data Encryption** - Sensitive information protected

***

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 4.2+ |
| **API** | Django REST Framework |
| **Database** | PostgreSQL (Production) / SQLite (Dev) |
| **Authentication** | JWT (djangorestframework-simplejwt) |
| **File Storage** | AWS S3 / Local Media |
| **Email** | SMTP (Gmail/SendGrid) |
| **Deployment** | Render / AWS / Railway |

***

## 📦 Installation & Setup

### **Prerequisites**
- Python 3.10+
- pip
- Virtual environment (recommended)

### **1. Clone the Repository**
```bash
git clone https://github.com/miashraf1818/antiragging-backend.git
cd antiragging-backend
```

### **2. Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### **3. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Configuration**
Create a `.env` file in the root directory:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL for production)
DATABASE_URL=postgres://user:password@localhost:5432/antiragging

# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@antiragging.com

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret
JWT_EXPIRATION_HOURS=24

# CORS (Add your frontend URL)
CORS_ALLOWED_ORIGINS=http://localhost:3000,https://your-frontend.vercel.app

# File Upload (AWS S3 - Optional)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=antiragging-complaints
```

### **5. Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### **6. Create Superuser (Admin)**
```bash
python manage.py createsuperuser
```

### **7. Run Development Server**
```bash
python manage.py runserver
```

**API will be available at:** `http://localhost:8000/api/`

***

## 📡 API Endpoints

### **Public Endpoints** (No Authentication Required)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/complaints/submit/` | Submit new complaint (anonymous) |
| `GET` | `/api/complaints/track/{id}/` | Track complaint status |
| `GET` | `/api/info/guidelines/` | Get anti-ragging guidelines |

### **Admin Endpoints** (Requires JWT Token)

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/auth/login/` | Admin login (get JWT token) |
| `GET` | `/api/complaints/` | List all complaints |
| `GET` | `/api/complaints/{id}/` | Get complaint details |
| `PATCH` | `/api/complaints/{id}/update/` | Update complaint status |
| `DELETE` | `/api/complaints/{id}/delete/` | Delete complaint (soft delete) |
| `GET` | `/api/analytics/summary/` | Get dashboard statistics |

***

## 🏗️ Project Structure

```
antiragging-backend/
├── complaints/           # Complaint management app
│   ├── models.py        # Complaint, Evidence models
│   ├── serializers.py   # DRF serializers
│   ├── views.py         # API views
│   └── urls.py          # API routes
├── users/               # User management (admins)
│   ├── models.py        # Custom User model
│   ├── views.py         # Auth views
│   └── permissions.py   # Role-based permissions
├── analytics/           # Analytics & reporting
│   └── views.py         # Dashboard statistics
├── config/              # Project settings
│   ├── settings.py      # Django configuration
│   ├── urls.py          # Main URL routing
│   └── wsgi.py          # WSGI config
├── media/               # Uploaded files (evidence)
├── static/              # Static files
├── .env.example         # Environment template
├── requirements.txt     # Dependencies
└── manage.py            # Django management script
```

***

## 🔐 Security Features

1. **Anonymous Reporting** - No user registration required for victims
2. **JWT Authentication** - Secure admin access with token expiration
3. **CORS Whitelisting** - Only trusted frontends can access API
4. **Input Validation** - Prevent SQL injection, XSS attacks
5. **Rate Limiting** - Prevent abuse and DoS attacks
6. **File Upload Validation** - Restrict file types and sizes
7. **Audit Logging** - Track all administrative actions

***

## 🚀 Deployment

### **Deploy to Render**

1. Create a new Web Service on [Render](https://render.com)
2. Connect your GitHub repository
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `gunicorn config.wsgi:application`
5. Add environment variables from `.env`
6. Deploy!

### **Environment Variables for Production**
```bash
DEBUG=False
ALLOWED_HOSTS=your-backend.onrender.com
DATABASE_URL=postgres://...  # Use PostgreSQL in production
SECRET_KEY=strong-random-key
```

***

## 📊 Database Models

### **Complaint Model**
```python
- id (UUID, primary key)
- title (CharField)
- description (TextField)
- complainant_name (CharField, optional)
- complainant_email (EmailField, optional)
- incident_date (DateTimeField)
- location (CharField)
- severity (CharField: Low/Medium/High/Critical)
- status (CharField: Pending/Investigating/Resolved/Closed)
- evidence_files (FileField, multiple)
- tracking_id (CharField, unique)
- created_at (DateTimeField)
- updated_at (DateTimeField)
```

***

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

***

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

***

## 👤 Author

**Mohammed Ikram Ashrafi**
- GitHub: [@miashraf1818](https://github.com/miashraf1818)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)
- Email: ikramshariff2005@gmail.com

***

## 🙏 Acknowledgments

- UGC Anti-Ragging Regulations
- Django & DRF Community
- All contributors who helped make this project possible

***

## 📞 Support

For issues, questions, or suggestions:
- **GitHub Issues**: [Report here](https://github.com/miashraf1818/antiragging-backend/issues)

---

**🚨 Together, let's create safer educational environments for everyone!**

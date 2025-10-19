from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

# --- Complaint Submitted Email ---
def send_complaint_submitted_email(complaint):
    if not complaint.student.email:
        return
    subject = f'Complaint Submitted Successfully - #{complaint.id}'
    frontend_url = settings.FRONTEND_URL  # ✅ Dynamic URL
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #2563eb; text-align: center;">🛡️ Guardian Portal</h2>
            <h3 style="color: #16a34a;">Complaint Submitted Successfully</h3>
            <p>Dear {complaint.student.username},</p>
            <p>Your complaint has been successfully submitted and is being reviewed.</p>
            <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Complaint ID:</strong> #{complaint.id}</p>
                <p><strong>Title:</strong> {complaint.title}</p>
                <p><strong>Status:</strong> <span style="color: #f59e0b;">Pending</span></p>
                <p><strong>Submitted:</strong> {complaint.created_at.strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            <p><strong>What happens next?</strong></p>
            <ul>
                <li>Your complaint will be reviewed within 24 hours</li>
                <li>It will be assigned to a squad member for investigation</li>
                <li>You'll receive email updates on status changes</li>
                <li>Track your complaint anytime in the dashboard</li>
            </ul>
            <p style="margin-top: 30px;">
                <a href="{frontend_url}/student/complaint/{complaint.id}" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    View Complaint Details
                </a>
            </p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
            <p style="font-size: 12px; color: #666; text-align: center;">
                This is an automated email from Guardian Anti-Ragging Portal.<br>
                Please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [complaint.student.email],
        html_message=html_message,
        fail_silently=True,
    )

# --- Complaint Status Update Email ---
def send_complaint_status_update_email(complaint, old_status):
    if not complaint.student.email:
        return
    status_colors = {
        'pending': '#f59e0b',
        'in_progress': '#3b82f6',
        'resolved': '#16a34a',
        'closed': '#6b7280'
    }
    status_messages = {
        'in_progress': 'Your complaint is now under investigation by our squad team.',
        'resolved': 'Great news! Your complaint has been resolved. Please submit feedback.',
        'closed': 'Your complaint has been closed.'
    }
    subject = f'Complaint Status Updated - #{complaint.id}'
    frontend_url = settings.FRONTEND_URL  # ✅ Dynamic URL
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #2563eb; text-align: center;">🛡️ Guardian Portal</h2>
            <h3 style="color: {status_colors.get(complaint.status, '#333')};">Complaint Status Updated</h3>
            <p>Dear {complaint.student.username},</p>
            <p>{status_messages.get(complaint.status, 'Your complaint status has been updated.')}</p>
            <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Complaint ID:</strong> #{complaint.id}</p>
                <p><strong>Title:</strong> {complaint.title}</p>
                <p><strong>Previous Status:</strong> <span style="color: {status_colors.get(old_status, '#666')};">{old_status.replace('_', ' ').title()}</span></p>
                <p><strong>New Status:</strong> <span style="color: {status_colors.get(complaint.status, '#333')};">{complaint.status.replace('_', ' ').title()}</span></p>
            </div>
            {'<p><strong>Action Required:</strong> Please provide feedback on the resolution of your complaint.</p>' if complaint.status == 'resolved' else ''}
            <p style="margin-top: 30px;">
                <a href="{frontend_url}/student/complaint/{complaint.id}" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    View Complaint Details
                </a>
            </p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
            <p style="font-size: 12px; color: #666; text-align: center;">
                This is an automated email from Guardian Anti-Ragging Portal.<br>
                Please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [complaint.student.email],
        html_message=html_message,
        fail_silently=True,
    )

# --- Complaint Assigned Email ---
def send_complaint_assigned_email(complaint):
    if not complaint.assigned_to or not complaint.assigned_to.email:
        return
    subject = f'New Complaint Assigned - #{complaint.id}'
    anonymous_status = 'Yes (Identity Hidden)' if complaint.is_anonymous else 'No'
    student_name = 'Anonymous Student' if complaint.is_anonymous else (complaint.student.username if complaint.student else 'Unknown')
    frontend_url = settings.FRONTEND_URL  # ✅ Dynamic URL
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px;">
            <h2 style="color: #2563eb; text-align: center;">🛡️ Guardian Portal</h2>
            <h3 style="color: #f59e0b;">New Complaint Assigned to You</h3>
            <p>Dear {complaint.assigned_to.username},</p>
            <p>A new complaint has been assigned to you for investigation.</p>
            <div style="background: #f3f4f6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                <p><strong>Complaint ID:</strong> #{complaint.id}</p>
                <p><strong>Title:</strong> {complaint.title}</p>
                <p><strong>Description:</strong> {complaint.description[:100]}...</p>
                <p><strong>Submitted By:</strong> {student_name}</p>
                <p><strong>Anonymous:</strong> {anonymous_status}</p>
                <p><strong>Status:</strong> <span style="color: #3b82f6;">In Progress</span></p>
                <p><strong>Assigned:</strong> {complaint.updated_at.strftime('%B %d, %Y at %I:%M %p')}</p>
            </div>
            <p><strong>Action Required:</strong></p>
            <ul>
                <li>Review the complaint details carefully</li>
                <li>Investigate the matter thoroughly</li>
                <li>Update the status as you progress</li>
                <li>Maintain confidentiality if complaint is anonymous</li>
            </ul>
            <p style="margin-top: 30px;">
                <a href="{frontend_url}/squad/complaint/{complaint.id}" style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block;">
                    View & Handle Complaint
                </a>
            </p>
            <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
            <p style="font-size: 12px; color: #666; text-align: center;">
                This is an automated email from Guardian Anti-Ragging Portal.<br>
                Please do not reply to this email.
            </p>
        </div>
    </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [complaint.assigned_to.email],
        html_message=html_message,
        fail_silently=True,
    )

# --- Welcome Email ---
def send_welcome_email(user):
    if not user.email:
        return
    role_display = {
        'student': 'Student',
        'principal': 'Principal',
        'squad': 'Squad Member',
        'admin': 'Administrator'
    }.get(user.role, user.role.capitalize())
    role_colors = {
        'student': {'bg': '#dbeafe', 'text': '#1e40af'},
        'principal': {'bg': '#fce7f3', 'text': '#9f1239'},
        'squad': {'bg': '#dcfce7', 'text': '#166534'},
        'admin': {'bg': '#fef3c7', 'text': '#92400e'}
    }
    role_color = role_colors.get(user.role, {'bg': '#e5e7eb', 'text': '#374151'})
    subject = f'🛡️ Welcome to Guardian Portal - {role_display}!'
    frontend_url = settings.FRONTEND_URL  # ✅ Dynamic URL
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
        <div style="max-width: 600px; margin: 0 auto; padding: 20px; border: 1px solid #ddd; border-radius: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <div style="background: white; padding: 30px; border-radius: 8px;">
                <h2 style="color: #2563eb; text-align: center; margin-bottom: 10px;">🛡️ Guardian Portal</h2>
                <h3 style="color: #16a34a; text-align: center; margin-top: 0;">Welcome Aboard!</h3>
                <p style="font-size: 16px;">Dear <strong>{user.username}</strong>,</p>
                <p>🎉 Welcome to <strong>Guardian Portal</strong> - Your trusted platform for reporting and preventing ragging incidents!</p>
                <div style="background: #f3f4f6; padding: 20px; border-radius: 8px; margin: 25px 0; border-left: 4px solid #2563eb;">
                    <h4 style="margin-top: 0; color: #2563eb;">📋 Your Account Details:</h4>
                    <p style="margin: 8px 0;"><strong>👤 Username:</strong> {user.username}</p>
                    <p style="margin: 8px 0;"><strong>📧 Email:</strong> {user.email}</p>
                    <p style="margin: 8px 0;"><strong>🎭 Role:</strong> <span style="background: {role_color['bg']}; color: {role_color['text']}; padding: 4px 12px; border-radius: 12px; font-weight: bold;">{role_display}</span></p>
                    <p style="margin: 8px 0;"><strong>🏫 College:</strong> {user.college.name if user.college else 'Not Set'}</p>
                </div>
                <div style="background: #ecfdf5; padding: 20px; border-radius: 8px; margin: 25px 0; border-left: 4px solid #16a34a;">
                    <h4 style="margin-top: 0; color: #16a34a;">✨ What You Can Do:</h4>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        {'<li style="margin: 8px 0;">📝 Submit complaints <strong>anonymously</strong> or with your identity</li>' if user.role == 'student' else ''}
                        {'<li style="margin: 8px 0;">👁️ View and manage all complaints from your college</li>' if user.role == 'principal' else ''}
                        {'<li style="margin: 8px 0;">🔍 Investigate and resolve assigned complaints</li>' if user.role == 'squad' else ''}
                        {'<li style="margin: 8px 0;">⚙️ Manage system-wide settings and users</li>' if user.role == 'admin' else ''}
                        <li style="margin: 8px 0;">📊 Track complaint status in <strong>real-time</strong></li>
                        <li style="margin: 8px 0;">📧 Receive <strong>email notifications</strong> on all updates</li>
                        <li style="margin: 8px 0;">💬 Provide feedback once complaints are resolved</li>
                        <li style="margin: 8px 0;">🔒 Your privacy and safety are <strong>guaranteed</strong></li>
                    </ul>
                </div>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{frontend_url}/login" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 14px 32px; text-decoration: none; border-radius: 8px; display: inline-block; font-weight: bold; font-size: 16px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        🚀 Login to Dashboard
                    </a>
                </div>
                <div style="background: #fef3c7; padding: 15px; border-radius: 8px; margin: 25px 0; border-left: 4px solid #f59e0b;">
                    <p style="margin: 0; color: #92400e;">
                        <strong>🔐 Security Tip:</strong> Keep your login credentials secure and never share them with anyone.
                    </p>
                </div>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #ddd;">
                <div style="text-align: center;">
                    <p style="font-size: 14px; color: #666; margin: 5px 0;">
                        Need help? Contact your college administrator
                    </p>
                    <p style="font-size: 12px; color: #999; margin: 15px 0;">
                        This is an automated email from Guardian Anti-Ragging Portal.<br>
                        Please do not reply to this email.
                    </p>
                    <p style="font-size: 12px; color: #2563eb; margin: 5px 0;">
                        <strong>Your safety is our priority! 🛡️</strong>
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    send_mail(
        subject,
        plain_message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        html_message=html_message,
        fail_silently=True,
    )

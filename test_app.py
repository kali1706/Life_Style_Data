import unittest
import os
import tempfile
from app import create_app
from models import db, User

class LifestyleAnalyticsTestCase(unittest.TestCase):
    """Test cases for Lifestyle Analytics Platform"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
    
    def tearDown(self):
        """Clean up after tests"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_app_creation(self):
        """Test app creation"""
        self.assertIsNotNone(self.app)
        self.assertTrue(self.app.config['TESTING'])
    
    def test_homepage(self):
        """Test homepage access"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Lifestyle Data Analytics', response.data)
    
    def test_register_page(self):
        """Test registration page"""
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Account', response.data)
    
    def test_login_page(self):
        """Test login page"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login', response.data)
    
    def test_user_registration(self):
        """Test user registration"""
        response = self.client.post('/register', 
            data={
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'password123',
                'confirm_password': 'password123'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
    
    def test_user_login(self):
        """Test user login"""
        # First create a user
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Then test login
        response = self.client.post('/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_access_without_login(self):
        """Test dashboard access without login"""
        response = self.client.get('/dashboard', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        # Should redirect to login page
        self.assertIn(b'Login', response.data)
    
    def test_profile_page(self):
        """Test profile page access"""
        # Create and login user
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Login
        self.client.post('/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            }
        )
        
        # Access profile page
        response = self.client.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Profile', response.data)
    
    def test_workout_tracker_page(self):
        """Test workout tracker page"""
        # Create and login user
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Login
        self.client.post('/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            }
        )
        
        # Access workout tracker
        response = self.client.get('/workout_tracker')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Workout Tracker', response.data)
    
    def test_nutrition_tracker_page(self):
        """Test nutrition tracker page"""
        # Create and login user
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Login
        self.client.post('/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            }
        )
        
        # Access nutrition tracker
        response = self.client.get('/nutrition_tracker')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Nutrition Tracker', response.data)
    
    def test_analytics_page(self):
        """Test analytics page"""
        # Create and login user
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Login
        self.client.post('/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            }
        )
        
        # Access analytics page
        response = self.client.get('/analytics')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Analytics Dashboard', response.data)
    
    def test_reports_page(self):
        """Test reports page"""
        # Create and login user
        with self.app.app_context():
            user = User(username='testuser', email='test@example.com')
            user.set_password('password123')
            db.session.add(user)
            db.session.commit()
        
        # Login
        self.client.post('/login',
            data={
                'username': 'testuser',
                'password': 'password123'
            }
        )
        
        # Access reports page
        response = self.client.get('/reports')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reports', response.data)

if __name__ == '__main__':
    unittest.main()
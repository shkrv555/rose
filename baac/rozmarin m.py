from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Tüm origin'lere izin ver

# Veri dosyası
DATA_FILE = 'portfolio_data.json'

def init_data():
    if not os.path.exists(DATA_FILE):
        base_data = {
            'projects': [
                {
                    'id': 1,
                    'title': 'Portfolio Website v1',
                    'description': 'Kişisel portfolio websitesi - Geleneksel tasarım',
                    'technologies': 'HTML, CSS, JavaScript, Python',
                    'project_url': 'https://shkrv555.github.io/ilkin01/',
                    'github_url': 'https://github.com/shkrv555/ilkin01',
                    'image_url': '/static/project1.jpg',
                    'featured': True
                },
                {
                    'id': 2,
                    'title': 'Portfolio Website v2',
                    'description': 'Modern React portfolio - Single page application',
                    'technologies': 'React, JavaScript, CSS, Python',
                    'project_url': 'https://shkrv555.github.io/ilkin/',
                    'github_url': 'https://github.com/shkrv555/ilkin',
                    'image_url': '/static/project2.jpg',
                    'featured': True
                }
            ],
            'skills': [
                {'id': 1, 'name': 'HTML/CSS', 'category': 'frontend', 'level': 90, 'icon': '🎨'},
                {'id': 2, 'name': 'JavaScript', 'category': 'frontend', 'level': 85, 'icon': '📜'},
                {'id': 3, 'name': 'React', 'category': 'frontend', 'level': 80, 'icon': '⚛️'},
                {'id': 4, 'name': 'Python', 'category': 'backend', 'level': 75, 'icon': '🐍'},
                {'id': 5, 'name': 'Flask', 'category': 'backend', 'level': 70, 'icon': '⚡'}
            ],
            'messages': [],
            'visitors': []
        }
        save_data(base_data)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'projects': [], 'skills': [], 'messages': [], 'visitors': []}

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# 🏠 Ana Sayfa
@app.route('/')
def home():
    return jsonify({
        'message': 'Portfolio Backend API Çalışıyor! 🚀',
        'version': '1.0',
        'frontend_repos': [
            'https://shkrv555.github.io/ilkin01/',
            'https://shkrv555.github.io/ilkin/'
        ],
        'endpoints': {
            '/api/projects': 'Tüm projeleri getir',
            '/api/projects/featured': 'Öne çıkan projeler',
            '/api/skills': 'Yetenekleri getir',
            '/api/contact': 'İletişim formu',
            '/api/visitors': 'Ziyaretçi sayısı'
        }
    })

# 📂 Projeler API
@app.route('/api/projects', methods=['GET'])
def get_projects():
    data = load_data()
    return jsonify({
        'success': True,
        'count': len(data['projects']),
        'projects': data['projects']
    })

@app.route('/api/projects/featured', methods=['GET'])
def get_featured_projects():
    data = load_data()
    featured = [p for p in data['projects'] if p.get('featured')]
    return jsonify({
        'success': True,
        'count': len(featured),
        'projects': featured
    })

# 💻 Yetenekler API
@app.route('/api/skills', methods=['GET'])
def get_skills():
    data = load_data()
    category = request.args.get('category')
    
    if category:
        skills = [s for s in data['skills'] if s.get('category') == category]
    else:
        skills = data['skills']
    
    return jsonify({
        'success': True,
        'count': len(skills),
        'skills': skills
    })

# 📧 İletişim Formu
@app.route('/api/contact', methods=['POST'])
def contact():
    try:
        data = request.get_json()
        
        # Validation
        if not data.get('name') or not data.get('email') or not data.get('message'):
            return jsonify({
                'success': False,
                'error': 'Lütfen tüm alanları doldurun'
            }), 400
        
        # Spam kontrolü
        if len(data['message']) < 5:
            return jsonify({
                'success': False,
                'error': 'Mesaj çok kısa'
            }), 400
        
        # Veriyi kaydet
        db_data = load_data()
        new_message = {
            'id': len(db_data['messages']) + 1,
            'name': data['name'],
            'email': data['email'],
            'subject': data.get('subject', 'İletişim Formu'),
            'message': data['message'],
            'ip': request.remote_addr,
            'timestamp': datetime.now().isoformat(),
            'read': False
        }
        
        db_data['messages'].append(new_message)
        save_data(db_data)
        
        # Başarılı yanıt
        return jsonify({
            'success': True,
            'message': '✅ Mesajınız başarıyla gönderildi! En kısa sürede dönüş yapacağım.',
            'message_id': new_message['id']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Sunucu hatası: {str(e)}'
        }), 500

# 👥 Ziyaretçi Takibi
@app.route('/api/visitors', methods=['GET', 'POST'])
def visitors():
    if request.method == 'GET':
        data = load_data()
        return jsonify({
            'success': True,
            'count': len(data['visitors'])
        })
    
    elif request.method == 'POST':
        data = load_data()
        visitor_data = {
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent', ''),
            'timestamp': datetime.now().isoformat(),
            'page': request.json.get('page', '/')
        }
        data['visitors'].append(visitor_data)
        save_data(data)
        
        return jsonify({'success': True})

# ❓ Health Check
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy 🟢',
        'timestamp': datetime.now().isoformat(),
        'service': 'Portfolio Backend API'
    })

if __name__ == '__main__':
    init_data()
    print("🚀 Portfolio Backend başlatılıyor...")
    print("📍 API URL: http://localhost:5000")
    print("📚 Endpoints:")
    print("   GET  /api/projects")
    print("   GET  /api/projects/featured") 
    print("   GET  /api/skills")
    print("   POST /api/contact")
    print("   POST /api/visitors")
    app.run(debug=True, host='0.0.0.0', port=5000)
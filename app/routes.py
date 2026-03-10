from flask import Blueprint, request, jsonify
from functools import wraps
import base64
from PIL import Image
from io import BytesIO
from app import db
from app.models import User, Card, UserCard

bp = Blueprint('api', __name__)

@bp.route('/', methods=['GET'])
def index():
    return """
    <html>
        <head>
            <title>CAA Board API</title>
            <style>
                body { font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background-color: #f0f2f5; margin: 0; }
                .container { text-align: center; background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; }
                p { color: #7f8c8d; }
                .status { display: inline-block; padding: 0.5rem 1rem; background-color: #2ecc71; color: white; border-radius: 20px; font-weight: bold; margin-top: 1rem; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>CAA Board API</h1>
                <p>O backend está rodando e pronto para receber requisições.</p>
                <div class="status">Online</div>
            </div>
        </body>
    </html>
    """

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
            
        current_user = User.query.filter_by(token=token).first()
        if not current_user:
            return jsonify({'message': 'Token is invalid!'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated

@bp.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Faltando usuário ou senha'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        token = user.get_token()
        db.session.commit()
        return jsonify({'token': token, 'username': user.username})
        
    return jsonify({'message': 'Usuário ou senha inválidos'}), 401

@bp.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'message': 'Faltando usuário ou senha'}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'message': 'Este usuário já existe.'}), 400
        
    user = User(username=data['username'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Parabéns, registro concluído! Agora você pode entrar.'})

@bp.route('/api/cards', methods=['GET'])
@token_required
def get_cards(current_user):
    # Load user's board (only visible cards)
    user_cards = UserCard.query.filter_by(user_id=current_user.id, is_hidden=False).order_by(UserCard.position).all()
    
    if not user_cards:
        default_cards = Card.query.filter_by(is_default=True).all()
        for idx, card in enumerate(default_cards):
            uc = UserCard(user_id=current_user.id, card_id=card.id, position=idx)
            db.session.add(uc)
        db.session.commit()
        user_cards = UserCard.query.filter_by(user_id=current_user.id, is_hidden=False).order_by(UserCard.position).all()
        
    cards_data = []
    for uc in user_cards:
        cards_data.append({
            'id': uc.id,
            'word': uc.card.word,
            'icon_class': uc.card.icon_class,
            'card_type': uc.card.card_type
        })
        
    return jsonify({'cards': cards_data})

@bp.route('/api/settings/cards', methods=['GET'])
@token_required
def get_settings_cards(current_user):
    user_cards = UserCard.query.filter_by(user_id=current_user.id).order_by(UserCard.position).all()
    
    if not user_cards:
        default_cards = Card.query.filter_by(is_default=True).all()
        for idx, card in enumerate(default_cards):
            uc = UserCard(user_id=current_user.id, card_id=card.id, position=idx, is_hidden=False)
            db.session.add(uc)
        db.session.commit()
        user_cards = UserCard.query.filter_by(user_id=current_user.id).order_by(UserCard.position).all()
        
    cards_data = []
    for uc in user_cards:
        cards_data.append({
            'id': uc.id,
            'word': uc.card.word,
            'icon_class': uc.card.icon_class,
            'card_type': uc.card.card_type,
            'is_hidden': uc.is_hidden,
            'is_default': uc.card.is_default,
            'user_id_matches': uc.card.user_id == current_user.id
        })
        
    return jsonify({'cards': cards_data})

@bp.route('/api/save_board', methods=['POST'])
@token_required
def save_board(current_user):
    data = request.get_json()
    card_ids = data.get('card_ids', [])
    
    for idx, uc_id in enumerate(card_ids):
        uc = UserCard.query.filter_by(id=uc_id, user_id=current_user.id).first()
        if uc:
            uc.position = idx
    db.session.commit()
    return jsonify({'status': 'success'})

@bp.route('/api/cards', methods=['POST'])
@token_required
def add_card(current_user):
    word = request.form.get('word', '').strip()
    icon = request.form.get('icon', '').strip()
    image_file = request.files.get('image_upload')
    
    if not word or len(word.split()) > 2:
        return jsonify({'message': 'A palavra deve ter no máximo 2 termos.'}), 400
        
    icon_val = icon
    if image_file and image_file.filename:
        allowed_exts = ('.png', '.jpg', '.jpeg', '.ico')
        if not image_file.filename.lower().endswith(allowed_exts):
            return jsonify({'message': 'Apenas imagens PNG, JPG, JPEG, ou ICO são permitidas.'}), 400
            
        file_data = image_file.read()
        if len(file_data) > 500 * 1024:
            return jsonify({'message': 'A imagem deve ter no máximo 500KB.'}), 400
            
        try:
            image_file.seek(0)
            img = Image.open(BytesIO(file_data))
            if img.mode not in ('RGB', 'RGBA'):
                img = img.convert('RGBA')
            width, height = img.size
            if width > 300 or height > 300:
                return jsonify({'message': f'Dimensões excedem 300x300px. A sua tem {width}x{height}px.'}), 400
                
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            icon_val = f"data:image/png;base64,{img_str}"
        except Exception as e:
            return jsonify({'message': 'Erro ao processar a imagem.'}), 400
            
    if not icon_val:
        return jsonify({'message': 'Você deve escolher um ícone ou enviar uma imagem.'}), 400
        
    new_card = Card(word=word, icon_class=icon_val, card_type='custom', is_default=False, user_id=current_user.id)
    db.session.add(new_card)
    db.session.flush()
    
    max_pos = db.session.query(db.func.max(UserCard.position)).filter_by(user_id=current_user.id).scalar()
    next_pos = (max_pos or 0) + 1
    uc = UserCard(user_id=current_user.id, card_id=new_card.id, position=next_pos, is_hidden=False)
    db.session.add(uc)
    db.session.commit()
    
    return jsonify({'status': 'success'})

@bp.route('/api/cards/<int:id>/toggle_visibility', methods=['POST'])
@token_required
def toggle_visibility(current_user, id):
    uc = UserCard.query.filter_by(id=id, user_id=current_user.id).first()
    if not uc:
        return jsonify({'message': 'Card não encontrado.'}), 404
        
    uc.is_hidden = not uc.is_hidden
    db.session.commit()
    return jsonify({'status': 'success'})

@bp.route('/api/cards/<int:id>', methods=['DELETE'])
@token_required
def delete_card(current_user, id):
    uc = UserCard.query.filter_by(id=id, user_id=current_user.id).first()
    if uc and uc.card.user_id == current_user.id:
        card = uc.card
        db.session.delete(uc)
        db.session.delete(card)
        db.session.commit()
        return jsonify({'status': 'success'})
    return jsonify({'message': 'Card não encontrado ou acesso negado.'}), 400

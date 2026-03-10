from app import create_app, db
from app.models import Card

default_cards_data = [
    # Verbs
    {"word": "Eu Quero", "code": "fa-solid fa-hand-pointer", "type": "verb"},
    {"word": "Comer", "code": "fa-solid fa-utensils", "type": "verb"},
    {"word": "Beber", "code": "fa-solid fa-glass-water", "type": "verb"},
    {"word": "Ir", "code": "fa-solid fa-person-walking", "type": "verb"},
    {"word": "Brincar", "code": "fa-solid fa-puzzle-piece", "type": "verb"},
    {"word": "Dormir", "code": "fa-solid fa-bed", "type": "verb"},
    {"word": "Assistir", "code": "fa-solid fa-tv", "type": "verb"},
    {"word": "Ouvir", "code": "fa-solid fa-headphones", "type": "verb"},
    {"word": "Falar", "code": "fa-solid fa-comment-dots", "type": "verb"},
    {"word": "Pegar", "code": "fa-solid fa-hand-holding", "type": "verb"},
    {"word": "Parar", "code": "fa-solid fa-hand", "type": "verb"},
    {"word": "Ajudar", "code": "fa-solid fa-handshake-angle", "type": "verb"},
    {"word": "Abrir", "code": "fa-solid fa-door-open", "type": "verb"},
    {"word": "Fechar", "code": "fa-solid fa-door-closed", "type": "verb"},
    {"word": "Vestir", "code": "fa-solid fa-shirt", "type": "verb"},
    {"word": "Tomar banho", "code": "fa-solid fa-bath", "type": "verb"},
    {"word": "Correr", "code": "fa-solid fa-person-running", "type": "verb"},
    {"word": "Pular", "code": "fa-solid fa-arrow-up", "type": "verb"},
    {"word": "Sentar", "code": "fa-solid fa-chair", "type": "verb"},

    # Objects
    {"word": "Banheiro", "code": "fa-solid fa-toilet", "type": "noun"},
    {"word": "Água", "code": "fa-solid fa-droplet", "type": "noun"},
    {"word": "Bola", "code": "fa-solid fa-futbol", "type": "noun"},
    {"word": "Celular", "code": "fa-solid fa-mobile-screen-button", "type": "noun"},
    {"word": "TV", "code": "fa-solid fa-tv", "type": "noun"},
    {"word": "Tablet", "code": "fa-solid fa-tablet-screen-button", "type": "noun"},
    {"word": "Livro", "code": "fa-solid fa-book-open", "type": "noun"},
    {"word": "Cama", "code": "fa-solid fa-bed", "type": "noun"},
    {"word": "Copo", "code": "fa-solid fa-mug-hot", "type": "noun"},
    {"word": "Prato", "code": "fa-solid fa-plate-wheat", "type": "noun"},
    {"word": "Garfo", "code": "fa-solid fa-utensils", "type": "noun"},
    {"word": "Colher", "code": "fa-solid fa-spoon", "type": "noun"},
    {"word": "Sabonete", "code": "fa-solid fa-soap", "type": "noun"},
    {"word": "Toalha", "code": "fa-solid fa-scroll", "type": "noun"},
    {"word": "Mochila", "code": "fa-solid fa-briefcase", "type": "noun"},
    {"word": "Tênis", "code": "fa-solid fa-shoe-prints", "type": "noun"},
    {"word": "Blusa", "code": "fa-solid fa-shirt", "type": "noun"},
    {"word": "Calça", "code": "fa-solid fa-user-tie", "type": "noun"},

    # Animals
    {"word": "Cachorro", "code": "fa-solid fa-dog", "type": "noun"},
    {"word": "Gato", "code": "fa-solid fa-cat", "type": "noun"},
    {"word": "Pássaro", "code": "fa-solid fa-dove", "type": "noun"},
    {"word": "Peixe", "code": "fa-solid fa-fish", "type": "noun"},
    {"word": "Cavalo", "code": "fa-solid fa-horse", "type": "noun"},
    {"word": "Vaca", "code": "fa-solid fa-cow", "type": "noun"},
    {"word": "Porco", "code": "fa-solid fa-piggy-bank", "type": "noun"},
    {"word": "Galinha", "code": "fa-solid fa-egg", "type": "noun"},
    {"word": "Leão", "code": "fa-solid fa-paw", "type": "noun"},
    {"word": "Macaco", "code": "fa-solid fa-paw", "type": "noun"},
    {"word": "Urso", "code": "fa-solid fa-paw", "type": "noun"},
    {"word": "Elefante", "code": "fa-solid fa-paw", "type": "noun"},
    {"word": "Girafa", "code": "fa-solid fa-paw", "type": "noun"},
    {"word": "Sapo", "code": "fa-solid fa-frog", "type": "noun"},
    {"word": "Cobra", "code": "fa-solid fa-worm", "type": "noun"},

    # Food
    {"word": "Limão", "code": "fa-solid fa-lemon", "type": "noun"},
    {"word": "Maçã", "code": "fa-solid fa-apple-whole", "type": "noun"},
    {"word": "Laranja", "code": "fa-solid fa-circle-minus", "type": "noun"},
    {"word": "Morango", "code": "fa-solid fa-leaf", "type": "noun"},
    {"word": "Uva", "code": "fa-solid fa-cubes-stacked", "type": "noun"},
    {"word": "Melancia", "code": "fa-solid fa-pizza-slice", "type": "noun"},
    {"word": "Pêra", "code": "fa-solid fa-apple-whole", "type": "noun"},
    {"word": "Abacaxi", "code": "fa-solid fa-tree", "type": "noun"},
    {"word": "Pão", "code": "fa-solid fa-bread-slice", "type": "noun"},
    {"word": "Arroz", "code": "fa-solid fa-bowl-rice", "type": "noun"},
    {"word": "Feijão", "code": "fa-solid fa-seedling", "type": "noun"},
    {"word": "Carne", "code": "fa-solid fa-bone", "type": "noun"},
    {"word": "Frango", "code": "fa-solid fa-drumstick-bite", "type": "noun"},
    {"word": "Ovo", "code": "fa-solid fa-egg", "type": "noun"},
    {"word": "Leite", "code": "fa-solid fa-glass-water", "type": "noun"},
    {"word": "Suco", "code": "fa-solid fa-bottle-water", "type": "noun"},
    {"word": "Biscoito", "code": "fa-solid fa-cookie", "type": "noun"},
    {"word": "Bolo", "code": "fa-solid fa-cake-candles", "type": "noun"},

    # Connectors & Feelings
    {"word": "Sim", "code": "fa-solid fa-thumbs-up", "type": "connector"},
    {"word": "Não", "code": "fa-solid fa-thumbs-down", "type": "connector"},
    {"word": "Mais", "code": "fa-solid fa-plus", "type": "connector"},
    {"word": "Acabou", "code": "fa-solid fa-ban", "type": "connector"},
    {"word": "Feliz", "code": "fa-solid fa-face-smile", "type": "connector"},
    {"word": "Triste", "code": "fa-solid fa-face-sad-cry", "type": "connector"},
    {"word": "Bravo", "code": "fa-solid fa-face-angry", "type": "connector"},
    {"word": "Assustado", "code": "fa-solid fa-face-surprise", "type": "connector"},
    {"word": "Com sono", "code": "fa-solid fa-face-tired", "type": "connector"},
    {"word": "Com fome", "code": "fa-solid fa-face-grin-tongue", "type": "connector"},
    {"word": "Com sede", "code": "fa-solid fa-glass-water", "type": "connector"},
    {"word": "Doendo", "code": "fa-solid fa-face-frown", "type": "connector"},
    {"word": "na", "code": "fa-solid fa-arrow-right", "type": "connector"},
    {"word": "no", "code": "fa-solid fa-arrow-right", "type": "connector"},
    {"word": "ao", "code": "fa-solid fa-arrow-right", "type": "connector"},
    {"word": "com", "code": "fa-solid fa-plus", "type": "connector"},
    {"word": "e", "code": "fa-solid fa-check", "type": "connector"},
]

app = create_app()

with app.app_context():
    if Card.query.first() is None:
        print("Inserting 70+ default cards with FontAwesome Free classes...")
        for c in default_cards_data:
            card = Card(word=c['word'], icon_class=c['code'], card_type=c['type'], is_default=True)
            db.session.add(card)
        db.session.commit()
        print("Initial database setup complete!")
    else:
        print("Cards already exist in DB.")

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from games.models import Focus, Material, Label, Game, TrainingSession, SessionGame


class Command(BaseCommand):
    help = 'Load sample data for MiniGameArchive'

    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write(self.style.SUCCESS('Created superuser: admin/admin123'))
        
        # Create focus areas
        focus_areas = [
            'Dribbling', 'Shooting', 'Passing', 'Defense', 'Teamwork', 
            'Conditioning', 'Agility', 'Speed', 'Strength', 'Coordination'
        ]
        
        for focus_name in focus_areas:
            focus, created = Focus.objects.get_or_create(name=focus_name)
            if created:
                self.stdout.write(f'Created focus: {focus_name}')
        
        # Create materials
        materials = [
            'Basketball', 'Halfcourt', 'Full Court', 'Hoop', 'Cones', 
            'Stopwatch', 'Whistle', 'Wall', 'Net', 'Rebounder'
        ]
        
        for material_name in materials:
            material, created = Material.objects.get_or_create(name=material_name)
            if created:
                self.stdout.write(f'Created material: {material_name}')
        
        # Create labels
        labels_data = [
            ('Warmup', '#28a745'),
            ('Cool-down', '#6c757d'),
            ('Competitive', '#dc3545'),
            ('Fun', '#ffc107'),
            ('Advanced', '#6f42c1'),
            ('Beginner', '#17a2b8'),
        ]
        
        for label_name, color in labels_data:
            label, created = Label.objects.get_or_create(name=label_name, defaults={'color': color})
            if created:
                self.stdout.write(f'Created label: {label_name}')
        
        # Create sample games
        sample_games = [
            {
                'name': 'Fruit Bowl',
                'description': 'Players dribble around cones while calling out different fruits. When "banana" is called, everyone must change direction. Great for dribbling skills and listening.',
                'player_count': '5-6',
                'duration': '10min',
                'focus': ['Dribbling', 'Coordination'],
                'materials': ['Basketball', 'Cones'],
                'labels': ['Fun', 'Beginner'],
                'variants': 'Add more fruits, increase speed, or add defensive players.'
            },
            {
                'name': 'Sharks and Minnows',
                'description': 'One player is the shark in the middle. Other players (minnows) must dribble from one end to the other without getting their ball stolen. If caught, they become a shark.',
                'player_count': '7-8',
                'duration': '15min',
                'focus': ['Dribbling', 'Defense', 'Agility'],
                'materials': ['Basketball', 'Halfcourt'],
                'labels': ['Competitive', 'Fun'],
                'variants': 'Add multiple balls, change the playing area, or add obstacles.'
            },
            {
                'name': 'Around the World',
                'description': 'Players shoot from different spots around the court. Must make a shot from each spot before moving to the next. Great for shooting practice and accuracy.',
                'player_count': '3-4',
                'duration': '20min',
                'focus': ['Shooting'],
                'materials': ['Basketball', 'Hoop'],
                'labels': ['Advanced'],
                'variants': 'Add time limits, increase distance, or add defensive pressure.'
            },
            {
                'name': 'Passing Relay',
                'description': 'Teams line up and pass the ball down the line. Last player dribbles to the front and the process continues. First team to get everyone through wins.',
                'player_count': '9-10',
                'duration': '10min',
                'focus': ['Passing', 'Teamwork'],
                'materials': ['Basketball'],
                'labels': ['Teamwork', 'Fun'],
                'variants': 'Add different types of passes, increase distance, or add obstacles.'
            },
            {
                'name': 'Defensive Slides',
                'description': 'Players practice defensive stance and sliding movements. Coach calls out directions and players slide accordingly. Focus on proper defensive positioning.',
                'player_count': '5-6',
                'duration': '15min',
                'focus': ['Defense', 'Conditioning'],
                'materials': ['Halfcourt'],
                'labels': ['Conditioning', 'Beginner'],
                'variants': 'Add offensive players, increase speed, or add different defensive techniques.'
            },
        ]
        
        for game_data in sample_games:
            game, created = Game.objects.get_or_create(
                name=game_data['name'],
                defaults={
                    'description': game_data['description'],
                    'player_count': game_data['player_count'],
                    'duration': game_data['duration'],
                    'variants': game_data['variants'],
                }
            )
            
            if created:
                # Add focus areas
                for focus_name in game_data['focus']:
                    try:
                        focus = Focus.objects.get(name=focus_name)
                        game.focus.add(focus)
                    except Focus.DoesNotExist:
                        self.stdout.write(f'Warning: Focus "{focus_name}" not found for game "{game_data["name"]}"')
                
                # Add materials
                for material_name in game_data['materials']:
                    try:
                        material = Material.objects.get(name=material_name)
                        game.materials.add(material)
                    except Material.DoesNotExist:
                        self.stdout.write(f'Warning: Material "{material_name}" not found for game "{game_data["name"]}"')
                
                # Add labels
                for label_name in game_data['labels']:
                    try:
                        label = Label.objects.get(name=label_name)
                        game.labels.add(label)
                    except Label.DoesNotExist:
                        self.stdout.write(f'Warning: Label "{label_name}" not found for game "{game_data["name"]}"')
                
                self.stdout.write(f'Created game: {game_data["name"]}')
        
        self.stdout.write(self.style.SUCCESS('Sample data loaded successfully!'))
        self.stdout.write('You can now login with admin/admin123 to access the admin panel.')
        
        # Create sample training sessions
        admin_user = User.objects.get(username='admin')
        sample_sessions = [
            {
                'name': 'Beginner Dribbling Session',
                'description': 'A focused session on dribbling fundamentals for beginners',
                'games': ['Fruit Bowl', 'Sharks and Minnows']
            },
            {
                'name': 'Advanced Shooting Session',
                'description': 'Advanced shooting practice with various drills',
                'games': ['Around the World']
            },
            {
                'name': 'Team Building Session',
                'description': 'Focus on teamwork and passing skills',
                'games': ['Passing Relay', 'Sharks and Minnows']
            }
        ]
        
        for session_data in sample_sessions:
            session, created = TrainingSession.objects.get_or_create(
                name=session_data['name'],
                defaults={
                    'description': session_data['description'],
                    'created_by': admin_user
                }
            )
            
            if created:
                # Add games to session
                for i, game_name in enumerate(session_data['games'], 1):
                    try:
                        game = Game.objects.get(name=game_name)
                        SessionGame.objects.get_or_create(
                            session=session,
                            game=game,
                            defaults={'order': i}
                        )
                    except Game.DoesNotExist:
                        self.stdout.write(f'Warning: Game "{game_name}" not found for session "{session_data["name"]}"')
                
                self.stdout.write(f'Created training session: {session_data["name"]}') 
from django.core.management.base import BaseCommand
from games.models import ImpressumContent


class Command(BaseCommand):
    help = 'Add sample Impressum content for MiniGameArchive'

    def handle(self, *args, **options):
        self.stdout.write('Adding sample Impressum content...')
        
        # Sample Impressum content based on the user's blog structure
        impressum_content = [
            {
                'title': 'Angaben gemäß § 5 TMG',
                'content': '''**Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV:**

Nils Brink
[Ihre Adresse hier einfügen]
Deutschland

**Kontakt:**
E-Mail: [Ihre E-Mail hier einfügen]
Website: https://minigamearchive.com

**Verantwortlich für den Inhalt nach § 55 Abs. 2 RStV:**
Nils Brink
[Ihre Adresse hier einfügen]
Deutschland''',
                'order': 1
            },
            {
                'title': 'Haftung für Inhalte',
                'content': '''Die Inhalte unserer Seiten wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte können wir jedoch keine Gewähr übernehmen.

Als Diensteanbieter sind wir gemäß § 7 Abs.1 TMG für eigene Inhalte auf diesen Seiten nach den allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 TMG sind wir als Diensteanbieter jedoch nicht verpflichtet, übermittelte oder gespeicherte fremde Informationen zu überwachen oder nach Umständen zu forschen, die auf eine rechtswidrige Tätigkeit hinweisen. Verpflichtungen zur Entfernung oder Sperrung der Nutzung von Informationen nach den allgemeinen Gesetzen bleiben hiervon unberührt. Eine diesbezügliche Haftung ist jedoch erst ab dem Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung möglich. Bei Bekanntwerden von entsprechenden Rechtsverletzungen werden wir diese Inhalte umgehend entfernen.''',
                'order': 2
            },
            {
                'title': 'Haftung für Links',
                'content': '''Unser Angebot enthält Links zu externen Webseiten Dritter, auf deren Inhalte wir keinen Einfluss haben. Deshalb können wir für diese fremden Inhalte auch keine Gewähr übernehmen. Für die Inhalte der verlinkten Seiten ist stets der jeweilige Anbieter oder Betreiber der Seiten verantwortlich. Die verlinkten Seiten wurden zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der Verlinkung nicht erkennbar.

Eine permanente inhaltliche Kontrolle der verlinkten Seiten ist jedoch ohne konkrete Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Links umgehend entfernen.''',
                'order': 3
            },
            {
                'title': 'Urheberrecht',
                'content': '''Die durch die Seitenbetreiber erstellten Inhalte und Werke auf diesen Seiten unterliegen dem deutschen Urheberrecht. Die Vervielfältigung, Bearbeitung, Verbreitung und jede Art der Verwertung außerhalb der Grenzen des Urheberrechtes bedürfen der schriftlichen Zustimmung des jeweiligen Autors bzw. Erstellers. Downloads und Kopien dieser Seite sind nur für den privaten, nicht kommerziellen Gebrauch gestattet.

Soweit die Inhalte auf dieser Seite nicht vom Betreiber erstellt wurden, werden die Urheberrechte Dritter beachtet. Insbesondere werden Inhalte Dritter als solche gekennzeichnet. Sollten Sie trotzdem auf eine Urheberrechtsverletzung aufmerksam werden, bitten wir um einen entsprechenden Hinweis. Bei Bekanntwerden von Rechtsverletzungen werden wir derartige Inhalte umgehend entfernen.''',
                'order': 4
            },
            {
                'title': 'Datenschutz',
                'content': '''Die Nutzung unserer Webseite ist in der Regel ohne Angabe personenbezogener Daten möglich. Soweit auf unseren Seiten personenbezogene Daten (beispielsweise Name, Anschrift oder E-Mail-Adressen) erhoben werden, erfolgt dies, soweit möglich, stets auf freiwilliger Basis. Diese Daten werden ohne Ihre ausdrückliche Zustimmung nicht an Dritte weitergegeben.

Wir weisen darauf hin, dass die Datenübertragung im Internet (z.B. bei der Kommunikation per E-Mail) Sicherheitslücken aufweisen kann. Ein lückenloser Schutz der Daten vor dem Zugriff durch Dritte ist nicht möglich.

Der Nutzung von im Rahmen der Impressumspflicht veröffentlichten Kontaktdaten durch Dritte zur Übersendung von nicht ausdrücklich angeforderter Werbung und Informationsmaterialien wird hiermit ausdrücklich widersprochen. Die Betreiber der Seiten behalten sich ausdrücklich rechtliche Schritte im Falle der unverlangten Zusendung von Werbeinformationen, etwa durch Spam-Mails, vor.''',
                'order': 5
            }
        ]
        
        for content_data in impressum_content:
            content, created = ImpressumContent.objects.get_or_create(
                title=content_data['title'],
                defaults={
                    'content': content_data['content'],
                    'order': content_data['order'],
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(f'Created Impressum content: {content_data["title"]}')
            else:
                self.stdout.write(f'Impressum content already exists: {content_data["title"]}')
        
        self.stdout.write(self.style.SUCCESS('Sample Impressum content added successfully!'))
        self.stdout.write('You can now edit the Impressum content through the admin panel.') 
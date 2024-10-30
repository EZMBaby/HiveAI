class CommandList:
    def __init__(self):
        self.help = [
        '/help', '/h', '/?', 'Welche Kommandos stehen zur Verfügung?',
        ]
        self.exit = [
            '/exit', '/e', '/quit', '/q', 'beenden'
        ]
        self.find = [
            '/find', '/suche', '/suchen', '/search', '/s', 'suche', 'suchen', 'search',
        ]
        self.weather = [
            'weather', '/weather', 'wetter', '/wetter', 'wetterbericht', '/wetterbericht',
        ]

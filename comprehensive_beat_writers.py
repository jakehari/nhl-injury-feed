def get_comprehensive_beat_writers():
    """Comprehensive NHL beat writer database organized by team and major networks."""
    beat_writers = {
        # National/Network Writers
        'national': [
            {'name': 'Elliotte Friedman', 'handle': '@FriedgeHNIC', 'outlet': 'Sportsnet', 'specialty': 'All teams, breaking news'},
            {'name': 'Darren Dreger', 'handle': '@DarrenDreger', 'outlet': 'TSN', 'specialty': 'All teams, insider'},
            {'name': 'Pierre LeBrun', 'handle': '@PierreVLeBrun', 'outlet': 'TSN/The Athletic', 'specialty': 'All teams'},
            {'name': 'Chris Johnston', 'handle': '@reporterchris', 'outlet': 'Sportsnet', 'specialty': 'All teams'},
            {'name': 'Frank Seravalli', 'handle': '@frank_seravalli', 'outlet': 'Daily Faceoff', 'specialty': 'All teams, trades'},
            {'name': 'Emily Kaplan', 'handle': '@emilymkaplan', 'outlet': 'ESPN', 'specialty': 'All teams'},
            {'name': 'Kevin Weekes', 'handle': '@KevinWeekes', 'outlet': 'ESPN/NHL Network', 'specialty': 'All teams'},
            {'name': 'Bob McKenzie', 'handle': '@TSNBobMcKenzie', 'outlet': 'TSN', 'specialty': 'All teams'},
            {'name': 'John Shannon', 'handle': '@JShannonhl', 'outlet': 'Sportsnet', 'specialty': 'All teams'},
            {'name': 'Jeff Marek', 'handle': '@JeffMarek', 'outlet': 'Sportsnet', 'specialty': 'All teams'},
        ],

        # Atlantic Division
        'BOS': [
            {'name': 'Conor Ryan', 'handle': '@ConorRyan_93', 'outlet': 'Boston Sports Journal', 'specialty': 'Bruins'},
            {'name': 'Fluto Shinzawa', 'handle': '@FlutoShinzawa', 'outlet': 'The Athletic', 'specialty': 'Bruins'},
            {'name': 'Matt Porter', 'handle': '@mattyports', 'outlet': 'Boston Globe', 'specialty': 'Bruins'},
        ],
        'BUF': [
            {'name': 'John Vogl', 'handle': '@JohnVogl', 'outlet': 'The Athletic', 'specialty': 'Sabres'},
            {'name': 'Lance Lysowski', 'handle': '@LLysowski', 'outlet': 'Buffalo News', 'specialty': 'Sabres'},
            {'name': 'Mike Harrington', 'handle': '@ByMHarrington', 'outlet': 'Buffalo News', 'specialty': 'Sabres'},
        ],
        'DET': [
            {'name': 'Max Bultman', 'handle': '@m_bultman', 'outlet': 'The Athletic', 'specialty': 'Red Wings'},
            {'name': 'Helene St. James', 'handle': '@HeleneStJames', 'outlet': 'Detroit Free Press', 'specialty': 'Red Wings'},
            {'name': 'Ted Kulfan', 'handle': '@tkulfan', 'outlet': 'Detroit News', 'specialty': 'Red Wings'},
        ],
        'FLA': [
            {'name': 'George Richards', 'handle': '@GeorgeRichards', 'outlet': 'Florida Hockey Now', 'specialty': 'Panthers'},
            {'name': 'Jameson Olive', 'handle': '@JamesonCoop', 'outlet': 'The Athletic', 'specialty': 'Panthers'},
        ],
        'MTL': [
            {'name': 'Arpon Basu', 'handle': '@ArponBasu', 'outlet': 'The Athletic', 'specialty': 'Canadiens'},
            {'name': 'Stu Cowan', 'handle': '@StuCowan1', 'outlet': 'Montreal Gazette', 'specialty': 'Canadiens'},
            {'name': 'Eric Engels', 'handle': '@EricEngels', 'outlet': 'Sportsnet', 'specialty': 'Canadiens'},
        ],
        'OTT': [
            {'name': 'Bruce Garrioch', 'handle': '@SunGarrioch', 'outlet': 'Ottawa Sun', 'specialty': 'Senators'},
            {'name': 'Ian Mendes', 'handle': '@ian_mendes', 'outlet': 'The Athletic', 'specialty': 'Senators'},
        ],
        'TBL': [
            {'name': 'Joe Smith', 'handle': '@JoeSmithTB', 'outlet': 'The Athletic', 'specialty': 'Lightning'},
            {'name': 'Eduardo Encina', 'handle': '@EduardoEncina', 'outlet': 'Tampa Bay Times', 'specialty': 'Lightning'},
        ],
        'TOR': [
            {'name': 'Jonas Siegel', 'handle': '@jonassiegel', 'outlet': 'The Athletic', 'specialty': 'Maple Leafs'},
            {'name': 'Kristen Shilton', 'handle': '@kristen_shilton', 'outlet': 'TSN', 'specialty': 'Maple Leafs'},
            {'name': 'Luke Fox', 'handle': '@lukefoxjukebox', 'outlet': 'Sportsnet', 'specialty': 'Maple Leafs'},
            {'name': 'David Alter', 'handle': '@dalter', 'outlet': 'The Hockey News', 'specialty': 'Maple Leafs'},
        ],

        # Metropolitan Division
        'CAR': [
            {'name': 'Chip Alexander', 'handle': '@ice_chip', 'outlet': 'News & Observer', 'specialty': 'Hurricanes'},
            {'name': 'Luke DeCock', 'handle': '@LukeDeCock', 'outlet': 'News & Observer', 'specialty': 'Hurricanes'},
        ],
        'CBJ': [
            {'name': 'Aaron Portzline', 'handle': '@Aportzline', 'outlet': 'The Athletic', 'specialty': 'Blue Jackets'},
            {'name': 'Brian Hedger', 'handle': '@BrianHedger', 'outlet': 'Columbus Dispatch', 'specialty': 'Blue Jackets'},
        ],
        'NJD': [
            {'name': 'Corey Masisak', 'handle': '@cmasisak22', 'outlet': 'The Athletic', 'specialty': 'Devils'},
            {'name': 'Amanda Stein', 'handle': '@amandacstein', 'outlet': 'MSG Networks', 'specialty': 'Devils'},
        ],
        'NYI': [
            {'name': 'Arthur Staple', 'handle': '@StapeAthletic', 'outlet': 'The Athletic', 'specialty': 'Islanders'},
            {'name': 'Andrew Gross', 'handle': '@AGrossRecord', 'outlet': 'Newsday', 'specialty': 'Islanders'},
        ],
        'NYR': [
            {'name': 'Mollie Walker', 'handle': '@MollieeWalkerr', 'outlet': 'New York Post', 'specialty': 'Rangers'},
            {'name': 'Vincent Mercogliano', 'handle': '@vzmercogliano', 'outlet': 'USA Today', 'specialty': 'Rangers'},
            {'name': 'Peter Baugh', 'handle': '@PeterBaugh13', 'outlet': 'The Athletic', 'specialty': 'Rangers'},
        ],
        'PHI': [
            {'name': 'Jordan Hall', 'handle': '@JHallNBCS', 'outlet': 'NBC Sports Philadelphia', 'specialty': 'Flyers'},
            {'name': 'Kevin Kurz', 'handle': '@KKurzNHL', 'outlet': 'The Athletic', 'specialty': 'Flyers'},
        ],
        'PIT': [
            {'name': 'Josh Yohe', 'handle': '@JoshYohe_PGH', 'outlet': 'The Athletic', 'specialty': 'Penguins'},
            {'name': 'Mike DeFabo', 'handle': '@MikeDeFabo', 'outlet': 'Pittsburgh Post-Gazette', 'specialty': 'Penguins'},
        ],
        'WSH': [
            {'name': 'Tarik El-Bashir', 'handle': '@Tarik_ElBashir', 'outlet': 'The Athletic', 'specialty': 'Capitals'},
            {'name': 'Samantha Pell', 'handle': '@SamanthaJPell', 'outlet': 'Washington Post', 'specialty': 'Capitals'},
        ],

        # Central Division
        'CHI': [
            {'name': 'Mark Lazerus', 'handle': '@MarkLazerus', 'outlet': 'The Athletic', 'specialty': 'Blackhawks'},
            {'name': 'Ben Pope', 'handle': '@BenPopeCST', 'outlet': 'Chicago Sun-Times', 'specialty': 'Blackhawks'},
        ],
        'COL': [
            {'name': 'Peter Baugh', 'handle': '@PeterBaugh13', 'outlet': 'The Athletic', 'specialty': 'Avalanche'},
            {'name': 'Mike Chambers', 'handle': '@MikeChambers', 'outlet': 'Denver Post', 'specialty': 'Avalanche'},
        ],
        'DAL': [
            {'name': 'Matthew DeFranks', 'handle': '@MDeFranks', 'outlet': 'Dallas Morning News', 'specialty': 'Stars'},
            {'name': 'Saad Yousuf', 'handle': '@SaadYousuf126', 'outlet': 'The Athletic', 'specialty': 'Stars'},
        ],
        'MIN': [
            {'name': 'Michael Russo', 'handle': '@RussoHockey', 'outlet': 'The Athletic', 'specialty': 'Wild'},
            {'name': 'Jessi Pierce', 'handle': '@jessipierce', 'outlet': 'The Hockey News', 'specialty': 'Wild'},
        ],
        'NSH': [
            {'name': 'Adam Vingan', 'handle': '@AdamVingan', 'outlet': 'The Athletic', 'specialty': 'Predators'},
            {'name': 'Paul Skrbina', 'handle': '@PaulSkrbina', 'outlet': 'Tennessean', 'specialty': 'Predators'},
        ],
        'STL': [
            {'name': 'Jeremy Rutherford', 'handle': '@jprutherford', 'outlet': 'The Athletic', 'specialty': 'Blues'},
            {'name': 'Lou Korac', 'handle': '@lkorac10', 'outlet': 'NHL.com', 'specialty': 'Blues'},
        ],
        'UTA': [
            {'name': 'Jose M. Romero', 'handle': '@RomeroJoseM', 'outlet': 'The Athletic', 'specialty': 'Utah HC'},
        ],
        'WPG': [
            {'name': 'Murat Ates', 'handle': '@WPGMurat', 'outlet': 'The Athletic', 'specialty': 'Jets'},
            {'name': 'Mike McIntyre', 'handle': '@mikemcintyrewpg', 'outlet': 'Winnipeg Free Press', 'specialty': 'Jets'},
        ],

        # Pacific Division
        'ANA': [
            {'name': 'Eric Stephens', 'handle': '@icemancometh', 'outlet': 'The Athletic', 'specialty': 'Ducks'},
        ],
        'CGY': [
            {'name': 'Salim Valji', 'handle': '@salimvalji', 'outlet': 'The Athletic', 'specialty': 'Flames'},
            {'name': 'Pat Steinberg', 'handle': '@Fan960Steinberg', 'outlet': 'Sportsnet 960', 'specialty': 'Flames'},
        ],
        'EDM': [
            {'name': 'Daniel Nugent-Bowman', 'handle': '@DNBsports', 'outlet': 'The Athletic', 'specialty': 'Oilers'},
            {'name': 'Jim Matheson', 'handle': '@NHLbyMatty', 'outlet': 'Edmonton Journal', 'specialty': 'Oilers'},
        ],
        'LAK': [
            {'name': 'Lisa Dillman', 'handle': '@reallisa', 'outlet': 'The Athletic', 'specialty': 'Kings'},
            {'name': 'Dennis Bernstein', 'handle': '@DennisTFP', 'outlet': 'The Fourth Period', 'specialty': 'Kings'},
        ],
        'SJS': [
            {'name': 'Kevin Kurz', 'handle': '@KKurzNHL', 'outlet': 'The Athletic', 'specialty': 'Sharks'},
            {'name': 'Sheng Peng', 'handle': '@Sheng_Peng', 'outlet': 'San Jose Hockey Now', 'specialty': 'Sharks'},
        ],
        'SEA': [
            {'name': 'Ryan S. Clark', 'handle': '@ryan_s_clark', 'outlet': 'The Athletic', 'specialty': 'Kraken'},
            {'name': 'Geoff Baker', 'handle': '@GeoffBakerTimes', 'outlet': 'Seattle Times', 'specialty': 'Kraken'},
        ],
        'VAN': [
            {'name': 'Thomas Drance', 'handle': '@ThomasDrance', 'outlet': 'The Athletic', 'specialty': 'Canucks'},
            {'name': 'Iain MacIntyre', 'handle': '@imacSportsnet', 'outlet': 'Sportsnet', 'specialty': 'Canucks'},
        ],
        'VGK': [
            {'name': 'Jesse Granger', 'handle': '@JesseGranger_', 'outlet': 'The Athletic', 'specialty': 'Golden Knights'},
            {'name': 'David Schoen', 'handle': '@DavidSchoenLVRJ', 'outlet': 'Las Vegas Review-Journal', 'specialty': 'Golden Knights'},
        ],
    }
    return beat_writers


def get_all_writers_flat():
    """Get all writers in a flat list for monitoring."""
    writers_db = get_comprehensive_beat_writers()
    all_writers = []
    for category, writers in writers_db.items():
        for writer in writers:
            w = writer.copy()
            w['category'] = category
            all_writers.append(w)
    return all_writers


def get_writers_by_team(team_code):
    """Get writers for a specific team (team writers + national writers)."""
    writers_db = get_comprehensive_beat_writers()
    team_writers = writers_db.get(team_code, [])
    national_writers = writers_db.get('national', [])
    return team_writers + national_writers

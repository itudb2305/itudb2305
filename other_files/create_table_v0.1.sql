create table competitions(
	competition_id varchar(50),
    competition_code varchar(50),
    competitions_name text,
    sub_type varchar(50),
    competitions_type varchar(50),
    country_id int,
    country_name varchar(50),
    domestic_league_code varchar(50),
    confederation varchar(50),
    url text,
    PRIMARY KEY(competition_id)
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\competitions.csv'
INTO TABLE competitions
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table clubs (
	club_id int,
    club_code text,
    clubs_name text,
    domestic_competition_id varchar(50),
    total_market_value text,
    squad_size int,
    average_age varchar(50),
    foreigners_number int,
    foreigners_percentage varchar(50),
    national_team_players int,
    stadium_name text,
    stadium_seats int,
    net_transfer_record text,
    coach_name text,
    last_season int,
    url text,
    PRIMARY KEY (club_id),
    FOREIGN KEY (domestic_competition_id)
		REFERENCES competitions(competition_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\clubs.csv'
INTO TABLE clubs
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table players(
	player_id int,
    first_name varchar(50),
    last_name varchar(50),
    players_name varchar(50),
    last_season int,
    current_club_id int,
    player_code varchar(50),
    country_of_birth varchar(50),
    city_of_birth varchar(100),
    country_of_citizenship varchar(50),
    date_of_birth varchar(50),
    sub_position varchar(50),
    position varchar(50),
    foot varchar(50),
    height_in_cm varchar(50),
    market_value_in_eur varchar(50),
    highest_market_value_in_eur varchar(50),
    contract_expiration_date varchar(50),
    agent_name varchar(50),
    image_url text,
    url text,
    current_club_domestic_competition_id varchar(50),
    current_club_name varchar(100),
    PRIMARY KEY (player_id),
    FOREIGN KEY (current_club_id)
		REFERENCES clubs(club_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\players.csv'
INTO TABLE players
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table player_valuations (
	player_id int,
    last_season int,
    player_valuations_datetime datetime,
    player_valuations_date date,
    dateweek date,
    market_value_in_eur int,
    n int,
    current_club_id int,
    player_club_domestic_competition_id varchar(50)
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\player_valuations.csv'
INTO TABLE player_valuations
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table games (
	game_id int,
    competition_id varchar(50),
    season int,
    games_round varchar(50),
    games_date date,
    home_club_id int,
    away_club_id int,
    home_club_goals int,
    away_club_goals int,
    home_club_position varchar(50),
    away_club_position varchar(50),
    home_club_manager_name varchar(50),
    away_club_manager_name varchar(50),
    stadium varchar(100),
    attendance varchar(50),
    referee varchar(50),
    url text,
    home_club_formation varchar(50),
    away_club_formation varchar(50),
    home_club_name varchar(100),
    away_club_name varchar(100),
    games_aggregate varchar(50),
    competition_type varchar(50),
    PRIMARY KEY (game_id),
    FOREIGN KEY (competition_id)
		REFERENCES competitions(competition_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL /*,
    FOREIGN KEY (home_club_id)
		REFERENCES clubs(club_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
	FOREIGN KEY (away_club_id)
		REFERENCES clubs(club_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL*/
    );

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\games.csv'
INTO TABLE games
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table game_events (
	game_event_id varchar(50),
    game_events_date date,
    game_id int,
    minute varchar(50),
    game_events_type varchar(50),
    club_id int,
    player_id int,
    description text,
    player_in_id varchar(50),
    player_assist_id varchar(50) /*,
    FOREIGN KEY (club_id)
		REFERENCES clubs(club_id)
		ON UPDATE CASCADE
        ON DELETE SET NULL,
    FOREIGN KEY (player_id)
		REFERENCES players(player_id)
		ON UPDATE CASCADE
        ON DELETE SET NULL */
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\game_events.csv'
INTO TABLE game_events
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table club_games (
	game_id int,
    club_id int,
    own_goals int,
    own_position varchar(50),
    own_manager_name varchar(50),
    opponent_id int,
    opponent_goals int,
    opponent_position varchar(50),
    opponent_manager_name varchar(50),
    hosting varchar(50),
    is_win int,
    FOREIGN KEY (game_id)
		REFERENCES games(game_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL /*,
		FOREIGN KEY (club_id)
		REFERENCES clubs(club_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
	FOREIGN KEY (opponent_id)
		REFERENCES clubs(club_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL */
);


LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\club_games.csv'
INTO TABLE club_games
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table appearances (
	appearance_id varchar(50),
    game_id int,
    player_id int,
    player_club_id int,
    player_current_club_id int,
    appearances_date date,
    player_name varchar(50),
    competition_id varchar(50),
    yellow_cards int,
    red_cards int,
    goals int,
    assists int,
    minutes_played int,
    PRIMARY KEY (appearance_id),
    FOREIGN KEY (game_id)
		REFERENCES games(game_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL /*,
	FOREIGN KEY (player_id)
		REFERENCES players(player_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL */
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\appearances.csv'
INTO TABLE appearances
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

create table game_lineups (
	game_lineups_id varchar(50),
    game_id int,
    club_id int,
    game_lineups_type varchar(50),
    game_lineups_number varchar(50),
    player_id int,
    player_name varchar(50),
    team_captain int,
    game_lineups_position varchar(50),
    PRIMARY KEY (game_lineups_id),
    FOREIGN KEY (game_id)
		REFERENCES games(game_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL/*,
	FOREIGN KEY (club_id)
		REFERENCES clubs(club_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL,
	FOREIGN KEY (player_id)
		REFERENCES players(player_id)
        ON UPDATE CASCADE
        ON DELETE SET NULL */
);

LOAD DATA INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.2\\Uploads\\futbalmania\\game_lineups.csv'
INTO TABLE game_lineups
COLUMNS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
ESCAPED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES;

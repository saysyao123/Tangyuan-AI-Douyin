PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS accounts (
    account_id TEXT PRIMARY KEY,
    case_id TEXT UNIQUE NOT NULL,
    sec_uid TEXT UNIQUE NOT NULL,
    douyin_id TEXT,
    current_nickname TEXT,
    profile_short_url TEXT,
    role TEXT,
    role_category TEXT,
    trend_weight REAL NOT NULL,
    visual_weight REAL NOT NULL,
    packaging_weight REAL NOT NULL,
    registry_source TEXT NOT NULL,
    r3_test_core INTEGER NOT NULL CHECK (r3_test_core IN (0,1)),
    active INTEGER NOT NULL CHECK (active IN (0,1)),
    last_verified_at TEXT,
    window_15d_complete INTEGER NOT NULL CHECK (window_15d_complete IN (0,1)),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS works (
    aweme_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL REFERENCES accounts(account_id),
    create_time TEXT NOT NULL,
    work_url TEXT NOT NULL,
    caption TEXT,
    type TEXT,
    duration_s REAL,
    music_title_raw TEXT,
    music_author_raw TEXT,
    hashtags TEXT,
    first_observed_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS work_metrics (
    aweme_id TEXT NOT NULL REFERENCES works(aweme_id),
    observed_at TEXT NOT NULL,
    digg_count INTEGER,
    comment_count INTEGER,
    share_count INTEGER,
    collect_count INTEGER,
    play_count INTEGER,
    PRIMARY KEY (aweme_id, observed_at)
);

CREATE TABLE IF NOT EXISTS ingestion_runs (
    run_id TEXT PRIMARY KEY,
    account_id TEXT NOT NULL REFERENCES accounts(account_id),
    window_start TEXT NOT NULL,
    window_end_exclusive TEXT NOT NULL,
    pages_fetched INTEGER NOT NULL,
    items_fetched INTEGER NOT NULL,
    items_in_window INTEGER NOT NULL,
    oldest_fetched TEXT,
    newest_fetched TEXT,
    terminal_has_more INTEGER,
    window_complete INTEGER NOT NULL CHECK (window_complete IN (0,1)),
    stop_reason TEXT,
    error TEXT,
    collector TEXT NOT NULL,
    observed_at TEXT NOT NULL
);

-- R3 correction: normalization is work-level, not raw-music-level.
-- One Douyin original-sound label may contain multiple different SONG_FAMILY values.
CREATE TABLE IF NOT EXISTS song_normalization (
    aweme_id TEXT PRIMARY KEY REFERENCES works(aweme_id),
    song_family TEXT,
    audio_version TEXT,
    normalization_status TEXT NOT NULL,
    confidence REAL,
    evidence_method TEXT,
    reviewed_at TEXT,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_works_account_time ON works(account_id, create_time);
CREATE INDEX IF NOT EXISTS idx_works_music_raw ON works(music_title_raw, music_author_raw);
CREATE INDEX IF NOT EXISTS idx_metrics_aweme_time ON work_metrics(aweme_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_ingestion_account_time ON ingestion_runs(account_id, observed_at);
CREATE INDEX IF NOT EXISTS idx_song_norm_family ON song_normalization(song_family);

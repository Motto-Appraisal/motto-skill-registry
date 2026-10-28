-- motto-skill-registry: memory.db bootstrap schema
-- Structural DDL only. Rows are personal and are NOT shipped; each machine grows its own KB.

CREATE TABLE embeddings (
            fact_id TEXT PRIMARY KEY REFERENCES facts(id) ON DELETE CASCADE,
            vector BLOB NOT NULL
        );

CREATE TABLE facts (
            id TEXT PRIMARY KEY,
            category TEXT NOT NULL,
            content TEXT NOT NULL,
            metadata TEXT DEFAULT '{}',
            created_at TEXT DEFAULT (datetime('now')),
            source TEXT DEFAULT 'rebuild',
            status TEXT DEFAULT 'live',
            relevance INTEGER DEFAULT 1
        , distilled INTEGER DEFAULT 0);

CREATE TABLE fleet_decisions (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    signal_class TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    confidence TEXT NOT NULL,
    confidence_score REAL NOT NULL,
    payoff REAL NOT NULL,
    risk TEXT NOT NULL,
    rationale TEXT,
    quorum_votes TEXT,
    outcome_query_hits INTEGER,
    was_correct INTEGER,
    metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),
    source TEXT DEFAULT 'fleet'
, verdict TEXT, action_inferred TEXT);

CREATE TABLE fleet_outcomes (
    id TEXT PRIMARY KEY,
    decision_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    signal_class TEXT NOT NULL,
    recommendation TEXT NOT NULL,
    handler_session_id TEXT,
    outcome TEXT NOT NULL,
    effective INTEGER DEFAULT 0,
    cost_seconds INTEGER,
    error_count INTEGER,
    human_intervention INTEGER DEFAULT 0,
    metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),
    source TEXT DEFAULT 'fleet'
);

CREATE TABLE fleet_predictions (
    id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    predicted_failure_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    evidence_facts TEXT,
    acted_on INTEGER DEFAULT 0,
    was_correct INTEGER,
    metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),
    source TEXT DEFAULT 'fleet'
);

CREATE TABLE fleet_state_journal (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entry_type TEXT NOT NULL,
    domain TEXT,
    payload TEXT NOT NULL,
    compacted INTEGER DEFAULT 0,
    created_at TEXT DEFAULT (datetime('now')),
    source TEXT DEFAULT 'fleet'
);

CREATE TABLE fleet_strategy (
    id TEXT PRIMARY KEY,
    domain TEXT,
    dimension TEXT NOT NULL,
    value TEXT NOT NULL,
    confidence REAL,
    drift_detected INTEGER DEFAULT 0,
    metadata TEXT DEFAULT '{}',
    created_at TEXT DEFAULT (datetime('now')),
    source TEXT DEFAULT 'fleet'
);

CREATE INDEX idx_facts_category ON facts(category);

CREATE INDEX idx_facts_category_status ON facts(category, status);

CREATE INDEX idx_facts_created ON facts(created_at);

CREATE INDEX idx_facts_relevance ON facts(relevance);

CREATE INDEX idx_facts_status ON facts(status);

CREATE INDEX idx_fleet_decisions_created_at ON fleet_decisions(created_at);

CREATE INDEX idx_fleet_decisions_domain ON fleet_decisions(domain);

CREATE INDEX idx_fleet_outcomes_created_at ON fleet_outcomes(created_at);

CREATE INDEX idx_fleet_outcomes_decision_id ON fleet_outcomes(decision_id);

CREATE INDEX idx_fleet_outcomes_domain ON fleet_outcomes(domain);

CREATE INDEX idx_fleet_predictions_created_at ON fleet_predictions(created_at);

CREATE INDEX idx_fleet_predictions_domain ON fleet_predictions(domain);

CREATE INDEX idx_fleet_state_journal_compacted ON fleet_state_journal(compacted);

CREATE INDEX idx_fleet_state_journal_created_at ON fleet_state_journal(created_at);

CREATE INDEX idx_fleet_state_journal_domain ON fleet_state_journal(domain);

CREATE INDEX idx_fleet_state_journal_entry_type ON fleet_state_journal(entry_type);

CREATE INDEX idx_fleet_strategy_created_at ON fleet_strategy(created_at);

CREATE INDEX idx_fleet_strategy_dimension ON fleet_strategy(dimension);

CREATE INDEX idx_fleet_strategy_domain ON fleet_strategy(domain);

CREATE TABLE kb_capabilities (
        action TEXT PRIMARY KEY,
        primary_path TEXT,
        latency TEXT,
        fallback TEXT,
        notes TEXT,
        category TEXT
    );

CREATE TABLE kb_credentials (
        what TEXT PRIMARY KEY,
        doppler_project TEXT,
        doppler_config TEXT,
        key_name TEXT
    );

CREATE TABLE kb_deprecations (
        name TEXT PRIMARY KEY,
        reason TEXT,
        superseded_by TEXT,
        archived_date TEXT
    );

CREATE TABLE kb_error_patterns (
        pattern TEXT,
        sessions INTEGER,
        action TEXT,
        last_seen TEXT
    );

CREATE TABLE kb_services (
        name TEXT,
        machine TEXT,
        url TEXT,
        purpose TEXT,
        category TEXT,
        PRIMARY KEY (name, machine)
    );

CREATE TABLE session_summaries (
            session_id TEXT PRIMARY KEY,
            summary_json TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            source TEXT DEFAULT 'rebuild'
        );

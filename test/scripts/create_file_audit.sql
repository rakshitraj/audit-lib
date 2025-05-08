CREATE SCHEMA IF NOT EXISTS data_store;

CREATE TABLE IF NOT EXISTS data_store.file_audit (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_id VARCHAR,
    target_layer VARCHAR,
    src_record_count INTEGER,
    target_record_count INTEGER,
    src_file VARCHAR,
    target_file VARCHAR,
    src_archive_file VARCHAR,
    transaction_trail VARCHAR,
    created_by VARCHAR,
    status VARCHAR,
    job_id VARCHAR,
    run_id VARCHAR,
    src_layer VARCHAR,
    target_archive_file VARCHAR,
    updated_by VARCHAR,
    created_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

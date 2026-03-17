CREATE SCHEMA auth;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

SET search_path TO auth;

CREATE TYPE user_status AS ENUM (
    'active',       -- simple user
    'inactive',     -- not verified email or disabled
    'suspended',    -- blocked
    'deleted'       -- soft delete
);

CREATE TABLE users (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  public_id TEXT UNIQUE NOT NULL DEFAULT encode(public.gen_random_bytes(12), 'hex'),
  login TEXT NOT NULL UNIQUE,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  status user_status NOT NULL DEFAULT 'inactive',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);


CREATE TABLE profile (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  age INT,
  about TEXT,
  avatar TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE devices (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  device_uuid TEXT NOT NULL,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  name TEXT,
  user_agent TEXT,
  last_ip INET,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  last_seen_at TIMESTAMPTZ
);

CREATE TABLE refresh_tokens (
  id BIGSERIAL NOT NULL PRIMARY KEY,
  device_id BIGINT NOT NULL REFERENCES devices(id) ON DELETE CASCADE,
  token_hash TEXT NOT NULL,
  expires_at TIMESTAMPTZ NOT NULL,
  revoked BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
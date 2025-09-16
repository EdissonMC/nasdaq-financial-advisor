import os
import sys
import time

def main():
    # Avoid pgpass interference (Windows: NUL)
    os.environ.setdefault("PGPASSFILE", "NUL")

    try:
        import psycopg2
        from psycopg2 import sql
    except Exception as e:
        print("ERROR: psycopg2 no está instalado en este entorno.")
        print(str(e))
        sys.exit(2)

    # Prefer IPv4 loopback to avoid IPv6 (::1) resolutions of 'localhost' hitting a different local server
    host_env = os.getenv("POSTGRES_HOST")
    host_candidates = []
    if host_env:
        host_candidates.append(host_env)
    # Try common options in order
    host_candidates.extend(["127.0.0.1", "localhost"])  # IPv4 first, then name
    port = int(os.getenv("POSTGRES_PORT", "5432"))
    user = os.getenv("POSTGRES_USER", "chatapi_user")
    password = os.getenv("POSTGRES_PASSWORD", "chatapi_password")
    dbname = os.getenv("POSTGRES_DB", "chatapi_db")

    last_error = None
    for host in host_candidates:
        dsn = f"host={host} port={port} dbname={dbname} user={user} password={password} options='-c client_encoding=UTF8'"
        print("Intentando conectar a Postgres…")
        print(f"  host={host} port={port} dbname={dbname} user={user}")
        try:
            conn = psycopg2.connect(dsn)
            conn.autocommit = True
            with conn.cursor() as cur:
                cur.execute("SELECT version(), current_database(), current_user, inet_server_addr(), inet_server_port(), current_setting('server_encoding')")
                version, current_db, current_user, server_addr, server_port, server_enc = cur.fetchone()
                print("Conexión EXITOSA ✅")
                print(f"  version: {version}")
                print(f"  database: {current_db}")
                print(f"  user: {current_user}")
                print(f"  server: {server_addr}:{server_port}")
                print(f"  server_encoding: {server_enc}")
            conn.close()
            sys.exit(0)
        except Exception as e:
            print("Conexión FALLIDA ❌")
            print(repr(e))
            last_error = e
            continue

    # If we reach here, all attempts failed
    msg = str(last_error) if last_error else "Unknown error"
    try:
        msg.encode('ascii')
        print("  Nota: Mensaje de error ASCII")
    except UnicodeEncodeError:
        print("  Nota: Mensaje de error contiene caracteres NO ASCII ⚠️")
    for name in ["POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB", "PGPASSFILE"]:
        val = os.getenv(name, "<unset>")
        try:
            val.encode('ascii')
            flag = 'ASCII'
        except Exception:
            flag = 'NON-ASCII ⚠️'
        display = val if name != "POSTGRES_PASSWORD" else "***"
        print(f"  {name}={display} [{flag}]")
    sys.exit(1)

if __name__ == "__main__":
    main()

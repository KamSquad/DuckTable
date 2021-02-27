database_init_script = """
            -- init tables
            drop table if exists tables;
            CREATE TABLE tables
            (id integer primary key autoincrement not null,
            msg_id text not null,
            
            datetime text not null,
            univer text not null,
            fak text not null,
            
            --object json not null,
            in_queue text not null);
            -- init default values
            --INSERT INTO tables (msg_id, object, in_queue)
            --VALUES ('0', '{"test": "ok"}', 'true');
            """

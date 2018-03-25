
```
sqlite3 db.sqlite3 
SQLite version 3.19.3 2017-06-27 16:48:08
Enter ".help" for usage hints.
sqlite> .tables
auth_group                  django_admin_log          
auth_group_permissions      django_content_type       
auth_permission             django_migrations         
auth_user                   django_session            
auth_user_groups            toys_toys                 
auth_user_user_permissions
sqlite> 



sqlite> .schema toys_toys
CREATE TABLE IF NOT EXISTS "toys_toy" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "created" datetime NOT NULL, "name" varchar(150) NOT NULL, "description" varchar(250) NOT NULL, "toy_category" varchar(200) NOT NULL, "release_date" datetime NOT NULL, "was_included_in_home" bool NOT NULL);

```

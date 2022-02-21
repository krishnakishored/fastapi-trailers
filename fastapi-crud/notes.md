1. **Data from User through API into the database**
    - Database definition ------ database.py
    - Model definition ------ models.py (type of data that goes into the database)
    - create database ------ main.py
    - schema definition ------ schemas.py (type of data that will carry the info from the user to API)
    - ORM functionality ------ db_user.py (performs the operation of putting the data in the database)
    - API functionality ------ user.py

    - Process
        1. Create database definition and run it in main.py
        2. Create database models(tables)
        3. Create functionality to write to the database
        4. Create Schemas
            - Data from user
            - Response to user
        5. Create API operation
### References

1. https://www.youtube.com/watch?v=neW9Y9xh4jc
1. https://www.youtube.com/watch?v=dfyB_ZVQ2jE
1. https://www.youtube.com/watch?v=i35OSGXt7wk
1. https://www.learndatasci.com/tutorials/using-databases-python-postgres-sqlalchemy-and-alembic/
1. https://www.youtube.com/watch?v=5-4W3m5gRAs
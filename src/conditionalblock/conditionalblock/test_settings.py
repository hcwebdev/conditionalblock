# Database settings - one of 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'
DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'testdb.sqlite3'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

INSTALLED_APPS = (
    # Put any other apps that your app depends on here
    'conditionalblock',
)
SITE_ID = 1

# This merely needs to be present - as long as your test case specifies a
# urls attribute, it does not need to be populated.
ROOT_URLCONF = ''
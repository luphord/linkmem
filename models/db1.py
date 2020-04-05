import datetime, uuid

db.define_table('profile',
    Field('identifier', 'string', writable=False, default=lambda: str(uuid.uuid4()), unique=True),
    Field('label', 'string'),
    auth.signature)

db.define_table('linkstore',
    Field('url', 'string', requires=[IS_NOT_EMPTY(), IS_URL(mode='generic')]),
    Field('title', 'string'),
    Field('excerpt', 'text'),
    Field('tags', 'list:string'),
    Field('profile', db.profile, writable=False, readable=False),
    auth.signature)

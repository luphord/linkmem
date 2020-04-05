# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    return locals()

@auth.requires_login()
def show():
    link = db.linkstore(request.args(0, cast=int)) or redirect(URL('index'))
    return locals()

@auth.requires_login()
def links():
    links = db(db.linkstore.created_by == auth.user).select(orderby=~db.linkstore.modified_on)
    return locals()

@auth.requires_login()
def profiles():
    grid = SQLFORM.smartgrid(db.profile, linked_tables=[])
    return locals()

@auth.requires_login()
def bookmarklets():
    rows = db(db.profile.created_by == auth.user).select()
    return locals()

def store():
    profile = db.profile(db.profile.identifier == request.args(0)) or redirect(URL('index'))
    db.linkstore.profile.default = profile.id
    db.linkstore.url.default = request.vars.get('url')
    db.linkstore.title.default = request.vars.get('title')
    db.linkstore.excerpt.default = request.vars.get('text')
    db.linkstore.created_by.default = profile.created_by
    db.linkstore.modified_by.default = profile.created_by
    form = SQLFORM(db.linkstore)
    if form.process().accepted:
        redirect(URL('links'))
    elif form.errors:
        response.flash = 'Errors in the form'
    else:
        response.flash = 'Please fill out the form'
    return locals()

# ---- API (example) -----
@auth.requires_login()
def api_get_user_email():
    if not request.env.request_method == 'GET': raise HTTP(403)
    return response.json({'status':'success', 'email':auth.user.email})

# ---- Smart Grid (example) -----
@auth.requires_membership('admin') # can only be accessed by members of admin groupd
def grid():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
    return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu() # add the wiki to the menu
    return auth.wiki()

# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())

# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

import datetime

from flask import current_app as app
from flask import jsonify
from models import db, CatalogOperations, CatalogUserRoles, RTCOnlineUsers, User, UserXRole

# -----------------------------------------------------------------------------------------------------
# DATABASE MINIMUM REQUIRED DATA
# POPULATION FUNCTIONS
# -----------------------------------------------------------------------------------------------------

# Initialize Database Populate Function
def initPopulateDB():
    # Add Operations Catalog
    populateCatalogOperations()

    # Add User Roles Catalog
    populateCatalogUserRoles()

    # Add Default Users
    populateDefaultUsers()

    # Add Default RTC_OUL
    populateDefaultRTC_OUL()


# Populate Default RTC Online User List
def populateDefaultRTC_OUL():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Default RTC Online User List')

        #Add Default RTC_OUL JSON
        nowdt = datetime.datetime.utcnow()
        operation = CatalogOperations.query.filter_by(name_short='ins').first()

        rtc_oul = RTCOnlineUsers()
        rtc_oul.id = nowdt
        rtc_oul.operation_id = operation.id
        rtc_oul.userlist = {
            'rtc_online_users': {
                'id': str(nowdt),
                'anon_users': [],
                'emp_users': [],
                'reg_users': []
            }
        }
        rtc_oul.enabled = True
        db.session.add(rtc_oul)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Default RTC Online User List Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Default Users
def populateDefaultUsers():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Default Users')

        # Add Admin User
        admin_user = User()
        admin_user.uid = 'CON-Administrator'
        admin_user.email = 'admusr@conecta.gob.hn'
        admin_user.name = 'Administrador CONECTA'
        admin_user.cmuserid = 'CON-ADM-200000-0001'
        db.session.add(admin_user)
        db.session.flush()
        # Add Admin Role
        admin_role = CatalogUserRoles.query.filter_by(name_short='adm').first()
        admin_userxrole = UserXRole()
        admin_userxrole.user_id = admin_user.id
        admin_userxrole.user_role_id = admin_role.id
        db.session.add(admin_userxrole)

        db.session.commit()

        # Add Anon User
        anon_user = User()
        anon_user.uid = 'CON-Anonim@'
        anon_user.email = 'anon@conecta.gob.hn'
        anon_user.name = 'Anonim@'
        anon_user.cmuserid = 'CON-ANN-200000-0001'
        db.session.add(anon_user)
        db.session.flush()
        # Add User Role
        user_role = CatalogUserRoles.query.filter_by(name_short='usr').first()
        anon_userxrole = UserXRole()
        anon_userxrole.user_id = anon_user.id
        anon_userxrole.user_role_id = user_role.id
        db.session.add(anon_userxrole)

        db.session.commit()

        # Add Advisor User
        advisor_user = User()
        advisor_user.uid = 'CON-Orientadora'
        advisor_user.email = 'orientadora@conecta.gob.hn'
        advisor_user.name = 'Orientadora CONECTA'
        advisor_user.cmuserid = 'CON-ORI-200000-0001'
        db.session.add(advisor_user)
        db.session.flush()
        # Add Advisor Role
        advisor_role = CatalogUserRoles.query.filter_by(name_short='ori').first()
        advisor_userxrole = UserXRole()
        advisor_userxrole.user_id = advisor_user.id
        advisor_userxrole.user_role_id = advisor_role.id
        db.session.add(advisor_userxrole)

        db.session.commit()

        # Add Lawyer User
        lawyer_user = User()
        lawyer_user.uid = 'CON-Abogada'
        lawyer_user.email = 'abogada@conecta.gob.hn'
        lawyer_user.name = 'Abogada CONECTA'
        lawyer_user.cmuserid = 'CON-ABO-200000-0001'
        db.session.add(lawyer_user)
        db.session.flush()
        # Add Lawyer Role
        lawyer_role = CatalogUserRoles.query.filter_by(name_short='abo').first()
        lawyer_userxrole = UserXRole()
        lawyer_userxrole.user_id = lawyer_user.id
        lawyer_userxrole.user_role_id = lawyer_role.id
        db.session.add(lawyer_userxrole)

        db.session.commit()

        # Add Psychologist User
        psy_user = User()
        psy_user.uid = 'CON-Psychologist'
        psy_user.email = 'psicologa@conecta.gob.hn'
        psy_user.name = 'Psicologa CONECTA'
        psy_user.cmuserid = 'CON-PSY-200000-0001'
        db.session.add(psy_user)
        db.session.flush()
        # Add Psychologist Role
        psy_role = CatalogUserRoles.query.filter_by(name_short='psi').first()
        psy_userxrole = UserXRole()
        psy_userxrole.user_id = psy_user.id
        psy_userxrole.user_role_id = psy_role.id
        db.session.add(psy_userxrole)

        db.session.commit()

        # Add Social Worker User
        social_user = User()
        social_user.uid = 'CON-TrabajadoraSocial'
        social_user.email = 'social@conecta.gob.hn'
        social_user.name = 'Trabajadora Social CONECTA'
        social_user.cmuserid = 'CON-SOC-200000-0001'
        db.session.add(social_user)
        db.session.flush()
        # Add Social Worker Role
        social_role = CatalogUserRoles.query.filter_by(name_short='soc').first()
        social_userxrole = UserXRole()
        social_userxrole.user_id = social_user.id
        social_userxrole.user_role_id = social_role.id
        db.session.add(social_userxrole)

        db.session.commit()

        # Add Coordinator User
        coor_user = User()
        coor_user.uid = 'CON-Coordinadora'
        coor_user.email = 'coordinadora@conecta.gob.hn'
        coor_user.name = 'Coordinadora CONECTA'
        coor_user.cmuserid = 'CON-COO-200000-0001'
        db.session.add(coor_user)
        db.session.flush()
        # Add Coordinator Role
        coor_role = CatalogUserRoles.query.filter_by(name_short='coo').first()
        coor_userxrole = UserXRole()
        coor_userxrole.user_id = coor_user.id
        coor_userxrole.user_role_id = coor_role.id
        db.session.add(coor_userxrole)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Default Users Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Catalog Operations Data
def populateCatalogOperations():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Catalog Operations')

        # Add Operation
        insert = CatalogOperations(name='Inserción', name_short='ins')
        db.session.add(insert)

        delete = CatalogOperations(name='Eliminación', name_short='del')
        db.session.add(delete)

        update = CatalogOperations(name='Actualización', name_short='upd')
        db.session.add(update)

        read = CatalogOperations(name='Lectura', name_short='read')
        db.session.add(read)

        connect = CatalogOperations(name='Conexión', name_short='con')
        db.session.add(connect)

        disconnect = CatalogOperations(name='Desconexión', name_short='dcon')
        db.session.add(disconnect)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Catalog Operations Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


# Populate Catalog User Roles Data
def populateCatalogUserRoles():
    try:
        app.logger.debug('** SWING_CMS ** - Populate Catalog User Roles')

        # Add User Roles
        user_role = CatalogUserRoles(name='Usuario', name_short='usr')
        db.session.add(user_role)

        admin_role = CatalogUserRoles(name='Administrador', name_short='adm')
        db.session.add(admin_role)
        
        counselor_role = CatalogUserRoles(name='Orientadora', name_short='ori')
        db.session.add(counselor_role)

        lawyer_role = CatalogUserRoles(name='Abogada', name_short='abo')
        db.session.add(lawyer_role)

        psych_role = CatalogUserRoles(name='Psicóloga', name_short='psi')
        db.session.add(psych_role)

        social_role = CatalogUserRoles(name='Trabajadora Social', name_short='soc')
        db.session.add(social_role)

        coordinator_role = CatalogUserRoles(name='Coordinadora', name_short='coo')
        db.session.add(coordinator_role)

        db.session.commit()

        return jsonify({ 'status': 'success' })
    except Exception as e:
        app.logger.error('** SWING_CMS ** - Populate Catalog User Roles Error: {}'.format(e))
        return jsonify({ 'status': 'error' })


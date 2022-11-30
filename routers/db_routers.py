class usersRouter:
    route_app_labels = {"users","smsroutes",}

    def db_for_read(self,model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "users_db"
        return None

    def db_for_write(self,model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "users_db"
        return None

    
    # def allow_migrate(self,db,app_label, model_name=None, **hints):
    #     if app_label in self.route_app_labels:
    #         return db == "kannel_db"
    #     return None


class smppRouter:
    route_app_labels = {"smpp","analytics"}

    def db_for_read(self,model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "smpp_db"
        return None

    def db_for_write(self,model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return "smpp_db"
        return None

    
    # def allow_migrate(self,db,app_label, model_name=None, **hints):
    #     if app_label in self.route_app_labels:
    #         return db == "kannel_db"
    #     return None
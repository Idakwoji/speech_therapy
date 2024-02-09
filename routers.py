class PublicTemplatesRouter:
    """
    A router to control all database operations on models in the
    public_templates application.
    """

    app_name = 'public_templates'

    def db_for_read(self, model, **hints):
        """
        Attempts to read public_templates models go to public_templates database.
        """
        if model._meta.app_label == self.app_name:
            return 'public_templates'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write public_templates models go to public_templates database.
        """
        if model._meta.app_label == self.app_name:
            return 'public_templates'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the public_templates app is involved.
        """
        if obj1._meta.app_label == self.app_name or obj2._meta.app_label == self.app_name:
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the public_templates app only appears in the 'public_templates'
        database.
        """
        if app_label == self.app_name:
            return db == 'public_templates'
        return None
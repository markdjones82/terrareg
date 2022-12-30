
import hashlib
import os

from flask import render_template, session

from terrareg.csrf import get_csrf_token
import terrareg.config
from terrareg.models import Namespace, Module, Session


class BaseHandler:
    """Provide base methods for handling requests and serving pages."""

    def _render_template(self, *args, **kwargs):
        """Override render_template, passing in base variables."""
        return render_template(
            *args, **kwargs,
            terrareg_application_name=terrareg.config.Config().APPLICATION_NAME,
            terrareg_logo_url=terrareg.config.Config().LOGO_URL,
            ALLOW_MODULE_HOSTING=terrareg.config.Config().ALLOW_MODULE_HOSTING,
            TRUSTED_NAMESPACE_LABEL=terrareg.config.Config().TRUSTED_NAMESPACE_LABEL,
            CONTRIBUTED_NAMESPACE_LABEL=terrareg.config.Config().CONTRIBUTED_NAMESPACE_LABEL,
            VERIFIED_MODULE_LABEL=terrareg.config.Config().VERIFIED_MODULE_LABEL,
            csrf_token=get_csrf_token()
        )

    def _module_provider_404(self, namespace: Namespace, module: Module,
                             module_provider_name: str):
        return self._render_template(
            'error.html',
            error_title='Module/Provider does not exist',
            error_description='The module {namespace}/{module}/{module_provider_name} does not exist'.format(
                namespace=namespace.name,
                module=module.name,
                module_provider_name=module_provider_name
            ),
            namespace=namespace,
            module=module,
            module_provider_name=module_provider_name
        ), 404

    def create_session(self):
        """Create session for user"""
        if not terrareg.config.Config().SECRET_KEY:
            return None

        # Check if a session already exists and delete it
        if session.get('session_id', None):
            session_obj = Session.check_session(session.get('session_id', None))
            if session_obj:
                session_obj.delete()

        session['csrf_token'] = hashlib.sha1(os.urandom(64)).hexdigest()
        session_obj = Session.create_session()
        session['session_id'] = session_obj.id
        session.modified = True

        # Whilst authenticating a user, piggyback the request
        # to take the opportunity to delete old sessions
        Session.cleanup_old_sessions()

        return session_obj

"""Add tables for provider sources, providers and tables for supporting data for provider versions

Revision ID: ee14b27baeb1
Revises: fb6a94791a14
Create Date: 2023-10-27 07:29:45.605137

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ee14b27baeb1'
down_revision = 'fb6a94791a14'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('provider_analytics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_version_id', sa.Integer(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('terraform_version', sa.String(length=128), nullable=True),
    sa.Column('namespace_name', sa.String(length=128), nullable=True),
    sa.Column('provider_name', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_provider_analytics_provider_version_id'), 'provider_analytics', ['provider_version_id'], unique=False)
    op.create_table('provider_category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('slug', sa.String(length=128), nullable=True),
    sa.Column('user_selectable', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug')
    )
    op.create_table('provider_source',
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('api_name', sa.String(length=128), nullable=True),
    sa.Column('provider_source_type', sa.Enum('GITHUB', name='providersourcetype'), nullable=True),
    sa.Column('config', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.PrimaryKeyConstraint('name')
    )
    op.create_table('gpg_key',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('namespace_id', sa.Integer(), nullable=False),
    sa.Column('ascii_armor', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.Column('key_id', sa.String(length=1024), nullable=True),
    sa.Column('fingerprint', sa.String(length=1024), nullable=True),
    sa.Column('source', sa.String(length=1024), nullable=True),
    sa.Column('source_url', sa.String(length=1024), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['namespace_id'], ['namespace.id'], name='fk_gpg_key_namespace_id_namespace_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('repository',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.String(length=128), nullable=True),
    sa.Column('owner', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.Column('clone_url', sa.String(length=1024), nullable=True),
    sa.Column('logo_url', sa.String(length=1024), nullable=True),
    sa.Column('provider_source_name', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['provider_source_name'], ['provider_source.name'], name='fk_repository_provider_source_name_provider_source_name', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provider',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('namespace_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=True),
    sa.Column('description', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.Column('tier', sa.Enum('OFFICIAL', 'COMMUNITY', name='providertier'), nullable=True),
    sa.Column('default_provider_source_auth', sa.Boolean(), nullable=True),
    sa.Column('provider_category_id', sa.Integer(), nullable=True),
    sa.Column('repository_id', sa.Integer(), nullable=True),
    sa.Column('latest_version_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['latest_version_id'], ['provider_version.id'], name='fk_provider_latest_version_id_provider_version_id', onupdate='CASCADE', ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['namespace_id'], ['namespace.id'], name='fk_provider_namespace_id_namespace_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_category_id'], ['provider_category.id'], name='fk_provider_provider_category_id_provider_category_id', onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['repository_id'], ['repository.id'], name='fk_provider_repository_id_repository_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provider_version',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_id', sa.Integer(), nullable=False),
    sa.Column('gpg_key_id', sa.Integer(), nullable=False),
    sa.Column('version', sa.String(length=128), nullable=True),
    sa.Column('git_tag', sa.String(length=128), nullable=True),
    sa.Column('beta', sa.BOOLEAN(), nullable=False),
    sa.Column('published_at', sa.DateTime(), nullable=True),
    sa.Column('extraction_version', sa.Integer(), nullable=True),
    sa.Column('protocol_versions', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.ForeignKeyConstraint(['gpg_key_id'], ['gpg_key.id'], name='fk_provider_version_gpg_key_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['provider_id'], ['provider.id'], name='fk_provider_version_provider_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provider_version_binary',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_version_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('operating_system', sa.Enum('FREEBSD', 'DARWIN', 'WINDOWS', 'LINUX', name='providerbinaryoperatingsystemtype'), nullable=False),
    sa.Column('architecture', sa.Enum('AMD64', 'ARM', 'ARM64', 'I386', name='providerbinaryarchitecturetype'), nullable=False),
    sa.Column('checksum', sa.String(length=128), nullable=False),
    sa.ForeignKeyConstraint(['provider_version_id'], ['provider_version.id'], name='fk_provider_version_binary_provider_version_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('provider_version_documentation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('provider_version_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('slug', sa.String(length=128), nullable=False),
    sa.Column('title', sa.String(length=128), nullable=True),
    sa.Column('description', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.Column('language', sa.String(length=128), nullable=False),
    sa.Column('subcategory', sa.String(length=128), nullable=True),
    sa.Column('filename', sa.String(length=128), nullable=False),
    sa.Column('documentation_type', sa.Enum('OVERVIEW', 'PROVIDER', 'RESOURCE', 'DATA_SOURCE', 'GUIDE', name='providerdocumentationtype'), nullable=False),
    sa.Column('content', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True),
    sa.ForeignKeyConstraint(['provider_version_id'], ['provider_version.id'], name='fk_provider_version_documentation_provider_version_id', onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('namespace', sa.Column('namespace_type', sa.Enum('NONE', 'GITHUB_USER', 'GITHUB_ORGANISATION', name='namespacetype'), nullable=True))
    bind = op.get_bind()
    bind.execute("UPDATE namespace SET namespace_type='NONE'")
    with op.batch_alter_table("namespace") as batch_op:
        batch_op.alter_column("namespace_type", nullable=False, existing_type=sa.Enum('NONE', 'GITHUB_USER', 'GITHUB_ORGANISATION', name='namespacetype'))

    op.add_column('session', sa.Column('provider_source_auth', sa.LargeBinary(length=16777215).with_variant(mysql.MEDIUMBLOB(), 'mysql'), nullable=True))

    if op.get_bind().engine.name == 'mysql':
        op.alter_column('audit_history', 'action',
            existing_type=sa.Enum(
                'NAMESPACE_CREATE', 'NAMESPACE_MODIFY_NAME', 'NAMESPACE_MODIFY_DISPLAY_NAME', 'MODULE_PROVIDER_CREATE', 'MODULE_PROVIDER_DELETE', 'MODULE_PROVIDER_UPDATE_GIT_TAG_FORMAT',
                'MODULE_PROVIDER_UPDATE_GIT_PROVIDER', 'MODULE_PROVIDER_UPDATE_GIT_PATH', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BASE_URL',
                'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_CLONE_URL', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BROWSE_URL', 'MODULE_PROVIDER_UPDATE_VERIFIED',
                'MODULE_VERSION_INDEX', 'MODULE_VERSION_PUBLISH', 'MODULE_VERSION_DELETE', 'USER_GROUP_CREATE', 'USER_GROUP_DELETE', 'USER_GROUP_NAMESPACE_PERMISSION_ADD',
                'USER_GROUP_NAMESPACE_PERMISSION_MODIFY', 'USER_GROUP_NAMESPACE_PERMISSION_DELETE', 'USER_LOGIN',
                'MODULE_PROVIDER_UPDATE_NAMESPACE', 'MODULE_PROVIDER_UPDATE_MODULE_NAME', 'MODULE_PROVIDER_UPDATE_PROVIDER_NAME', 'NAMESPACE_DELETE', 'MODULE_PROVIDER_REDIRECT_DELETE', name='auditaction'),
            type_=sa.Enum(
                'NAMESPACE_CREATE', 'NAMESPACE_MODIFY_NAME', 'NAMESPACE_MODIFY_DISPLAY_NAME', 'MODULE_PROVIDER_CREATE', 'MODULE_PROVIDER_DELETE', 'MODULE_PROVIDER_UPDATE_GIT_TAG_FORMAT',
                'MODULE_PROVIDER_UPDATE_GIT_PROVIDER', 'MODULE_PROVIDER_UPDATE_GIT_PATH', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BASE_URL',
                'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_CLONE_URL', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BROWSE_URL', 'MODULE_PROVIDER_UPDATE_VERIFIED',
                'MODULE_VERSION_INDEX', 'MODULE_VERSION_PUBLISH', 'MODULE_VERSION_DELETE', 'USER_GROUP_CREATE', 'USER_GROUP_DELETE', 'USER_GROUP_NAMESPACE_PERMISSION_ADD',
                'USER_GROUP_NAMESPACE_PERMISSION_MODIFY', 'USER_GROUP_NAMESPACE_PERMISSION_DELETE', 'USER_LOGIN',
                'MODULE_PROVIDER_UPDATE_NAMESPACE', 'MODULE_PROVIDER_UPDATE_MODULE_NAME', 'MODULE_PROVIDER_UPDATE_PROVIDER_NAME', 'NAMESPACE_DELETE', 'MODULE_PROVIDER_REDIRECT_DELETE',
                'GPG_KEY_CREATE', 'GPG_KEY_DELETE', 'PROVIDER_CREATE', 'PROVIDER_DELETE', 'PROVIDER_VERSION_INDEX', 'PROVIDER_VERSION_DELETE', 'REPOSITORY_CREATE', 'REPOSITORY_UPDATE', 'REPOSITORY_DELETE',
                name='auditaction'),
            nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    if op.get_bind().engine.name == 'mysql':
        op.alter_column('audit_history', 'action',
            existing_type=sa.Enum(
                'NAMESPACE_CREATE', 'NAMESPACE_MODIFY_NAME', 'NAMESPACE_MODIFY_DISPLAY_NAME', 'MODULE_PROVIDER_CREATE', 'MODULE_PROVIDER_DELETE', 'MODULE_PROVIDER_UPDATE_GIT_TAG_FORMAT',
                'MODULE_PROVIDER_UPDATE_GIT_PROVIDER', 'MODULE_PROVIDER_UPDATE_GIT_PATH', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BASE_URL',
                'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_CLONE_URL', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BROWSE_URL', 'MODULE_PROVIDER_UPDATE_VERIFIED',
                'MODULE_VERSION_INDEX', 'MODULE_VERSION_PUBLISH', 'MODULE_VERSION_DELETE', 'USER_GROUP_CREATE', 'USER_GROUP_DELETE', 'USER_GROUP_NAMESPACE_PERMISSION_ADD',
                'USER_GROUP_NAMESPACE_PERMISSION_MODIFY', 'USER_GROUP_NAMESPACE_PERMISSION_DELETE', 'USER_LOGIN',
                'MODULE_PROVIDER_UPDATE_NAMESPACE', 'MODULE_PROVIDER_UPDATE_MODULE_NAME', 'MODULE_PROVIDER_UPDATE_PROVIDER_NAME', 'NAMESPACE_DELETE', 'MODULE_PROVIDER_REDIRECT_DELETE',
                'GPG_KEY_CREATE', 'GPG_KEY_DELETE', 'PROVIDER_CREATE', 'PROVIDER_DELETE', 'PROVIDER_VERSION_INDEX', 'PROVIDER_VERSION_DELETE', 'REPOSITORY_CREATE', 'REPOSITORY_UPDATE', 'REPOSITORY_DELETE',
                name='auditaction'),
            type_=sa.Enum(
                'NAMESPACE_CREATE', 'NAMESPACE_MODIFY_NAME', 'NAMESPACE_MODIFY_DISPLAY_NAME', 'MODULE_PROVIDER_CREATE', 'MODULE_PROVIDER_DELETE', 'MODULE_PROVIDER_UPDATE_GIT_TAG_FORMAT',
                'MODULE_PROVIDER_UPDATE_GIT_PROVIDER', 'MODULE_PROVIDER_UPDATE_GIT_PATH', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BASE_URL',
                'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_CLONE_URL', 'MODULE_PROVIDER_UPDATE_GIT_CUSTOM_BROWSE_URL', 'MODULE_PROVIDER_UPDATE_VERIFIED',
                'MODULE_VERSION_INDEX', 'MODULE_VERSION_PUBLISH', 'MODULE_VERSION_DELETE', 'USER_GROUP_CREATE', 'USER_GROUP_DELETE', 'USER_GROUP_NAMESPACE_PERMISSION_ADD',
                'USER_GROUP_NAMESPACE_PERMISSION_MODIFY', 'USER_GROUP_NAMESPACE_PERMISSION_DELETE', 'USER_LOGIN',
                'MODULE_PROVIDER_UPDATE_NAMESPACE', 'MODULE_PROVIDER_UPDATE_MODULE_NAME', 'MODULE_PROVIDER_UPDATE_PROVIDER_NAME', 'NAMESPACE_DELETE', 'MODULE_PROVIDER_REDIRECT_DELETE', name='auditaction'),
            nullable=False)

    with op.batch_alter_table("session") as batch_op:
        batch_op.drop_column('provider_source_auth')
    with op.batch_alter_table("namespace") as batch_op:
        batch_op.drop_column('namespace_type')
    op.drop_table('provider_version_documentation')
    op.drop_table('provider_version_binary')
    op.drop_table('provider_version')
    op.drop_table('provider')
    op.drop_table('repository')
    op.drop_table('gpg_key')
    op.drop_table('provider_source')
    op.drop_table('provider_category')
    op.drop_index(op.f('ix_provider_analytics_provider_version_id'), table_name='provider_analytics')
    op.drop_table('provider_analytics')
    # ### end Alembic commands ###

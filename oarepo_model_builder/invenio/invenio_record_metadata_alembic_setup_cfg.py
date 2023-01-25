from ..builders import OutputBuilder
from ..builders.utils import ensure_parent_modules
from ..outputs.cfg import CFGOutput
from ..utils.verbose import log


class InvenioRecordMetadataAlembicSetupCfgBuilder(OutputBuilder):
    TYPE = "invenio_record_metadata_alembic_setup_cfg"

    def finish(self):
        super().finish()

        output: CFGOutput = self.builder.get_output("cfg", "setup.cfg")
        output.add_entry_point(
            "invenio_db.alembic",
            self.current_model.record_schema_metadata_alembic,
            f"{self.current_model.package}:alembic",
        )

        python_path = self.current_model.package_path / "alembic" / "__init__.py"
        # create parent modules if they do not exist
        ensure_parent_modules(
            self.builder, python_path, max_depth=len(python_path.parts)
        )

        # and create empty __init__.py
        init_builder = self.builder.get_output("python", python_path)
        if init_builder.created:
            # TODO: replace instructions with running bootstrap script
            log(
                log.INFO,
                f"""Do not forget to run:
    
    # if the initial database does not exist yet 
    invenio db init
    
    # if the tables do not exist yet (that is, after invenio db init); you have to manually remove 
    # {self.current_model.record_metadata_table_name} and its versioned counterpart, otherwise
    # alembic below will not work !
    invenio db create 
            
    # create the branch
    invenio alembic revision "Create {self.current_model.record_schema_metadata_alembic} branch."  -b {self.current_model.record_schema_metadata_alembic} -p dbdbc1b19cf2 --empty
    
    # apply the branch
    invenio alembic upgrade heads
    
    # initial revision
    invenio alembic revision "Initial revision." -b {self.current_model.record_schema_metadata_alembic}
    
    # inspect the generated file and add import sqlalchemy_utils (invenio template does not contain it
    # remove length=16 from UUIDType(length=16), replace Text() with sa.Text()
    
    # create db tables
    invenio alembic upgrade heads
            """,
            )

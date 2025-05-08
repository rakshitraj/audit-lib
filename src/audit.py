from src.include.models.file_audit_orm import FileAudit
from src.include.rdsops import RDSOps

class Audit:
    table = FileAudit.__tablename__

    def capture(self, session, record: dict){
        session = Session()

        rds
        
    }
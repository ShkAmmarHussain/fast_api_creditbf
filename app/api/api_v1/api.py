from fastapi import APIRouter
# from app.api.api_v1.endpoints import users, profile
from app.api.api_v1.endpoints.actionplan_ratio import api_actionplan
from app.api.api_v1.endpoints.actionplan_ratio import api_uratio
from app.api.api_v1.endpoints.audit import audit_api
from app.api.api_v1.endpoints.dispute_letter import dispute_test
from app.api.api_v1.endpoints.report_analysis import api_reportanalysis

api_router = APIRouter()
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(profile.router, prefix="/profile", tags=["profile"])
api_router.include_router(api_actionplan.router, prefix="/actionplan", tags=["actionplan"])
api_router.include_router(api_uratio.router, prefix="/u_ratio", tags=["Utilization Ratio"])
api_router.include_router(audit_api.router, prefix="/audit", tags=["Audit"])
api_router.include_router(dispute_test.router, prefix="/letter", tags=["Dispute Letter"])
api_router.include_router(api_reportanalysis.router, prefix="/analysis", tags=["Report Analysis"])
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from src.apis.v1.models.practices_model import practices
from src.apis.v1.db.session import engine, get_db
from . import oauth2_scheme
from src.apis.v1.controllers.practices_controller import PracticesController
from src.apis.v1.validators.practices_validator import PracticeValidatorIn, PracticeValidatorOut
from src.apis.v1.validators.common_validators import ErrorResponseValidator

router = APIRouter(tags=["practices"])


@router.post("/practices", summary="Create a new practice", responses={201: {"model": PracticeValidatorOut},404: {"model": ErrorResponseValidator, "description": "Error Occured when not found"}, 500: {"description": "Internal Server Error", "model": ErrorResponseValidator}})
async def create_practice(practice_validator: PracticeValidatorIn, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        """
            Create Practice
        """
        resp = PracticesController(db).create_practice(practice_validator.dict())
        return resp


@router.delete("/practices/{practice_id}", summary="Delete a practice", responses={200: {"description": "Delete a practice and all associated applications"}})
async def delete_practice(practice_id: int, token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
     This api deletes the practice and associated apps

    """

    practice_to_delete = PracticesController(db).delete_practice(practice_id)
    return practice_to_delete

# Update Practice ??




    # import pandas as pd

    # df = pd.read_excel (r'List.xlsx')
    # df = pd.DataFrame(df)
    # column = [3 for i in range(41)]
    # # index = [i for i in range(337,378)]
    # df.rename(columns = {'UserRole':'label'}, inplace = True)
    # df = df[91:307]
    # # df['id'] = index
    # # df['name'] = df['label']
    # print(df)
    # print(df[:84])
    # df.to_sql('practices', con=engine, if_exists='append', index=False)
    # db.query(practices).filter_by(sp_apps_id=4).delete()
    # db.commit()



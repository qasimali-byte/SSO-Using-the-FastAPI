from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from src.apis.v1.models.practices_model import practices
from src.apis.v1.db.session import engine, get_db

router = APIRouter(tags=["practices"])

@router.post("/practices", summary="Create a new practice",)
async def create_practices(db: Session = Depends(get_db)):
    """
        Create a new practice
    """
    return 
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



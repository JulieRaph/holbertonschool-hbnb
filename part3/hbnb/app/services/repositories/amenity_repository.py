from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
        
    def get_by_attribute(self, name):
        return self.model.query.filter(Amenity.name.ilike(name)).first()
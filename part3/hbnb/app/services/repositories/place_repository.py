from app.models.place import Place
from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
        
    # def create_place(self, place_data: dict, amenities_ids: list = None) -> Place:
    #     """Creates a new place and adds amenities."""
    #     amenities = []
    #     if amenities_ids:
    #         amenities = Amenity.query.filter(Amenity.id.in_(amenities_ids)).all()

    #     new_place = Place(**place_data)
    #     new_place.amenities.extend(amenities)

    #     db.session.add(new_place)
    #     db.session.commit()
    #     db.session.refresh(new_place)
    #     return new_place
    
    def get_place(place_id, options=None):
        place = Place.query.filter_by(id=place_id)
        if options:
            place = place.options(*options)
        return place.first()
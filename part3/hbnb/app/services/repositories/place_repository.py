from app.models.place import Place
from app.models.amenity import Amenity
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
        
    def add(self, place, amenities):
        db.session.add(place)

        if amenities:
            amenities_ids = []
            for amenity_id in amenities:
                amenity = Amenity.query.filter_by(id=amenity_id).first()
                if amenity:
                    amenities_ids.append(amenity)
                else:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")

            place.place_amenities.extend(amenities_ids)

        db.session.flush()
        db.session.commit()
        return place
    
    def update(self, place_id, place_data, amenities):
        place = self.get(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)

            if amenities is not None:
                place.place_amenities = []
                amenities_ids = []
                for amenity_id in amenities:
                    amenity = Amenity.query.filter_by(id=amenity_id).first()
                    if amenity:
                        amenities_ids.append(amenity)
                    else:
                        raise ValueError(f"Amenity with ID {amenity_id} not found")

                place.place_amenities.extend(amenities_ids)

            db.session.flush()
            db.session.commit()
            return place
        return None 
        
    def get_place(place_id, options=None):
        place = Place.query.filter_by(id=place_id)
        if options:
            place = place.options(*options)
        return place.first()
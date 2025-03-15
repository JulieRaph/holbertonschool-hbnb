from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app import db
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
        
    def add_amenities(self, place, amenities):
        place.place_amenities = []
        amenities_ids = []
        for amenity_id in amenities:
            amenity = Amenity.query.filter_by(id=amenity_id).first()
            if amenity:
                amenities_ids.append(amenity)
            else:
                raise ValueError(f"Amenity with ID {amenity_id} not found")

        place.place_amenities.extend(amenities_ids)
        
        
    def add(self, place, amenities):
        db.session.add(place)

        self.add_amenities(place, amenities)

        db.session.flush()
        db.session.commit()
        return place
    
    def update(self, place_id, place_data, amenities):
        place = self.get(place_id)
        if place:
            for key, value in place_data.items():
                setattr(place, key, value)

            self.add_amenities(place, amenities)

            db.session.flush()
            db.session.commit()
            return place
        return None 
    
    def delete(self, place_id):
        place = self.get(place_id)
        if place:
            Review.query.filter(Review.place_id == place_id).delete(synchronize_session=False)
            
            db.session.delete(place)
            db.session.commit()
        
    def get_place(place_id, options=None):
        place = Place.query.filter_by(id=place_id)
        if options:
            place = place.options(*options)
        return place.first()
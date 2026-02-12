from app.models.address import Address
from app.models.mover import Mover

class PricingService:
    # Average rates for Nairobi (based on typical local market)
    BASE_RATES = {
        "bedsitter": 6000,
        "1_bedroom": 10000,
        "2_bedroom": 15000,
        "3_bedroom": 22000,
        "4_bedroom": 30000,
    }

    PRICE_PER_KM = 150  # KES per kilometer

    @staticmethod
    def calculate_quote(pickup_address=None, dropoff_address=None, mover_id=None, house_size=None, distance_km=None):
        """
        Calculates the estimated cost of a move.
        
        Can be called with either:
        - pickup_address, dropoff_address, mover_id (will calculate distance using Google Maps)
        - house_size, distance_km (manual input)
        
        Args:
            pickup_address: Dict with street, city, state, zip_code
            dropoff_address: Dict with street, city, state, zip_code
            mover_id: ID of the mover (optional)
            house_size: Size of the house (bedsitter, 1_bedroom, etc.)
            distance_km: Distance in kilometers
        
        Returns:
            Dict with quote details
        """
        # If addresses provided, calculate distance
        if pickup_address and dropoff_address:
            distance_km = PricingService._calculate_distance(pickup_address, dropoff_address)
            house_size = house_size or '1_bedroom'  # Default size
        elif distance_km is None:
            distance_km = 10  # Default distance
        
        base_price = PricingService.BASE_RATES.get(house_size, 10000)
        distance_cost = distance_km * PricingService.PRICE_PER_KM

        total = base_price + distance_cost

        return {
            "base_price": base_price,
            "distance_km": distance_km,
            "distance_cost": distance_cost,
            "total_estimate": total,
            "currency": "KES",
            "house_size": house_size,
            "valid_for": "24 hours"
        }

    @staticmethod
    def _calculate_distance(pickup_address, dropoff_address):
        """
        Calculate distance between two addresses.
        For now, uses a simple estimation.
        In production, this would use Google Maps API.
        """
        # Simple distance estimation based on city comparison
        pickup_city = pickup_address.get('city', '').lower()
        dropoff_city = dropoff_address.get('city', '').lower()
        
        # Same city - estimate 5-15 km
        if pickup_city == dropoff_city:
            return 10  # Default 10 km for same city
        
        # Different cities - estimate based on general distance
        # This is a placeholder - in production use Google Maps API
        return 50  # Default 50 km for different cities


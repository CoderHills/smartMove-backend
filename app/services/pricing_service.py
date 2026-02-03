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
    def calculate_quote(house_size, distance_km):
        """
        Calculates the estimated cost of a move.
        """
        base_price = PricingService.BASE_RATES.get(house_size, 10000)
        distance_cost = distance_km * PricingService.PRICE_PER_KM

        total = base_price + distance_cost

        return {
            "base_price": base_price,
            "distance_cost": distance_cost,
            "total_estimate": total,
            "currency": "KES",
        }

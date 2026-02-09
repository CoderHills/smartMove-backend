from app.services.pricing_service import PricingService


def test_quote_calculation():
    # 10km distance for a 1 bedroom
    quote = PricingService.calculate_quote(house_size="1_bedroom", distance_km=10)
    # 10,000 (base) + (10 * 150) = 11,500
    assert quote["total_estimate"] == 11500

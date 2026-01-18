"""Insurance quote service."""
from typing import List
import logging

logger = logging.getLogger(__name__)


class QuoteService:
    """Service for insurance quote operations."""
    
    @staticmethod
    def get_quotes(
        vehicle_make: str,
        vehicle_model: str,
        vehicle_year: int,
        coverage_type: str = "full"
    ) -> List[dict]:
        """
        Get insurance quotes for a vehicle. This is a mock implementation for Phase 1.
        
        Args:
            vehicle_make: Vehicle make (e.g., "Toyota")
            vehicle_model: Vehicle model (e.g., "Camry")
            vehicle_year: Vehicle year (e.g., 2023)
            coverage_type: Type of coverage - "liability", "comprehensive", or "full"
            
        Returns:
            List of quote dictionaries with provider, premium, and coverage details
        """
        logger.info(
            f"Get quotes: {vehicle_make} {vehicle_model} {vehicle_year}, "
            f"coverage={coverage_type}"
        )
        
        # Mock deterministic quotes
        base_premiums = {
            "liability": 50.0,
            "comprehensive": 120.0,
            "full": 180.0
        }
        
        base_premium = base_premiums.get(coverage_type.lower(), 180.0)
        
        # Generate 3 mock quotes with slight variations
        quotes = [
            {
                "provider": "SafeDrive Insurance",
                "premium_monthly": round(base_premium * 0.9, 2),
                "coverage": coverage_type.lower(),
                "details": {
                    "deductible": 500,
                    "policy_limit": 100000,
                    "special_features": ["Roadside assistance", "Rental car coverage"]
                }
            },
            {
                "provider": "BudgetCover Insurance",
                "premium_monthly": round(base_premium * 0.85, 2),
                "coverage": coverage_type.lower(),
                "details": {
                    "deductible": 1000,
                    "policy_limit": 50000,
                    "special_features": ["Basic coverage"]
                }
            },
            {
                "provider": "PremiumGuard Insurance",
                "premium_monthly": round(base_premium * 1.1, 2),
                "coverage": coverage_type.lower(),
                "details": {
                    "deductible": 250,
                    "policy_limit": 250000,
                    "special_features": [
                        "24/7 support",
                        "Accident forgiveness",
                        "New car replacement"
                    ]
                }
            }
        ]
        
        return quotes



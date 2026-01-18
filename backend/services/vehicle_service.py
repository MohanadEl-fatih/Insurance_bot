"""Vehicle lookup service."""
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class VehicleService:
    """Service for vehicle lookup operations."""
    
    @staticmethod
    def lookup_vehicle(
        vin: Optional[str] = None,
        make: Optional[str] = None,
        model: Optional[str] = None,
        year: Optional[int] = None
    ) -> dict:
        """
        Look up vehicle information. This is a mock implementation for Phase 1.
        
        Args:
            vin: Vehicle Identification Number (optional)
            make: Vehicle make (e.g., "Toyota")
            model: Vehicle model (e.g., "Camry")
            year: Vehicle year (e.g., 2023)
            
        Returns:
            Dictionary with vehicle information
        """
        logger.info(f"Vehicle lookup: vin={vin}, make={make}, model={model}, year={year}")
        
        # Mock deterministic responses
        if vin:
            # Return a mock vehicle based on VIN pattern
            return {
                "vin": vin,
                "make": make or "Toyota",
                "model": model or "Camry",
                "year": year or 2023,
                "status": "found"
            }
        
        if make and model and year:
            return {
                "vin": f"MOCK{year}{make[:3].upper()}{model[:3].upper()}",
                "make": make,
                "model": model,
                "year": year,
                "status": "found"
            }
        
        # Return a default mock vehicle
        return {
            "vin": "MOCK2023TOYCAM",
            "make": "Toyota",
            "model": "Camry",
            "year": 2023,
            "status": "found"
        }



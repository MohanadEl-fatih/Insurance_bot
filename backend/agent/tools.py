"""LangChain tools that wrap service layer business logic."""
from langchain_core.tools import tool
from typing import List, Optional
from services.vehicle_service import VehicleService
from services.quote_service import QuoteService
import logging

logger = logging.getLogger(__name__)


@tool
def mock_vehicle_lookup(vin: str = None, make: str = None, model: str = None, year: int = None) -> dict:
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
    logger.info(f"Vehicle lookup tool called: vin={vin}, make={make}, model={model}, year={year}")
    
    # Delegate to service layer
    return VehicleService.lookup_vehicle(vin=vin, make=make, model=model, year=year)


@tool
def mock_get_quote(vehicle_make: str, vehicle_model: str, vehicle_year: int, coverage_type: str = "full") -> List[dict]:
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
        f"Get quote tool called: {vehicle_make} {vehicle_model} {vehicle_year}, "
        f"coverage={coverage_type}"
    )
    
    # Delegate to service layer
    return QuoteService.get_quotes(
        vehicle_make=vehicle_make,
        vehicle_model=vehicle_model,
        vehicle_year=vehicle_year,
        coverage_type=coverage_type
    )


def get_tools():
    """Get list of available LangChain tools for the agent."""
    return [mock_vehicle_lookup, mock_get_quote]


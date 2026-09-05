from app.models import User, Inventory, Requirement, FarmerProfile
from app.extensions import db

class MatchingService:
    @staticmethod
    def find_matching_farmers_for_requirement(requirement: Requirement):
        """
        Rule-based matching algorithm that finds eligible, available farmers
        matching the buyer's requirement product, quantity, and preferences.
        """
        # 1. Base query: Active farmers with matching product in inventory
        inventories = Inventory.query.filter(
            Inventory.product_name.ilike(f"%{requirement.product_name}%"),
            Inventory.status == 'available',
            Inventory.available_quantity > 0
        ).all()
        
        matches = []
        req_qty_kg = requirement.required_quantity
        if requirement.unit.lower() == 'quintal':
            req_qty_kg *= 100
        elif requirement.unit.lower() == 'ton':
            req_qty_kg *= 1000

        for inv in inventories:
            farmer = inv.farmer
            if not farmer or not farmer.is_active:
                continue
                
            profile = farmer.farmer_profile
            
            # Convert inventory quantity to kg for comparison
            inv_qty_kg = inv.available_quantity
            if inv.unit.lower() == 'quintal':
                inv_qty_kg *= 100
            elif inv.unit.lower() == 'ton':
                inv_qty_kg *= 1000
                
            # Quantity preference check
            passes_preference = True
            if profile:
                if not profile.open_to_all_quantities:
                    if req_qty_kg < profile.min_qty_kg or req_qty_kg > profile.max_qty_kg:
                        passes_preference = False
                        
            if not passes_preference:
                continue
                
            # Calculate match score (0 - 100)
            score = 70.0 # Base score for product match
            
            # Inventory adequacy bonus
            if inv_qty_kg >= req_qty_kg:
                score += 15.0
            else:
                # Partial fulfillment
                ratio = inv_qty_kg / max(req_qty_kg, 1.0)
                score += ratio * 10.0
                
            # Verification bonus
            if farmer.is_verified:
                score += 10.0
                
            # Location proximity bonus (same district / state)
            if profile and requirement.delivery_district and profile.district:
                if profile.district.lower() == requirement.delivery_district.lower():
                    score += 5.0
                    
            matches.append({
                'farmer': farmer,
                'farmer_profile': profile,
                'inventory': inv,
                'match_score': min(round(score, 1), 100.0),
                'available_quantity': inv.available_quantity,
                'unit': inv.unit,
                'expected_price': inv.expected_price_per_unit,
                'quality_grade': inv.quality_grade,
                'district': profile.district if profile else inv.location_district,
                'state': profile.state if profile else inv.location_state,
                'is_verified': farmer.is_verified
            })
            
        # Sort by match score descending
        matches.sort(key=lambda x: x['match_score'], reverse=True)
        return matches

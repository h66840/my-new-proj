"""
Dynamic Pricing Model for Real-time Price Optimization
This module implements a dynamic pricing algorithm that adjusts prices based on:
- Market demand
- Competitor pricing
- Inventory levels
- Time-based factors
- Customer segments
"""

import json
import math
import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class CustomerSegment(Enum):
    PREMIUM = "premium"
    STANDARD = "standard"
    BUDGET = "budget"

class PriceStrategy(Enum):
    DEMAND_BASED = "demand_based"
    COMPETITION_BASED = "competition_based"
    INVENTORY_BASED = "inventory_based"
    TIME_BASED = "time_based"

@dataclass
class PricingInput:
    """Input parameters for pricing calculation"""
    base_price: float
    demand_score: float  # 0-1 scale
    competitor_price: Optional[float] = None
    inventory_level: int = 100
    max_inventory: int = 1000
    customer_segment: CustomerSegment = CustomerSegment.STANDARD
    time_factor: float = 1.0  # Peak hours multiplier
    margin_target: float = 0.3  # 30% margin target

@dataclass
class PricingOutput:
    """Output of pricing calculation"""
    recommended_price: float
    price_change_percentage: float
    strategy_used: PriceStrategy
    confidence_score: float
    reasoning: str

class DynamicPricingModel:
    """Main dynamic pricing model class"""
    
    def __init__(self):
        self.min_price_multiplier = 0.7  # Minimum 70% of base price
        self.max_price_multiplier = 2.0  # Maximum 200% of base price
        self.demand_sensitivity = 0.5
        self.competition_sensitivity = 0.3
        self.inventory_sensitivity = 0.4
        
    def calculate_demand_multiplier(self, demand_score: float) -> float:
        """Calculate price multiplier based on demand"""
        # Higher demand = higher price
        return 1.0 + (demand_score - 0.5) * self.demand_sensitivity
    
    def calculate_competition_multiplier(self, base_price: float, competitor_price: Optional[float]) -> float:
        """Calculate price multiplier based on competitor pricing"""
        if competitor_price is None:
            return 1.0
        
        price_ratio = competitor_price / base_price
        # If competitor is more expensive, we can increase price slightly
        # If competitor is cheaper, we need to be competitive
        if price_ratio > 1.1:
            return min(1.1, price_ratio * 0.95)  # Price slightly below competitor
        elif price_ratio < 0.9:
            return max(0.9, price_ratio * 1.05)  # Price slightly above competitor
        else:
            return 1.0
    
    def calculate_inventory_multiplier(self, inventory_level: int, max_inventory: int) -> float:
        """Calculate price multiplier based on inventory levels"""
        inventory_ratio = inventory_level / max_inventory
        
        if inventory_ratio < 0.1:  # Very low inventory
            return 1.2  # Increase price to slow demand
        elif inventory_ratio < 0.3:  # Low inventory
            return 1.1
        elif inventory_ratio > 0.8:  # High inventory
            return 0.9  # Decrease price to move inventory
        else:
            return 1.0
    
    def calculate_segment_multiplier(self, segment: CustomerSegment) -> float:
        """Calculate price multiplier based on customer segment"""
        multipliers = {
            CustomerSegment.PREMIUM: 1.2,
            CustomerSegment.STANDARD: 1.0,
            CustomerSegment.BUDGET: 0.85
        }
        return multipliers.get(segment, 1.0)
    
    def calculate_time_multiplier(self, time_factor: float) -> float:
        """Calculate price multiplier based on time factors (peak hours, seasons, etc.)"""
        return time_factor
    
    def determine_primary_strategy(self, pricing_input: PricingInput) -> PriceStrategy:
        """Determine which pricing strategy should be primary"""
        # Priority logic based on business rules
        if pricing_input.demand_score > 0.8:
            return PriceStrategy.DEMAND_BASED
        elif pricing_input.competitor_price and abs(pricing_input.competitor_price - pricing_input.base_price) / pricing_input.base_price > 0.15:
            return PriceStrategy.COMPETITION_BASED
        elif pricing_input.inventory_level / pricing_input.max_inventory < 0.2 or pricing_input.inventory_level / pricing_input.max_inventory > 0.8:
            return PriceStrategy.INVENTORY_BASED
        elif pricing_input.time_factor != 1.0:
            return PriceStrategy.TIME_BASED
        else:
            return PriceStrategy.DEMAND_BASED
    
    def calculate_confidence_score(self, pricing_input: PricingInput, final_multiplier: float) -> float:
        """Calculate confidence score for the pricing recommendation"""
        confidence = 0.5  # Base confidence
        
        # Higher confidence with more data points
        if pricing_input.competitor_price:
            confidence += 0.2
        if pricing_input.demand_score > 0.1:
            confidence += 0.2
        if pricing_input.inventory_level > 0:
            confidence += 0.1
        
        # Lower confidence for extreme price changes
        if abs(final_multiplier - 1.0) > 0.5:
            confidence -= 0.2
        
        return max(0.1, min(1.0, confidence))
    
    def calculate_price(self, pricing_input: PricingInput) -> PricingOutput:
        """Main method to calculate dynamic price"""
        
        # Calculate individual multipliers
        demand_mult = self.calculate_demand_multiplier(pricing_input.demand_score)
        competition_mult = self.calculate_competition_multiplier(pricing_input.base_price, pricing_input.competitor_price)
        inventory_mult = self.calculate_inventory_multiplier(pricing_input.inventory_level, pricing_input.max_inventory)
        segment_mult = self.calculate_segment_multiplier(pricing_input.customer_segment)
        time_mult = self.calculate_time_multiplier(pricing_input.time_factor)
        
        # Determine primary strategy
        primary_strategy = self.determine_primary_strategy(pricing_input)
        
        # Weight multipliers based on strategy
        if primary_strategy == PriceStrategy.DEMAND_BASED:
            final_multiplier = demand_mult * 0.6 + competition_mult * 0.2 + inventory_mult * 0.1 + time_mult * 0.1
        elif primary_strategy == PriceStrategy.COMPETITION_BASED:
            final_multiplier = competition_mult * 0.6 + demand_mult * 0.2 + inventory_mult * 0.1 + time_mult * 0.1
        elif primary_strategy == PriceStrategy.INVENTORY_BASED:
            final_multiplier = inventory_mult * 0.6 + demand_mult * 0.2 + competition_mult * 0.1 + time_mult * 0.1
        else:  # TIME_BASED
            final_multiplier = time_mult * 0.6 + demand_mult * 0.2 + competition_mult * 0.1 + inventory_mult * 0.1
        
        # Apply segment multiplier
        final_multiplier *= segment_mult
        
        # Apply bounds
        final_multiplier = max(self.min_price_multiplier, min(self.max_price_multiplier, final_multiplier))
        
        # Calculate final price
        recommended_price = pricing_input.base_price * final_multiplier
        
        # Round to reasonable precision
        recommended_price = round(recommended_price, 2)
        
        # Calculate percentage change
        price_change_percentage = ((recommended_price - pricing_input.base_price) / pricing_input.base_price) * 100
        
        # Calculate confidence score
        confidence_score = self.calculate_confidence_score(pricing_input, final_multiplier)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(pricing_input, primary_strategy, final_multiplier, demand_mult, competition_mult, inventory_mult, time_mult)
        
        return PricingOutput(
            recommended_price=recommended_price,
            price_change_percentage=round(price_change_percentage, 2),
            strategy_used=primary_strategy,
            confidence_score=round(confidence_score, 2),
            reasoning=reasoning
        )
    
    def _generate_reasoning(self, pricing_input: PricingInput, strategy: PriceStrategy, 
                          final_mult: float, demand_mult: float, competition_mult: float, 
                          inventory_mult: float, time_mult: float) -> str:
        """Generate human-readable reasoning for the pricing decision"""
        
        reasons = []
        
        if strategy == PriceStrategy.DEMAND_BASED:
            if pricing_input.demand_score > 0.7:
                reasons.append("High demand detected, increasing price to optimize revenue")
            elif pricing_input.demand_score < 0.3:
                reasons.append("Low demand detected, considering price reduction to stimulate sales")
        
        if pricing_input.competitor_price:
            comp_diff = (pricing_input.competitor_price - pricing_input.base_price) / pricing_input.base_price
            if comp_diff > 0.1:
                reasons.append(f"Competitor pricing is {comp_diff*100:.1f}% higher, opportunity to increase price")
            elif comp_diff < -0.1:
                reasons.append(f"Competitor pricing is {abs(comp_diff)*100:.1f}% lower, need to stay competitive")
        
        inventory_ratio = pricing_input.inventory_level / pricing_input.max_inventory
        if inventory_ratio < 0.2:
            reasons.append("Low inventory levels, increasing price to manage demand")
        elif inventory_ratio > 0.8:
            reasons.append("High inventory levels, reducing price to accelerate sales")
        
        if pricing_input.time_factor > 1.1:
            reasons.append("Peak time period, applying premium pricing")
        elif pricing_input.time_factor < 0.9:
            reasons.append("Off-peak period, offering discounted pricing")
        
        if pricing_input.customer_segment == CustomerSegment.PREMIUM:
            reasons.append("Premium customer segment, applying premium pricing")
        elif pricing_input.customer_segment == CustomerSegment.BUDGET:
            reasons.append("Budget-conscious customer segment, offering competitive pricing")
        
        return "; ".join(reasons) if reasons else "Standard pricing applied based on current market conditions"

def create_pricing_api_response(pricing_input_dict: Dict) -> Dict:
    """
    API wrapper function for the pricing model
    This function will be used in the Supabase Edge Function
    """
    try:
        # Parse input
        pricing_input = PricingInput(
            base_price=pricing_input_dict.get('base_price', 100.0),
            demand_score=pricing_input_dict.get('demand_score', 0.5),
            competitor_price=pricing_input_dict.get('competitor_price'),
            inventory_level=pricing_input_dict.get('inventory_level', 100),
            max_inventory=pricing_input_dict.get('max_inventory', 1000),
            customer_segment=CustomerSegment(pricing_input_dict.get('customer_segment', 'standard')),
            time_factor=pricing_input_dict.get('time_factor', 1.0),
            margin_target=pricing_input_dict.get('margin_target', 0.3)
        )
        
        # Calculate pricing
        model = DynamicPricingModel()
        result = model.calculate_price(pricing_input)
        
        # Return response
        return {
            'success': True,
            'data': {
                'recommended_price': result.recommended_price,
                'price_change_percentage': result.price_change_percentage,
                'strategy_used': result.strategy_used.value,
                'confidence_score': result.confidence_score,
                'reasoning': result.reasoning,
                'timestamp': datetime.datetime.utcnow().isoformat()
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'timestamp': datetime.datetime.utcnow().isoformat()
        }

# Example usage
if __name__ == "__main__":
    # Test the pricing model
    test_input = PricingInput(
        base_price=100.0,
        demand_score=0.8,
        competitor_price=110.0,
        inventory_level=50,
        max_inventory=1000,
        customer_segment=CustomerSegment.PREMIUM,
        time_factor=1.2
    )
    
    model = DynamicPricingModel()
    result = model.calculate_price(test_input)
    
    print("Dynamic Pricing Result:")
    print(f"Recommended Price: ${result.recommended_price}")
    print(f"Price Change: {result.price_change_percentage}%")
    print(f"Strategy: {result.strategy_used.value}")
    print(f"Confidence: {result.confidence_score}")
    print(f"Reasoning: {result.reasoning}")
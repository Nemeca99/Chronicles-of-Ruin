#!/usr/bin/env python3
"""
Economy System for Chronicles of Ruin: Sunderfall
Manages player gold, trading, and market mechanics
"""

import json
import os
from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta


class TransactionType(Enum):
    """Types of transactions"""
    EARNED = "earned"
    SPENT = "spent"
    TRADED = "traded"
    REFUNDED = "refunded"


class TradeStatus(Enum):
    """Trade status"""
    PENDING = "pending"
    ACCEPTED = "accepted"
    DECLINED = "declined"
    CANCELLED = "cancelled"
    EXPIRED = "expired"


class EconomySystem:
    """Manages player economy and trading"""
    
    def __init__(self, player_system=None, items_system=None):
        self.player_system = player_system
        self.items_system = items_system
        self.player_economy = {}
        self.trades = {}
        self.market_prices = {}
        self._load_market_prices()
    
    def _load_market_prices(self):
        """Load base market prices for items"""
        self.market_prices = {
            "iron_sword": 100,
            "steel_sword": 250,
            "magic_sword": 500,
            "leather_armor": 75,
            "chain_armor": 200,
            "plate_armor": 400,
            "health_potion": 25,
            "mana_potion": 30,
            "strength_potion": 50,
            "healing_herb": 5,
            "mana_herb": 8,
            "rare_gem": 1000,
            "gold_coin": 1,
            "silver_coin": 0.1,
            "copper_coin": 0.01
        }
    
    def get_player_economy(self, player_id: str) -> Dict[str, Any]:
        """Get economy data for a player"""
        if player_id not in self.player_economy:
            self.player_economy[player_id] = {
                "gold": 100,  # Starting gold
                "transactions": [],
                "trades": [],
                "market_listings": [],
                "last_updated": datetime.now()
            }
        return self.player_economy[player_id]
    
    def add_gold(self, player_id: str, amount: int, reason: str = "Earned"):
        """Add gold to a player"""
        economy = self.get_player_economy(player_id)
        economy["gold"] += amount
        
        # Record transaction
        transaction = {
            "type": TransactionType.EARNED.value,
            "amount": amount,
            "reason": reason,
            "timestamp": datetime.now(),
            "balance_after": economy["gold"]
        }
        economy["transactions"].append(transaction)
        economy["last_updated"] = datetime.now()
        
        print(f"💰 {amount} gold added to {player_id} ({reason})")
    
    def spend_gold(self, player_id: str, amount: int, reason: str = "Spent") -> bool:
        """Spend gold from a player"""
        economy = self.get_player_economy(player_id)
        
        if economy["gold"] < amount:
            print(f"❌ Insufficient gold: {economy['gold']} < {amount}")
            return False
        
        economy["gold"] -= amount
        
        # Record transaction
        transaction = {
            "type": TransactionType.SPENT.value,
            "amount": amount,
            "reason": reason,
            "timestamp": datetime.now(),
            "balance_after": economy["gold"]
        }
        economy["transactions"].append(transaction)
        economy["last_updated"] = datetime.now()
        
        print(f"💸 {amount} gold spent by {player_id} ({reason})")
        return True
    
    def get_gold(self, player_id: str) -> int:
        """Get player's current gold amount"""
        economy = self.get_player_economy(player_id)
        return economy["gold"]
    
    def get_transaction_history(self, player_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent transaction history for a player"""
        economy = self.get_player_economy(player_id)
        return economy["transactions"][-limit:]
    
    def create_trade(self, player_id: str, target_player_id: str, 
                    offered_items: List[str], requested_items: List[str]) -> Dict[str, Any]:
        """Create a trade offer"""
        if player_id == target_player_id:
            return {"success": False, "error": "Cannot trade with yourself"}
        
        # Validate offered items
        if self.items_system:
            player_inventory = self.items_system.get_inventory(player_id)
            for item in offered_items:
                if not self.items_system.has_item(player_id, item):
                    return {"success": False, "error": f"Don't own item: {item}"}
        
        trade_id = f"trade_{len(self.trades)}_{datetime.now().timestamp()}"
        
        trade = {
            "trade_id": trade_id,
            "initiator": player_id,
            "target": target_player_id,
            "offered_items": offered_items,
            "requested_items": requested_items,
            "status": TradeStatus.PENDING.value,
            "created_at": datetime.now(),
            "expires_at": datetime.now() + timedelta(hours=24)
        }
        
        self.trades[trade_id] = trade
        
        # Add to player's trade list
        economy = self.get_player_economy(player_id)
        economy["trades"].append(trade_id)
        
        print(f"🤝 Trade offer created: {player_id} -> {target_player_id}")
        print(f"   Offered: {offered_items}")
        print(f"   Requested: {requested_items}")
        
        return {"success": True, "trade_id": trade_id}
    
    def accept_trade(self, player_id: str, trade_id: str) -> Dict[str, Any]:
        """Accept a trade offer"""
        if trade_id not in self.trades:
            return {"success": False, "error": "Trade not found"}
        
        trade = self.trades[trade_id]
        
        if trade["target"] != player_id:
            return {"success": False, "error": "Not the target of this trade"}
        
        if trade["status"] != TradeStatus.PENDING.value:
            return {"success": False, "error": "Trade is not pending"}
        
        if datetime.now() > trade["expires_at"]:
            trade["status"] = TradeStatus.EXPIRED.value
            return {"success": False, "error": "Trade has expired"}
        
        # Validate requested items
        if self.items_system:
            player_inventory = self.items_system.get_inventory(player_id)
            for item in trade["requested_items"]:
                if not self.items_system.has_item(player_id, item):
                    return {"success": False, "error": f"Don't own item: {item}"}
        
        # Execute the trade
        if self._execute_trade(trade):
            trade["status"] = TradeStatus.ACCEPTED.value
            trade["accepted_at"] = datetime.now()
            
            print(f"✅ Trade accepted: {trade_id}")
            return {"success": True, "trade_id": trade_id}
        else:
            return {"success": False, "error": "Failed to execute trade"}
    
    def _execute_trade(self, trade: Dict[str, Any]) -> bool:
        """Execute a trade between players"""
        if not self.items_system:
            return False
        
        try:
            # Transfer offered items from initiator to target
            for item in trade["offered_items"]:
                if self.items_system.has_item(trade["initiator"], item):
                    self.items_system.remove_item_from_inventory(trade["initiator"], item, 1)
                    self.items_system.add_item_to_inventory(trade["target"], item, 1)
                else:
                    return False
            
            # Transfer requested items from target to initiator
            for item in trade["requested_items"]:
                if self.items_system.has_item(trade["target"], item):
                    self.items_system.remove_item_from_inventory(trade["target"], item, 1)
                    self.items_system.add_item_to_inventory(trade["initiator"], item, 1)
                else:
                    return False
            
            return True
        except Exception as e:
            print(f"❌ Trade execution failed: {e}")
            return False
    
    def decline_trade(self, player_id: str, trade_id: str) -> Dict[str, Any]:
        """Decline a trade offer"""
        if trade_id not in self.trades:
            return {"success": False, "error": "Trade not found"}
        
        trade = self.trades[trade_id]
        
        if trade["target"] != player_id:
            return {"success": False, "error": "Not the target of this trade"}
        
        if trade["status"] != TradeStatus.PENDING.value:
            return {"success": False, "error": "Trade is not pending"}
        
        trade["status"] = TradeStatus.DECLINED.value
        trade["declined_at"] = datetime.now()
        
        print(f"❌ Trade declined: {trade_id}")
        return {"success": True, "trade_id": trade_id}
    
    def cancel_trade(self, player_id: str, trade_id: str) -> Dict[str, Any]:
        """Cancel a trade offer"""
        if trade_id not in self.trades:
            return {"success": False, "error": "Trade not found"}
        
        trade = self.trades[trade_id]
        
        if trade["initiator"] != player_id:
            return {"success": False, "error": "Not the initiator of this trade"}
        
        if trade["status"] != TradeStatus.PENDING.value:
            return {"success": False, "error": "Trade is not pending"}
        
        trade["status"] = TradeStatus.CANCELLED.value
        trade["cancelled_at"] = datetime.now()
        
        print(f"🚫 Trade cancelled: {trade_id}")
        return {"success": True, "trade_id": trade_id}
    
    def get_player_trades(self, player_id: str) -> Dict[str, Any]:
        """Get all trades for a player"""
        economy = self.get_player_economy(player_id)
        
        pending_trades = []
        completed_trades = []
        
        for trade_id in economy["trades"]:
            if trade_id in self.trades:
                trade = self.trades[trade_id]
                
                if trade["status"] == TradeStatus.PENDING.value:
                    pending_trades.append({
                        "trade_id": trade_id,
                        "initiator": trade["initiator"],
                        "target": trade["target"],
                        "offered_items": trade["offered_items"],
                        "requested_items": trade["requested_items"],
                        "created_at": trade["created_at"],
                        "expires_at": trade["expires_at"]
                    })
                else:
                    completed_trades.append({
                        "trade_id": trade_id,
                        "initiator": trade["initiator"],
                        "target": trade["target"],
                        "offered_items": trade["offered_items"],
                        "requested_items": trade["requested_items"],
                        "status": trade["status"],
                        "created_at": trade["created_at"]
                    })
        
        return {
            "pending_trades": pending_trades,
            "completed_trades": completed_trades
        }
    
    def get_item_price(self, item_id: str) -> int:
        """Get the base price of an item"""
        return self.market_prices.get(item_id, 10)  # Default price
    
    def calculate_item_value(self, item_id: str, quantity: int = 1) -> int:
        """Calculate the total value of items"""
        base_price = self.get_item_price(item_id)
        return base_price * quantity
    
    def get_economy_stats(self, player_id: str) -> Dict[str, Any]:
        """Get economy statistics for a player"""
        economy = self.get_player_economy(player_id)
        
        total_earned = sum(t["amount"] for t in economy["transactions"] 
                          if t["type"] == TransactionType.EARNED.value)
        total_spent = sum(t["amount"] for t in economy["transactions"] 
                         if t["type"] == TransactionType.SPENT.value)
        
        return {
            "current_gold": economy["gold"],
            "total_earned": total_earned,
            "total_spent": total_spent,
            "net_worth": economy["gold"],
            "transaction_count": len(economy["transactions"]),
            "trade_count": len(economy["trades"])
        }

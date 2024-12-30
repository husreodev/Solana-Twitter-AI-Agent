from typing import Dict, Any, Optional
import logging
from src.core.expert_base import ExpertBase
from src.utils.cache import Cache
from src.core.openai_client import OpenAIClient

logger = logging.getLogger(__name__)

class SportsExpert(ExpertBase):
    def __init__(self, config: Dict[str, Any]):
        """Initialize SportsExpert
        
        Args:
            config (Dict[str, Any]): Configuration dictionary
        """
        super().__init__("sports")
        self.config = config
        self.cache = Cache(
            enabled=config["experts"]["sports"]["cache_enabled"],
            ttl=config["experts"]["sports"]["cache_ttl"]
        )
        self.openai_client = OpenAIClient()
        
    async def get_response(self, question: str) -> Optional[str]:
        """Get response for sports related question
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Response or None if no answer found
        """
        try:
            # Check cache first
            cached_response = self.cache.get(question)
            if cached_response:
                logger.info("Cache hit for question: %s", question)
                return cached_response
                
            # Generate response using OpenAI
            response = await self._generate_response(question)
            
            # Cache the response
            if response:
                self.cache.set(question, response)
                
            return response
            
        except Exception as e:
            logger.error("Error getting sports response: %s", str(e))
            return None
            
    async def _generate_response(self, question: str) -> Optional[str]:
        """Generate response using OpenAI
        
        Args:
            question (str): User's question
            
        Returns:
            Optional[str]: Generated response or None
        """
        system_prompt = """Sen bir spor uzmanısın. 
        Futbol, basketbol, voleybol ve diğer sporlar hakkında detaylı bilgi sahibisin.
        Kullanıcının sorduğu spor ile ilgili soruları yanıtla.
        Eğer soru sporla ilgili değilse, bunu belirt."""
        
        try:
            response = await self.openai_client.get_completion(system_prompt, question)
            return response
        except Exception as e:
            logger.error("Error generating sports response: %s", str(e))
            return None 
from dataclasses import dataclass

@dataclass
class Defaults(frozen=True):
    #Database defaults
    channel_limit: int = 1
    channel_status: int = 1
    channel_avg_score: float = 5.0

    #Middlewares defaults
    cooldown_seconds: int = 1

defaults = Defaults()

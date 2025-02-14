# Theme keywords for sentiment analysis
THEME_KEYWORDS = {
    'work_life_balance': ['balance', 'hours', 'flexible', 'schedule'],
    'compensation': ['salary', 'pay', 'compensation', 'benefits'],
    'growth': ['growth', 'promotion', 'learning', 'development'],
    'management': ['manager', 'leadership', 'supervisor', 'team lead']
}

# Model configurations
MODEL_CONFIGS = {
    'sentiment': {
        'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
        'max_length': 512,
        'batch_size': 32
    }
}
from wordcloud import WordCloud
import io
import re
from utils.globals import STOP_WORDS

def _get_wordcloud_image(text: str, width=800, height=400) -> bytes:
    text = re.sub(r'[^а-яёА-ЯЁa-zA-Z\s]', ' ', text.lower())
    words = text.split()
    filtered_words = [w for w in words if len(w) > 2 and w not in STOP_WORDS]
    full_text = " ".join(filtered_words)
    
    wc = WordCloud(
        width=width,
        height=height,
        background_color='white',
        max_words=50,
        colormap='viridis',
        random_state=42
    ).generate(full_text)

    img_buffer = io.BytesIO()
    wc.to_image().save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer.getvalue()
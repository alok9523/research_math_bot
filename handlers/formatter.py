def format_wolfram_response(response):
    formatted_text = ""
    images = []
    
    for pod in response.pods:
        if pod.title:
            formatted_text += f"**{pod.title}**\n"
        for sub in pod.subpods:
            if sub.plaintext:
                formatted_text += f"`{sub.plaintext}`\n\n"
            if sub.img:
                images.append(sub.img.src)
    
    if not formatted_text:
        return "No solution found", images
    
    formatted_text = formatted_text.replace('\\', '').replace('_', '\\_')
    return formatted_text, images

def format_concept_explanation(text):
    formatted = text.replace('**', '*').replace('\\n', '\n')
    formatted = f"📚 Explanation:\n\n{formatted}"
    return formatted

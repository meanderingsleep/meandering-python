# Get some context from the the previous story output
def getLast20Words(context):
    context_words = context.split()
    last_20_words = context_words[-20:]
    context = ' '.join(last_20_words)
    return context